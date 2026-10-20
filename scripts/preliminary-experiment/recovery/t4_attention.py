"""Opt-in public SDPA integration; CPU checks are not T4/model acceptance.

Each kernel batch is one KV-head group from the same batch-one episode.
Expanded K/V remain storage aliases. CUDA permits only efficient attention;
CPU math is used solely for numerical integration checks. No kernel is added.
Importing this module never imports the optional inference stack.
"""

T4_ATTENTION = "recovery_t4_sdpa"
PREFILL_CHUNK_SIZE = 256


def grouped_inputs(query, key, value, attention_mask=None):
    """Return grouped Q and broadcast K/V/bias without materializing KV heads."""
    import torch
    from torch.nn import functional as F

    if (any(t.ndim != 4 for t in (query, key, value))
            or any(t.shape[0] != 1 for t in (query, key, value))
            or key.shape != value.shape
            or query.shape[-1] != key.shape[-1]
            or any(t.dtype != query.dtype or t.device != query.device for t in (key, value))
            or any(t.stride(-1) != 1 for t in (query, key, value))
            or any(d <= 0 for t in (query, key, value) for d in t.shape)):
        raise ValueError("batch-one dense Q/K/V with matching dtype/device/dimension and contiguous columns required")
    heads, length, dim = query.shape[1:]
    kv_heads, kv_length, _ = key.shape[1:]
    if heads % kv_heads:
        raise ValueError("query heads must be an integer multiple of KV heads")
    groups = heads // kv_heads
    q = query[0].unflatten(0, (kv_heads, groups))
    k = key[0].unsqueeze(1).expand(kv_heads, groups, kv_length, dim)
    v = value[0].unsqueeze(1).expand(kv_heads, groups, kv_length, dim)
    bias = attention_mask
    if bias is not None:
        if (bias.ndim != 4 or bias.shape[:2] != (1, 1)
                or bias.shape[2] not in (1, length) or bias.shape[3] != kv_length
                or bias.device != query.device or bias.dtype not in (torch.bool, query.dtype)):
            raise ValueError("native head-shared 4D boolean or same-dtype additive mask required")
        # Convert/align before broadcast: Torch otherwise may materialize its
        # boolean conversion or alignment across every grouped head.
        if bias.dtype == torch.bool:
            bias = torch.zeros_like(bias, dtype=query.dtype).masked_fill_(~bias, float("-inf"))
        padding = (-kv_length) % 8
        if padding:
            bias = F.pad(bias, (0, padding))[..., :kv_length]
        elif bias.stride(-1) != 1 or bias.stride(-2) % 8:
            bias = bias.contiguous()
        bias = bias.expand(kv_heads, groups, bias.shape[2], kv_length)
    return q, k, v, bias


def t4_sdpa_forward(module, query, key, value, attention_mask, dropout=0.0,
                    scaling=None, is_causal=None, **kwargs):
    """Transformers attention interface, preserving native masks and head order."""
    import torch
    from torch.nn.attention import SDPBackend, sdpa_kernel

    if module.training or dropout != 0.0 or kwargs.get("output_attentions", False):
        raise ValueError("inference-only attention with zero dropout and no attention-weight output")
    if query.dtype not in (torch.float16, torch.float32, torch.float64):
        raise ValueError("FP16 CUDA or floating CPU numerical checks required")
    q, k, v, bias = grouped_inputs(query, key, value, attention_mask)
    if getattr(module, "num_key_value_groups", None) != query.shape[1] // key.shape[1]:
        raise ValueError("module and tensor KV-head grouping differ")
    causal = getattr(module, "is_causal", True) if is_causal is None else is_causal
    if type(causal) is not bool:
        raise ValueError("explicit causal flag must be boolean")
    if causal and bias is None and query.shape[2] > 1 and query.shape[2] != key.shape[2]:
        raise ValueError("cached multi-query causal attention requires its native offset mask")
    causal = causal and bias is None and query.shape[2] > 1
    if query.device.type == "cuda":
        if (str(torch.__version__) != "2.11.0+cu128" or torch.version.cuda != "12.8"
                or torch.cuda.get_device_capability(query.device) != (7, 5)
                or query.dtype != torch.float16
                or query.shape[1] != 16 or key.shape[1] != 4 or query.shape[-1] != 256):
            raise ValueError("reviewed Torch/CUDA/T4 FP16 16/4-head dimension-256 candidate required")
        backend = SDPBackend.EFFICIENT_ATTENTION
    elif query.device.type == "cpu":
        backend = SDPBackend.MATH  # Reference/integration only; ModelFactory refuses CPU.
    else:
        raise ValueError("actual T4 CUDA or explicit CPU numerical verification only")
    with sdpa_kernel(backend):
        output = torch.nn.functional.scaled_dot_product_attention(
            q, k, v, attn_mask=bias, dropout_p=0.0, is_causal=causal, scale=scaling)
    # Head group order is the same as repeat_interleave(K/V, groups, dim=1).
    output = output.permute(2, 0, 1, 3).reshape(1, query.shape[2], query.shape[1], query.shape[-1])
    return output.contiguous(), None


def register_t4_attention():
    """Register only this candidate's public attention/mask entries, idempotently."""
    import importlib.metadata
    if importlib.metadata.version("transformers") != "5.12.0":
        raise ValueError("reviewed Transformers 5.12.0 candidate required")
    from transformers import AttentionInterface, AttentionMaskInterface
    from transformers.masking_utils import sdpa_mask

    for interface, function in ((AttentionInterface, t4_sdpa_forward), (AttentionMaskInterface, sdpa_mask)):
        existing = interface().get(T4_ATTENTION)
        if existing is not None and existing is not function:
            raise ValueError("candidate attention/mask name already belongs to different code")
    AttentionInterface.register(T4_ATTENTION, t4_sdpa_forward)
    AttentionMaskInterface.register(T4_ATTENTION, sdpa_mask)
