# Course M5 R7 offline continuation

11 October 2026, starting at `2c566b4` on
`feat/course-m5-inference-preparation`, with a clean tree. The user explicitly
requested resolution of R7 offline, preserving the scientific contract and
avoiding GPU execution. Authority remains
[specification Section 11](../../PROJECT_SPECIFICATION.md#11-adopted-absiis-course-regime)
and [course M5-T01](../todos/course/M5/M5-T01-course-inference-and-smoke-preparation.md).

Reuse the [verified preparation](course-m5-inference-and-smoke-preparation.md),
complete native input argument, pinned metadata and maintained source. Investigate
a sound tighter byte/merge certificate and the actual chunk/cache/quantization
tensor lifetimes and native workspace allocations. A proof tightening may change
analysis bounds; it must change no rendered bytes, protocol limits, outcomes,
populations, model revision or thesis defaults. Samples are challenges, not proof.

Preserve prior source packets/results and prerequisite artifacts. Starting hashes
are retained in [the new baseline](../../notebooks/validation/course-m5-r7/baseline-files.json.gz).
Commands/results belong in [the R7 evidence folder](../../notebooks/validation/course-m5-r7/).
No GPU, model weight staging, actual-host acceptance, pilot/main, freeze or
publication is authorized here. Preparation remains withheld until the
three-outcome R7 contract has a sufficient reviewed outcome. No terminal model
failure is inferred from an incomplete memory subtotal.

**Current outcome:** a sound tighter complete input bound is verified. R7's
complete physical memory/headroom argument is **still unresolved**, so
course/M5-T01 remains blocked and unfinished. No terminal model feasibility
failure is accepted. This continuation used metadata, tokenizer, native source
and virtual meta tensors only; no language weights were staged or loaded,
CUDA initialized, GPU reserved or experiment executed.

## Capacity checkpoint

The [supplemental proof](../implementation-research/course-m5-r7-capacity-proof.md)
reduces both native payload factors to 32, giving 109,851 input plus the
unchanged 256 output reserve: **110,107 resident tokens**. All five families
remain covered. The native audit covers all 248,077 loaded entries, all
1,112,064 Unicode scalars and the 243 unassigned output IDs that decode empty.
Five focused source checks pass with zero skips, including original literal
requests, ASCII regex/contraction boundaries and cross-token normalization.
See [the source report](../../notebooks/validation/course-m5-r7/native-tightening-source.json)
and [exact command](../../notebooks/validation/course-m5-r7/native-tightening-source-command.json).
The initial failed receipt retains a test-harness assumption about an absent
saved fixture field; the corrected checks compare actual native counts and
literal history. It establishes no model failure. Independent outside-checkout
verification and the final memory decision are recorded below.

## Outside-checkout verification

At capacity checkpoint `5ce6d5f`, all five checks reproduce with zero skips
outside the repository and a fresh hash seed (211). The copied new proof is
checked against the exact committed bytes. All 29 maintained runtime modules
match the previously verified installed wheel at `0260ca6`; no source
`PYTHONPATH` is injected and the actual imported package path is audited.
The complete resulting report equals the source report, including every
family's arithmetic, vocabulary/Unicode coverage and pinned metadata identity.
See [the command](../../notebooks/validation/course-m5-r7/outside-native-command.json),
[lossless log](../../notebooks/validation/course-m5-r7/outside-native.txt.gz) and
[provenance/result](../../notebooks/validation/course-m5-r7/outside-provenance.json).
The unchanged course M1–M4 gates and 64 source/64 installed adapter/packet checks
were reused; no broad lifecycle, attainability or model smoke was repeated.

Environment: local Python 3.11, Tokenizers 0.22.2, Transformers 5.12.0 and
Torch 2.11.0+cpu. Critical maintained Transformers files match the eight hashes
already retained for the candidate. This is not acceptance of the Linux 3.13
CUDA package host, its library dispatch, precision or performance.

## Tensor and native-source review

The read-only [review helper](../../notebooks/validation/course-m5-r7/review_memory.py)
reuses the existing language inventory, `memory_review` and `model_estimates`;
it changes only their analytical resident length. The
[saved result](../../notebooks/validation/course-m5-r7/offline-memory-review.json)
retains original arithmetic separately and keeps all admission flags false.

| Quantity | Bytes | Scope |
|---|---:|---|
| FP16 eight-layer KV at 110,107 | 3,607,986,176 | Architecture arithmetic |
| KV reduction from 156,251 | 1,512,046,592 | About 1.41 GiB; no runtime cap change |
| Tightened conditional component sum | 7,400,914,336 | Weights/metadata/states/KV/copy/mask terms; incomplete peak |
| Historical native total minus 1.5-GiB headroom | 14,025,424,896 | Run 6 per T4; current free memory remains unknown |
| Remaining allowance for omitted terms | 6,624,510,560 | Positive slack, not a bound on those terms |

The [meta trace](../../notebooks/validation/course-m5-r7/trace_meta_memory.py)
constructs the actual pinned text model on the meta device, excluding parameter
storage, and follows tensor storage aliases/lifetimes through all 32 layers.
The efficient CUDA kernel is substituted with its source-declared FP16 output
and conservative FP32 accumulator. The real grouped K/V view helper runs and
alias checks pass. All eight attention layers execute per case. Virtual cache
shapes cover a first 256-token chunk, a 256-token chunk at the complete bound
and single-token decode at that bound; these are shape-analysis constructions,
not fabricated legal requests or pretrained-model outputs.

| Case | Observed meta storage bytes | Peak operator |
|---|---:|---|
| First prefill | 93,315,072 | add |
| Largest cached chunk | 3,897,131,776 | cache concatenation |
| Full-envelope decode | 3,860,368,171 | cache concatenation |

The [corrected trace/result](../../notebooks/validation/course-m5-r7/meta-memory-corrected.json)
and [command](../../notebooks/validation/course-m5-r7/meta-memory-corrected-command.json)
retain all stage peaks, operation counts and source hashes. The initial trace
is preserved; its only correction resets the stage label before each case.
Peaks are unchanged. Weak-reference meta accounting observes virtual tensor
storage, not CUDA allocator reservation or non-Tensor native allocations.
It excludes quantized parameters, actual loading, real kernel execution and
whole-generation mask preparation; the existing conservative mask arithmetic
remains separate. Do not add this observation to the conditional subtotal or
call it a complete GPU upper bound.

Twelve inspected public native sources (Torch 2.11.0, bitsandbytes 0.49.2,
Tokenizers 0.22.2), with URLs, exact bytes and hashes, are preserved in
[the source archive](../../notebooks/validation/course-m5-r7/native-sources.json.gz).
[Capture](../../notebooks/validation/course-m5-r7/source-capture-command.json)
verifies 722,473 source bytes; it downloads/stages no model assets.

- The [efficient-attention wrapper](https://github.com/pytorch/pytorch/blob/v2.11.0/aten/src/ATen/native/transformers/cuda/attention.cu)
  allocates output and an optional same-shape FP32 accumulator. Its CUDA path
  receives actual K/V strides, including the adapter's broadcast batch stride;
  no global score matrix or explicit repeated K/V allocation appears there.
  The chunk output is 2,097,152 bytes and the optional accumulator 4,194,304.
  The inspected path still requires eventual candidate-host acceptance.
- The [NF4 forward](https://github.com/bitsandbytes-foundation/bitsandbytes/blob/0.49.2/bitsandbytes/autograd/_functions.py)
  dequantizes one active projection for chunked linear operations, rather than
  all matrices simultaneously. The largest inventoried matrix has 23,592,960
  elements: one FP16 copy is 47,185,920 bytes. Two such copies and two FP32
  absmax arrays conservatively total 97,320,960 bytes under the proposed FP16
  state. This is a conditional projection allowance, not verified loading peak.
- [Torch's cuBLAS pools](https://github.com/pytorch/pytorch/blob/v2.11.0/aten/src/ATen/cuda/CublasHandlePool.cpp)
  default to 8,519,680 cuBLAS bytes and 1,048,576 cuBLASLt bytes per relevant
  handle/stream on this architecture. They do not bound other library/context
  occupancy or establish actual host overrides/handle counts.
- The reviewed [convolution selector](https://github.com/pytorch/pytorch/blob/v2.11.0/aten/src/ATen/native/Convolution.cpp)
  can admit FP16 1-D depthwise convolution to cuDNN; filter width four does
  not rule that route out. The [cuDNN wrapper](https://github.com/pytorch/pytorch/blob/v2.11.0/aten/src/ATen/native/cudnn/Conv_v8.cpp)
  allocates the selected plan's reported workspace. That host-specific amount
  is absent from the CPU/meta trace and cannot be assigned zero.
- The [caching allocator](https://github.com/pytorch/pytorch/blob/v2.11.0/c10/cuda/CUDACachingAllocator.cpp)
  may retain freed blocks while cache sizes grow across chunks. Live tensor
  bytes therefore do not bound reserved physical memory. No allocator setting
  changed. An allocation cap alone would limit reservations or cause OOM; it
  would not prove that the complete call fits or bound other CUDA occupancy.

## Preparation decision and handoff

The input portion of R7 has advanced: use **110,107** for supplemental course
memory analysis, while retaining the original capacity archive and exact
24-request CPU packet unchanged. No scientific limit or implementation setting
changed. The original packet remains a verified CPU-only artifact at `0260ca6`;
it has not become an executable model-smoke packet from this analysis.

No R7 outcome yet supplies a complete supported physical peak/headroom bound
or proves that the candidate cannot support the required envelope. The remaining
work needs a supported bound for actual quantized loading/native workspaces and
allocator/context occupancy across the full call, including prior serial calls.
Neither the short stress requests, synthetic meta caches nor arbitrary reserve
allowances close it. Current task status is blocked; M5-T02 and M6 remain blocked.
Refresh committed source/request/host provenance only when a sufficient R7
argument permits the next preparation step. Actual host acceptance, recovered
prior spending, quota/duration/release and GPU authorization remain separate.

The [completion audit](../../notebooks/validation/course-m5-r7/completion-audit.json)
checks protected baseline bytes, unchanged pre-course plan/specification and
thesis defaults/todos, task counts/links, source/installed report agreement and
all withheld admission/unknown fields. This audit verifies the limited offline
outcome; it does not mark M5-T01 complete.
