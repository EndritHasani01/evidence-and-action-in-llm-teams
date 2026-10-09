"""Small CPU doubles for the direct adapter; never model or GPU evidence."""

from contextlib import nullcontext
import os
from types import SimpleNamespace

from recovery.inference import TRANSPORT_ID, PAD_ID, TransformersBackend, QWEN_9B


class Tokenizer:
    eos_token_id = TRANSPORT_ID
    pad_token_id = PAD_ID
    chat_template = "CPU mock user turn; non-thinking assistant prefix"

    def convert_ids_to_tokens(self, token):
        return {TRANSPORT_ID: "<|im_end|>", PAD_ID: "<|endoftext|>"}.get(token, chr(token))

    def encode(self, text, *, add_special_tokens=False):
        from recovery.state import PUBLIC_FEEDBACK
        if text in PUBLIC_FEEDBACK.values():
            return list(range(len(text.split())))
        return [ord(c) for c in text]

    def apply_chat_template(self, messages, *, tokenize, add_generation_prompt, enable_thinking):
        assert not tokenize and add_generation_prompt and enable_thinking is False
        return "USER\n" + messages[0]["content"] + "\nASSISTANT\n"

    def __call__(self, text, **kwargs):
        assert kwargs == dict(add_special_tokens=False, truncation=False, padding=False, return_attention_mask=True)
        ids = self.encode(text)
        return dict(input_ids=ids, attention_mask=[1] * len(ids))

    def decode(self, ids, *, skip_special_tokens, clean_up_tokenization_spaces):
        assert skip_special_tokens is False and clean_up_tokenization_spaces is False
        return "".join(self.convert_ids_to_tokens(i) for i in ids)


class Tensor:
    def __init__(self, data=None, *, dtype="torch.float16", device="cuda:0"):
        self.data, self.dtype = data, dtype
        self.device = SimpleNamespace(type=device.split(":")[0], index=int(device.split(":")[1]) if ":" in device else None)
        self.shape = (2, 2)

    def is_floating_point(self):
        return self.dtype != "torch.uint8"

    def tolist(self):
        return [list(row) for row in self.data]


class Cache:
    def __init__(self, *, config):
        self.length = 0
        self.recurrent = False

    def get_seq_length(self):
        return self.length

    def has_previous_state(self):
        return self.recurrent


class GenerationConfig:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def to_dict(self):
        return vars(self)


class Torch:
    long = "torch.int64"
    float16 = "torch.float16"

    def __init__(self):
        self.seed = self.cuda_seed = None
        self.finite = True
        self.cuda = SimpleNamespace(
            manual_seed_all=self.set_cuda_seed, initial_seed=lambda: self.cuda_seed,
            reset_peak_memory_stats=lambda device: None, synchronize=lambda device: None,
            mem_get_info=lambda device: (2 * 1024**3, 16 * 1024**3),
            memory_allocated=lambda device: 500, memory_reserved=lambda device: 600,
            max_memory_allocated=lambda device: 750, max_memory_reserved=lambda device: 800,
            is_initialized=lambda: False, is_available=lambda: True,
            device_count=lambda: 1, get_device_name=lambda device: "Tesla T4")
        self.version = SimpleNamespace(cuda="CPU mock")

    def manual_seed(self, seed):
        self.seed = seed

    def set_cuda_seed(self, seed):
        self.cuda_seed = seed

    def initial_seed(self):
        return self.seed

    def tensor(self, data, *, dtype, device):
        return Tensor(data, dtype=dtype, device=device)

    def inference_mode(self):
        return nullcontext()

    def isfinite(self, scores):
        return SimpleNamespace(all=lambda: SimpleNamespace(item=lambda: self.finite))


class Qwen3_5ForCausalLM:
    def __init__(self, *, tied=False):
        self.config = SimpleNamespace(model_type="qwen3_5_text", tie_word_embeddings=tied)
        self.is_loaded_in_4bit = True
        self.hf_quantizer = SimpleNamespace(quantization_config=SimpleNamespace(
            bnb_4bit_quant_type="nf4", bnb_4bit_use_double_quant=True,
            bnb_4bit_compute_dtype="torch.float16"))
        self.embedding = Tensor()
        self.head = self.embedding if tied else Tensor()
        self.hf_device_map = {"": 0}
        self.hooks = []
        self.calls = []
        self.reply_ids = tuple(ord(c) for c in '{"candidate":[0,0,0,0,0,0,0,0],"send":[]}') + (TRANSPORT_ID,)
        self.fail = False

    def named_parameters(self):
        return iter([("model.embed_tokens.weight", self.embedding)] +
                    ([] if self.head is self.embedding else [("lm_head.weight", self.head)]))

    def named_buffers(self):
        return iter(())

    def get_input_embeddings(self):
        return SimpleNamespace(weight=self.embedding)

    def get_output_embeddings(self):
        return SimpleNamespace(weight=self.head)

    def eval(self):
        return self

    def register_forward_pre_hook(self, hook, *, with_kwargs):
        assert with_kwargs
        self.hooks.append(hook)
        return SimpleNamespace(remove=lambda: self.hooks.remove(hook))

    def generate(self, **kwargs):
        import weakref
        for hook in self.hooks:
            hook(self, (), dict(past_key_values=kwargs["past_key_values"]))
        cache = kwargs["past_key_values"]
        self.calls.append(dict(seed=kwargs["logits_processor"][0].torch.seed,
            cache=weakref.ref(cache), config=vars(kwargs["generation_config"]),
            inputs=kwargs["input_ids"].tolist(), kwargs=tuple(kwargs)))
        kwargs["logits_processor"][0](kwargs["input_ids"], Tensor())
        if self.fail:
            raise ValueError("CPU simulated generation defect")
        cache.length = 123
        cache.recurrent = True
        return SimpleNamespace(sequences=Tensor([kwargs["input_ids"].tolist()[0] + list(self.reply_ids)]))


def backend():
    return TransformersBackend(Torch(), Qwen3_5ForCausalLM(), Tokenizer(), QWEN_9B,
                               {"kind": "CPU mock load", "pid": os.getpid(),
                                "cuda_visible_devices": os.environ.get("CUDA_VISIBLE_DEVICES")})


def mock_transformers():
    return SimpleNamespace(DynamicCache=Cache, GenerationConfig=GenerationConfig, LogitsProcessorList=list)


def process_backend():
    """Picklable fixture: the existing subprocess invokes the actual adapter."""
    import sys
    sys.modules["transformers"] = mock_transformers()
    return backend()


def process_nonfinite_backend():
    value = process_backend()
    value.torch.finite = False
    return value


LOADING_INFO = dict(missing_keys=set(), unexpected_keys=set(), mismatched_keys=set(), error_msgs=[])
