"""Real pinned Transformers configuration/processors, CPU tensors, no model."""

from copy import deepcopy
from types import SimpleNamespace


def check_generation_contract(tokenizer, settings, *, model_eos=248044):
    import torch
    from transformers import GenerationConfig, __version__
    from transformers.generation.utils import GenerationMixin
    from transformers.generation.logits_process import LogitsProcessorList
    from transformers.generation.stopping_criteria import StoppingCriteriaList
    from recovery.inference import _FiniteScores

    if __version__ != "5.12.0":
        raise ValueError("check the exact pinned Transformers implementation")

    class ConfigurationOnly(GenerationMixin):
        config = SimpleNamespace(is_encoder_decoder=False)
        generation_config = GenerationConfig(eos_token_id=model_eos)

    owner = ConfigurationOnly()
    before = deepcopy(settings)
    ordinary, _ = owner._prepare_generation_config(GenerationConfig(**settings["generation"]))
    assert ordinary.eos_token_id == settings["generation"]["eos_token_id"] == [248044, 248046]
    ids = torch.ones((1, 109851), dtype=torch.long, device="cpu")
    observed = {}
    for label, eos in (("old_none", None), ("diagnostic", [])):
        requested = GenerationConfig(**settings["generation"])
        requested.eos_token_id = eos
        requested.min_new_tokens = requested.max_new_tokens = 256
        config, _ = owner._prepare_generation_config(requested)
        owner._prepare_special_tokens(config, kwargs_has_attention_mask=True, device="cpu")
        config = owner._prepare_generated_length(config, has_default_max_length=True,
            has_default_min_length=True, model_input_name="input_ids", input_ids_length=109851, inputs_tensor=ids)
        finite = _FiniteScores(torch)
        processors = owner._get_logits_processor(config, input_ids_seq_length=109851,
            logits_processor=LogitsProcessorList([finite]), device="cpu", model_kwargs={})
        scores = torch.zeros((1, 248047), device="cpu")
        rejected = False
        try:
            for processor in processors:
                scores = processor(ids, scores)
                if processor is finite:
                    break  # sampling warpers intentionally mask scores AFTER this audit
        except ValueError as error:
            if "nonfinite model scores" not in str(error):
                raise
            rejected = True
        if label == "old_none":
            assert config.eos_token_id == model_eos and rejected
        else:
            assert config.eos_token_id == [] and not rejected and finite.steps == 1
            assert config.max_length == config.min_length == 110107
            criteria = owner._get_stopping_criteria(config, stopping_criteria=StoppingCriteriaList(), tokenizer=tokenizer)
            assert not criteria(ids, scores).any().item()
        observed[label] = dict(effective_eos=config.eos_token_id, finite_check_rejected=rejected,
            processors=[type(p).__name__ for p in processors])
    assert settings == before
    return dict(transformers=__version__, torch=torch.__version__, tensor_device="cpu",
        native_model_loaded=False, gpu_calls=0, ordinary_settings_unchanged=True,
        forced_output_tokens=256, checks=observed)
