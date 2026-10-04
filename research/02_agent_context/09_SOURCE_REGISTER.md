# Source register

Research checked on **2026-09-24**. “Inspected” means the relevant text/documentation was accessible and reviewed; it does not mean the software or paper results were reproduced. Living docs and repository metadata must be checked again when versions are locked.

## Research sources

| ID | Primary source | Evidence status and scope |
|---|---|---|
| R1 | [From Faulty Memories to Corrected Actions — v1](https://arxiv.org/html/2608.10502v1) · [abstract](https://arxiv.org/abs/2608.10502) | Relevant method sections and prompt-contract appendix inspected; dated August 2026. |
| R2 | [MemTX — v2](https://arxiv.org/html/2607.23929v2) · [abstract](https://arxiv.org/abs/2607.23929) · [linked repository](https://github.com/lxy1134/MEMTX_) | Relevant method/evaluation sections inspected; repository README/listing inspected. No runtime reproduction or permission-to-vendor conclusion. |
| R3 | [REVISE — v1](https://arxiv.org/html/2609.00643v1) · [abstract](https://arxiv.org/abs/2609.00643) | Relevant method/evaluation text inspected. Specific official code repository not verified in this update. |
| R4 | [MemoRepair — v1](https://arxiv.org/html/2605.07242v1) · [abstract](https://arxiv.org/abs/2605.07242) | Relevant withdrawal/repair method inspected. |
| R5 | [Repair Sets Before Repair Choices: Identifiable Rollback Families for Self-Evolving Agent Memory](https://openreview.net/forum?id=IJoWb6T3RJ) · [PDF route](https://openreview.net/pdf?id=IJoWb6T3RJ) | Index/title located; forum/PDF access challenged; full-text comparison unresolved. Do not treat indexed snippets as a complete method review. |
| R6 | [AgentGit paper](https://arxiv.org/abs/2511.00628) · [research repository](https://github.com/MAS-Infra-Layer/Agent-Git) | Repository description and paper metadata reviewed; runtime suitability untested. |

## Technology sources

| ID | Official source | Evidence status and intended use |
|---|---|---|
| T1 | [LangGraph time travel](https://docs.langchain.com/oss/python/langgraph/use-time-travel) · [persistence](https://docs.langchain.com/oss/python/langgraph/persistence) · [repository](https://github.com/langchain-ai/langgraph) | Documentation verified. Establishes documented checkpoint/replay behavior, not project-specific isolation correctness. |
| T2 | [Microsoft Agent Framework workflow checkpoints](https://learn.microsoft.com/en-us/agent-framework/workflows/checkpoints) · [repository](https://github.com/microsoft/agent-framework) | Documented checkpoint scope reviewed. Exact counterfactual branch semantics need testing. |
| T3 | [PydanticAI graph](https://pydantic.dev/docs/ai/graph/graph/) · [durable execution](https://pydantic.dev/docs/ai/capabilities/durable_execution/overview/) | Relevant typed/durable alternatives reviewed. Not selected or tested. |
| T4 | [vLLM GPU installation](https://docs.vllm.ai/en/stable/getting_started/installation/gpu/) | Current documented GPU baseline includes T4. Actual runtime/wheel/environment compatibility untested. |
| T5 | [vLLM quantization](https://docs.vllm.ai/en/stable/features/quantization/) · [structured outputs](https://docs.vllm.ai/en/stable/features/structured_outputs/) | Current compatibility matrix and API changes inspected. A supported combination is not a throughput guarantee. |
| T6 | [Transformers bitsandbytes](https://huggingface.co/docs/transformers/en/quantization/bitsandbytes) | Relevant quantization documentation reviewed. Model-specific memory and speed unmeasured. |
| T7 | [Inspect documentation](https://inspect.aisi.org.uk/) · [multi-agent evaluations](https://inspect.aisi.org.uk/multi-agent.html) | Evaluation framework capabilities reviewed; optional candidate only. |
| T8 | [Phoenix documentation](https://arize.com/docs/phoenix) | Tracing/inspection capability reviewed; not necessary to scientific semantics. |
| T9 | [NetworkX descendants](https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.dag.descendants.html) | Reachability API; does not establish sufficient-support semantics. |
| T10 | [DuckDB Parquet documentation](https://duckdb.org/docs/current/data/parquet/overview.html) | Analysis/storage option, not a selected infrastructure requirement. |
| T11 | [Official AutoGen project update](https://github.com/microsoft/autogen/discussions/7066) | Maintenance-direction evidence; verify again before selecting a new long-lived dependency. |
| T12 | [LangChain State of Agent Engineering](https://www.langchain.com/state-of-agent-engineering) | Vendor survey reviewed as contextual adoption evidence only. Not a representative ranking of production framework usage. |

## Inherited repository audit — not freshly pinned

These identifiers are copied from the original `source_audit.json`; current commit-level contents were not all independently verified in this update.

| Repository | Inherited commit | Action before reuse |
|---|---|---|
| [SILO](https://github.com/jwyjohn/acl26-silo-bench) | `e74127782ed1c42fff474249961f022c063d76f2` | Verify commit, actual dependency boundary, Python requirements, and license metadata. |
| [MemTX](https://github.com/lxy1134/MEMTX_) | `4e1124ccd5fd384857463020e3497aa73ec93be6` | Verify commit and licensing before importing code; current README review does not replace that check. |
| [MasDrift](https://github.com/ZhuoningXu/MasDrift) | `7119c09c0266162f89db29d3faa32d496837b5c3` | Verify dataset semantics, provenance and license; distinguish controlled adaptation from native evaluation. |

## Evidence not supplied by web research

User preferences and the two confirmed answers come from this conversation. The 34-file baseline and inherited budgets come from the original ZIP. Acceptance tests, stack recommendations, and causal-risk analysis in this companion are analytical proposals, not claims of experimental success. The unchanged background reports are secondary historical material.

## Search limits

The review prioritized the blueprint's closest repair/provenance papers, checkpoint semantics, current local-serving compatibility, and relevant evaluation tools. It did not establish an exhaustive survey, global deployment ranking, complete license clearance, benchmark reproduction, or empirical T4 results. Keep this distinction when converting context into the specification.

## Model amendment sources

**T13 — official Qwen model cards:** [Qwen3.5-9B](https://huggingface.co/Qwen/Qwen3.5-9B) and [Qwen3.5-4B](https://huggingface.co/Qwen/Qwen3.5-4B), inspected 2026-09-24. These establish available sizes and documented model architecture/interfaces; they do not establish measured T4 memory or throughput. Weight-memory figures in the compute note are approximate parameter arithmetic, not benchmark results. The 9B 4-bit choice is a pilot recommendation informed by earlier project context; 4B remains the lower-memory fallback.
