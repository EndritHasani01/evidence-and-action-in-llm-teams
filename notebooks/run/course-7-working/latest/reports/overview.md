# I-01 course recovery report — complete

Execution policy: i01-recorded-outcomes-run-all-2026-10-15. Human communication/mechanism review: retrospective_pending. Automatic pilot checks establish protocol/evidence/resource eligibility, not useful communication or human approval. See pilot_checks.csv and the complete conversations.

Intended main population: 20 independent worlds; known paired outcomes: 20/20. Budget scope: independent-study. Current-study physical attempts: 252; prior-study charges: 0; campaign total: 252/500. Shared contingency used: 0/28; historical 45 recorded separately.

## Qualification and protocol admission

Mathematical accuracy is reported separately from protocol eligibility. Historical decisions retain their original rule. Thinking completion is not inferred from a missing aggregate.

| Mode | Committed / planned | Correct | Wrong scalar | Invalid | Unexecuted | Current eligible | Ready seconds | Tokens | Historical passed |
|---|---:|---:|---:|---:|---:|---|---:|---:|---|
| direct | 12/12 | 10 | 2 | 0 | 0 | True | 27.516 | 193 | True |
| thinking | 0/12 | 0 | 0 | 0 | 12 | False | 0.000 | 0 | not recorded |

See qualification_controls.csv and conversations.html for every planned control, exact answer/truth, validity, effort and call reference. Unresolved attempts and raw-but-uncommitted calls are pending, not unexecuted.

Known prior studies still requiring reconciliation: []. Remaining allowance: 248 (unknown blocks admission).

Clear-minus-retain mean: 0.0; unknown bounds: [0.0, 0.0]. Correct-prefix descriptive denominator: 3; unknown prefixes: 0.

This is a controlled recovery extension of SILO-BENCH I-01. Clearing removes remote information in prior messages. Small sample and one seed/prefix per world limit inference; zero-width intervals do not establish equivalence. Principal effort is ready-model recovery inference time. Costs of unsuccessful episodes are spending, not useful efficiency. Loading, observed allocation and unknown provider time are separate. Shared prefix is physically charged once and logically to both policies. No native benchmark, pure anchoring, correction-specific, broad generalization or superiority claim follows.

Review every trace using the frozen rubric; human labels require call references. Ambiguous mechanisms remain ambiguous. Save the executed notebook separately and download the latest portable archive off session.

```json
{
  "status": "complete",
  "intended_worlds": 20,
  "known_pairs": 20,
  "paired_counts": {
    "neither": 17,
    "clear_only": 1,
    "retain_only": 1,
    "both": 1
  },
  "clear_minus_retain": 0.0,
  "complete_case_descriptive_mean": 0.0,
  "missingness_bounds": [
    0.0,
    0.0
  ],
  "interval": {
    "low": -0.1,
    "high": 0.1,
    "confidence": 0.95,
    "draws": 10000,
    "strata": "owner/first-speaker",
    "caveat": "Exploratory small-sample interval."
  },
  "correct_prefix_denominator": 3,
  "unknown_prefixes": 0,
  "correct_prefix_interval": {
    "low": 0.0,
    "high": 0.6666666666666666,
    "confidence": 0.95,
    "draws": 10000,
    "strata": "owner/first-speaker",
    "caveat": "Exploratory small-sample interval."
  },
  "correct_prefix_mean": 0.3333333333333333,
  "attempts": 252,
  "contingency": 0,
  "hard_limit": 500,
  "historical_attempts_separate": 45,
  "in_flight": 0,
  "gates": {
    "logical_slot": 0,
    "qualification_policy": "i01-direct-protocol-2026-10-15",
    "attempt_scope": "independent-study",
    "required_preparation_studies": [],
    "window": {
      "deadline": "2026-10-16T05:20:47.399377+00:00",
      "evidence": "User reports an approximately 12-hour session; 700-minute fresh-session planning bound, provider quota/deadline not independently verified.",
      "observation": {
        "at": "2026-10-15T17:40:47.399455+00:00",
        "basis": "planning_estimate",
        "remaining_minutes": 700
      },
      "observed_start": "2026-10-15T17:44:39.516556+00:00",
      "session": "a7bb7845-cf04-4efd-9b68-f74b9595cfaa"
    },
    "selfcheck": {
      "checks": [
        "native fixture 827/revised 780; duplicates/negative/boundary",
        "fixed strata/seeds; private views; finality/wait; literal siblings; invalid actions",
        "raw-before-effects; idempotence; pre-persistence retry; 499/500; backup/ZIP/expanded restore; unknown vs zero"
      ],
      "environment": "scripted temporary DBs; no model loaded",
      "executed_at": "2026-10-15T17:44:54.096080+00:00",
      "model_attempts": 0,
      "native_tokenizer": true,
      "passed": true,
      "tokenizer": {
        "conservative_input_bound": 6885,
        "framing": "native exact template; no truncation",
        "input_limit": 8192,
        "resident_direct": 8704,
        "resident_thinking": 12288,
        "template": "{%- set image_count = namespace(value=0) %}\n{%- set video_count = namespace(value=0) %}\n{%- macro render_content(content, do_vision_count, is_system_content=false) %}\n    {%- if content is string %}\n        {{- content }}\n    {%- elif content is iterable and content is not mapping %}\n        {%- for item in content %}\n            {%- if 'image' in item or 'image_url' in item or item.type == 'image' %}\n                {%- if is_system_content %}\n                    {{- raise_exception('System message cannot contain images.') }}\n                {%- endif %}\n                {%- if do_vision_count %}\n                    {%- set image_count.value = image_count.value + 1 %}\n                {%- endif %}\n                {%- if add_vision_id %}\n                    {{- 'Picture ' ~ image_count.value ~ ': ' }}\n                {%- endif %}\n                {{- '<|vision_start|><|image_pad|><|vision_end|>' }}\n            {%- elif 'video' in item or item.type == 'video' %}\n                {%- if is_system_content %}\n                    {{- raise_exception('System message cannot contain videos.') }}\n                {%- endif %}\n                {%- if do_vision_count %}\n                    {%- set video_count.value = video_count.value + 1 %}\n                {%- endif %}\n                {%- if add_vision_id %}\n                    {{- 'Video ' ~ video_count.value ~ ': ' }}\n                {%- endif %}\n                {{- '<|vision_start|><|video_pad|><|vision_end|>' }}\n            {%- elif 'text' in item %}\n                {{- item.text }}\n            {%- else %}\n                {{- raise_exception('Unexpected item type in content.') }}\n            {%- endif %}\n        {%- endfor %}\n    {%- elif content is none or content is undefined %}\n        {{- '' }}\n    {%- else %}\n        {{- raise_exception('Unexpected content type.') }}\n    {%- endif %}\n{%- endmacro %}\n{%- if not messages %}\n    {{- raise_exception('No messages provided.') }}\n{%- endif %}\n{%- if tools and tools is iterable and tools is not mapping %}\n    {{- '<|im_start|>system\\n' }}\n    {{- \"# Tools\\n\\nYou have access to the following functions:\\n\\n<tools>\" }}\n    {%- for tool in tools %}\n        {{- \"\\n\" }}\n        {{- tool | tojson }}\n    {%- endfor %}\n    {{- \"\\n</tools>\" }}\n    {{- '\\n\\nIf you choose to call a function ONLY reply in the following format with NO suffix:\\n\\n<tool_call>\\n<function=example_function_name>\\n<parameter=example_parameter_1>\\nvalue_1\\n</parameter>\\n<parameter=example_parameter_2>\\nThis is the value for the second parameter\\nthat can span\\nmultiple lines\\n</parameter>\\n</function>\\n</tool_call>\\n\\n<IMPORTANT>\\nReminder:\\n- Function calls MUST follow the specified format: an inner <function=...></function> block must be nested within <tool_call></tool_call> XML tags\\n- Required parameters MUST be specified\\n- You may provide optional reasoning for your function call in natural language BEFORE the function call, but NOT after\\n- If there is no function call available, answer the question like normal with your current knowledge and do not tell the user about function calls\\n</IMPORTANT>' }}\n    {%- if messages[0].role == 'system' %}\n        {%- set content = render_content(messages[0].content, false, true)|trim %}\n        {%- if content %}\n            {{- '\\n\\n' + content }}\n        {%- endif %}\n    {%- endif %}\n    {{- '<|im_end|>\\n' }}\n{%- else %}\n    {%- if messages[0].role == 'system' %}\n        {%- set content = render_content(messages[0].content, false, true)|trim %}\n        {{- '<|im_start|>system\\n' + content + '<|im_end|>\\n' }}\n    {%- endif %}\n{%- endif %}\n{%- set ns = namespace(multi_step_tool=true, last_query_index=messages|length - 1) %}\n{%- for message in messages[::-1] %}\n    {%- set index = (messages|length - 1) - loop.index0 %}\n    {%- if ns.multi_step_tool and message.role == \"user\" %}\n        {%- set content = render_content(message.content, false)|trim %}\n        {%- if not(content.startswith('<tool_response>') and content.endswith('</tool_response>')) %}\n            {%- set ns.multi_step_tool = false %}\n            {%- set ns.last_query_index = index %}\n        {%- endif %}\n    {%- endif %}\n{%- endfor %}\n{%- if ns.multi_step_tool %}\n    {{- raise_exception('No user query found in messages.') }}\n{%- endif %}\n{%- for message in messages %}\n    {%- set content = render_content(message.content, true)|trim %}\n    {%- if message.role == \"system\" %}\n        {%- if not loop.first %}\n            {{- raise_exception('System message must be at the beginning.') }}\n        {%- endif %}\n    {%- elif message.role == \"user\" %}\n        {{- '<|im_start|>' + message.role + '\\n' + content + '<|im_end|>' + '\\n' }}\n    {%- elif message.role == \"assistant\" %}\n        {%- set reasoning_content = '' %}\n        {%- if message.reasoning_content is string %}\n            {%- set reasoning_content = message.reasoning_content %}\n        {%- else %}\n            {%- if '</think>' in content %}\n                {%- set reasoning_content = content.split('</think>')[0].rstrip('\\n').split('<think>')[-1].lstrip('\\n') %}\n                {%- set content = content.split('</think>')[-1].lstrip('\\n') %}\n            {%- endif %}\n        {%- endif %}\n        {%- set reasoning_content = reasoning_content|trim %}\n        {%- if loop.index0 > ns.last_query_index %}\n            {{- '<|im_start|>' + message.role + '\\n<think>\\n' + reasoning_content + '\\n</think>\\n\\n' + content }}\n        {%- else %}\n            {{- '<|im_start|>' + message.role + '\\n' + content }}\n        {%- endif %}\n        {%- if message.tool_calls and message.tool_calls is iterable and message.tool_calls is not mapping %}\n            {%- for tool_call in message.tool_calls %}\n                {%- if tool_call.function is defined %}\n                    {%- set tool_call = tool_call.function %}\n                {%- endif %}\n                {%- if loop.first %}\n                    {%- if content|trim %}\n                        {{- '\\n\\n<tool_call>\\n<function=' + tool_call.name + '>\\n' }}\n                    {%- else %}\n                        {{- '<tool_call>\\n<function=' + tool_call.name + '>\\n' }}\n                    {%- endif %}\n                {%- else %}\n                    {{- '\\n<tool_call>\\n<function=' + tool_call.name + '>\\n' }}\n                {%- endif %}\n                {%- if tool_call.arguments is defined %}\n                    {%- for args_name, args_value in tool_call.arguments|items %}\n                        {{- '<parameter=' + args_name + '>\\n' }}\n                        {%- set args_value = args_value | tojson | safe if args_value is mapping or (args_value is sequence and args_value is not string) else args_value | string %}\n                        {{- args_value }}\n                        {{- '\\n</parameter>\\n' }}\n                    {%- endfor %}\n                {%- endif %}\n                {{- '</function>\\n</tool_call>' }}\n            {%- endfor %}\n        {%- endif %}\n        {{- '<|im_end|>\\n' }}\n    {%- elif message.role == \"tool\" %}\n        {%- if loop.previtem and loop.previtem.role != \"tool\" %}\n            {{- '<|im_start|>user' }}\n        {%- endif %}\n        {{- '\\n<tool_response>\\n' }}\n        {{- content }}\n        {{- '\\n</tool_response>' }}\n        {%- if not loop.last and loop.nextitem.role != \"tool\" %}\n            {{- '<|im_end|>\\n' }}\n        {%- elif loop.last %}\n            {{- '<|im_end|>\\n' }}\n        {%- endif %}\n    {%- else %}\n        {{- raise_exception('Unexpected message role.') }}\n    {%- endif %}\n{%- endfor %}\n{%- if add_generation_prompt %}\n    {{- '<|im_start|>assistant\\n' }}\n    {%- if enable_thinking is defined and enable_thinking is false %}\n        {{- '<think>\\n\\n</think>\\n\\n' }}\n    {%- else %}\n        {{- '<think>\\n' }}\n    {%- endif %}\n{%- endif %}"
      }
    },
    "resident_load": "a7bb7845-cf04-4efd-9b68-f74b9595cfaa/load-0",
    "loaded_session": "a7bb7845-cf04-4efd-9b68-f74b9595cfaa",
    "execution_plan": {
      "at": "2026-10-15T17:49:51.504874+00:00",
      "external_download_verified": false,
      "human_review": "retrospective_pending",
      "human_understanding_verified": false,
      "main_admission": "three objective pilot passes and adequate measured resources; no settings tuning",
      "main_batches": 10,
      "manifest": {
        "config": {
          "agents": 2,
          "attempt_limit": 500,
          "bootstrap_confidence": 0.95,
          "bootstrap_draws": 10000,
          "bootstrap_seed": 2026101402,
          "checkpoint_seconds": 300,
          "contingency_limit": 28,
          "direct_output_tokens": 512,
          "direct_timeout_seconds": 180,
          "export_reserve_seconds": 120,
          "feedback_tokens": 32,
          "headroom_bytes": 1610612736,
          "historical_attempts_separate": 45,
          "input_tokens": 8192,
          "load_timeout_seconds": 600,
          "main_worlds": 20,
          "master_seed": 2026101401,
          "max_proposals": 1000,
          "model": "Qwen/Qwen3.5-9B",
          "pilot_worlds": 3,
          "qualification_worlds": 6,
          "regime": "i01-course-v1",
          "revision": "c202236235762e1c871ad0ccb60c8ee5ba337b9a",
          "rubric": [
            "wrong_submission",
            "noncompletion",
            "premature_finalization",
            "obsolete_value_repeated",
            "malformed_action",
            "truncated_action",
            "waiting_deadlock",
            "horizon_exhausted",
            "provider_failure",
            "ambiguous"
          ],
          "schema": 1,
          "shard_size": 20,
          "termination_seconds": 5,
          "thinking_output_tokens": 4096,
          "thinking_timeout_seconds": 900,
          "turns_per_agent": 3,
          "visible_output_tokens": 512
        },
        "created_at": "2026-10-15T17:44:38.664054+00:00",
        "direct_first_attempts": 460,
        "historical_attempts_separate": 45,
        "planned_first_attempts": 472,
        "regime": "i01-course-v1",
        "source_identity": {
          "configs/i01-course.json": "89e91b0e69f8f0851083e5016020b30c1d0b635dc5a00f142f9955bdd60c9a23",
          "configs/i01-runtime.lock": "5b1d91aa431a39ff725cfe4314706fe7a854af85a6e3ea492dd22d8c68d9bc56",
          "pyproject.toml": "d851f00351b3221aef8c92b5757aecf477f2942b03afbfb6925190220b1494b1",
          "recovery/__init__.py": "b11591ab36164605ffe2de304b0503780e6b2c340b2c466e51b9c132dae0d738",
          "recovery/__main__.py": "a32e2fa488314eae101a42fb5520951565d7ab5f5c9f36aa4feeac88c529325a",
          "recovery/accounting.py": "4b910adf52a7583550fc60d8a201671e2a13d125cd4bfe67588acb85df3315d1",
          "recovery/analysis.py": "3740e341f07dfd3884363cf24935bdbf3b93de49e99b31b2b935928b46aa9e22",
          "recovery/attempts.py": "bac975625c7da55d5abcd4d2d75ba6ad91bb1cdd5b23028ff90794c84e502eb4",
          "recovery/costs.py": "6e2f8358177c00313b1f71fb755ec3bbb1b522d38e60ad22fabe8aec939bf82b",
          "recovery/edits.py": "bc378e9c65bb6abe243416b20b54be8a59eadb15fe2b70c2c4ce46527ab064fc",
          "recovery/evaluate.py": "2beb6d6f14ad10c7f474208ed66e9cca76b9ebb2880c7201ff351491884e1ec8",
          "recovery/events.py": "500ad12f8d68ee760e4fa2b2108089119f281b8d98db83113abe3e4a067d6704",
          "recovery/figures.py": "fab52110727c3dc9b8ed3e1da3a015fb1a437119e560be64cd36499b39c285c9",
          "recovery/i01/__init__.py": "b5fdf1bece3e01a5ab794227e5c278e3b8cf979ff5e27fce0d7ca953151a7e41",
          "recovery/i01/archive.py": "836a5d1cf5296eccbcb72f2f40e9b2e37d549307ca164a5479b9741623c65697",
          "recovery/i01/checks.py": "926d90992c64ffa5f1ffe48fad1bb3b6a46e5635bbe56305c0ab9e4e26dd9283",
          "recovery/i01/cli.py": "48e9b8ae4bbf4bc8101ec652dc56761b4af44f85c3ea93960a094651eb5daf21",
          "recovery/i01/client.py": "fbc6b2a31f63932831d55990479be2e69a3eb0ebe808cb1af4a150a2817f90b4",
          "recovery/i01/continuation.py": "d077353ed7a41c99b0b4140308ed2ee0e716e514c3934d09a389d45e47d25b70",
          "recovery/i01/core.py": "ce442f3f5505fc60e0b8791317e3f5db4d4c50cb5e670b0b7052cf6db2c20a88",
          "recovery/i01/inference.py": "7b3f04e683d15ed58d3d0135db281abb6425c5334a0765c49ace2fb70edf7588",
          "recovery/i01/notebook.py": "450f34e1c57efd6deb5914f6e4f3fc755cd2d4512c0e9915fb77c548cf238988",
          "recovery/i01/policy.py": "1306578cc76a8cff962cd06137a0fd4b06c73d93d06c8ca3f787241f98847e32",
          "recovery/i01/process.py": "17314150320b97c8d07edd3262d117db1f59c6b1c41728f48a45434cffe24fb0",
          "recovery/i01/report.py": "9d9043a4e643385112998223d34ea3db4b6162031de9df48d1e75db0b4ccfec3",
          "recovery/i01/runtime.py": "39fb2de57d5401c0ad553e4dd0da78159442f39bd3f281dacfa464ee0c2ed09b",
          "recovery/i01/setup.py": "f75ecb3083b9826b525c4b21c32e0ecc4e962ccb94fb158c62d9c694a3169c56",
          "recovery/i01/store.py": "14c28a627c42d9083b65f5df9aef002b7338a7126917392bdb36e20908efb092",
          "recovery/i01/ui.py": "1768e81bce4ac9232fb7d3a38f994d5a7cae3f06a93daeebbdc2e700442ee00f",
          "recovery/i01/workflow.py": "5d0252d2b2bfe2d0cfd40d8868f22119f7cdec09931904bd770ff5748fa0e8d7",
          "recovery/inference.py": "561386a74cc951a24cc08457665d71ee77d0075aca1794a5946d6d7fe52ee026",
          "recovery/information.py": "9c8bf958955b60e73ac26ac565831cee5e45e8e52f4244e88b43345e46c1df19",
          "recovery/manifests.py": "f6157e9f945b5f185ad5dde079e5b5e902665b644b9b9ba3a58936cdfa895b82",
          "recovery/populations.py": "808c4f29a0b7cb90574d040d9f49e402291a6eadd2bacc2141f50cf97fba05c7",
          "recovery/prompts.py": "a3cefd5d802cef08233a7b404cfd01f328dd3469db7d23857db25aadefd45cdc",
          "recovery/protocol.py": "e12de998036f40cac1f0d5dbfb5a293785bbf6ce6239f3cc11784c894fd7f3cf",
          "recovery/replay.py": "36e8be2946aadd71666c697b794d76f3c58b696bedc27a4408e32063bbb55840",
          "recovery/report.py": "6c37e92c9c338f7901fb0bda7fe6d2ea79fa998af3b33356e4b33c69d4df9fd3",
          "recovery/rounds.py": "2c59648c4cc8d720d1c510f27e663165ab2654d9044c57e222323664a2f631bf",
          "recovery/runner.py": "8723cf0c11b7988900275118d0565645f0585647274269a3e343206664d43b8a",
          "recovery/schedule.py": "396d8322e28ef1031803322f94f501be7fd778f69c0489854f78c228e87354d6",
          "recovery/state.py": "acf99320366e55c18778b4a4836003dfeb820abd77bc314172c3d538d35d4276",
          "recovery/storage.py": "e688428c2f07dcba28d928dcfbc163920ac6eeec37d15801d623dca35810a0d3",
          "recovery/t4_attention.py": "b5f7e9b8e7a7f4fe0193c31628d907f1476812983e3178beb20c297b7d172ee8",
          "recovery/tasks.py": "59d80c0e47c005af082626253ec86b6f3fc56be0dc57bad0369d1a263ba7e9a4",
          "recovery/truth.py": "bfc51e6da767258fc3e27a516b7fd44b48bb58f61f8fde73ccbb7ff51e9c8b2c",
          "recovery/uncertainty.py": "8cfbb1a89110a07536b8937b9248851ed0fbcea963d6950cd290a550e8036dad",
          "recovery/witness.py": "15e25c69e44da2ac2eccae2032c7ecce4bd33a033d91e4acc76ec1f79d0e523b",
          "recovery/workers.py": "300c06a6b30de089ef71e7c8dcf74a433d99b62e206a234e208aeefe9eb832a9"
        },
        "study_id": "b709c9bd-8d95-40c6-a19e-62a5f5e3c587",
        "worlds": [
          {
            "after": -551,
            "before": 950,
            "control_seeds": {
              "original": 7034365729602933730,
              "revised": 6470821694236683869
            },
            "device": 0,
            "first": 0,
            "group": "qualification",
            "id": "qualification-00",
            "index": 0,
            "original": [
              [
                -189,
                93,
                -801,
                703,
                257,
                888,
                -442,
                508,
                104,
                569,
                156,
                -943,
                950,
                -380,
                714,
                -695,
                619,
                284,
                642,
                -143
              ],
              [
                -578,
                487,
                -581,
                787,
                -324,
                -909,
                -27,
                478,
                611,
                -23,
                259,
                78,
                46,
                -354,
                921,
                185,
                896,
                -172,
                -499,
                24
              ]
            ],
            "original_truth": 950,
            "owner": 0,
            "proposals": 5,
            "rejections": {
              "nonunique_maximum": 0,
              "owner_block": 4,
              "remaining_at_floor": 0
            },
            "revised": [
              [
                -189,
                93,
                -801,
                703,
                257,
                888,
                -442,
                508,
                104,
                569,
                156,
                -943,
                -551,
                -380,
                714,
                -695,
                619,
                284,
                642,
                -143
              ],
              [
                -578,
                487,
                -581,
                787,
                -324,
                -909,
                -27,
                478,
                611,
                -23,
                259,
                78,
                46,
                -354,
                921,
                185,
                896,
                -172,
                -499,
                24
              ]
            ],
            "revised_truth": 921,
            "row": 12,
            "seeds": {
              "prefix": [
                [
                  4482506065534555318,
                  412927343023830623,
                  2109148965411192606
                ],
                [
                  4385276486813606184,
                  6912345805180829586,
                  3455170723590595527
                ]
              ],
              "recovery": [
                [
                  6526188895888695232,
                  6571403304274566053,
                  1954062805293530039
                ],
                [
                  1359658016784884329,
                  3243757618503762265,
                  4201019103053384133
                ]
              ]
            },
            "treatments": [
              "retain",
              "clear"
            ]
          },
          {
            "after": -81,
            "before": 999,
            "control_seeds": {
              "original": 5667570157035812265,
              "revised": 1898883763934146872
            },
            "device": 1,
            "first": 0,
            "group": "qualification",
            "id": "qualification-01",
            "index": 1,
            "original": [
              [
                416,
                -90,
                -164,
                608,
                -266,
                579,
                279,
                -562,
                -678,
                577,
                693,
                -648,
                -766,
                145,
                -320,
                -408,
                696,
                -65,
                -302,
                -208
              ],
              [
                573,
                582,
                931,
                56,
                731,
                918,
                415,
                566,
                704,
                557,
                864,
                -288,
                845,
                999,
                -639,
                654,
                -643,
                -297,
                818,
                -968
              ]
            ],
            "original_truth": 999,
            "owner": 1,
            "proposals": 1,
            "rejections": {
              "nonunique_maximum": 0,
              "owner_block": 0,
              "remaining_at_floor": 0
            },
            "revised": [
              [
                416,
                -90,
                -164,
                608,
                -266,
                579,
                279,
                -562,
                -678,
                577,
                693,
                -648,
                -766,
                145,
                -320,
                -408,
                696,
                -65,
                -302,
                -208
              ],
              [
                573,
                582,
                931,
                56,
                731,
                918,
                415,
                566,
                704,
                557,
                864,
                -288,
                845,
                -81,
                -639,
                654,
                -643,
                -297,
                818,
                -968
              ]
            ],
            "revised_truth": 931,
            "row": 13,
            "seeds": {
              "prefix": [
                [
                  365357283853728219,
                  6184368565983629280,
                  6573458992883911497
                ],
                [
                  8824162750632232244,
                  1963080267908642730,
                  8008088415356868384
                ]
              ],
              "recovery": [
                [
                  3371633447917534772,
                  2459147922575136351,
                  737103979760305227
                ],
                [
                  398948568915266817,
                  1845177985900587717,
                  8709297716995974328
                ]
              ]
            },
            "treatments": [
              "clear",
              "retain"
            ]
          },
          {
            "after": 851,
            "before": 1000,
            "control_seeds": {
              "original": 2474994583072236036,
              "revised": 6776502664314749800
            },
            "device": 0,
            "first": 1,
            "group": "qualification",
            "id": "qualification-02",
            "index": 2,
            "original": [
              [
                413,
                756,
                -172,
                1000,
                669,
                711,
                974,
                -532,
                65,
                832,
                -817,
                -770,
                -660,
                163,
                671,
                -1,
                -94,
                -130,
                451,
                -350
              ],
              [
                -753,
                739,
                -915,
                -994,
                501,
                -783,
                347,
                -742,
                535,
                228,
                -937,
                -747,
                -565,
                -367,
                981,
                -174,
                -887,
                714,
                327,
                -67
              ]
            ],
            "original_truth": 1000,
            "owner": 0,
            "proposals": 1,
            "rejections": {
              "nonunique_maximum": 0,
              "owner_block": 0,
              "remaining_at_floor": 0
            },
            "revised": [
              [
                413,
                756,
                -172,
                851,
                669,
                711,
                974,
                -532,
                65,
                832,
                -817,
                -770,
                -660,
                163,
                671,
                -1,
                -94,
                -130,
                451,
                -350
              ],
              [
                -753,
                739,
                -915,
                -994,
                501,
                -783,
                347,
                -742,
                535,
                228,
                -937,
                -747,
                -565,
                -367,
                981,
                -174,
                -887,
                714,
                327,
                -67
              ]
            ],
            "revised_truth": 981,
            "row": 3,
            "seeds": {
              "prefix": [
                [
                  2725852844225677593,
                  343399023915924421,
                  6513937643200348787
                ],
                [
                  332949247850107498,
                  9223309259806105505,
                  8493465789884601367
                ]
              ],
              "recovery": [
                [
                  5991453042001611951,
                  405237326680081307,
                  3605784421770664104
                ],
                [
                  7171198284295607958,
                  1357884721838184654,
                  583911871428831293
                ]
              ]
            },
            "treatments": [
              "retain",
              "clear"
            ]
          },
          {
            "after": -801,
            "before": 951,
            "control_seeds": {
              "original": 367958775560601292,
              "revised": 6417685603553177256
            },
            "device": 1,
            "first": 1,
            "group": "qualification",
            "id": "qualification-03",
            "index": 3,
            "original": [
              [
                231,
                -122,
                -551,
                -958,
                -149,
                -438,
                -273,
                -439,
                719,
                -881,
                -215,
                652,
                49,
                -40,
                -600,
                -929,
                340,
                -855,
                -862,
                -74
              ],
              [
                -376,
                -238,
                630,
                -897,
                674,
                920,
                266,
                788,
                92,
                815,
                290,
                -807,
                951,
                315,
                211,
                -348,
                587,
                188,
                -594,
                -554
              ]
            ],
            "original_truth": 951,
            "owner": 1,
            "proposals": 4,
            "rejections": {
              "nonunique_maximum": 0,
              "owner_block": 3,
              "remaining_at_floor": 0
            },
            "revised": [
              [
                231,
                -122,
                -551,
                -958,
                -149,
                -438,
                -273,
                -439,
                719,
                -881,
                -215,
                652,
                49,
                -40,
                -600,
                -929,
                340,
                -855,
                -862,
                -74
              ],
              [
                -376,
                -238,
                630,
                -897,
                674,
                920,
                266,
                788,
                92,
                815,
                290,
                -807,
                -801,
                315,
                211,
                -348,
                587,
                188,
                -594,
                -554
              ]
            ],
            "revised_truth": 920,
            "row": 12,
            "seeds": {
              "prefix": [
                [
                  5842624249297478730,
                  7547121839162710815,
                  1352492997533588836
                ],
                [
                  1344439115857738985,
                  1079843083168087572,
                  7617097022874114035
                ]
              ],
              "recovery": [
                [
                  8108280748331842908,
                  8437003048688256050,
                  6133085469547552948
                ],
                [
                  6103782264426076364,
                  1751848125169274649,
                  8431676853465120181
                ]
              ]
            },
            "treatments": [
              "clear",
              "retain"
            ]
          },
          {
            "after": 421,
            "before": 956,
            "control_seeds": {
              "original": 8507201115962376320,
              "revised": 6694793944570056551
            },
            "device": 0,
            "first": 0,
            "group": "qualification",
            "id": "qualification-04",
            "index": 4,
            "original": [
              [
                608,
                918,
                -461,
                408,
                37,
                -184,
                -421,
                -751,
                727,
                891,
                -595,
                -6,
                -4,
                -982,
                409,
                470,
                673,
                626,
                956,
                -330
              ],
              [
                -33,
                376,
                891,
                -805,
                458,
                -12,
                -22,
                -871,
                623,
                -826,
                -877,
                713,
                301,
                -820,
                -919,
                572,
                740,
                715,
                -282,
                24
              ]
            ],
            "original_truth": 956,
            "owner": 0,
            "proposals": 1,
            "rejections": {
              "nonunique_maximum": 0,
              "owner_block": 0,
              "remaining_at_floor": 0
            },
            "revised": [
              [
                608,
                918,
                -461,
                408,
                37,
                -184,
                -421,
                -751,
                727,
                891,
                -595,
                -6,
                -4,
                -982,
                409,
                470,
                673,
                626,
                421,
                -330
              ],
              [
                -33,
                376,
                891,
                -805,
                458,
                -12,
                -22,
                -871,
                623,
                -826,
                -877,
                713,
                301,
                -820,
                -919,
                572,
                740,
                715,
                -282,
                24
              ]
            ],
            "revised_truth": 918,
            "row": 18,
            "seeds": {
              "prefix": [
                [
                  3295759024446938111,
                  5349855107132709397,
                  2576173335502911682
                ],
                [
                  2918184825410101474,
                  4771007641962023599,
                  5074997840835365104
                ]
              ],
              "recovery": [
                [
                  2102144469767209590,
                  2320326146230977479,
                  1195334323631400666
                ],
                [
                  5418334346809178747,
                  2451041410674132400,
                  4624696849032298719
                ]
              ]
            },
            "treatments": [
              "retain",
              "clear"
            ]
          },
          {
            "after": -70,
            "before": 992,
            "control_seeds": {
              "original": 8287168954115719378,
              "revised": 7213998243262002842
            },
            "device": 1,
            "first": 0,
            "group": "qualification",
            "id": "qualification-05",
            "index": 5,
            "original": [
              [
                -86,
                313,
                -619,
                -204,
                -514,
                306,
                -908,
                -440,
                -834,
                -644,
                -715,
                -497,
                312,
                -735,
                117,
                -715,
                718,
                -909,
                -150,
                332
              ],
              [
                704,
                451,
                -239,
                -93,
                316,
                -503,
                888,
                -143,
                902,
                -244,
                -574,
                -447,
                987,
                631,
                -325,
                221,
                992,
                -307,
                313,
                557
              ]
            ],
            "original_truth": 992,
            "owner": 1,
            "proposals": 3,
            "rejections": {
              "nonunique_maximum": 0,
              "owner_block": 2,
              "remaining_at_floor": 0
            },
            "revised": [
              [
                -86,
                313,
                -619,
                -204,
                -514,
                306,
                -908,
                -440,
                -834,
                -644,
                -715,
                -497,
                312,
                -735,
                117,
                -715,
                718,
                -909,
                -150,
                332
              ],
              [
                704,
                451,
                -239,
                -93,
                316,
                -503,
                888,
                -143,
                902,
                -244,
                -574,
                -447,
                987,
                631,
                -325,
                221,
                -70,
                -307,
                313,
                557
              ]
            ],
            "revised_truth": 987,
            "row": 16,
            "seeds": {
              "prefix": [
                [
                  2597585026013381622,
                  4370624990697627220,
                  5244815374157118196
                ],
                [
                  1219403910651976828,
                  3049850324603457136,
                  6156949131002834945
                ]
              ],
              "recovery": [
                [
                  7272918335240750646,
                  7216275556166713247,
                  9040793799429680484
                ],
                [
                  7887485458797552039,
                  7482477457175227765,
                  1533108740253534760
                ]
              ]
            },
            "treatments": [
              "clear",
              "retain"
            ]
          },
          {
            "after": 672,
            "before": 988,
            "control_seeds": {
              "original": 7202948235205110027,
              "revised": 2712785873405090662
            },
            "device": 0,
            "first": 0,
            "group": "pilot",
            "id": "pilot-00",
            "index": 0,
            "original": [
              [
                932,
                -841,
                161,
                698,
                568,
                784,
                698,
                16,
                845,
                -978,
                685,
                -334,
                2,
                872,
                906,
                988,
                678,
                -336,
                -925,
                821
              ],
              [
                613,
                411,
                599,
                491,
                291,
                -96,
                220,
                261,
                -323,
                923,
                500,
                102,
                -976,
                224,
                -688,
                -23,
                -796,
                -962,
                -521,
                -918
              ]
            ],
            "original_truth": 988,
            "owner": 0,
            "proposals": 2,
            "rejections": {
              "nonunique_maximum": 0,
              "owner_block": 1,
              "remaining_at_floor": 0
            },
            "revised": [
              [
                932,
                -841,
                161,
                698,
                568,
                784,
                698,
                16,
                845,
                -978,
                685,
                -334,
                2,
                872,
                906,
                672,
                678,
                -336,
                -925,
                821
              ],
              [
                613,
                411,
                599,
                491,
                291,
                -96,
                220,
                261,
                -323,
                923,
                500,
                102,
                -976,
                224,
                -688,
                -23,
                -796,
                -962,
                -521,
                -918
              ]
            ],
            "revised_truth": 932,
            "row": 15,
            "seeds": {
              "prefix": [
                [
                  4862200359885706185,
                  1023110753385749315,
                  2736320403664395003
                ],
                [
                  5241200695438049338,
                  7358009148274838779,
                  1407075676669500463
                ]
              ],
              "recovery": [
                [
                  3347234689565640300,
                  7926385093500598411,
                  567848943222847789
                ],
                [
                  7951545925196133279,
                  9068172075070223439,
                  4242985494088566540
                ]
              ]
            },
            "treatments": [
              "retain",
              "clear"
            ]
          },
          {
            "after": 25,
            "before": 985,
            "control_seeds": {
              "original": 2432397541971568865,
              "revised": 4564994103806736101
            },
            "device": 1,
            "first": 0,
            "group": "pilot",
            "id": "pilot-01",
            "index": 1,
            "original": [
              [
                634,
                813,
                664,
                -820,
                738,
                71,
                590,
                536,
                92,
                502,
                -192,
                116,
                -767,
                -42,
                -464,
                -547,
                -690,
                169,
                -567,
                -156
              ],
              [
                497,
                966,
                -234,
                36,
                849,
                815,
                -663,
                -6,
                -768,
                34,
                -430,
                328,
                -282,
                -891,
                740,
                985,
                -998,
                -348,
                150,
                -746
              ]
            ],
            "original_truth": 985,
            "owner": 1,
            "proposals": 1,
            "rejections": {
              "nonunique_maximum": 0,
              "owner_block": 0,
              "remaining_at_floor": 0
            },
            "revised": [
              [
                634,
                813,
                664,
                -820,
                738,
                71,
                590,
                536,
                92,
                502,
                -192,
                116,
                -767,
                -42,
                -464,
                -547,
                -690,
                169,
                -567,
                -156
              ],
              [
                497,
                966,
                -234,
                36,
                849,
                815,
                -663,
                -6,
                -768,
                34,
                -430,
                328,
                -282,
                -891,
                740,
                25,
                -998,
                -348,
                150,
                -746
              ]
            ],
            "revised_truth": 966,
            "row": 15,
            "seeds": {
              "prefix": [
                [
                  6068910610471527175,
                  5109202408067130647,
                  4110699780713550369
                ],
                [
                  8024261074218990468,
                  7684684620624210612,
                  4404566881294605269
                ]
              ],
              "recovery": [
                [
                  3259302922276671101,
                  5227453265228557459,
                  3465729064646047018
                ],
                [
                  657496878342466428,
                  3727060405587847742,
                  1396722624471132836
                ]
              ]
            },
            "treatments": [
              "clear",
              "retain"
            ]
          },
          {
            "after": -481,
            "before": 981,
            "control_seeds": {
              "original": 8384168939389075560,
              "revised": 6801689851870198115
            },
            "device": 0,
            "first": 1,
            "group": "pilot",
            "id": "pilot-02",
            "index": 2,
            "original": [
              [
                -367,
                552,
                478,
                -49,
                -696,
                84,
                647,
                -869,
                -417,
                981,
                -904,
                -101,
                484,
                173,
                34,
                -618,
                76,
                -127,
                302,
                -659
              ],
              [
                201,
                -369,
                911,
                670,
                23,
                876,
                627,
                -251,
                393,
                -788,
                -196,
                97,
                -678,
                -916,
                338,
                -974,
                524,
                -241,
                -71,
                -995
              ]
            ],
            "original_truth": 981,
            "owner": 0,
            "proposals": 1,
            "rejections": {
              "nonunique_maximum": 0,
              "owner_block": 0,
              "remaining_at_floor": 0
            },
            "revised": [
              [
                -367,
                552,
                478,
                -49,
                -696,
                84,
                647,
                -869,
                -417,
                -481,
                -904,
                -101,
                484,
                173,
                34,
                -618,
                76,
                -127,
                302,
                -659
              ],
              [
                201,
                -369,
                911,
                670,
                23,
                876,
                627,
                -251,
                393,
                -788,
                -196,
                97,
                -678,
                -916,
                338,
                -974,
                524,
                -241,
                -71,
                -995
              ]
            ],
            "revised_truth": 911,
            "row": 9,
            "seeds": {
              "prefix": [
                [
                  7049442019502801809,
                  6836940397847036542,
                  8179466357591922044
                ],
                [
                  4114484684654210243,
                  1303939391147026415,
                  3202899689243768497
                ]
              ],
              "recovery": [
                [
                  4792976250752518887,
                  3333023835528811287,
                  6692826379925589624
                ],
                [
                  8763162528738937420,
                  8536876883942813207,
                  6687515527582378326
                ]
              ]
            },
            "treatments": [
              "retain",
              "clear"
            ]
          },
          {
            "after": 753,
            "before": 894,
            "control_seeds": {
              "original": 2147891498950564844,
              "revised": 298906340986623092
            },
            "device": 0,
            "first": 0,
            "group": "main",
            "id": "main-00",
            "index": 0,
            "original": [
              [
                113,
                273,
                387,
                -548,
                439,
                561,
                -211,
                588,
                -220,
                616,
                703,
                683,
                576,
                -293,
                -842,
                894,
                -973,
                -921,
                585,
                -576
              ],
              [
                210,
                -308,
                -245,
                -955,
                189,
                642,
                827,
                -983,
                579,
                -320,
                872,
                -439,
                -982,
                -78,
                312,
                834,
                180,
                -800,
                -905,
                -381
              ]
            ],
            "original_truth": 894,
            "owner": 0,
            "proposals": 1,
            "rejections": {
              "nonunique_maximum": 0,
              "owner_block": 0,
              "remaining_at_floor": 0
            },
            "revised": [
              [
                113,
                273,
                387,
                -548,
                439,
                561,
                -211,
                588,
                -220,
                616,
                703,
                683,
                576,
                -293,
                -842,
                753,
                -973,
                -921,
                585,
                -576
              ],
              [
                210,
                -308,
                -245,
                -955,
                189,
                642,
                827,
                -983,
                579,
                -320,
                872,
                -439,
                -982,
                -78,
                312,
                834,
                180,
                -800,
                -905,
                -381
              ]
            ],
            "revised_truth": 872,
            "row": 15,
            "seeds": {
              "prefix": [
                [
                  7613389024471320949,
                  2430595037025299620,
                  7632132044748201474
                ],
                [
                  4798458808050766445,
                  8822928244286280046,
                  7068274016831448234
                ]
              ],
              "recovery": [
                [
                  3459283983308522598,
                  534857686012084730,
                  7779589634043449186
                ],
                [
                  1252619848572711051,
                  9024046278804602435,
                  2114440144336600496
                ]
              ]
            },
            "treatments": [
              "retain",
              "clear"
            ]
          },
          {
            "after": -152,
            "before": 936,
            "control_seeds": {
              "original": 133001457366662095,
              "revised": 6352946184833924874
            },
            "device": 1,
            "first": 0,
            "group": "main",
            "id": "main-01",
            "index": 1,
            "original": [
              [
                -200,
                723,
                -96,
                -833,
                299,
                -297,
                -604,
                234,
                -294,
                380,
                598,
                151,
                -284,
                247,
                344,
                936,
                -526,
                224,
                473,
                -862
              ],
              [
                -992,
                -957,
                304,
                -101,
                53,
                404,
                -735,
                749,
                -543,
                293,
                507,
                138,
                -760,
                -749,
                619,
                534,
                910,
                -839,
                841,
                -759
              ]
            ],
            "original_truth": 936,
            "owner": 0,
            "proposals": 1,
            "rejections": {
              "nonunique_maximum": 0,
              "owner_block": 0,
              "remaining_at_floor": 0
            },
            "revised": [
              [
                -200,
                723,
                -96,
                -833,
                299,
                -297,
                -604,
                234,
                -294,
                380,
                598,
                151,
                -284,
                247,
                344,
                -152,
                -526,
                224,
                473,
                -862
              ],
              [
                -992,
                -957,
                304,
                -101,
                53,
                404,
                -735,
                749,
                -543,
                293,
                507,
                138,
                -760,
                -749,
                619,
                534,
                910,
                -839,
                841,
                -759
              ]
            ],
            "revised_truth": 910,
            "row": 15,
            "seeds": {
              "prefix": [
                [
                  1619430377463203250,
                  100071804121729356,
                  7693732580013016497
                ],
                [
                  2392044105153311016,
                  4915930630265407126,
                  2770636549167397914
                ]
              ],
              "recovery": [
                [
                  6784604259975473913,
                  5265313454849479903,
                  5554753004093747182
                ],
                [
                  4385210743583052582,
                  7239859807044094272,
                  9034891210502621966
                ]
              ]
            },
            "treatments": [
              "clear",
              "retain"
            ]
          },
          {
            "after": -452,
            "before": 957,
            "control_seeds": {
              "original": 4794547254492634117,
              "revised": 1417816023888265619
            },
            "device": 0,
            "first": 0,
            "group": "main",
            "id": "main-02",
            "index": 2,
            "original": [
              [
                -831,
                -342,
                -592,
                -608,
                -812,
                183,
                -871,
                802,
                90,
                -26,
                -733,
                -257,
                957,
                -252,
                558,
                -12,
                830,
                756,
                784,
                -786
              ],
              [
                -376,
                -526,
                338,
                -196,
                152,
                214,
                -29,
                532,
                -941,
                -920,
                627,
                348,
                -848,
                -512,
                -363,
                -964,
                887,
                -849,
                914,
                449
              ]
            ],
            "original_truth": 957,
            "owner": 0,
            "proposals": 2,
            "rejections": {
              "nonunique_maximum": 0,
              "owner_block": 1,
              "remaining_at_floor": 0
            },
            "revised": [
              [
                -831,
                -342,
                -592,
                -608,
                -812,
                183,
                -871,
                802,
                90,
                -26,
                -733,
                -257,
                -452,
                -252,
                558,
                -12,
                830,
                756,
                784,
                -786
              ],
              [
                -376,
                -526,
                338,
                -196,
                152,
                214,
                -29,
                532,
                -941,
                -920,
                627,
                348,
                -848,
                -512,
                -363,
                -964,
                887,
                -849,
                914,
                449
              ]
            ],
            "revised_truth": 914,
            "row": 12,
            "seeds": {
              "prefix": [
                [
                  3978482016353816917,
                  4027682472747877123,
                  193044703599591544
                ],
                [
                  8476846841885711904,
                  2229360315824126971,
                  2051761436065831103
                ]
              ],
              "recovery": [
                [
                  5960279899263789434,
                  1749033961600293646,
                  5527288603516730547
                ],
                [
                  740317857514137191,
                  2618489332901524746,
                  5404139388152553139
                ]
              ]
            },
            "treatments": [
              "retain",
              "clear"
            ]
          },
          {
            "after": -489,
            "before": 993,
            "control_seeds": {
              "original": 8471554357770356529,
              "revised": 6470849730561868516
            },
            "device": 1,
            "first": 0,
            "group": "main",
            "id": "main-03",
            "index": 3,
            "original": [
              [
                -182,
                -829,
                -726,
                354,
                -805,
                -532,
                -375,
                993,
                230,
                -384,
                -449,
                -25,
                115,
                -576,
                693,
                67,
                783,
                201,
                -515,
                -283
              ],
              [
                36,
                -135,
                -15,
                340,
                -218,
                64,
                -703,
                -847,
                822,
                -964,
                -680,
                -41,
                -206,
                14,
                -801,
                -531,
                -320,
                -125,
                566,
                196
              ]
            ],
            "original_truth": 993,
            "owner": 0,
            "proposals": 1,
            "rejections": {
              "nonunique_maximum": 0,
              "owner_block": 0,
              "remaining_at_floor": 0
            },
            "revised": [
              [
                -182,
                -829,
                -726,
                354,
                -805,
                -532,
                -375,
                -489,
                230,
                -384,
                -449,
                -25,
                115,
                -576,
                693,
                67,
                783,
                201,
                -515,
                -283
              ],
              [
                36,
                -135,
                -15,
                340,
                -218,
                64,
                -703,
                -847,
                822,
                -964,
                -680,
                -41,
                -206,
                14,
                -801,
                -531,
                -320,
                -125,
                566,
                196
              ]
            ],
            "revised_truth": 822,
            "row": 7,
            "seeds": {
              "prefix": [
                [
                  139902953584322306,
                  3268728654576400253,
                  7125301707374441810
                ],
                [
                  2983288974554191250,
                  4521724768519690317,
                  8909413058330369264
                ]
              ],
              "recovery": [
                [
                  1775432120674568221,
                  5017298312933826769,
                  6523901000912654712
                ],
                [
                  5387240266317778948,
                  1014741761784909330,
                  2065938479339020309
                ]
              ]
            },
            "treatments": [
              "clear",
              "retain"
            ]
          },
          {
            "after": 629,
            "before": 994,
            "control_seeds": {
              "original": 4960720530651022430,
              "revised": 8889708095582152789
            },
            "device": 0,
            "first": 0,
            "group": "main",
            "id": "main-04",
            "index": 4,
            "original": [
              [
                994,
                485,
                341,
                -519,
                8,
                -316,
                150,
                881,
                -205,
                -795,
                -174,
                -968,
                255,
                -795,
                450,
                294,
                943,
                -707,
                662,
                276
              ],
              [
                -871,
                -703,
                959,
                -861,
                58,
                855,
                96,
                587,
                -934,
                638,
                -605,
                -41,
                -711,
                -113,
                366,
                371,
                -610,
                474,
                -81,
                101
              ]
            ],
            "original_truth": 994,
            "owner": 0,
            "proposals": 1,
            "rejections": {
              "nonunique_maximum": 0,
              "owner_block": 0,
              "remaining_at_floor": 0
            },
            "revised": [
              [
                629,
                485,
                341,
                -519,
                8,
                -316,
                150,
                881,
                -205,
                -795,
                -174,
                -968,
                255,
                -795,
                450,
                294,
                943,
                -707,
                662,
                276
              ],
              [
                -871,
                -703,
                959,
                -861,
                58,
                855,
                96,
                587,
                -934,
                638,
                -605,
                -41,
                -711,
                -113,
                366,
                371,
                -610,
                474,
                -81,
                101
              ]
            ],
            "revised_truth": 959,
            "row": 0,
            "seeds": {
              "prefix": [
                [
                  4452187471933571023,
                  7321724501442330755,
                  1750068862954404733
                ],
                [
                  4099672381084009203,
                  3104069450291277575,
                  328549809509255860
                ]
              ],
              "recovery": [
                [
                  8994721194012826067,
                  3800838350043971346,
                  10834238225407660
                ],
                [
                  214198652916756762,
                  1043855508657754351,
                  1866335026032308508
                ]
              ]
            },
            "treatments": [
              "retain",
              "clear"
            ]
          },
          {
            "after": -91,
            "before": 949,
            "control_seeds": {
              "original": 2164810558525433393,
              "revised": 1928374090232088953
            },
            "device": 1,
            "first": 1,
            "group": "main",
            "id": "main-05",
            "index": 5,
            "original": [
              [
                -807,
                -498,
                -251,
                134,
                -707,
                -513,
                -264,
                -78,
                -674,
                -808,
                412,
                915,
                -137,
                -325,
                949,
                -906,
                -718,
                873,
                464,
                -299
              ],
              [
                506,
                -479,
                -379,
                749,
                512,
                391,
                292,
                -546,
                -559,
                644,
                124,
                -376,
                870,
                147,
                -723,
                -43,
                573,
                -497,
                489,
                -442
              ]
            ],
            "original_truth": 949,
            "owner": 0,
            "proposals": 2,
            "rejections": {
              "nonunique_maximum": 0,
              "owner_block": 1,
              "remaining_at_floor": 0
            },
            "revised": [
              [
                -807,
                -498,
                -251,
                134,
                -707,
                -513,
                -264,
                -78,
                -674,
                -808,
                412,
                915,
                -137,
                -325,
                -91,
                -906,
                -718,
                873,
                464,
                -299
              ],
              [
                506,
                -479,
                -379,
                749,
                512,
                391,
                292,
                -546,
                -559,
                644,
                124,
                -376,
                870,
                147,
                -723,
                -43,
                573,
                -497,
                489,
                -442
              ]
            ],
            "revised_truth": 915,
            "row": 14,
            "seeds": {
              "prefix": [
                [
                  561649063181457771,
                  6508216825219903062,
                  2107932907533430008
                ],
                [
                  7259646355533685262,
                  2976846420035572698,
                  6092476739546730244
                ]
              ],
              "recovery": [
                [
                  1504507442207819565,
                  5407287651997673118,
                  4382105864275936713
                ],
                [
                  7914258068898711446,
                  2836955077332054162,
                  6625670272031382701
                ]
              ]
            },
            "treatments": [
              "clear",
              "retain"
            ]
          },
          {
            "after": 905,
            "before": 977,
            "control_seeds": {
              "original": 1959322347283275910,
              "revised": 5151532955772563227
            },
            "device": 0,
            "first": 1,
            "group": "main",
            "id": "main-06",
            "index": 6,
            "original": [
              [
                522,
                791,
                -988,
                -610,
                977,
                263,
                744,
                -585,
                656,
                336,
                124,
                883,
                324,
                807,
                116,
                314,
                838,
                -606,
                -56,
                298
              ],
              [
                -339,
                926,
                29,
                -917,
                564,
                -406,
                681,
                646,
                -174,
                352,
                787,
                792,
                678,
                568,
                -6,
                -461,
                92,
                79,
                -974,
                -929
              ]
            ],
            "original_truth": 977,
            "owner": 0,
            "proposals": 2,
            "rejections": {
              "nonunique_maximum": 0,
              "owner_block": 1,
              "remaining_at_floor": 0
            },
            "revised": [
              [
                522,
                791,
                -988,
                -610,
                905,
                263,
                744,
                -585,
                656,
                336,
                124,
                883,
                324,
                807,
                116,
                314,
                838,
                -606,
                -56,
                298
              ],
              [
                -339,
                926,
                29,
                -917,
                564,
                -406,
                681,
                646,
                -174,
                352,
                787,
                792,
                678,
                568,
                -6,
                -461,
                92,
                79,
                -974,
                -929
              ]
            ],
            "revised_truth": 926,
            "row": 4,
            "seeds": {
              "prefix": [
                [
                  9107563587078734982,
                  5402733660104209960,
                  2528101576028971409
                ],
                [
                  8228629113183717777,
                  3209517545748347934,
                  128343983576175246
                ]
              ],
              "recovery": [
                [
                  1426073051744467116,
                  4230107165784492271,
                  4131646186970840278
                ],
                [
                  8414519180560761855,
                  2417252706394484963,
                  2050904192548928404
                ]
              ]
            },
            "treatments": [
              "retain",
              "clear"
            ]
          },
          {
            "after": -721,
            "before": 917,
            "control_seeds": {
              "original": 4368901468440162144,
              "revised": 1741964262489296062
            },
            "device": 1,
            "first": 1,
            "group": "main",
            "id": "main-07",
            "index": 7,
            "original": [
              [
                -369,
                917,
                -931,
                33,
                -595,
                13,
                52,
                654,
                461,
                155,
                98,
                -126,
                -540,
                -122,
                -531,
                759,
                519,
                701,
                133,
                -838
              ],
              [
                669,
                414,
                241,
                840,
                -878,
                89,
                603,
                -589,
                -148,
                -730,
                869,
                -445,
                534,
                880,
                97,
                -353,
                -515,
                695,
                774,
                -612
              ]
            ],
            "original_truth": 917,
            "owner": 0,
            "proposals": 3,
            "rejections": {
              "nonunique_maximum": 0,
              "owner_block": 2,
              "remaining_at_floor": 0
            },
            "revised": [
              [
                -369,
                -721,
                -931,
                33,
                -595,
                13,
                52,
                654,
                461,
                155,
                98,
                -126,
                -540,
                -122,
                -531,
                759,
                519,
                701,
                133,
                -838
              ],
              [
                669,
                414,
                241,
                840,
                -878,
                89,
                603,
                -589,
                -148,
                -730,
                869,
                -445,
                534,
                880,
                97,
                -353,
                -515,
                695,
                774,
                -612
              ]
            ],
            "revised_truth": 880,
            "row": 1,
            "seeds": {
              "prefix": [
                [
                  6065529762186739126,
                  924384901063280048,
                  8716017849433003299
                ],
                [
                  8440419528886959979,
                  84465805100603968,
                  941681735522333411
                ]
              ],
              "recovery": [
                [
                  7480473105748484397,
                  5682402573496401995,
                  349580090625612606
                ],
                [
                  2369861748578623633,
                  5113988670878644717,
                  1417998081918525862
                ]
              ]
            },
            "treatments": [
              "clear",
              "retain"
            ]
          },
          {
            "after": -933,
            "before": 965,
            "control_seeds": {
              "original": 4393186238040900385,
              "revised": 8453823791653888183
            },
            "device": 0,
            "first": 1,
            "group": "main",
            "id": "main-08",
            "index": 8,
            "original": [
              [
                0,
                916,
                965,
                610,
                -48,
                -163,
                948,
                -977,
                -33,
                652,
                260,
                -766,
                960,
                189,
                -382,
                938,
                -933,
                -288,
                -944,
                309
              ],
              [
                -209,
                -400,
                230,
                -987,
                91,
                -305,
                652,
                917,
                928,
                -730,
                -366,
                695,
                -18,
                791,
                -955,
                -716,
                263,
                -740,
                -590,
                -789
              ]
            ],
            "original_truth": 965,
            "owner": 0,
            "proposals": 3,
            "rejections": {
              "nonunique_maximum": 0,
              "owner_block": 2,
              "remaining_at_floor": 0
            },
            "revised": [
              [
                0,
                916,
                -933,
                610,
                -48,
                -163,
                948,
                -977,
                -33,
                652,
                260,
                -766,
                960,
                189,
                -382,
                938,
                -933,
                -288,
                -944,
                309
              ],
              [
                -209,
                -400,
                230,
                -987,
                91,
                -305,
                652,
                917,
                928,
                -730,
                -366,
                695,
                -18,
                791,
                -955,
                -716,
                263,
                -740,
                -590,
                -789
              ]
            ],
            "revised_truth": 960,
            "row": 2,
            "seeds": {
              "prefix": [
                [
                  192950164726274557,
                  4774456550148206825,
                  6594954879850626019
                ],
                [
                  1257499277584708772,
                  9193106247132483019,
                  4993213291275076191
                ]
              ],
              "recovery": [
                [
                  6344436267273193217,
                  2648734091400131420,
                  4411572305060160406
                ],
                [
                  9158899219688889798,
                  7558524973736859106,
                  5820781040901160327
                ]
              ]
            },
            "treatments": [
              "retain",
              "clear"
            ]
          },
          {
            "after": 283,
            "before": 999,
            "control_seeds": {
              "original": 9214668301875570868,
              "revised": 4628258382748303628
            },
            "device": 1,
            "first": 1,
            "group": "main",
            "id": "main-09",
            "index": 9,
            "original": [
              [
                916,
                850,
                532,
                165,
                84,
                999,
                232,
                -488,
                -994,
                -935,
                446,
                -239,
                381,
                -148,
                654,
                304,
                418,
                -585,
                -882,
                102
              ],
              [
                601,
                -854,
                -630,
                297,
                353,
                97,
                2,
                -669,
                166,
                -126,
                933,
                852,
                96,
                -237,
                296,
                -7,
                -276,
                787,
                214,
                676
              ]
            ],
            "original_truth": 999,
            "owner": 0,
            "proposals": 1,
            "rejections": {
              "nonunique_maximum": 0,
              "owner_block": 0,
              "remaining_at_floor": 0
            },
            "revised": [
              [
                916,
                850,
                532,
                165,
                84,
                283,
                232,
                -488,
                -994,
                -935,
                446,
                -239,
                381,
                -148,
                654,
                304,
                418,
                -585,
                -882,
                102
              ],
              [
                601,
                -854,
                -630,
                297,
                353,
                97,
                2,
                -669,
                166,
                -126,
                933,
                852,
                96,
                -237,
                296,
                -7,
                -276,
                787,
                214,
                676
              ]
            ],
            "revised_truth": 933,
            "row": 5,
            "seeds": {
              "prefix": [
                [
                  4685134624984108094,
                  5169167145342257419,
                  3643973146271904957
                ],
                [
                  6803160303860818703,
                  7564060563883581650,
                  162423314457967112
                ]
              ],
              "recovery": [
                [
                  8023923800489086619,
                  1130665023006752772,
                  4285012345147662237
                ],
                [
                  1010564286941044410,
                  1640805139424063780,
                  6827608508764498384
                ]
              ]
            },
            "treatments": [
              "clear",
              "retain"
            ]
          },
          {
            "after": 867,
            "before": 937,
            "control_seeds": {
              "original": 1226459450355933647,
              "revised": 8687626564131041381
            },
            "device": 0,
            "first": 0,
            "group": "main",
            "id": "main-10",
            "index": 10,
            "original": [
              [
                -677,
                -465,
                323,
                -563,
                124,
                615,
                -169,
                -497,
                700,
                -208,
                341,
                317,
                297,
                559,
                -118,
                -954,
                429,
                659,
                758,
                -381
              ],
              [
                814,
                515,
                349,
                196,
                -467,
                94,
                50,
                -298,
                -925,
                937,
                -768,
                -997,
                918,
                888,
                -152,
                67,
                -155,
                559,
                379,
                -276
              ]
            ],
            "original_truth": 937,
            "owner": 1,
            "proposals": 2,
            "rejections": {
              "nonunique_maximum": 0,
              "owner_block": 1,
              "remaining_at_floor": 0
            },
            "revised": [
              [
                -677,
                -465,
                323,
                -563,
                124,
                615,
                -169,
                -497,
                700,
                -208,
                341,
                317,
                297,
                559,
                -118,
                -954,
                429,
                659,
                758,
                -381
              ],
              [
                814,
                515,
                349,
                196,
                -467,
                94,
                50,
                -298,
                -925,
                867,
                -768,
                -997,
                918,
                888,
                -152,
                67,
                -155,
                559,
                379,
                -276
              ]
            ],
            "revised_truth": 918,
            "row": 9,
            "seeds": {
              "prefix": [
                [
                  5661297641176745221,
                  2988932701086763153,
                  632323218981940050
                ],
                [
                  5965690742242668860,
                  2416004198644876313,
                  2994460492752693716
                ]
              ],
              "recovery": [
                [
                  4570728588175425658,
                  6630952362004802828,
                  6039937866577557379
                ],
                [
                  7146153813596516521,
                  1616327101951968020,
                  525932557302377982
                ]
              ]
            },
            "treatments": [
              "retain",
              "clear"
            ]
          },
          {
            "after": -453,
            "before": 972,
            "control_seeds": {
              "original": 4033333652152207591,
              "revised": 7011718913799078458
            },
            "device": 1,
            "first": 0,
            "group": "main",
            "id": "main-11",
            "index": 11,
            "original": [
              [
                68,
                -916,
                560,
                757,
                229,
                -675,
                -927,
                747,
                708,
                -57,
                -950,
                26,
                715,
                -364,
                -842,
                267,
                216,
                331,
                -127,
                596
              ],
              [
                972,
                -424,
                -379,
                -509,
                172,
                688,
                928,
                203,
                -227,
                812,
                -133,
                347,
                122,
                -520,
                608,
                -855,
                474,
                -143,
                963,
                -402
              ]
            ],
            "original_truth": 972,
            "owner": 1,
            "proposals": 2,
            "rejections": {
              "nonunique_maximum": 0,
              "owner_block": 1,
              "remaining_at_floor": 0
            },
            "revised": [
              [
                68,
                -916,
                560,
                757,
                229,
                -675,
                -927,
                747,
                708,
                -57,
                -950,
                26,
                715,
                -364,
                -842,
                267,
                216,
                331,
                -127,
                596
              ],
              [
                -453,
                -424,
                -379,
                -509,
                172,
                688,
                928,
                203,
                -227,
                812,
                -133,
                347,
                122,
                -520,
                608,
                -855,
                474,
                -143,
                963,
                -402
              ]
            ],
            "revised_truth": 963,
            "row": 0,
            "seeds": {
              "prefix": [
                [
                  2699441716391527412,
                  3035259578590224976,
                  2971972859960784202
                ],
                [
                  5136283076468002978,
                  6319628260057940435,
                  6577424467119165128
                ]
              ],
              "recovery": [
                [
                  5721108965903856331,
                  11167153662719915,
                  3224564801068027648
                ],
                [
                  2618425764677916156,
                  8860473879125021793,
                  3058225647350318428
                ]
              ]
            },
            "treatments": [
              "clear",
              "retain"
            ]
          },
          {
            "after": 142,
            "before": 997,
            "control_seeds": {
              "original": 3150153611169757532,
              "revised": 4270835832855700703
            },
            "device": 0,
            "first": 0,
            "group": "main",
            "id": "main-12",
            "index": 12,
            "original": [
              [
                983,
                502,
                144,
                785,
                654,
                13,
                157,
                549,
                -864,
                32,
                10,
                -5,
                420,
                959,
                884,
                630,
                762,
                966,
                -762,
                918
              ],
              [
                -730,
                280,
                997,
                -666,
                287,
                420,
                548,
                284,
                -538,
                -801,
                -308,
                45,
                -956,
                -789,
                -280,
                -703,
                -237,
                -97,
                -894,
                448
              ]
            ],
            "original_truth": 997,
            "owner": 1,
            "proposals": 1,
            "rejections": {
              "nonunique_maximum": 0,
              "owner_block": 0,
              "remaining_at_floor": 0
            },
            "revised": [
              [
                983,
                502,
                144,
                785,
                654,
                13,
                157,
                549,
                -864,
                32,
                10,
                -5,
                420,
                959,
                884,
                630,
                762,
                966,
                -762,
                918
              ],
              [
                -730,
                280,
                142,
                -666,
                287,
                420,
                548,
                284,
                -538,
                -801,
                -308,
                45,
                -956,
                -789,
                -280,
                -703,
                -237,
                -97,
                -894,
                448
              ]
            ],
            "revised_truth": 983,
            "row": 2,
            "seeds": {
              "prefix": [
                [
                  8067617777804797891,
                  557664866961384201,
                  8709815472197141218
                ],
                [
                  8805643309456860035,
                  5844005573012226274,
                  2109457162888020055
                ]
              ],
              "recovery": [
                [
                  5987524421992088977,
                  7777712625100116258,
                  3567485187867362033
                ],
                [
                  1394962814262892434,
                  6684962908305202929,
                  3927869302931546758
                ]
              ]
            },
            "treatments": [
              "retain",
              "clear"
            ]
          },
          {
            "after": -318,
            "before": 982,
            "control_seeds": {
              "original": 3047043693510280639,
              "revised": 2635468176680950715
            },
            "device": 1,
            "first": 0,
            "group": "main",
            "id": "main-13",
            "index": 13,
            "original": [
              [
                -645,
                -828,
                615,
                -614,
                506,
                -480,
                -301,
                -170,
                -778,
                106,
                -432,
                -31,
                357,
                -917,
                716,
                572,
                -60,
                737,
                -559,
                -54
              ],
              [
                -872,
                161,
                -148,
                -469,
                692,
                -355,
                -10,
                865,
                -10,
                -822,
                481,
                -484,
                953,
                -798,
                -639,
                -821,
                982,
                -196,
                929,
                27
              ]
            ],
            "original_truth": 982,
            "owner": 1,
            "proposals": 1,
            "rejections": {
              "nonunique_maximum": 0,
              "owner_block": 0,
              "remaining_at_floor": 0
            },
            "revised": [
              [
                -645,
                -828,
                615,
                -614,
                506,
                -480,
                -301,
                -170,
                -778,
                106,
                -432,
                -31,
                357,
                -917,
                716,
                572,
                -60,
                737,
                -559,
                -54
              ],
              [
                -872,
                161,
                -148,
                -469,
                692,
                -355,
                -10,
                865,
                -10,
                -822,
                481,
                -484,
                953,
                -798,
                -639,
                -821,
                -318,
                -196,
                929,
                27
              ]
            ],
            "revised_truth": 953,
            "row": 16,
            "seeds": {
              "prefix": [
                [
                  3979908319941421135,
                  2393529629678929350,
                  5094173747872294098
                ],
                [
                  2998798001136738158,
                  3915350704564495490,
                  2032733688510320421
                ]
              ],
              "recovery": [
                [
                  2239360232027024199,
                  5764790047426674101,
                  5097061125250303561
                ],
                [
                  5771648798121642707,
                  9036171998834330482,
                  3599751875578752418
                ]
              ]
            },
            "treatments": [
              "clear",
              "retain"
            ]
          },
          {
            "after": -220,
            "before": 984,
            "control_seeds": {
              "original": 4904115945039636251,
              "revised": 7921154408136709599
            },
            "device": 0,
            "first": 0,
            "group": "main",
            "id": "main-14",
            "index": 14,
            "original": [
              [
                -776,
                -983,
                -210,
                400,
                117,
                461,
                -202,
                -764,
                111,
                712,
                -517,
                310,
                -872,
                -520,
                -580,
                -884,
                -629,
                236,
                -712,
                -56
              ],
              [
                -173,
                425,
                984,
                -623,
                -620,
                -274,
                -785,
                261,
                44,
                -973,
                -218,
                730,
                302,
                233,
                -954,
                -651,
                325,
                101,
                533,
                -467
              ]
            ],
            "original_truth": 984,
            "owner": 1,
            "proposals": 2,
            "rejections": {
              "nonunique_maximum": 0,
              "owner_block": 1,
              "remaining_at_floor": 0
            },
            "revised": [
              [
                -776,
                -983,
                -210,
                400,
                117,
                461,
                -202,
                -764,
                111,
                712,
                -517,
                310,
                -872,
                -520,
                -580,
                -884,
                -629,
                236,
                -712,
                -56
              ],
              [
                -173,
                425,
                -220,
                -623,
                -620,
                -274,
                -785,
                261,
                44,
                -973,
                -218,
                730,
                302,
                233,
                -954,
                -651,
                325,
                101,
                533,
                -467
              ]
            ],
            "revised_truth": 730,
            "row": 2,
            "seeds": {
              "prefix": [
                [
                  2382279863713379274,
                  7221813534107381903,
                  1830575940988971568
                ],
                [
                  1974500441739583894,
                  7166617257048818533,
                  4786707485556870973
                ]
              ],
              "recovery": [
                [
                  5734893163594118816,
                  8920205055925856671,
                  2106084752359392235
                ],
                [
                  8148979525226795087,
                  5528510670377592352,
                  653736666617253595
                ]
              ]
            },
            "treatments": [
              "retain",
              "clear"
            ]
          },
          {
            "after": -614,
            "before": 967,
            "control_seeds": {
              "original": 2330237667479163395,
              "revised": 4807181268986667867
            },
            "device": 1,
            "first": 1,
            "group": "main",
            "id": "main-15",
            "index": 15,
            "original": [
              [
                -210,
                775,
                -884,
                557,
                -297,
                447,
                -152,
                -393,
                -417,
                -18,
                -303,
                111,
                745,
                -207,
                959,
                -285,
                -902,
                821,
                787,
                -578
              ],
              [
                -423,
                -859,
                -995,
                -244,
                734,
                584,
                831,
                -418,
                559,
                -124,
                947,
                -631,
                967,
                924,
                -640,
                3,
                -862,
                -381,
                -467,
                806
              ]
            ],
            "original_truth": 967,
            "owner": 1,
            "proposals": 1,
            "rejections": {
              "nonunique_maximum": 0,
              "owner_block": 0,
              "remaining_at_floor": 0
            },
            "revised": [
              [
                -210,
                775,
                -884,
                557,
                -297,
                447,
                -152,
                -393,
                -417,
                -18,
                -303,
                111,
                745,
                -207,
                959,
                -285,
                -902,
                821,
                787,
                -578
              ],
              [
                -423,
                -859,
                -995,
                -244,
                734,
                584,
                831,
                -418,
                559,
                -124,
                947,
                -631,
                -614,
                924,
                -640,
                3,
                -862,
                -381,
                -467,
                806
              ]
            ],
            "revised_truth": 959,
            "row": 12,
            "seeds": {
              "prefix": [
                [
                  8049316475296984749,
                  6651311606282137597,
                  2428136916549517310
                ],
                [
                  3863189380517531492,
                  9210302312644362371,
                  5107330403958620136
                ]
              ],
              "recovery": [
                [
                  8853190939237816913,
                  2662960213906330612,
                  1865128207707360999
                ],
                [
                  1307808059499793038,
                  2793050492793667061,
                  171509841350124668
                ]
              ]
            },
            "treatments": [
              "clear",
              "retain"
            ]
          },
          {
            "after": -627,
            "before": 919,
            "control_seeds": {
              "original": 1503848339326062111,
              "revised": 5319984730134778560
            },
            "device": 0,
            "first": 1,
            "group": "main",
            "id": "main-16",
            "index": 16,
            "original": [
              [
                324,
                -682,
                887,
                304,
                14,
                656,
                -467,
                579,
                486,
                229,
                477,
                37,
                508,
                -460,
                -255,
                -482,
                916,
                -676,
                -838,
                -20
              ],
              [
                -260,
                788,
                919,
                -221,
                629,
                -63,
                334,
                -319,
                574,
                752,
                792,
                -664,
                880,
                -864,
                753,
                -803,
                297,
                -54,
                895,
                652
              ]
            ],
            "original_truth": 919,
            "owner": 1,
            "proposals": 4,
            "rejections": {
              "nonunique_maximum": 0,
              "owner_block": 3,
              "remaining_at_floor": 0
            },
            "revised": [
              [
                324,
                -682,
                887,
                304,
                14,
                656,
                -467,
                579,
                486,
                229,
                477,
                37,
                508,
                -460,
                -255,
                -482,
                916,
                -676,
                -838,
                -20
              ],
              [
                -260,
                788,
                -627,
                -221,
                629,
                -63,
                334,
                -319,
                574,
                752,
                792,
                -664,
                880,
                -864,
                753,
                -803,
                297,
                -54,
                895,
                652
              ]
            ],
            "revised_truth": 916,
            "row": 2,
            "seeds": {
              "prefix": [
                [
                  9133351367866927780,
                  4708268123332630951,
                  8101133946723231055
                ],
                [
                  3149931738709346887,
                  4096448280584167478,
                  6863410623319663693
                ]
              ],
              "recovery": [
                [
                  8097089018640116083,
                  7312699544095183027,
                  8009409243665888063
                ],
                [
                  8661375194255689629,
                  6911446480698722895,
                  3051672257619254603
                ]
              ]
            },
            "treatments": [
              "retain",
              "clear"
            ]
          },
          {
            "after": -71,
            "before": 885,
            "control_seeds": {
              "original": 8042247140532174822,
              "revised": 4019721016965024234
            },
            "device": 1,
            "first": 1,
            "group": "main",
            "id": "main-17",
            "index": 17,
            "original": [
              [
                -633,
                -352,
                811,
                246,
                58,
                605,
                99,
                -392,
                269,
                840,
                -911,
                60,
                -915,
                300,
                878,
                -859,
                250,
                392,
                205,
                -720
              ],
              [
                278,
                -711,
                521,
                -414,
                -830,
                97,
                39,
                -150,
                -263,
                -981,
                -424,
                885,
                -836,
                -927,
                748,
                658,
                -780,
                -894,
                407,
                774
              ]
            ],
            "original_truth": 885,
            "owner": 1,
            "proposals": 4,
            "rejections": {
              "nonunique_maximum": 0,
              "owner_block": 3,
              "remaining_at_floor": 0
            },
            "revised": [
              [
                -633,
                -352,
                811,
                246,
                58,
                605,
                99,
                -392,
                269,
                840,
                -911,
                60,
                -915,
                300,
                878,
                -859,
                250,
                392,
                205,
                -720
              ],
              [
                278,
                -711,
                521,
                -414,
                -830,
                97,
                39,
                -150,
                -263,
                -981,
                -424,
                -71,
                -836,
                -927,
                748,
                658,
                -780,
                -894,
                407,
                774
              ]
            ],
            "revised_truth": 878,
            "row": 11,
            "seeds": {
              "prefix": [
                [
                  7370203119696101683,
                  8676882964858688617,
                  1285738219610523296
                ],
                [
                  1558207476444573364,
                  3854852960831798470,
                  3362734413617082988
                ]
              ],
              "recovery": [
                [
                  5749282179274952530,
                  439220088649944670,
                  2665823271028982252
                ],
                [
                  7007927364177320798,
                  1454269570792637695,
                  86856773501310504
                ]
              ]
            },
            "treatments": [
              "clear",
              "retain"
            ]
          },
          {
            "after": 333,
            "before": 908,
            "control_seeds": {
              "original": 1966245509280641185,
              "revised": 4928770713416526446
            },
            "device": 0,
            "first": 1,
            "group": "main",
            "id": "main-18",
            "index": 18,
            "original": [
              [
                133,
                -605,
                823,
                71,
                -809,
                -606,
                313,
                487,
                769,
                788,
                780,
                -826,
                -211,
                539,
                -250,
                185,
                807,
                -906,
                848,
                -745
              ],
              [
                -114,
                -245,
                -441,
                649,
                -322,
                -702,
                -814,
                632,
                326,
                165,
                -144,
                813,
                -706,
                525,
                -90,
                908,
                348,
                827,
                781,
                333
              ]
            ],
            "original_truth": 908,
            "owner": 1,
            "proposals": 1,
            "rejections": {
              "nonunique_maximum": 0,
              "owner_block": 0,
              "remaining_at_floor": 0
            },
            "revised": [
              [
                133,
                -605,
                823,
                71,
                -809,
                -606,
                313,
                487,
                769,
                788,
                780,
                -826,
                -211,
                539,
                -250,
                185,
                807,
                -906,
                848,
                -745
              ],
              [
                -114,
                -245,
                -441,
                649,
                -322,
                -702,
                -814,
                632,
                326,
                165,
                -144,
                813,
                -706,
                525,
                -90,
                333,
                348,
                827,
                781,
                333
              ]
            ],
            "revised_truth": 848,
            "row": 15,
            "seeds": {
              "prefix": [
                [
                  7598135116584668381,
                  9146236957778840145,
                  114920852746157201
                ],
                [
                  3316022409743939391,
                  4027773770743399252,
                  4930560188190906841
                ]
              ],
              "recovery": [
                [
                  4118538573955015757,
                  8850344356207479036,
                  7160915629396249838
                ],
                [
                  307394048295980151,
                  5122264955052118727,
                  2565077992634760225
                ]
              ]
            },
            "treatments": [
              "retain",
              "clear"
            ]
          },
          {
            "after": 213,
            "before": 951,
            "control_seeds": {
              "original": 7740961541298929508,
              "revised": 245690049236384587
            },
            "device": 1,
            "first": 1,
            "group": "main",
            "id": "main-19",
            "index": 19,
            "original": [
              [
                -546,
                -244,
                -664,
                -17,
                128,
                446,
                -155,
                551,
                -233,
                944,
                414,
                -703,
                61,
                92,
                -941,
                -142,
                -47,
                944,
                -435,
                -519
              ],
              [
                726,
                -445,
                362,
                -718,
                951,
                758,
                735,
                -443,
                521,
                689,
                -805,
                -8,
                -197,
                713,
                -176,
                -165,
                319,
                626,
                -194,
                875
              ]
            ],
            "original_truth": 951,
            "owner": 1,
            "proposals": 3,
            "rejections": {
              "nonunique_maximum": 0,
              "owner_block": 2,
              "remaining_at_floor": 0
            },
            "revised": [
              [
                -546,
                -244,
                -664,
                -17,
                128,
                446,
                -155,
                551,
                -233,
                944,
                414,
                -703,
                61,
                92,
                -941,
                -142,
                -47,
                944,
                -435,
                -519
              ],
              [
                726,
                -445,
                362,
                -718,
                213,
                758,
                735,
                -443,
                521,
                689,
                -805,
                -8,
                -197,
                713,
                -176,
                -165,
                319,
                626,
                -194,
                875
              ]
            ],
            "revised_truth": 944,
            "row": 4,
            "seeds": {
              "prefix": [
                [
                  7887811878140492104,
                  6255283482707103244,
                  3632073470791873446
                ],
                [
                  6235676957750292586,
                  2326562108051485717,
                  5493582434092557490
                ]
              ],
              "recovery": [
                [
                  9092468552002419456,
                  9019583098529008256,
                  5921040231014388108
                ],
                [
                  5217546261940366333,
                  1178083047056805454,
                  491617388332277490
                ]
              ]
            },
            "treatments": [
              "clear",
              "retain"
            ]
          }
        ]
      },
      "mode": "direct",
      "pilot_admission": "fixed scalar qualification; terminal committed pilot phases/controls and intact runtime/resources; ordinary model errors and original completion diagnostic",
      "policy": "i01-recorded-outcomes-run-all-2026-10-15",
      "settings": {
        "attention": "recovery_t4_sdpa",
        "chat_template": "{%- set image_count = namespace(value=0) %}\n{%- set video_count = namespace(value=0) %}\n{%- macro render_content(content, do_vision_count, is_system_content=false) %}\n    {%- if content is string %}\n        {{- content }}\n    {%- elif content is iterable and content is not mapping %}\n        {%- for item in content %}\n            {%- if 'image' in item or 'image_url' in item or item.type == 'image' %}\n                {%- if is_system_content %}\n                    {{- raise_exception('System message cannot contain images.') }}\n                {%- endif %}\n                {%- if do_vision_count %}\n                    {%- set image_count.value = image_count.value + 1 %}\n                {%- endif %}\n                {%- if add_vision_id %}\n                    {{- 'Picture ' ~ image_count.value ~ ': ' }}\n                {%- endif %}\n                {{- '<|vision_start|><|image_pad|><|vision_end|>' }}\n            {%- elif 'video' in item or item.type == 'video' %}\n                {%- if is_system_content %}\n                    {{- raise_exception('System message cannot contain videos.') }}\n                {%- endif %}\n                {%- if do_vision_count %}\n                    {%- set video_count.value = video_count.value + 1 %}\n                {%- endif %}\n                {%- if add_vision_id %}\n                    {{- 'Video ' ~ video_count.value ~ ': ' }}\n                {%- endif %}\n                {{- '<|vision_start|><|video_pad|><|vision_end|>' }}\n            {%- elif 'text' in item %}\n                {{- item.text }}\n            {%- else %}\n                {{- raise_exception('Unexpected item type in content.') }}\n            {%- endif %}\n        {%- endfor %}\n    {%- elif content is none or content is undefined %}\n        {{- '' }}\n    {%- else %}\n        {{- raise_exception('Unexpected content type.') }}\n    {%- endif %}\n{%- endmacro %}\n{%- if not messages %}\n    {{- raise_exception('No messages provided.') }}\n{%- endif %}\n{%- if tools and tools is iterable and tools is not mapping %}\n    {{- '<|im_start|>system\\n' }}\n    {{- \"# Tools\\n\\nYou have access to the following functions:\\n\\n<tools>\" }}\n    {%- for tool in tools %}\n        {{- \"\\n\" }}\n        {{- tool | tojson }}\n    {%- endfor %}\n    {{- \"\\n</tools>\" }}\n    {{- '\\n\\nIf you choose to call a function ONLY reply in the following format with NO suffix:\\n\\n<tool_call>\\n<function=example_function_name>\\n<parameter=example_parameter_1>\\nvalue_1\\n</parameter>\\n<parameter=example_parameter_2>\\nThis is the value for the second parameter\\nthat can span\\nmultiple lines\\n</parameter>\\n</function>\\n</tool_call>\\n\\n<IMPORTANT>\\nReminder:\\n- Function calls MUST follow the specified format: an inner <function=...></function> block must be nested within <tool_call></tool_call> XML tags\\n- Required parameters MUST be specified\\n- You may provide optional reasoning for your function call in natural language BEFORE the function call, but NOT after\\n- If there is no function call available, answer the question like normal with your current knowledge and do not tell the user about function calls\\n</IMPORTANT>' }}\n    {%- if messages[0].role == 'system' %}\n        {%- set content = render_content(messages[0].content, false, true)|trim %}\n        {%- if content %}\n            {{- '\\n\\n' + content }}\n        {%- endif %}\n    {%- endif %}\n    {{- '<|im_end|>\\n' }}\n{%- else %}\n    {%- if messages[0].role == 'system' %}\n        {%- set content = render_content(messages[0].content, false, true)|trim %}\n        {{- '<|im_start|>system\\n' + content + '<|im_end|>\\n' }}\n    {%- endif %}\n{%- endif %}\n{%- set ns = namespace(multi_step_tool=true, last_query_index=messages|length - 1) %}\n{%- for message in messages[::-1] %}\n    {%- set index = (messages|length - 1) - loop.index0 %}\n    {%- if ns.multi_step_tool and message.role == \"user\" %}\n        {%- set content = render_content(message.content, false)|trim %}\n        {%- if not(content.startswith('<tool_response>') and content.endswith('</tool_response>')) %}\n            {%- set ns.multi_step_tool = false %}\n            {%- set ns.last_query_index = index %}\n        {%- endif %}\n    {%- endif %}\n{%- endfor %}\n{%- if ns.multi_step_tool %}\n    {{- raise_exception('No user query found in messages.') }}\n{%- endif %}\n{%- for message in messages %}\n    {%- set content = render_content(message.content, true)|trim %}\n    {%- if message.role == \"system\" %}\n        {%- if not loop.first %}\n            {{- raise_exception('System message must be at the beginning.') }}\n        {%- endif %}\n    {%- elif message.role == \"user\" %}\n        {{- '<|im_start|>' + message.role + '\\n' + content + '<|im_end|>' + '\\n' }}\n    {%- elif message.role == \"assistant\" %}\n        {%- set reasoning_content = '' %}\n        {%- if message.reasoning_content is string %}\n            {%- set reasoning_content = message.reasoning_content %}\n        {%- else %}\n            {%- if '</think>' in content %}\n                {%- set reasoning_content = content.split('</think>')[0].rstrip('\\n').split('<think>')[-1].lstrip('\\n') %}\n                {%- set content = content.split('</think>')[-1].lstrip('\\n') %}\n            {%- endif %}\n        {%- endif %}\n        {%- set reasoning_content = reasoning_content|trim %}\n        {%- if loop.index0 > ns.last_query_index %}\n            {{- '<|im_start|>' + message.role + '\\n<think>\\n' + reasoning_content + '\\n</think>\\n\\n' + content }}\n        {%- else %}\n            {{- '<|im_start|>' + message.role + '\\n' + content }}\n        {%- endif %}\n        {%- if message.tool_calls and message.tool_calls is iterable and message.tool_calls is not mapping %}\n            {%- for tool_call in message.tool_calls %}\n                {%- if tool_call.function is defined %}\n                    {%- set tool_call = tool_call.function %}\n                {%- endif %}\n                {%- if loop.first %}\n                    {%- if content|trim %}\n                        {{- '\\n\\n<tool_call>\\n<function=' + tool_call.name + '>\\n' }}\n                    {%- else %}\n                        {{- '<tool_call>\\n<function=' + tool_call.name + '>\\n' }}\n                    {%- endif %}\n                {%- else %}\n                    {{- '\\n<tool_call>\\n<function=' + tool_call.name + '>\\n' }}\n                {%- endif %}\n                {%- if tool_call.arguments is defined %}\n                    {%- for args_name, args_value in tool_call.arguments|items %}\n                        {{- '<parameter=' + args_name + '>\\n' }}\n                        {%- set args_value = args_value | tojson | safe if args_value is mapping or (args_value is sequence and args_value is not string) else args_value | string %}\n                        {{- args_value }}\n                        {{- '\\n</parameter>\\n' }}\n                    {%- endfor %}\n                {%- endif %}\n                {{- '</function>\\n</tool_call>' }}\n            {%- endfor %}\n        {%- endif %}\n        {{- '<|im_end|>\\n' }}\n    {%- elif message.role == \"tool\" %}\n        {%- if loop.previtem and loop.previtem.role != \"tool\" %}\n            {{- '<|im_start|>user' }}\n        {%- endif %}\n        {{- '\\n<tool_response>\\n' }}\n        {{- content }}\n        {{- '\\n</tool_response>' }}\n        {%- if not loop.last and loop.nextitem.role != \"tool\" %}\n            {{- '<|im_end|>\\n' }}\n        {%- elif loop.last %}\n            {{- '<|im_end|>\\n' }}\n        {%- endif %}\n    {%- else %}\n        {{- raise_exception('Unexpected message role.') }}\n    {%- endif %}\n{%- endfor %}\n{%- if add_generation_prompt %}\n    {{- '<|im_start|>assistant\\n' }}\n    {%- if enable_thinking is defined and enable_thinking is false %}\n        {{- '<think>\\n\\n</think>\\n\\n' }}\n    {%- else %}\n        {{- '<think>\\n' }}\n    {%- endif %}\n{%- endif %}",
        "generation": {
          "do_sample": true,
          "eos_token_id": [
            248044,
            248046
          ],
          "max_new_tokens": 512,
          "min_p": 0.0,
          "num_beams": 1,
          "output_scores": false,
          "pad_token_id": 248044,
          "prefill_chunk_size": 256,
          "remove_invalid_values": false,
          "repetition_penalty": 1.0,
          "return_dict_in_generate": true,
          "temperature": 0.7,
          "top_k": 20,
          "top_p": 0.8,
          "use_cache": true
        },
        "input_limit": 8192,
        "mode": "direct",
        "model": "Qwen/Qwen3.5-9B",
        "presence_penalty": 0,
        "quantization": "NF4-double-FP16",
        "regime": "i01-course-v1",
        "revision": "c202236235762e1c871ad0ccb60c8ee5ba337b9a",
        "visible_limit": 512
      },
      "useful_communication": null,
      "worlds_per_batch": 2
    },
    "readiness": {
      "ABA_equal": [
        true,
        true
      ],
      "equality_policy": "Diagnostic: unexpected differences require explicit state-isolation review before qualification; no extra samples or decoding changes.",
      "needs_review": false,
      "passed": true,
      "results": [
        {
          "label": "A1",
          "outcome": {
            "backend": {
              "allocated_bytes": 7685424128,
              "cache": {
                "calls": 14,
                "disposed_after_call": true,
                "initial_empty": true,
                "same_call_cache": true
              },
              "cpu_seed": 2895223694339253810,
              "cuda_seed": 2895223694339253810,
              "device": "cuda:0",
              "finite_score_steps": 14,
              "free_bytes_with_cache": 7603027968,
              "memory_samples": 75,
              "observed_free_min_bytes": 7603027968,
              "observed_peak_free_lower_bytes": 7603027968,
              "peak_reserved_bytes": 7889485824,
              "pid": 351,
              "raw_suffix_text": "{\"message\":null,\"submit\":3,\"wait\":false}<|im_end|>",
              "removed_terminal_id": 248046,
              "reserved_bytes": 7889485824,
              "seed": 2895223694339253810,
              "total_bytes": 15636037632
            },
            "dispatch_seconds": 3.95522743000015,
            "failure": null,
            "framing_error": null,
            "generated_tokens": 14,
            "input_tokens": 67,
            "peak_memory_bytes": 7793119744,
            "raw_text": "{\"message\":null,\"submit\":3,\"wait\":false}",
            "ready_seconds": 3.9131304960001216,
            "termination": "eos",
            "thinking": null,
            "token_ids": [
              4754,
              1927,
              763,
              2827,
              1288,
              5769,
              763,
              18,
              1288,
              11158,
              763,
              3721,
              92,
              248046
            ],
            "truncated": false,
            "visible_text": "{\"message\":null,\"submit\":3,\"wait\":false}"
          },
          "slot": 0
        },
        {
          "label": "B",
          "outcome": {
            "backend": {
              "allocated_bytes": 7685555200,
              "cache": {
                "calls": 16,
                "disposed_after_call": true,
                "initial_empty": true,
                "same_call_cache": true
              },
              "cpu_seed": 1172835993072093706,
              "cuda_seed": 1172835993072093706,
              "device": "cuda:0",
              "finite_score_steps": 16,
              "free_bytes_with_cache": 7603027968,
              "memory_samples": 46,
              "observed_free_min_bytes": 7603027968,
              "observed_peak_free_lower_bytes": 7603027968,
              "peak_reserved_bytes": 7889485824,
              "pid": 351,
              "raw_suffix_text": "{\"message\":null,\"submit\":100,\"wait\":false}<|im_end|>",
              "removed_terminal_id": 248046,
              "reserved_bytes": 7889485824,
              "seed": 1172835993072093706,
              "total_bytes": 15636037632
            },
            "dispatch_seconds": 2.2790992019999976,
            "failure": null,
            "framing_error": null,
            "generated_tokens": 16,
            "input_tokens": 69,
            "peak_memory_bytes": 7793251840,
            "raw_text": "{\"message\":null,\"submit\":100,\"wait\":false}",
            "ready_seconds": 2.27661537899985,
            "termination": "eos",
            "thinking": null,
            "token_ids": [
              4754,
              1927,
              763,
              2827,
              1288,
              5769,
              763,
              16,
              15,
              15,
              1288,
              11158,
              763,
              3721,
              92,
              248046
            ],
            "truncated": false,
            "visible_text": "{\"message\":null,\"submit\":100,\"wait\":false}"
          },
          "slot": 0
        },
        {
          "label": "A2",
          "outcome": {
            "backend": {
              "allocated_bytes": 7685424128,
              "cache": {
                "calls": 14,
                "disposed_after_call": true,
                "initial_empty": true,
                "same_call_cache": true
              },
              "cpu_seed": 2895223694339253810,
              "cuda_seed": 2895223694339253810,
              "device": "cuda:0",
              "finite_score_steps": 14,
              "free_bytes_with_cache": 7603027968,
              "memory_samples": 36,
              "observed_free_min_bytes": 7603027968,
              "observed_peak_free_lower_bytes": 7603027968,
              "peak_reserved_bytes": 7889485824,
              "pid": 351,
              "raw_suffix_text": "{\"message\":null,\"submit\":3,\"wait\":false}<|im_end|>",
              "removed_terminal_id": 248046,
              "reserved_bytes": 7889485824,
              "seed": 2895223694339253810,
              "total_bytes": 15636037632
            },
            "dispatch_seconds": 1.7934442490000038,
            "failure": null,
            "framing_error": null,
            "generated_tokens": 14,
            "input_tokens": 67,
            "peak_memory_bytes": 7793119744,
            "raw_text": "{\"message\":null,\"submit\":3,\"wait\":false}",
            "ready_seconds": 1.790842100999953,
            "termination": "eos",
            "thinking": null,
            "token_ids": [
              4754,
              1927,
              763,
              2827,
              1288,
              5769,
              763,
              18,
              1288,
              11158,
              763,
              3721,
              92,
              248046
            ],
            "truncated": false,
            "visible_text": "{\"message\":null,\"submit\":3,\"wait\":false}"
          },
          "slot": 0
        },
        {
          "label": "A1",
          "outcome": {
            "backend": {
              "allocated_bytes": 7685424128,
              "cache": {
                "calls": 14,
                "disposed_after_call": true,
                "initial_empty": true,
                "same_call_cache": true
              },
              "cpu_seed": 9113091594724103221,
              "cuda_seed": 9113091594724103221,
              "device": "cuda:0",
              "finite_score_steps": 14,
              "free_bytes_with_cache": 7603027968,
              "memory_samples": 55,
              "observed_free_min_bytes": 7603027968,
              "observed_peak_free_lower_bytes": 7603027968,
              "peak_reserved_bytes": 7889485824,
              "pid": 365,
              "raw_suffix_text": "{\"message\":null,\"submit\":3,\"wait\":false}<|im_end|>",
              "removed_terminal_id": 248046,
              "reserved_bytes": 7889485824,
              "seed": 9113091594724103221,
              "total_bytes": 15636037632
            },
            "dispatch_seconds": 2.865736879999986,
            "failure": null,
            "framing_error": null,
            "generated_tokens": 14,
            "input_tokens": 67,
            "peak_memory_bytes": 7793119744,
            "raw_text": "{\"message\":null,\"submit\":3,\"wait\":false}",
            "ready_seconds": 2.8277453229998173,
            "termination": "eos",
            "thinking": null,
            "token_ids": [
              4754,
              1927,
              763,
              2827,
              1288,
              5769,
              763,
              18,
              1288,
              11158,
              763,
              3721,
              92,
              248046
            ],
            "truncated": false,
            "visible_text": "{\"message\":null,\"submit\":3,\"wait\":false}"
          },
          "slot": 1
        },
        {
          "label": "B",
          "outcome": {
            "backend": {
              "allocated_bytes": 7685555200,
              "cache": {
                "calls": 16,
                "disposed_after_call": true,
                "initial_empty": true,
                "same_call_cache": true
              },
              "cpu_seed": 718885271260442133,
              "cuda_seed": 718885271260442133,
              "device": "cuda:0",
              "finite_score_steps": 16,
              "free_bytes_with_cache": 7603027968,
              "memory_samples": 45,
              "observed_free_min_bytes": 7603027968,
              "observed_peak_free_lower_bytes": 7603027968,
              "peak_reserved_bytes": 7889485824,
              "pid": 365,
              "raw_suffix_text": "{\"message\":null,\"submit\":100,\"wait\":false}<|im_end|>",
              "removed_terminal_id": 248046,
              "reserved_bytes": 7889485824,
              "seed": 718885271260442133,
              "total_bytes": 15636037632
            },
            "dispatch_seconds": 2.2303744820001157,
            "failure": null,
            "framing_error": null,
            "generated_tokens": 16,
            "input_tokens": 69,
            "peak_memory_bytes": 7793251840,
            "raw_text": "{\"message\":null,\"submit\":100,\"wait\":false}",
            "ready_seconds": 2.22765913499984,
            "termination": "eos",
            "thinking": null,
            "token_ids": [
              4754,
              1927,
              763,
              2827,
              1288,
              5769,
              763,
              16,
              15,
              15,
              1288,
              11158,
              763,
              3721,
              92,
              248046
            ],
            "truncated": false,
            "visible_text": "{\"message\":null,\"submit\":100,\"wait\":false}"
          },
          "slot": 1
        },
        {
          "label": "A2",
          "outcome": {
            "backend": {
              "allocated_bytes": 7685424128,
              "cache": {
                "calls": 14,
                "disposed_after_call": true,
                "initial_empty": true,
                "same_call_cache": true
              },
              "cpu_seed": 9113091594724103221,
              "cuda_seed": 9113091594724103221,
              "device": "cuda:0",
              "finite_score_steps": 14,
              "free_bytes_with_cache": 7603027968,
              "memory_samples": 35,
              "observed_free_min_bytes": 7603027968,
              "observed_peak_free_lower_bytes": 7603027968,
              "peak_reserved_bytes": 7889485824,
              "pid": 365,
              "raw_suffix_text": "{\"message\":null,\"submit\":3,\"wait\":false}<|im_end|>",
              "removed_terminal_id": 248046,
              "reserved_bytes": 7889485824,
              "seed": 9113091594724103221,
              "total_bytes": 15636037632
            },
            "dispatch_seconds": 1.7158115610000095,
            "failure": null,
            "framing_error": null,
            "generated_tokens": 14,
            "input_tokens": 67,
            "peak_memory_bytes": 7793119744,
            "raw_text": "{\"message\":null,\"submit\":3,\"wait\":false}",
            "ready_seconds": 1.7131544569999733,
            "termination": "eos",
            "thinking": null,
            "token_ids": [
              4754,
              1927,
              763,
              2827,
              1288,
              5769,
              763,
              18,
              1288,
              11158,
              763,
              3721,
              92,
              248046
            ],
            "truncated": false,
            "visible_text": "{\"message\":null,\"submit\":3,\"wait\":false}"
          },
          "slot": 1
        }
      ]
    },
    "screen/direct": {
      "correct": 10,
      "passed": true,
      "policy": "i01-direct-protocol-2026-10-15",
      "protocol_errors": 0,
      "reason": "",
      "total": 12
    },
    "envelope": {
      "loads": [
        "a7bb7845-cf04-4efd-9b68-f74b9595cfaa/load-0",
        "a7bb7845-cf04-4efd-9b68-f74b9595cfaa/load-0"
      ],
      "mode": "direct",
      "passed": true,
      "reload": false,
      "results": [
        {
          "backend": {
            "allocated_bytes": 7968180224,
            "cache": {
              "calls": 543,
              "disposed_after_call": true,
              "initial_empty": true,
              "same_call_cache": true
            },
            "cpu_seed": 3554240822569505675,
            "cuda_seed": 3554240822569505675,
            "device": "cuda:0",
            "finite_score_steps": 512,
            "free_bytes_with_cache": 7288455168,
            "memory_samples": 1372,
            "observed_free_min_bytes": 7288455168,
            "observed_peak_free_lower_bytes": 7288455168,
            "peak_reserved_bytes": 8204058624,
            "pid": 351,
            "raw_suffix_text": "{\"message\":null,\"submit\":1,\"wait\":false}<|im_end|>\n<|endoftext|><|im_start|>user\nComplete input: [0, 1]<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n{\"message\":null,\"submit\":1,\"wait\":false}<|im_end|>\n<|endoftext|><|im_start|>user\nComplete input: [0, 1]<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n{\"message\":null,\"submit\":1,\"wait\":false}<|im_end|>\n<|endoftext|><|im_start|>user\nComplete input: [0, 1]<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n{\"message\":null,\"submit\":1,\"wait\":false}<|im_end|>\n<|endoftext|><|im_start|>user\nComplete input: [0, 1]<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n{\"message\":null,\"submit\":1,\"wait\":false}<|im_end|>\n<|endoftext|><|im_start|>user\nComplete input: [0, 1]<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n{\"message\":null,\"submit\":1,\"wait\":false}<|im_end|>\n<|im_start|>user\nComplete input: [0, 1]<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n{\"message\":null,\"submit\":1,\"wait\":false}<|im_end|>\n<|im_start|>user\nComplete input: [0, 1]<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n{\"message\":null,\"submit\":1,\"wait\":false}<|im_end|>\n<|im_start|>user\nComplete input: [0, 1]<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n{\"message\":null,\"submit\":1,\"wait\":false}<|im_end|>\n<|im_start|>user\nComplete input: [0, 1]<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n{\"message\":null,\"submit\":1,\"wait\":false}<|im_end|>\n<|im_start|>user\nComplete input: [0, 1]<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n{\"message\":null,\"submit\":1,\"wait\":false}<|im_end|>\n<|im_start|>user\nComplete input: [0, 1]<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n{\"message\":null,\"submit\":1,\"wait\":false}<|im_end|>\n<|im_start|>user\nComplete input: [0, 1]<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n{\"message\":null,\"submit\":1,\"wait\":false}<|im_end|>\n<|im_start|>user\nComplete input: [0, 1]<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n{\"message\":null,\"submit\":1,\"wait\":false}<|im_end|>\n<|im_start|>user\nComplete input: [0, 1]<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n{\"message\":",
            "removed_terminal_id": null,
            "reserved_bytes": 8204058624,
            "seed": 3554240822569505675,
            "total_bytes": 15636037632
          },
          "dispatch_seconds": 68.98037374899991,
          "failure": null,
          "framing_error": null,
          "generated_tokens": 512,
          "input_tokens": 8192,
          "peak_memory_bytes": 8077826048,
          "raw_text": "{\"message\":null,\"submit\":1,\"wait\":false}<|im_end|>\n<|endoftext|><|im_start|>user\nComplete input: [0, 1]<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n{\"message\":null,\"submit\":1,\"wait\":false}<|im_end|>\n<|endoftext|><|im_start|>user\nComplete input: [0, 1]<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n{\"message\":null,\"submit\":1,\"wait\":false}<|im_end|>\n<|endoftext|><|im_start|>user\nComplete input: [0, 1]<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n{\"message\":null,\"submit\":1,\"wait\":false}<|im_end|>\n<|endoftext|><|im_start|>user\nComplete input: [0, 1]<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n{\"message\":null,\"submit\":1,\"wait\":false}<|im_end|>\n<|endoftext|><|im_start|>user\nComplete input: [0, 1]<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n{\"message\":null,\"submit\":1,\"wait\":false}<|im_end|>\n<|im_start|>user\nComplete input: [0, 1]<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n{\"message\":null,\"submit\":1,\"wait\":false}<|im_end|>\n<|im_start|>user\nComplete input: [0, 1]<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n{\"message\":null,\"submit\":1,\"wait\":false}<|im_end|>\n<|im_start|>user\nComplete input: [0, 1]<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n{\"message\":null,\"submit\":1,\"wait\":false}<|im_end|>\n<|im_start|>user\nComplete input: [0, 1]<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n{\"message\":null,\"submit\":1,\"wait\":false}<|im_end|>\n<|im_start|>user\nComplete input: [0, 1]<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n{\"message\":null,\"submit\":1,\"wait\":false}<|im_end|>\n<|im_start|>user\nComplete input: [0, 1]<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n{\"message\":null,\"submit\":1,\"wait\":false}<|im_end|>\n<|im_start|>user\nComplete input: [0, 1]<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n{\"message\":null,\"submit\":1,\"wait\":false}<|im_end|>\n<|im_start|>user\nComplete input: [0, 1]<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n{\"message\":null,\"submit\":1,\"wait\":false}<|im_end|>\n<|im_start|>user\nComplete input: [0, 1]<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n{\"message\":",
          "ready_seconds": 68.96988406799983,
          "termination": "length",
          "thinking": null,
          "token_ids": [
            4754,
            1927,
            763,
            2827,
            1288,
            5769,
            763,
            16,
            1288,
            11158,
            763,
            3721,
            92,
            248046,
            198,
            248044,
            248045,
            846,
            198,
            12188,
            1879,
            25,
            498,
            15,
            11,
            220,
            16,
            60,
            248046,
            198,
            248045,
            74455,
            198,
            248068,
            271,
            248069,
            271,
            4754,
            1927,
            763,
            2827,
            1288,
            5769,
            763,
            16,
            1288,
            11158,
            763,
            3721,
            92,
            248046,
            198,
            248044,
            248045,
            846,
            198,
            12188,
            1879,
            25,
            498,
            15,
            11,
            220,
            16,
            60,
            248046,
            198,
            248045,
            74455,
            198,
            248068,
            271,
            248069,
            271,
            4754,
            1927,
            763,
            2827,
            1288,
            5769,
            763,
            16,
            1288,
            11158,
            763,
            3721,
            92,
            248046,
            198,
            248044,
            248045,
            846,
            198,
            12188,
            1879,
            25,
            498,
            15,
            11,
            220,
            16,
            60,
            248046,
            198,
            248045,
            74455,
            198,
            248068,
            271,
            248069,
            271,
            4754,
            1927,
            763,
            2827,
            1288,
            5769,
            763,
            16,
            1288,
            11158,
            763,
            3721,
            92,
            248046,
            198,
            248044,
            248045,
            846,
            198,
            12188,
            1879,
            25,
            498,
            15,
            11,
            220,
            16,
            60,
            248046,
            198,
            248045,
            74455,
            198,
            248068,
            271,
            248069,
            271,
            4754,
            1927,
            763,
            2827,
            1288,
            5769,
            763,
            16,
            1288,
            11158,
            763,
            3721,
            92,
            248046,
            198,
            248044,
            248045,
            846,
            198,
            12188,
            1879,
            25,
            498,
            15,
            11,
            220,
            16,
            60,
            248046,
            198,
            248045,
            74455,
            198,
            248068,
            271,
            248069,
            271,
            4754,
            1927,
            763,
            2827,
            1288,
            5769,
            763,
            16,
            1288,
            11158,
            763,
            3721,
            92,
            248046,
            198,
            248045,
            846,
            198,
            12188,
            1879,
            25,
            498,
            15,
            11,
            220,
            16,
            60,
            248046,
            198,
            248045,
            74455,
            198,
            248068,
            271,
            248069,
            271,
            4754,
            1927,
            763,
            2827,
            1288,
            5769,
            763,
            16,
            1288,
            11158,
            763,
            3721,
            92,
            248046,
            198,
            248045,
            846,
            198,
            12188,
            1879,
            25,
            498,
            15,
            11,
            220,
            16,
            60,
            248046,
            198,
            248045,
            74455,
            198,
            248068,
            271,
            248069,
            271,
            4754,
            1927,
            763,
            2827,
            1288,
            5769,
            763,
            16,
            1288,
            11158,
            763,
            3721,
            92,
            248046,
            198,
            248045,
            846,
            198,
            12188,
            1879,
            25,
            498,
            15,
            11,
            220,
            16,
            60,
            248046,
            198,
            248045,
            74455,
            198,
            248068,
            271,
            248069,
            271,
            4754,
            1927,
            763,
            2827,
            1288,
            5769,
            763,
            16,
            1288,
            11158,
            763,
            3721,
            92,
            248046,
            198,
            248045,
            846,
            198,
            12188,
            1879,
            25,
            498,
            15,
            11,
            220,
            16,
            60,
            248046,
            198,
            248045,
            74455,
            198,
            248068,
            271,
            248069,
            271,
            4754,
            1927,
            763,
            2827,
            1288,
            5769,
            763,
            16,
            1288,
            11158,
            763,
            3721,
            92,
            248046,
            198,
            248045,
            846,
            198,
            12188,
            1879,
            25,
            498,
            15,
            11,
            220,
            16,
            60,
            248046,
            198,
            248045,
            74455,
            198,
            248068,
            271,
            248069,
            271,
            4754,
            1927,
            763,
            2827,
            1288,
            5769,
            763,
            16,
            1288,
            11158,
            763,
            3721,
            92,
            248046,
            198,
            248045,
            846,
            198,
            12188,
            1879,
            25,
            498,
            15,
            11,
            220,
            16,
            60,
            248046,
            198,
            248045,
            74455,
            198,
            248068,
            271,
            248069,
            271,
            4754,
            1927,
            763,
            2827,
            1288,
            5769,
            763,
            16,
            1288,
            11158,
            763,
            3721,
            92,
            248046,
            198,
            248045,
            846,
            198,
            12188,
            1879,
            25,
            498,
            15,
            11,
            220,
            16,
            60,
            248046,
            198,
            248045,
            74455,
            198,
            248068,
            271,
            248069,
            271,
            4754,
            1927,
            763,
            2827,
            1288,
            5769,
            763,
            16,
            1288,
            11158,
            763,
            3721,
            92,
            248046,
            198,
            248045,
            846,
            198,
            12188,
            1879,
            25,
            498,
            15,
            11,
            220,
            16,
            60,
            248046,
            198,
            248045,
            74455,
            198,
            248068,
            271,
            248069,
            271,
            4754,
            1927,
            763,
            2827,
            1288,
            5769,
            763,
            16,
            1288,
            11158,
            763,
            3721,
            92,
            248046,
            198,
            248045,
            846,
            198,
            12188,
            1879,
            25,
            498,
            15,
            11,
            220,
            16,
            60,
            248046,
            198,
            248045,
            74455,
            198,
            248068,
            271,
            248069,
            271,
            4754,
            1927,
            763
          ],
          "truncated": true,
          "visible_text": ""
        },
        {
          "backend": {
            "allocated_bytes": 7968180224,
            "cache": {
              "calls": 543,
              "disposed_after_call": true,
              "initial_empty": true,
              "same_call_cache": true
            },
            "cpu_seed": 6895241862355992459,
            "cuda_seed": 6895241862355992459,
            "device": "cuda:0",
            "finite_score_steps": 512,
            "free_bytes_with_cache": 7284260864,
            "memory_samples": 1377,
            "observed_free_min_bytes": 7284260864,
            "observed_peak_free_lower_bytes": 7284260864,
            "peak_reserved_bytes": 8208252928,
            "pid": 365,
            "raw_suffix_text": "{\"message\":null,\"submit\":1,\"wait\":false}<|im_end|>\n<|endoftext|><|im_start|>user\nComplete input: [0, 1]<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n{\"message\":null,\"submit\":1,\"wait\":false}<|im_end|>\n<|endoftext|><|im_start|>user\nComplete input: [0, 1]<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n{\"message\":null,\"submit\":1,\"wait\":false}<|im_end|>\n<|endoftext|><|im_start|>user\nComplete input: [0, 1]<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n{\"message\":null,\"submit\":1,\"wait\":false}<|im_end|>\n<|endoftext|><|im_start|>user\nComplete input: [0, 1]<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n{\"message\":null,\"submit\":1,\"wait\":false}<|im_end|>\n<|endoftext|><|im_start|>user\nComplete input: [0, 1]<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n{\"message\":null,\"submit\":1,\"wait\":false}<|im_end|>\n<|im_start|>user\nComplete input: [0, 1]<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n{\"message\":null,\"submit\":1,\"wait\":false}<|im_end|>\n<|im_start|>user\nComplete input: [0, 1]<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n{\"message\":null,\"submit\":1,\"wait\":false}<|im_end|>\n<|im_start|>user\nComplete input: [0, 1]<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n{\"message\":null,\"submit\":1,\"wait\":false}<|im_end|>\n<|im_start|>user\nComplete input: [0, 1]<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n{\"message\":null,\"submit\":1,\"wait\":false}<|im_end|>\n<|im_start|>user\nComplete input: [0, 1]<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n{\"message\":null,\"submit\":1,\"wait\":false}<|im_end|>\n<|im_start|>user\nComplete input: [0, 1]<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n{\"message\":null,\"submit\":1,\"wait\":false}<|im_end|>\n<|im_start|>user\nComplete input: [0, 1]<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n{\"message\":null,\"submit\":1,\"wait\":false}<|im_end|>\n<|im_start|>user\nComplete input: [0, 1]<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n{\"message\":null,\"submit\":1,\"wait\":false}<|im_end|>\n<|im_start|>user\nComplete input: [0, 1]<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n{\"message\":",
            "removed_terminal_id": null,
            "reserved_bytes": 8208252928,
            "seed": 6895241862355992459,
            "total_bytes": 15636037632
          },
          "dispatch_seconds": 69.214263372,
          "failure": null,
          "framing_error": null,
          "generated_tokens": 512,
          "input_tokens": 8192,
          "peak_memory_bytes": 8077826048,
          "raw_text": "{\"message\":null,\"submit\":1,\"wait\":false}<|im_end|>\n<|endoftext|><|im_start|>user\nComplete input: [0, 1]<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n{\"message\":null,\"submit\":1,\"wait\":false}<|im_end|>\n<|endoftext|><|im_start|>user\nComplete input: [0, 1]<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n{\"message\":null,\"submit\":1,\"wait\":false}<|im_end|>\n<|endoftext|><|im_start|>user\nComplete input: [0, 1]<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n{\"message\":null,\"submit\":1,\"wait\":false}<|im_end|>\n<|endoftext|><|im_start|>user\nComplete input: [0, 1]<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n{\"message\":null,\"submit\":1,\"wait\":false}<|im_end|>\n<|endoftext|><|im_start|>user\nComplete input: [0, 1]<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n{\"message\":null,\"submit\":1,\"wait\":false}<|im_end|>\n<|im_start|>user\nComplete input: [0, 1]<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n{\"message\":null,\"submit\":1,\"wait\":false}<|im_end|>\n<|im_start|>user\nComplete input: [0, 1]<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n{\"message\":null,\"submit\":1,\"wait\":false}<|im_end|>\n<|im_start|>user\nComplete input: [0, 1]<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n{\"message\":null,\"submit\":1,\"wait\":false}<|im_end|>\n<|im_start|>user\nComplete input: [0, 1]<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n{\"message\":null,\"submit\":1,\"wait\":false}<|im_end|>\n<|im_start|>user\nComplete input: [0, 1]<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n{\"message\":null,\"submit\":1,\"wait\":false}<|im_end|>\n<|im_start|>user\nComplete input: [0, 1]<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n{\"message\":null,\"submit\":1,\"wait\":false}<|im_end|>\n<|im_start|>user\nComplete input: [0, 1]<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n{\"message\":null,\"submit\":1,\"wait\":false}<|im_end|>\n<|im_start|>user\nComplete input: [0, 1]<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n{\"message\":null,\"submit\":1,\"wait\":false}<|im_end|>\n<|im_start|>user\nComplete input: [0, 1]<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n{\"message\":",
          "ready_seconds": 69.20362282499991,
          "termination": "length",
          "thinking": null,
          "token_ids": [
            4754,
            1927,
            763,
            2827,
            1288,
            5769,
            763,
            16,
            1288,
            11158,
            763,
            3721,
            92,
            248046,
            198,
            248044,
            248045,
            846,
            198,
            12188,
            1879,
            25,
            498,
            15,
            11,
            220,
            16,
            60,
            248046,
            198,
            248045,
            74455,
            198,
            248068,
            271,
            248069,
            271,
            4754,
            1927,
            763,
            2827,
            1288,
            5769,
            763,
            16,
            1288,
            11158,
            763,
            3721,
            92,
            248046,
            198,
            248044,
            248045,
            846,
            198,
            12188,
            1879,
            25,
            498,
            15,
            11,
            220,
            16,
            60,
            248046,
            198,
            248045,
            74455,
            198,
            248068,
            271,
            248069,
            271,
            4754,
            1927,
            763,
            2827,
            1288,
            5769,
            763,
            16,
            1288,
            11158,
            763,
            3721,
            92,
            248046,
            198,
            248044,
            248045,
            846,
            198,
            12188,
            1879,
            25,
            498,
            15,
            11,
            220,
            16,
            60,
            248046,
            198,
            248045,
            74455,
            198,
            248068,
            271,
            248069,
            271,
            4754,
            1927,
            763,
            2827,
            1288,
            5769,
            763,
            16,
            1288,
            11158,
            763,
            3721,
            92,
            248046,
            198,
            248044,
            248045,
            846,
            198,
            12188,
            1879,
            25,
            498,
            15,
            11,
            220,
            16,
            60,
            248046,
            198,
            248045,
            74455,
            198,
            248068,
            271,
            248069,
            271,
            4754,
            1927,
            763,
            2827,
            1288,
            5769,
            763,
            16,
            1288,
            11158,
            763,
            3721,
            92,
            248046,
            198,
            248044,
            248045,
            846,
            198,
            12188,
            1879,
            25,
            498,
            15,
            11,
            220,
            16,
            60,
            248046,
            198,
            248045,
            74455,
            198,
            248068,
            271,
            248069,
            271,
            4754,
            1927,
            763,
            2827,
            1288,
            5769,
            763,
            16,
            1288,
            11158,
            763,
            3721,
            92,
            248046,
            198,
            248045,
            846,
            198,
            12188,
            1879,
            25,
            498,
            15,
            11,
            220,
            16,
            60,
            248046,
            198,
            248045,
            74455,
            198,
            248068,
            271,
            248069,
            271,
            4754,
            1927,
            763,
            2827,
            1288,
            5769,
            763,
            16,
            1288,
            11158,
            763,
            3721,
            92,
            248046,
            198,
            248045,
            846,
            198,
            12188,
            1879,
            25,
            498,
            15,
            11,
            220,
            16,
            60,
            248046,
            198,
            248045,
            74455,
            198,
            248068,
            271,
            248069,
            271,
            4754,
            1927,
            763,
            2827,
            1288,
            5769,
            763,
            16,
            1288,
            11158,
            763,
            3721,
            92,
            248046,
            198,
            248045,
            846,
            198,
            12188,
            1879,
            25,
            498,
            15,
            11,
            220,
            16,
            60,
            248046,
            198,
            248045,
            74455,
            198,
            248068,
            271,
            248069,
            271,
            4754,
            1927,
            763,
            2827,
            1288,
            5769,
            763,
            16,
            1288,
            11158,
            763,
            3721,
            92,
            248046,
            198,
            248045,
            846,
            198,
            12188,
            1879,
            25,
            498,
            15,
            11,
            220,
            16,
            60,
            248046,
            198,
            248045,
            74455,
            198,
            248068,
            271,
            248069,
            271,
            4754,
            1927,
            763,
            2827,
            1288,
            5769,
            763,
            16,
            1288,
            11158,
            763,
            3721,
            92,
            248046,
            198,
            248045,
            846,
            198,
            12188,
            1879,
            25,
            498,
            15,
            11,
            220,
            16,
            60,
            248046,
            198,
            248045,
            74455,
            198,
            248068,
            271,
            248069,
            271,
            4754,
            1927,
            763,
            2827,
            1288,
            5769,
            763,
            16,
            1288,
            11158,
            763,
            3721,
            92,
            248046,
            198,
            248045,
            846,
            198,
            12188,
            1879,
            25,
            498,
            15,
            11,
            220,
            16,
            60,
            248046,
            198,
            248045,
            74455,
            198,
            248068,
            271,
            248069,
            271,
            4754,
            1927,
            763,
            2827,
            1288,
            5769,
            763,
            16,
            1288,
            11158,
            763,
            3721,
            92,
            248046,
            198,
            248045,
            846,
            198,
            12188,
            1879,
            25,
            498,
            15,
            11,
            220,
            16,
            60,
            248046,
            198,
            248045,
            74455,
            198,
            248068,
            271,
            248069,
            271,
            4754,
            1927,
            763,
            2827,
            1288,
            5769,
            763,
            16,
            1288,
            11158,
            763,
            3721,
            92,
            248046,
            198,
            248045,
            846,
            198,
            12188,
            1879,
            25,
            498,
            15,
            11,
            220,
            16,
            60,
            248046,
            198,
            248045,
            74455,
            198,
            248068,
            271,
            248069,
            271,
            4754,
            1927,
            763,
            2827,
            1288,
            5769,
            763,
            16,
            1288,
            11158,
            763,
            3721,
            92,
            248046,
            198,
            248045,
            846,
            198,
            12188,
            1879,
            25,
            498,
            15,
            11,
            220,
            16,
            60,
            248046,
            198,
            248045,
            74455,
            198,
            248068,
            271,
            248069,
            271,
            4754,
            1927,
            763
          ],
          "truncated": true,
          "visible_text": ""
        }
      ],
      "session": "a7bb7845-cf04-4efd-9b68-f74b9595cfaa"
    },
    "selected_mode": "direct",
    "reload_required": false,
    "automatic/pilot-1": {
      "checks": {
        "committed_calls": true,
        "every_episode_has_calls": true,
        "inspectable_checkpoint": true,
        "reconciled_spending": true,
        "runtime_integrity": true,
        "terminal_evidence": true
      },
      "control_protocol_errors": 0,
      "human_review": "retrospective_pending",
      "original_messages": 2,
      "original_team_completed": true,
      "passed": true,
      "pilot": 1,
      "policy": "i01-recorded-outcomes-run-all-2026-10-15",
      "prefix_protocol_errors": 0,
      "protocol_errors": 2,
      "recorded_calls": 12,
      "recovery_protocol_errors": 2,
      "useful_communication": null,
      "validation": [
        {
          "admission_blocking": false,
          "call": "pilot-00/prefix/agent-0/invocation-0",
          "error": null,
          "json_valid": true,
          "legal_action": true,
          "phase": "prefix",
          "reason": null,
          "runtime_safe": true,
          "schema_valid": true
        },
        {
          "admission_blocking": false,
          "call": "pilot-00/prefix/agent-1/invocation-0",
          "error": null,
          "json_valid": true,
          "legal_action": true,
          "phase": "prefix",
          "reason": null,
          "runtime_safe": true,
          "schema_valid": true
        },
        {
          "admission_blocking": false,
          "call": "pilot-00/prefix/agent-0/invocation-1",
          "error": null,
          "json_valid": true,
          "legal_action": true,
          "phase": "prefix",
          "reason": null,
          "runtime_safe": true,
          "schema_valid": true
        },
        {
          "admission_blocking": false,
          "call": "pilot-00/retain/agent-0/invocation-0",
          "error": null,
          "json_valid": true,
          "legal_action": true,
          "phase": "retain",
          "reason": null,
          "runtime_safe": true,
          "schema_valid": true
        },
        {
          "admission_blocking": false,
          "call": "pilot-00/retain/agent-1/invocation-0",
          "error": "malformed_action",
          "json_valid": true,
          "legal_action": false,
          "phase": "retain",
          "reason": "wait_requires_null_message_and_submit",
          "runtime_safe": true,
          "schema_valid": true
        },
        {
          "admission_blocking": false,
          "call": "pilot-00/retain/agent-1/invocation-1",
          "error": null,
          "json_valid": true,
          "legal_action": true,
          "phase": "retain",
          "reason": null,
          "runtime_safe": true,
          "schema_valid": true
        },
        {
          "admission_blocking": false,
          "call": "pilot-00/retain/agent-1/invocation-2",
          "error": null,
          "json_valid": true,
          "legal_action": true,
          "phase": "retain",
          "reason": null,
          "runtime_safe": true,
          "schema_valid": true
        },
        {
          "admission_blocking": false,
          "call": "pilot-00/clear/agent-0/invocation-0",
          "error": "malformed_action",
          "json_valid": true,
          "legal_action": false,
          "phase": "clear",
          "reason": "wait_requires_null_message_and_submit",
          "runtime_safe": true,
          "schema_valid": true
        },
        {
          "admission_blocking": false,
          "call": "pilot-00/clear/agent-1/invocation-0",
          "error": null,
          "json_valid": true,
          "legal_action": true,
          "phase": "clear",
          "reason": null,
          "runtime_safe": true,
          "schema_valid": true
        },
        {
          "admission_blocking": false,
          "call": "pilot-00/clear/agent-0/invocation-1",
          "error": null,
          "json_valid": true,
          "legal_action": true,
          "phase": "clear",
          "reason": null,
          "runtime_safe": true,
          "schema_valid": true
        },
        {
          "admission_blocking": false,
          "call": "pilot-00/control-original-direct",
          "error": null,
          "json_valid": true,
          "legal_action": true,
          "phase": "control-original-direct",
          "reason": null,
          "runtime_safe": true,
          "schema_valid": true
        },
        {
          "admission_blocking": false,
          "call": "pilot-00/control-revised-direct",
          "error": null,
          "json_valid": true,
          "legal_action": true,
          "phase": "control-revised-direct",
          "reason": null,
          "runtime_safe": true,
          "schema_valid": true
        }
      ],
      "world": "pilot-00"
    },
    "automatic/pilot-2": {
      "checks": {
        "committed_calls": true,
        "every_episode_has_calls": true,
        "inspectable_checkpoint": true,
        "reconciled_spending": true,
        "runtime_integrity": true,
        "terminal_evidence": true
      },
      "control_protocol_errors": 0,
      "human_review": "retrospective_pending",
      "original_messages": 1,
      "original_team_completed": true,
      "passed": true,
      "pilot": 2,
      "policy": "i01-recorded-outcomes-run-all-2026-10-15",
      "prefix_protocol_errors": 1,
      "protocol_errors": 2,
      "recorded_calls": 11,
      "recovery_protocol_errors": 1,
      "useful_communication": null,
      "validation": [
        {
          "admission_blocking": false,
          "call": "pilot-01/prefix/agent-0/invocation-0",
          "error": null,
          "json_valid": true,
          "legal_action": true,
          "phase": "prefix",
          "reason": null,
          "runtime_safe": true,
          "schema_valid": true
        },
        {
          "admission_blocking": false,
          "call": "pilot-01/prefix/agent-1/invocation-0",
          "error": "malformed_action",
          "json_valid": true,
          "legal_action": false,
          "phase": "prefix",
          "reason": "wait_requires_null_message_and_submit",
          "runtime_safe": true,
          "schema_valid": true
        },
        {
          "admission_blocking": false,
          "call": "pilot-01/prefix/agent-1/invocation-1",
          "error": null,
          "json_valid": true,
          "legal_action": true,
          "phase": "prefix",
          "reason": null,
          "runtime_safe": true,
          "schema_valid": true
        },
        {
          "admission_blocking": false,
          "call": "pilot-01/prefix/agent-0/invocation-1",
          "error": null,
          "json_valid": true,
          "legal_action": true,
          "phase": "prefix",
          "reason": null,
          "runtime_safe": true,
          "schema_valid": true
        },
        {
          "admission_blocking": false,
          "call": "pilot-01/clear/agent-0/invocation-0",
          "error": "malformed_action",
          "json_valid": true,
          "legal_action": false,
          "phase": "clear",
          "reason": "wait_requires_null_message_and_submit",
          "runtime_safe": true,
          "schema_valid": true
        },
        {
          "admission_blocking": false,
          "call": "pilot-01/clear/agent-1/invocation-0",
          "error": null,
          "json_valid": true,
          "legal_action": true,
          "phase": "clear",
          "reason": null,
          "runtime_safe": true,
          "schema_valid": true
        },
        {
          "admission_blocking": false,
          "call": "pilot-01/clear/agent-0/invocation-1",
          "error": null,
          "json_valid": true,
          "legal_action": true,
          "phase": "clear",
          "reason": null,
          "runtime_safe": true,
          "schema_valid": true
        },
        {
          "admission_blocking": false,
          "call": "pilot-01/retain/agent-0/invocation-0",
          "error": null,
          "json_valid": true,
          "legal_action": true,
          "phase": "retain",
          "reason": null,
          "runtime_safe": true,
          "schema_valid": true
        },
        {
          "admission_blocking": false,
          "call": "pilot-01/retain/agent-1/invocation-0",
          "error": null,
          "json_valid": true,
          "legal_action": true,
          "phase": "retain",
          "reason": null,
          "runtime_safe": true,
          "schema_valid": true
        },
        {
          "admission_blocking": false,
          "call": "pilot-01/control-original-direct",
          "error": null,
          "json_valid": true,
          "legal_action": true,
          "phase": "control-original-direct",
          "reason": null,
          "runtime_safe": true,
          "schema_valid": true
        },
        {
          "admission_blocking": false,
          "call": "pilot-01/control-revised-direct",
          "error": null,
          "json_valid": true,
          "legal_action": true,
          "phase": "control-revised-direct",
          "reason": null,
          "runtime_safe": true,
          "schema_valid": true
        }
      ],
      "world": "pilot-01"
    },
    "automatic/pilot-3": {
      "checks": {
        "committed_calls": true,
        "every_episode_has_calls": true,
        "inspectable_checkpoint": true,
        "reconciled_spending": true,
        "runtime_integrity": true,
        "terminal_evidence": true
      },
      "control_protocol_errors": 0,
      "human_review": "retrospective_pending",
      "original_messages": 2,
      "original_team_completed": true,
      "passed": true,
      "pilot": 3,
      "policy": "i01-recorded-outcomes-run-all-2026-10-15",
      "prefix_protocol_errors": 3,
      "protocol_errors": 3,
      "recorded_calls": 12,
      "recovery_protocol_errors": 0,
      "useful_communication": null,
      "validation": [
        {
          "admission_blocking": false,
          "call": "pilot-02/prefix/agent-1/invocation-0",
          "error": "malformed_action",
          "json_valid": true,
          "legal_action": false,
          "phase": "prefix",
          "reason": "wait_requires_null_message_and_submit",
          "runtime_safe": true,
          "schema_valid": true
        },
        {
          "admission_blocking": false,
          "call": "pilot-02/prefix/agent-0/invocation-0",
          "error": "malformed_action",
          "json_valid": true,
          "legal_action": false,
          "phase": "prefix",
          "reason": "wait_requires_null_message_and_submit",
          "runtime_safe": true,
          "schema_valid": true
        },
        {
          "admission_blocking": false,
          "call": "pilot-02/prefix/agent-1/invocation-1",
          "error": "malformed_action",
          "json_valid": true,
          "legal_action": false,
          "phase": "prefix",
          "reason": "wait_requires_null_message_and_submit",
          "runtime_safe": true,
          "schema_valid": true
        },
        {
          "admission_blocking": false,
          "call": "pilot-02/prefix/agent-0/invocation-1",
          "error": null,
          "json_valid": true,
          "legal_action": true,
          "phase": "prefix",
          "reason": null,
          "runtime_safe": true,
          "schema_valid": true
        },
        {
          "admission_blocking": false,
          "call": "pilot-02/prefix/agent-1/invocation-2",
          "error": null,
          "json_valid": true,
          "legal_action": true,
          "phase": "prefix",
          "reason": null,
          "runtime_safe": true,
          "schema_valid": true
        },
        {
          "admission_blocking": false,
          "call": "pilot-02/retain/agent-1/invocation-0",
          "error": null,
          "json_valid": true,
          "legal_action": true,
          "phase": "retain",
          "reason": null,
          "runtime_safe": true,
          "schema_valid": true
        },
        {
          "admission_blocking": false,
          "call": "pilot-02/retain/agent-0/invocation-0",
          "error": null,
          "json_valid": true,
          "legal_action": true,
          "phase": "retain",
          "reason": null,
          "runtime_safe": true,
          "schema_valid": true
        },
        {
          "admission_blocking": false,
          "call": "pilot-02/retain/agent-1/invocation-1",
          "error": null,
          "json_valid": true,
          "legal_action": true,
          "phase": "retain",
          "reason": null,
          "runtime_safe": true,
          "schema_valid": true
        },
        {
          "admission_blocking": false,
          "call": "pilot-02/clear/agent-1/invocation-0",
          "error": null,
          "json_valid": true,
          "legal_action": true,
          "phase": "clear",
          "reason": null,
          "runtime_safe": true,
          "schema_valid": true
        },
        {
          "admission_blocking": false,
          "call": "pilot-02/clear/agent-0/invocation-0",
          "error": null,
          "json_valid": true,
          "legal_action": true,
          "phase": "clear",
          "reason": null,
          "runtime_safe": true,
          "schema_valid": true
        },
        {
          "admission_blocking": false,
          "call": "pilot-02/control-original-direct",
          "error": null,
          "json_valid": true,
          "legal_action": true,
          "phase": "control-original-direct",
          "reason": null,
          "runtime_safe": true,
          "schema_valid": true
        },
        {
          "admission_blocking": false,
          "call": "pilot-02/control-revised-direct",
          "error": null,
          "json_valid": true,
          "legal_action": true,
          "phase": "control-revised-direct",
          "reason": null,
          "runtime_safe": true,
          "schema_valid": true
        }
      ],
      "world": "pilot-02"
    },
    "freeze": {
      "at": "2026-10-15T17:57:54.267336+00:00",
      "execution_policy": "i01-recorded-outcomes-run-all-2026-10-15",
      "forecast": {
        "caveat": "Observed maximum with 25% margin is a forecast, not a runtime guarantee; two allocated GPUs also consume idle time.",
        "conservative_wall_seconds": 12549.959422824908,
        "estimated_checkpoint_overhead_seconds": 265.35725439599537,
        "estimated_remaining_exports": 76,
        "forecast_scope": "main_only; not a whole-session completion guarantee",
        "includes_idle_inspection": false,
        "measured_checkpoint_seconds": 3.491542820999939,
        "observed_max_ready_seconds": 22.168335626999806,
        "remaining_attempt_allowance": 445,
        "remaining_pilot_first_attempts": 0,
        "remaining_pilots": 0,
        "remaining_session_seconds": 40973.132483,
        "session_observation": {
          "at": "2026-10-15T17:40:47.399455+00:00",
          "basis": "planning_estimate",
          "remaining_minutes": 700
        },
        "timeout_worst_case_seconds": 68520,
        "whole_forecast_basis": "remaining pilot/main calls, observed maximum +25% and 5s/call, observed export maximum; heuristic, excludes setup/load and abnormal tails",
        "whole_remaining_wall_seconds": 12815.316677220904,
        "worst_remaining_first_attempts": 380
      },
      "human_review": "retrospective_pending",
      "implementation_transition": null,
      "manifest": {
        "config": {
          "agents": 2,
          "attempt_limit": 500,
          "bootstrap_confidence": 0.95,
          "bootstrap_draws": 10000,
          "bootstrap_seed": 2026101402,
          "checkpoint_seconds": 300,
          "contingency_limit": 28,
          "direct_output_tokens": 512,
          "direct_timeout_seconds": 180,
          "export_reserve_seconds": 120,
          "feedback_tokens": 32,
          "headroom_bytes": 1610612736,
          "historical_attempts_separate": 45,
          "input_tokens": 8192,
          "load_timeout_seconds": 600,
          "main_worlds": 20,
          "master_seed": 2026101401,
          "max_proposals": 1000,
          "model": "Qwen/Qwen3.5-9B",
          "pilot_worlds": 3,
          "qualification_worlds": 6,
          "regime": "i01-course-v1",
          "revision": "c202236235762e1c871ad0ccb60c8ee5ba337b9a",
          "rubric": [
            "wrong_submission",
            "noncompletion",
            "premature_finalization",
            "obsolete_value_repeated",
            "malformed_action",
            "truncated_action",
            "waiting_deadlock",
            "horizon_exhausted",
            "provider_failure",
            "ambiguous"
          ],
          "schema": 1,
          "shard_size": 20,
          "termination_seconds": 5,
          "thinking_output_tokens": 4096,
          "thinking_timeout_seconds": 900,
          "turns_per_agent": 3,
          "visible_output_tokens": 512
        },
        "created_at": "2026-10-15T17:44:38.664054+00:00",
        "direct_first_attempts": 460,
        "historical_attempts_separate": 45,
        "planned_first_attempts": 472,
        "regime": "i01-course-v1",
        "source_identity": {
          "configs/i01-course.json": "89e91b0e69f8f0851083e5016020b30c1d0b635dc5a00f142f9955bdd60c9a23",
          "configs/i01-runtime.lock": "5b1d91aa431a39ff725cfe4314706fe7a854af85a6e3ea492dd22d8c68d9bc56",
          "pyproject.toml": "d851f00351b3221aef8c92b5757aecf477f2942b03afbfb6925190220b1494b1",
          "recovery/__init__.py": "b11591ab36164605ffe2de304b0503780e6b2c340b2c466e51b9c132dae0d738",
          "recovery/__main__.py": "a32e2fa488314eae101a42fb5520951565d7ab5f5c9f36aa4feeac88c529325a",
          "recovery/accounting.py": "4b910adf52a7583550fc60d8a201671e2a13d125cd4bfe67588acb85df3315d1",
          "recovery/analysis.py": "3740e341f07dfd3884363cf24935bdbf3b93de49e99b31b2b935928b46aa9e22",
          "recovery/attempts.py": "bac975625c7da55d5abcd4d2d75ba6ad91bb1cdd5b23028ff90794c84e502eb4",
          "recovery/costs.py": "6e2f8358177c00313b1f71fb755ec3bbb1b522d38e60ad22fabe8aec939bf82b",
          "recovery/edits.py": "bc378e9c65bb6abe243416b20b54be8a59eadb15fe2b70c2c4ce46527ab064fc",
          "recovery/evaluate.py": "2beb6d6f14ad10c7f474208ed66e9cca76b9ebb2880c7201ff351491884e1ec8",
          "recovery/events.py": "500ad12f8d68ee760e4fa2b2108089119f281b8d98db83113abe3e4a067d6704",
          "recovery/figures.py": "fab52110727c3dc9b8ed3e1da3a015fb1a437119e560be64cd36499b39c285c9",
          "recovery/i01/__init__.py": "b5fdf1bece3e01a5ab794227e5c278e3b8cf979ff5e27fce0d7ca953151a7e41",
          "recovery/i01/archive.py": "836a5d1cf5296eccbcb72f2f40e9b2e37d549307ca164a5479b9741623c65697",
          "recovery/i01/checks.py": "926d90992c64ffa5f1ffe48fad1bb3b6a46e5635bbe56305c0ab9e4e26dd9283",
          "recovery/i01/cli.py": "48e9b8ae4bbf4bc8101ec652dc56761b4af44f85c3ea93960a094651eb5daf21",
          "recovery/i01/client.py": "fbc6b2a31f63932831d55990479be2e69a3eb0ebe808cb1af4a150a2817f90b4",
          "recovery/i01/continuation.py": "d077353ed7a41c99b0b4140308ed2ee0e716e514c3934d09a389d45e47d25b70",
          "recovery/i01/core.py": "ce442f3f5505fc60e0b8791317e3f5db4d4c50cb5e670b0b7052cf6db2c20a88",
          "recovery/i01/inference.py": "7b3f04e683d15ed58d3d0135db281abb6425c5334a0765c49ace2fb70edf7588",
          "recovery/i01/notebook.py": "450f34e1c57efd6deb5914f6e4f3fc755cd2d4512c0e9915fb77c548cf238988",
          "recovery/i01/policy.py": "1306578cc76a8cff962cd06137a0fd4b06c73d93d06c8ca3f787241f98847e32",
          "recovery/i01/process.py": "17314150320b97c8d07edd3262d117db1f59c6b1c41728f48a45434cffe24fb0",
          "recovery/i01/report.py": "9d9043a4e643385112998223d34ea3db4b6162031de9df48d1e75db0b4ccfec3",
          "recovery/i01/runtime.py": "39fb2de57d5401c0ad553e4dd0da78159442f39bd3f281dacfa464ee0c2ed09b",
          "recovery/i01/setup.py": "f75ecb3083b9826b525c4b21c32e0ecc4e962ccb94fb158c62d9c694a3169c56",
          "recovery/i01/store.py": "14c28a627c42d9083b65f5df9aef002b7338a7126917392bdb36e20908efb092",
          "recovery/i01/ui.py": "1768e81bce4ac9232fb7d3a38f994d5a7cae3f06a93daeebbdc2e700442ee00f",
          "recovery/i01/workflow.py": "5d0252d2b2bfe2d0cfd40d8868f22119f7cdec09931904bd770ff5748fa0e8d7",
          "recovery/inference.py": "561386a74cc951a24cc08457665d71ee77d0075aca1794a5946d6d7fe52ee026",
          "recovery/information.py": "9c8bf958955b60e73ac26ac565831cee5e45e8e52f4244e88b43345e46c1df19",
          "recovery/manifests.py": "f6157e9f945b5f185ad5dde079e5b5e902665b644b9b9ba3a58936cdfa895b82",
          "recovery/populations.py": "808c4f29a0b7cb90574d040d9f49e402291a6eadd2bacc2141f50cf97fba05c7",
          "recovery/prompts.py": "a3cefd5d802cef08233a7b404cfd01f328dd3469db7d23857db25aadefd45cdc",
          "recovery/protocol.py": "e12de998036f40cac1f0d5dbfb5a293785bbf6ce6239f3cc11784c894fd7f3cf",
          "recovery/replay.py": "36e8be2946aadd71666c697b794d76f3c58b696bedc27a4408e32063bbb55840",
          "recovery/report.py": "6c37e92c9c338f7901fb0bda7fe6d2ea79fa998af3b33356e4b33c69d4df9fd3",
          "recovery/rounds.py": "2c59648c4cc8d720d1c510f27e663165ab2654d9044c57e222323664a2f631bf",
          "recovery/runner.py": "8723cf0c11b7988900275118d0565645f0585647274269a3e343206664d43b8a",
          "recovery/schedule.py": "396d8322e28ef1031803322f94f501be7fd778f69c0489854f78c228e87354d6",
          "recovery/state.py": "acf99320366e55c18778b4a4836003dfeb820abd77bc314172c3d538d35d4276",
          "recovery/storage.py": "e688428c2f07dcba28d928dcfbc163920ac6eeec37d15801d623dca35810a0d3",
          "recovery/t4_attention.py": "b5f7e9b8e7a7f4fe0193c31628d907f1476812983e3178beb20c297b7d172ee8",
          "recovery/tasks.py": "59d80c0e47c005af082626253ec86b6f3fc56be0dc57bad0369d1a263ba7e9a4",
          "recovery/truth.py": "bfc51e6da767258fc3e27a516b7fd44b48bb58f61f8fde73ccbb7ff51e9c8b2c",
          "recovery/uncertainty.py": "8cfbb1a89110a07536b8937b9248851ed0fbcea963d6950cd290a550e8036dad",
          "recovery/witness.py": "15e25c69e44da2ac2eccae2032c7ecce4bd33a033d91e4acc76ec1f79d0e523b",
          "recovery/workers.py": "300c06a6b30de089ef71e7c8dcf74a433d99b62e206a234e208aeefe9eb832a9"
        },
        "study_id": "b709c9bd-8d95-40c6-a19e-62a5f5e3c587",
        "worlds": [
          {
            "after": -551,
            "before": 950,
            "control_seeds": {
              "original": 7034365729602933730,
              "revised": 6470821694236683869
            },
            "device": 0,
            "first": 0,
            "group": "qualification",
            "id": "qualification-00",
            "index": 0,
            "original": [
              [
                -189,
                93,
                -801,
                703,
                257,
                888,
                -442,
                508,
                104,
                569,
                156,
                -943,
                950,
                -380,
                714,
                -695,
                619,
                284,
                642,
                -143
              ],
              [
                -578,
                487,
                -581,
                787,
                -324,
                -909,
                -27,
                478,
                611,
                -23,
                259,
                78,
                46,
                -354,
                921,
                185,
                896,
                -172,
                -499,
                24
              ]
            ],
            "original_truth": 950,
            "owner": 0,
            "proposals": 5,
            "rejections": {
              "nonunique_maximum": 0,
              "owner_block": 4,
              "remaining_at_floor": 0
            },
            "revised": [
              [
                -189,
                93,
                -801,
                703,
                257,
                888,
                -442,
                508,
                104,
                569,
                156,
                -943,
                -551,
                -380,
                714,
                -695,
                619,
                284,
                642,
                -143
              ],
              [
                -578,
                487,
                -581,
                787,
                -324,
                -909,
                -27,
                478,
                611,
                -23,
                259,
                78,
                46,
                -354,
                921,
                185,
                896,
                -172,
                -499,
                24
              ]
            ],
            "revised_truth": 921,
            "row": 12,
            "seeds": {
              "prefix": [
                [
                  4482506065534555318,
                  412927343023830623,
                  2109148965411192606
                ],
                [
                  4385276486813606184,
                  6912345805180829586,
                  3455170723590595527
                ]
              ],
              "recovery": [
                [
                  6526188895888695232,
                  6571403304274566053,
                  1954062805293530039
                ],
                [
                  1359658016784884329,
                  3243757618503762265,
                  4201019103053384133
                ]
              ]
            },
            "treatments": [
              "retain",
              "clear"
            ]
          },
          {
            "after": -81,
            "before": 999,
            "control_seeds": {
              "original": 5667570157035812265,
              "revised": 1898883763934146872
            },
            "device": 1,
            "first": 0,
            "group": "qualification",
            "id": "qualification-01",
            "index": 1,
            "original": [
              [
                416,
                -90,
                -164,
                608,
                -266,
                579,
                279,
                -562,
                -678,
                577,
                693,
                -648,
                -766,
                145,
                -320,
                -408,
                696,
                -65,
                -302,
                -208
              ],
              [
                573,
                582,
                931,
                56,
                731,
                918,
                415,
                566,
                704,
                557,
                864,
                -288,
                845,
                999,
                -639,
                654,
                -643,
                -297,
                818,
                -968
              ]
            ],
            "original_truth": 999,
            "owner": 1,
            "proposals": 1,
            "rejections": {
              "nonunique_maximum": 0,
              "owner_block": 0,
              "remaining_at_floor": 0
            },
            "revised": [
              [
                416,
                -90,
                -164,
                608,
                -266,
                579,
                279,
                -562,
                -678,
                577,
                693,
                -648,
                -766,
                145,
                -320,
                -408,
                696,
                -65,
                -302,
                -208
              ],
              [
                573,
                582,
                931,
                56,
                731,
                918,
                415,
                566,
                704,
                557,
                864,
                -288,
                845,
                -81,
                -639,
                654,
                -643,
                -297,
                818,
                -968
              ]
            ],
            "revised_truth": 931,
            "row": 13,
            "seeds": {
              "prefix": [
                [
                  365357283853728219,
                  6184368565983629280,
                  6573458992883911497
                ],
                [
                  8824162750632232244,
                  1963080267908642730,
                  8008088415356868384
                ]
              ],
              "recovery": [
                [
                  3371633447917534772,
                  2459147922575136351,
                  737103979760305227
                ],
                [
                  398948568915266817,
                  1845177985900587717,
                  8709297716995974328
                ]
              ]
            },
            "treatments": [
              "clear",
              "retain"
            ]
          },
          {
            "after": 851,
            "before": 1000,
            "control_seeds": {
              "original": 2474994583072236036,
              "revised": 6776502664314749800
            },
            "device": 0,
            "first": 1,
            "group": "qualification",
            "id": "qualification-02",
            "index": 2,
            "original": [
              [
                413,
                756,
                -172,
                1000,
                669,
                711,
                974,
                -532,
                65,
                832,
                -817,
                -770,
                -660,
                163,
                671,
                -1,
                -94,
                -130,
                451,
                -350
              ],
              [
                -753,
                739,
                -915,
                -994,
                501,
                -783,
                347,
                -742,
                535,
                228,
                -937,
                -747,
                -565,
                -367,
                981,
                -174,
                -887,
                714,
                327,
                -67
              ]
            ],
            "original_truth": 1000,
            "owner": 0,
            "proposals": 1,
            "rejections": {
              "nonunique_maximum": 0,
              "owner_block": 0,
              "remaining_at_floor": 0
            },
            "revised": [
              [
                413,
                756,
                -172,
                851,
                669,
                711,
                974,
                -532,
                65,
                832,
                -817,
                -770,
                -660,
                163,
                671,
                -1,
                -94,
                -130,
                451,
                -350
              ],
              [
                -753,
                739,
                -915,
                -994,
                501,
                -783,
                347,
                -742,
                535,
                228,
                -937,
                -747,
                -565,
                -367,
                981,
                -174,
                -887,
                714,
                327,
                -67
              ]
            ],
            "revised_truth": 981,
            "row": 3,
            "seeds": {
              "prefix": [
                [
                  2725852844225677593,
                  343399023915924421,
                  6513937643200348787
                ],
                [
                  332949247850107498,
                  9223309259806105505,
                  8493465789884601367
                ]
              ],
              "recovery": [
                [
                  5991453042001611951,
                  405237326680081307,
                  3605784421770664104
                ],
                [
                  7171198284295607958,
                  1357884721838184654,
                  583911871428831293
                ]
              ]
            },
            "treatments": [
              "retain",
              "clear"
            ]
          },
          {
            "after": -801,
            "before": 951,
            "control_seeds": {
              "original": 367958775560601292,
              "revised": 6417685603553177256
            },
            "device": 1,
            "first": 1,
            "group": "qualification",
            "id": "qualification-03",
            "index": 3,
            "original": [
              [
                231,
                -122,
                -551,
                -958,
                -149,
                -438,
                -273,
                -439,
                719,
                -881,
                -215,
                652,
                49,
                -40,
                -600,
                -929,
                340,
                -855,
                -862,
                -74
              ],
              [
                -376,
                -238,
                630,
                -897,
                674,
                920,
                266,
                788,
                92,
                815,
                290,
                -807,
                951,
                315,
                211,
                -348,
                587,
                188,
                -594,
                -554
              ]
            ],
            "original_truth": 951,
            "owner": 1,
            "proposals": 4,
            "rejections": {
              "nonunique_maximum": 0,
              "owner_block": 3,
              "remaining_at_floor": 0
            },
            "revised": [
              [
                231,
                -122,
                -551,
                -958,
                -149,
                -438,
                -273,
                -439,
                719,
                -881,
                -215,
                652,
                49,
                -40,
                -600,
                -929,
                340,
                -855,
                -862,
                -74
              ],
              [
                -376,
                -238,
                630,
                -897,
                674,
                920,
                266,
                788,
                92,
                815,
                290,
                -807,
                -801,
                315,
                211,
                -348,
                587,
                188,
                -594,
                -554
              ]
            ],
            "revised_truth": 920,
            "row": 12,
            "seeds": {
              "prefix": [
                [
                  5842624249297478730,
                  7547121839162710815,
                  1352492997533588836
                ],
                [
                  1344439115857738985,
                  1079843083168087572,
                  7617097022874114035
                ]
              ],
              "recovery": [
                [
                  8108280748331842908,
                  8437003048688256050,
                  6133085469547552948
                ],
                [
                  6103782264426076364,
                  1751848125169274649,
                  8431676853465120181
                ]
              ]
            },
            "treatments": [
              "clear",
              "retain"
            ]
          },
          {
            "after": 421,
            "before": 956,
            "control_seeds": {
              "original": 8507201115962376320,
              "revised": 6694793944570056551
            },
            "device": 0,
            "first": 0,
            "group": "qualification",
            "id": "qualification-04",
            "index": 4,
            "original": [
              [
                608,
                918,
                -461,
                408,
                37,
                -184,
                -421,
                -751,
                727,
                891,
                -595,
                -6,
                -4,
                -982,
                409,
                470,
                673,
                626,
                956,
                -330
              ],
              [
                -33,
                376,
                891,
                -805,
                458,
                -12,
                -22,
                -871,
                623,
                -826,
                -877,
                713,
                301,
                -820,
                -919,
                572,
                740,
                715,
                -282,
                24
              ]
            ],
            "original_truth": 956,
            "owner": 0,
            "proposals": 1,
            "rejections": {
              "nonunique_maximum": 0,
              "owner_block": 0,
              "remaining_at_floor": 0
            },
            "revised": [
              [
                608,
                918,
                -461,
                408,
                37,
                -184,
                -421,
                -751,
                727,
                891,
                -595,
                -6,
                -4,
                -982,
                409,
                470,
                673,
                626,
                421,
                -330
              ],
              [
                -33,
                376,
                891,
                -805,
                458,
                -12,
                -22,
                -871,
                623,
                -826,
                -877,
                713,
                301,
                -820,
                -919,
                572,
                740,
                715,
                -282,
                24
              ]
            ],
            "revised_truth": 918,
            "row": 18,
            "seeds": {
              "prefix": [
                [
                  3295759024446938111,
                  5349855107132709397,
                  2576173335502911682
                ],
                [
                  2918184825410101474,
                  4771007641962023599,
                  5074997840835365104
                ]
              ],
              "recovery": [
                [
                  2102144469767209590,
                  2320326146230977479,
                  1195334323631400666
                ],
                [
                  5418334346809178747,
                  2451041410674132400,
                  4624696849032298719
                ]
              ]
            },
            "treatments": [
              "retain",
              "clear"
            ]
          },
          {
            "after": -70,
            "before": 992,
            "control_seeds": {
              "original": 8287168954115719378,
              "revised": 7213998243262002842
            },
            "device": 1,
            "first": 0,
            "group": "qualification",
            "id": "qualification-05",
            "index": 5,
            "original": [
              [
                -86,
                313,
                -619,
                -204,
                -514,
                306,
                -908,
                -440,
                -834,
                -644,
                -715,
                -497,
                312,
                -735,
                117,
                -715,
                718,
                -909,
                -150,
                332
              ],
              [
                704,
                451,
                -239,
                -93,
                316,
                -503,
                888,
                -143,
                902,
                -244,
                -574,
                -447,
                987,
                631,
                -325,
                221,
                992,
                -307,
                313,
                557
              ]
            ],
            "original_truth": 992,
            "owner": 1,
            "proposals": 3,
            "rejections": {
              "nonunique_maximum": 0,
              "owner_block": 2,
              "remaining_at_floor": 0
            },
            "revised": [
              [
                -86,
                313,
                -619,
                -204,
                -514,
                306,
                -908,
                -440,
                -834,
                -644,
                -715,
                -497,
                312,
                -735,
                117,
                -715,
                718,
                -909,
                -150,
                332
              ],
              [
                704,
                451,
                -239,
                -93,
                316,
                -503,
                888,
                -143,
                902,
                -244,
                -574,
                -447,
                987,
                631,
                -325,
                221,
                -70,
                -307,
                313,
                557
              ]
            ],
            "revised_truth": 987,
            "row": 16,
            "seeds": {
              "prefix": [
                [
                  2597585026013381622,
                  4370624990697627220,
                  5244815374157118196
                ],
                [
                  1219403910651976828,
                  3049850324603457136,
                  6156949131002834945
                ]
              ],
              "recovery": [
                [
                  7272918335240750646,
                  7216275556166713247,
                  9040793799429680484
                ],
                [
                  7887485458797552039,
                  7482477457175227765,
                  1533108740253534760
                ]
              ]
            },
            "treatments": [
              "clear",
              "retain"
            ]
          },
          {
            "after": 672,
            "before": 988,
            "control_seeds": {
              "original": 7202948235205110027,
              "revised": 2712785873405090662
            },
            "device": 0,
            "first": 0,
            "group": "pilot",
            "id": "pilot-00",
            "index": 0,
            "original": [
              [
                932,
                -841,
                161,
                698,
                568,
                784,
                698,
                16,
                845,
                -978,
                685,
                -334,
                2,
                872,
                906,
                988,
                678,
                -336,
                -925,
                821
              ],
              [
                613,
                411,
                599,
                491,
                291,
                -96,
                220,
                261,
                -323,
                923,
                500,
                102,
                -976,
                224,
                -688,
                -23,
                -796,
                -962,
                -521,
                -918
              ]
            ],
            "original_truth": 988,
            "owner": 0,
            "proposals": 2,
            "rejections": {
              "nonunique_maximum": 0,
              "owner_block": 1,
              "remaining_at_floor": 0
            },
            "revised": [
              [
                932,
                -841,
                161,
                698,
                568,
                784,
                698,
                16,
                845,
                -978,
                685,
                -334,
                2,
                872,
                906,
                672,
                678,
                -336,
                -925,
                821
              ],
              [
                613,
                411,
                599,
                491,
                291,
                -96,
                220,
                261,
                -323,
                923,
                500,
                102,
                -976,
                224,
                -688,
                -23,
                -796,
                -962,
                -521,
                -918
              ]
            ],
            "revised_truth": 932,
            "row": 15,
            "seeds": {
              "prefix": [
                [
                  4862200359885706185,
                  1023110753385749315,
                  2736320403664395003
                ],
                [
                  5241200695438049338,
                  7358009148274838779,
                  1407075676669500463
                ]
              ],
              "recovery": [
                [
                  3347234689565640300,
                  7926385093500598411,
                  567848943222847789
                ],
                [
                  7951545925196133279,
                  9068172075070223439,
                  4242985494088566540
                ]
              ]
            },
            "treatments": [
              "retain",
              "clear"
            ]
          },
          {
            "after": 25,
            "before": 985,
            "control_seeds": {
              "original": 2432397541971568865,
              "revised": 4564994103806736101
            },
            "device": 1,
            "first": 0,
            "group": "pilot",
            "id": "pilot-01",
            "index": 1,
            "original": [
              [
                634,
                813,
                664,
                -820,
                738,
                71,
                590,
                536,
                92,
                502,
                -192,
                116,
                -767,
                -42,
                -464,
                -547,
                -690,
                169,
                -567,
                -156
              ],
              [
                497,
                966,
                -234,
                36,
                849,
                815,
                -663,
                -6,
                -768,
                34,
                -430,
                328,
                -282,
                -891,
                740,
                985,
                -998,
                -348,
                150,
                -746
              ]
            ],
            "original_truth": 985,
            "owner": 1,
            "proposals": 1,
            "rejections": {
              "nonunique_maximum": 0,
              "owner_block": 0,
              "remaining_at_floor": 0
            },
            "revised": [
              [
                634,
                813,
                664,
                -820,
                738,
                71,
                590,
                536,
                92,
                502,
                -192,
                116,
                -767,
                -42,
                -464,
                -547,
                -690,
                169,
                -567,
                -156
              ],
              [
                497,
                966,
                -234,
                36,
                849,
                815,
                -663,
                -6,
                -768,
                34,
                -430,
                328,
                -282,
                -891,
                740,
                25,
                -998,
                -348,
                150,
                -746
              ]
            ],
            "revised_truth": 966,
            "row": 15,
            "seeds": {
              "prefix": [
                [
                  6068910610471527175,
                  5109202408067130647,
                  4110699780713550369
                ],
                [
                  8024261074218990468,
                  7684684620624210612,
                  4404566881294605269
                ]
              ],
              "recovery": [
                [
                  3259302922276671101,
                  5227453265228557459,
                  3465729064646047018
                ],
                [
                  657496878342466428,
                  3727060405587847742,
                  1396722624471132836
                ]
              ]
            },
            "treatments": [
              "clear",
              "retain"
            ]
          },
          {
            "after": -481,
            "before": 981,
            "control_seeds": {
              "original": 8384168939389075560,
              "revised": 6801689851870198115
            },
            "device": 0,
            "first": 1,
            "group": "pilot",
            "id": "pilot-02",
            "index": 2,
            "original": [
              [
                -367,
                552,
                478,
                -49,
                -696,
                84,
                647,
                -869,
                -417,
                981,
                -904,
                -101,
                484,
                173,
                34,
                -618,
                76,
                -127,
                302,
                -659
              ],
              [
                201,
                -369,
                911,
                670,
                23,
                876,
                627,
                -251,
                393,
                -788,
                -196,
                97,
                -678,
                -916,
                338,
                -974,
                524,
                -241,
                -71,
                -995
              ]
            ],
            "original_truth": 981,
            "owner": 0,
            "proposals": 1,
            "rejections": {
              "nonunique_maximum": 0,
              "owner_block": 0,
              "remaining_at_floor": 0
            },
            "revised": [
              [
                -367,
                552,
                478,
                -49,
                -696,
                84,
                647,
                -869,
                -417,
                -481,
                -904,
                -101,
                484,
                173,
                34,
                -618,
                76,
                -127,
                302,
                -659
              ],
              [
                201,
                -369,
                911,
                670,
                23,
                876,
                627,
                -251,
                393,
                -788,
                -196,
                97,
                -678,
                -916,
                338,
                -974,
                524,
                -241,
                -71,
                -995
              ]
            ],
            "revised_truth": 911,
            "row": 9,
            "seeds": {
              "prefix": [
                [
                  7049442019502801809,
                  6836940397847036542,
                  8179466357591922044
                ],
                [
                  4114484684654210243,
                  1303939391147026415,
                  3202899689243768497
                ]
              ],
              "recovery": [
                [
                  4792976250752518887,
                  3333023835528811287,
                  6692826379925589624
                ],
                [
                  8763162528738937420,
                  8536876883942813207,
                  6687515527582378326
                ]
              ]
            },
            "treatments": [
              "retain",
              "clear"
            ]
          },
          {
            "after": 753,
            "before": 894,
            "control_seeds": {
              "original": 2147891498950564844,
              "revised": 298906340986623092
            },
            "device": 0,
            "first": 0,
            "group": "main",
            "id": "main-00",
            "index": 0,
            "original": [
              [
                113,
                273,
                387,
                -548,
                439,
                561,
                -211,
                588,
                -220,
                616,
                703,
                683,
                576,
                -293,
                -842,
                894,
                -973,
                -921,
                585,
                -576
              ],
              [
                210,
                -308,
                -245,
                -955,
                189,
                642,
                827,
                -983,
                579,
                -320,
                872,
                -439,
                -982,
                -78,
                312,
                834,
                180,
                -800,
                -905,
                -381
              ]
            ],
            "original_truth": 894,
            "owner": 0,
            "proposals": 1,
            "rejections": {
              "nonunique_maximum": 0,
              "owner_block": 0,
              "remaining_at_floor": 0
            },
            "revised": [
              [
                113,
                273,
                387,
                -548,
                439,
                561,
                -211,
                588,
                -220,
                616,
                703,
                683,
                576,
                -293,
                -842,
                753,
                -973,
                -921,
                585,
                -576
              ],
              [
                210,
                -308,
                -245,
                -955,
                189,
                642,
                827,
                -983,
                579,
                -320,
                872,
                -439,
                -982,
                -78,
                312,
                834,
                180,
                -800,
                -905,
                -381
              ]
            ],
            "revised_truth": 872,
            "row": 15,
            "seeds": {
              "prefix": [
                [
                  7613389024471320949,
                  2430595037025299620,
                  7632132044748201474
                ],
                [
                  4798458808050766445,
                  8822928244286280046,
                  7068274016831448234
                ]
              ],
              "recovery": [
                [
                  3459283983308522598,
                  534857686012084730,
                  7779589634043449186
                ],
                [
                  1252619848572711051,
                  9024046278804602435,
                  2114440144336600496
                ]
              ]
            },
            "treatments": [
              "retain",
              "clear"
            ]
          },
          {
            "after": -152,
            "before": 936,
            "control_seeds": {
              "original": 133001457366662095,
              "revised": 6352946184833924874
            },
            "device": 1,
            "first": 0,
            "group": "main",
            "id": "main-01",
            "index": 1,
            "original": [
              [
                -200,
                723,
                -96,
                -833,
                299,
                -297,
                -604,
                234,
                -294,
                380,
                598,
                151,
                -284,
                247,
                344,
                936,
                -526,
                224,
                473,
                -862
              ],
              [
                -992,
                -957,
                304,
                -101,
                53,
                404,
                -735,
                749,
                -543,
                293,
                507,
                138,
                -760,
                -749,
                619,
                534,
                910,
                -839,
                841,
                -759
              ]
            ],
            "original_truth": 936,
            "owner": 0,
            "proposals": 1,
            "rejections": {
              "nonunique_maximum": 0,
              "owner_block": 0,
              "remaining_at_floor": 0
            },
            "revised": [
              [
                -200,
                723,
                -96,
                -833,
                299,
                -297,
                -604,
                234,
                -294,
                380,
                598,
                151,
                -284,
                247,
                344,
                -152,
                -526,
                224,
                473,
                -862
              ],
              [
                -992,
                -957,
                304,
                -101,
                53,
                404,
                -735,
                749,
                -543,
                293,
                507,
                138,
                -760,
                -749,
                619,
                534,
                910,
                -839,
                841,
                -759
              ]
            ],
            "revised_truth": 910,
            "row": 15,
            "seeds": {
              "prefix": [
                [
                  1619430377463203250,
                  100071804121729356,
                  7693732580013016497
                ],
                [
                  2392044105153311016,
                  4915930630265407126,
                  2770636549167397914
                ]
              ],
              "recovery": [
                [
                  6784604259975473913,
                  5265313454849479903,
                  5554753004093747182
                ],
                [
                  4385210743583052582,
                  7239859807044094272,
                  9034891210502621966
                ]
              ]
            },
            "treatments": [
              "clear",
              "retain"
            ]
          },
          {
            "after": -452,
            "before": 957,
            "control_seeds": {
              "original": 4794547254492634117,
              "revised": 1417816023888265619
            },
            "device": 0,
            "first": 0,
            "group": "main",
            "id": "main-02",
            "index": 2,
            "original": [
              [
                -831,
                -342,
                -592,
                -608,
                -812,
                183,
                -871,
                802,
                90,
                -26,
                -733,
                -257,
                957,
                -252,
                558,
                -12,
                830,
                756,
                784,
                -786
              ],
              [
                -376,
                -526,
                338,
                -196,
                152,
                214,
                -29,
                532,
                -941,
                -920,
                627,
                348,
                -848,
                -512,
                -363,
                -964,
                887,
                -849,
                914,
                449
              ]
            ],
            "original_truth": 957,
            "owner": 0,
            "proposals": 2,
            "rejections": {
              "nonunique_maximum": 0,
              "owner_block": 1,
              "remaining_at_floor": 0
            },
            "revised": [
              [
                -831,
                -342,
                -592,
                -608,
                -812,
                183,
                -871,
                802,
                90,
                -26,
                -733,
                -257,
                -452,
                -252,
                558,
                -12,
                830,
                756,
                784,
                -786
              ],
              [
                -376,
                -526,
                338,
                -196,
                152,
                214,
                -29,
                532,
                -941,
                -920,
                627,
                348,
                -848,
                -512,
                -363,
                -964,
                887,
                -849,
                914,
                449
              ]
            ],
            "revised_truth": 914,
            "row": 12,
            "seeds": {
              "prefix": [
                [
                  3978482016353816917,
                  4027682472747877123,
                  193044703599591544
                ],
                [
                  8476846841885711904,
                  2229360315824126971,
                  2051761436065831103
                ]
              ],
              "recovery": [
                [
                  5960279899263789434,
                  1749033961600293646,
                  5527288603516730547
                ],
                [
                  740317857514137191,
                  2618489332901524746,
                  5404139388152553139
                ]
              ]
            },
            "treatments": [
              "retain",
              "clear"
            ]
          },
          {
            "after": -489,
            "before": 993,
            "control_seeds": {
              "original": 8471554357770356529,
              "revised": 6470849730561868516
            },
            "device": 1,
            "first": 0,
            "group": "main",
            "id": "main-03",
            "index": 3,
            "original": [
              [
                -182,
                -829,
                -726,
                354,
                -805,
                -532,
                -375,
                993,
                230,
                -384,
                -449,
                -25,
                115,
                -576,
                693,
                67,
                783,
                201,
                -515,
                -283
              ],
              [
                36,
                -135,
                -15,
                340,
                -218,
                64,
                -703,
                -847,
                822,
                -964,
                -680,
                -41,
                -206,
                14,
                -801,
                -531,
                -320,
                -125,
                566,
                196
              ]
            ],
            "original_truth": 993,
            "owner": 0,
            "proposals": 1,
            "rejections": {
              "nonunique_maximum": 0,
              "owner_block": 0,
              "remaining_at_floor": 0
            },
            "revised": [
              [
                -182,
                -829,
                -726,
                354,
                -805,
                -532,
                -375,
                -489,
                230,
                -384,
                -449,
                -25,
                115,
                -576,
                693,
                67,
                783,
                201,
                -515,
                -283
              ],
              [
                36,
                -135,
                -15,
                340,
                -218,
                64,
                -703,
                -847,
                822,
                -964,
                -680,
                -41,
                -206,
                14,
                -801,
                -531,
                -320,
                -125,
                566,
                196
              ]
            ],
            "revised_truth": 822,
            "row": 7,
            "seeds": {
              "prefix": [
                [
                  139902953584322306,
                  3268728654576400253,
                  7125301707374441810
                ],
                [
                  2983288974554191250,
                  4521724768519690317,
                  8909413058330369264
                ]
              ],
              "recovery": [
                [
                  1775432120674568221,
                  5017298312933826769,
                  6523901000912654712
                ],
                [
                  5387240266317778948,
                  1014741761784909330,
                  2065938479339020309
                ]
              ]
            },
            "treatments": [
              "clear",
              "retain"
            ]
          },
          {
            "after": 629,
            "before": 994,
            "control_seeds": {
              "original": 4960720530651022430,
              "revised": 8889708095582152789
            },
            "device": 0,
            "first": 0,
            "group": "main",
            "id": "main-04",
            "index": 4,
            "original": [
              [
                994,
                485,
                341,
                -519,
                8,
                -316,
                150,
                881,
                -205,
                -795,
                -174,
                -968,
                255,
                -795,
                450,
                294,
                943,
                -707,
                662,
                276
              ],
              [
                -871,
                -703,
                959,
                -861,
                58,
                855,
                96,
                587,
                -934,
                638,
                -605,
                -41,
                -711,
                -113,
                366,
                371,
                -610,
                474,
                -81,
                101
              ]
            ],
            "original_truth": 994,
            "owner": 0,
            "proposals": 1,
            "rejections": {
              "nonunique_maximum": 0,
              "owner_block": 0,
              "remaining_at_floor": 0
            },
            "revised": [
              [
                629,
                485,
                341,
                -519,
                8,
                -316,
                150,
                881,
                -205,
                -795,
                -174,
                -968,
                255,
                -795,
                450,
                294,
                943,
                -707,
                662,
                276
              ],
              [
                -871,
                -703,
                959,
                -861,
                58,
                855,
                96,
                587,
                -934,
                638,
                -605,
                -41,
                -711,
                -113,
                366,
                371,
                -610,
                474,
                -81,
                101
              ]
            ],
            "revised_truth": 959,
            "row": 0,
            "seeds": {
              "prefix": [
                [
                  4452187471933571023,
                  7321724501442330755,
                  1750068862954404733
                ],
                [
                  4099672381084009203,
                  3104069450291277575,
                  328549809509255860
                ]
              ],
              "recovery": [
                [
                  8994721194012826067,
                  3800838350043971346,
                  10834238225407660
                ],
                [
                  214198652916756762,
                  1043855508657754351,
                  1866335026032308508
                ]
              ]
            },
            "treatments": [
              "retain",
              "clear"
            ]
          },
          {
            "after": -91,
            "before": 949,
            "control_seeds": {
              "original": 2164810558525433393,
              "revised": 1928374090232088953
            },
            "device": 1,
            "first": 1,
            "group": "main",
            "id": "main-05",
            "index": 5,
            "original": [
              [
                -807,
                -498,
                -251,
                134,
                -707,
                -513,
                -264,
                -78,
                -674,
                -808,
                412,
                915,
                -137,
                -325,
                949,
                -906,
                -718,
                873,
                464,
                -299
              ],
              [
                506,
                -479,
                -379,
                749,
                512,
                391,
                292,
                -546,
                -559,
                644,
                124,
                -376,
                870,
                147,
                -723,
                -43,
                573,
                -497,
                489,
                -442
              ]
            ],
            "original_truth": 949,
            "owner": 0,
            "proposals": 2,
            "rejections": {
              "nonunique_maximum": 0,
              "owner_block": 1,
              "remaining_at_floor": 0
            },
            "revised": [
              [
                -807,
                -498,
                -251,
                134,
                -707,
                -513,
                -264,
                -78,
                -674,
                -808,
                412,
                915,
                -137,
                -325,
                -91,
                -906,
                -718,
                873,
                464,
                -299
              ],
              [
                506,
                -479,
                -379,
                749,
                512,
                391,
                292,
                -546,
                -559,
                644,
                124,
                -376,
                870,
                147,
                -723,
                -43,
                573,
                -497,
                489,
                -442
              ]
            ],
            "revised_truth": 915,
            "row": 14,
            "seeds": {
              "prefix": [
                [
                  561649063181457771,
                  6508216825219903062,
                  2107932907533430008
                ],
                [
                  7259646355533685262,
                  2976846420035572698,
                  6092476739546730244
                ]
              ],
              "recovery": [
                [
                  1504507442207819565,
                  5407287651997673118,
                  4382105864275936713
                ],
                [
                  7914258068898711446,
                  2836955077332054162,
                  6625670272031382701
                ]
              ]
            },
            "treatments": [
              "clear",
              "retain"
            ]
          },
          {
            "after": 905,
            "before": 977,
            "control_seeds": {
              "original": 1959322347283275910,
              "revised": 5151532955772563227
            },
            "device": 0,
            "first": 1,
            "group": "main",
            "id": "main-06",
            "index": 6,
            "original": [
              [
                522,
                791,
                -988,
                -610,
                977,
                263,
                744,
                -585,
                656,
                336,
                124,
                883,
                324,
                807,
                116,
                314,
                838,
                -606,
                -56,
                298
              ],
              [
                -339,
                926,
                29,
                -917,
                564,
                -406,
                681,
                646,
                -174,
                352,
                787,
                792,
                678,
                568,
                -6,
                -461,
                92,
                79,
                -974,
                -929
              ]
            ],
            "original_truth": 977,
            "owner": 0,
            "proposals": 2,
            "rejections": {
              "nonunique_maximum": 0,
              "owner_block": 1,
              "remaining_at_floor": 0
            },
            "revised": [
              [
                522,
                791,
                -988,
                -610,
                905,
                263,
                744,
                -585,
                656,
                336,
                124,
                883,
                324,
                807,
                116,
                314,
                838,
                -606,
                -56,
                298
              ],
              [
                -339,
                926,
                29,
                -917,
                564,
                -406,
                681,
                646,
                -174,
                352,
                787,
                792,
                678,
                568,
                -6,
                -461,
                92,
                79,
                -974,
                -929
              ]
            ],
            "revised_truth": 926,
            "row": 4,
            "seeds": {
              "prefix": [
                [
                  9107563587078734982,
                  5402733660104209960,
                  2528101576028971409
                ],
                [
                  8228629113183717777,
                  3209517545748347934,
                  128343983576175246
                ]
              ],
              "recovery": [
                [
                  1426073051744467116,
                  4230107165784492271,
                  4131646186970840278
                ],
                [
                  8414519180560761855,
                  2417252706394484963,
                  2050904192548928404
                ]
              ]
            },
            "treatments": [
              "retain",
              "clear"
            ]
          },
          {
            "after": -721,
            "before": 917,
            "control_seeds": {
              "original": 4368901468440162144,
              "revised": 1741964262489296062
            },
            "device": 1,
            "first": 1,
            "group": "main",
            "id": "main-07",
            "index": 7,
            "original": [
              [
                -369,
                917,
                -931,
                33,
                -595,
                13,
                52,
                654,
                461,
                155,
                98,
                -126,
                -540,
                -122,
                -531,
                759,
                519,
                701,
                133,
                -838
              ],
              [
                669,
                414,
                241,
                840,
                -878,
                89,
                603,
                -589,
                -148,
                -730,
                869,
                -445,
                534,
                880,
                97,
                -353,
                -515,
                695,
                774,
                -612
              ]
            ],
            "original_truth": 917,
            "owner": 0,
            "proposals": 3,
            "rejections": {
              "nonunique_maximum": 0,
              "owner_block": 2,
              "remaining_at_floor": 0
            },
            "revised": [
              [
                -369,
                -721,
                -931,
                33,
                -595,
                13,
                52,
                654,
                461,
                155,
                98,
                -126,
                -540,
                -122,
                -531,
                759,
                519,
                701,
                133,
                -838
              ],
              [
                669,
                414,
                241,
                840,
                -878,
                89,
                603,
                -589,
                -148,
                -730,
                869,
                -445,
                534,
                880,
                97,
                -353,
                -515,
                695,
                774,
                -612
              ]
            ],
            "revised_truth": 880,
            "row": 1,
            "seeds": {
              "prefix": [
                [
                  6065529762186739126,
                  924384901063280048,
                  8716017849433003299
                ],
                [
                  8440419528886959979,
                  84465805100603968,
                  941681735522333411
                ]
              ],
              "recovery": [
                [
                  7480473105748484397,
                  5682402573496401995,
                  349580090625612606
                ],
                [
                  2369861748578623633,
                  5113988670878644717,
                  1417998081918525862
                ]
              ]
            },
            "treatments": [
              "clear",
              "retain"
            ]
          },
          {
            "after": -933,
            "before": 965,
            "control_seeds": {
              "original": 4393186238040900385,
              "revised": 8453823791653888183
            },
            "device": 0,
            "first": 1,
            "group": "main",
            "id": "main-08",
            "index": 8,
            "original": [
              [
                0,
                916,
                965,
                610,
                -48,
                -163,
                948,
                -977,
                -33,
                652,
                260,
                -766,
                960,
                189,
                -382,
                938,
                -933,
                -288,
                -944,
                309
              ],
              [
                -209,
                -400,
                230,
                -987,
                91,
                -305,
                652,
                917,
                928,
                -730,
                -366,
                695,
                -18,
                791,
                -955,
                -716,
                263,
                -740,
                -590,
                -789
              ]
            ],
            "original_truth": 965,
            "owner": 0,
            "proposals": 3,
            "rejections": {
              "nonunique_maximum": 0,
              "owner_block": 2,
              "remaining_at_floor": 0
            },
            "revised": [
              [
                0,
                916,
                -933,
                610,
                -48,
                -163,
                948,
                -977,
                -33,
                652,
                260,
                -766,
                960,
                189,
                -382,
                938,
                -933,
                -288,
                -944,
                309
              ],
              [
                -209,
                -400,
                230,
                -987,
                91,
                -305,
                652,
                917,
                928,
                -730,
                -366,
                695,
                -18,
                791,
                -955,
                -716,
                263,
                -740,
                -590,
                -789
              ]
            ],
            "revised_truth": 960,
            "row": 2,
            "seeds": {
              "prefix": [
                [
                  192950164726274557,
                  4774456550148206825,
                  6594954879850626019
                ],
                [
                  1257499277584708772,
                  9193106247132483019,
                  4993213291275076191
                ]
              ],
              "recovery": [
                [
                  6344436267273193217,
                  2648734091400131420,
                  4411572305060160406
                ],
                [
                  9158899219688889798,
                  7558524973736859106,
                  5820781040901160327
                ]
              ]
            },
            "treatments": [
              "retain",
              "clear"
            ]
          },
          {
            "after": 283,
            "before": 999,
            "control_seeds": {
              "original": 9214668301875570868,
              "revised": 4628258382748303628
            },
            "device": 1,
            "first": 1,
            "group": "main",
            "id": "main-09",
            "index": 9,
            "original": [
              [
                916,
                850,
                532,
                165,
                84,
                999,
                232,
                -488,
                -994,
                -935,
                446,
                -239,
                381,
                -148,
                654,
                304,
                418,
                -585,
                -882,
                102
              ],
              [
                601,
                -854,
                -630,
                297,
                353,
                97,
                2,
                -669,
                166,
                -126,
                933,
                852,
                96,
                -237,
                296,
                -7,
                -276,
                787,
                214,
                676
              ]
            ],
            "original_truth": 999,
            "owner": 0,
            "proposals": 1,
            "rejections": {
              "nonunique_maximum": 0,
              "owner_block": 0,
              "remaining_at_floor": 0
            },
            "revised": [
              [
                916,
                850,
                532,
                165,
                84,
                283,
                232,
                -488,
                -994,
                -935,
                446,
                -239,
                381,
                -148,
                654,
                304,
                418,
                -585,
                -882,
                102
              ],
              [
                601,
                -854,
                -630,
                297,
                353,
                97,
                2,
                -669,
                166,
                -126,
                933,
                852,
                96,
                -237,
                296,
                -7,
                -276,
                787,
                214,
                676
              ]
            ],
            "revised_truth": 933,
            "row": 5,
            "seeds": {
              "prefix": [
                [
                  4685134624984108094,
                  5169167145342257419,
                  3643973146271904957
                ],
                [
                  6803160303860818703,
                  7564060563883581650,
                  162423314457967112
                ]
              ],
              "recovery": [
                [
                  8023923800489086619,
                  1130665023006752772,
                  4285012345147662237
                ],
                [
                  1010564286941044410,
                  1640805139424063780,
                  6827608508764498384
                ]
              ]
            },
            "treatments": [
              "clear",
              "retain"
            ]
          },
          {
            "after": 867,
            "before": 937,
            "control_seeds": {
              "original": 1226459450355933647,
              "revised": 8687626564131041381
            },
            "device": 0,
            "first": 0,
            "group": "main",
            "id": "main-10",
            "index": 10,
            "original": [
              [
                -677,
                -465,
                323,
                -563,
                124,
                615,
                -169,
                -497,
                700,
                -208,
                341,
                317,
                297,
                559,
                -118,
                -954,
                429,
                659,
                758,
                -381
              ],
              [
                814,
                515,
                349,
                196,
                -467,
                94,
                50,
                -298,
                -925,
                937,
                -768,
                -997,
                918,
                888,
                -152,
                67,
                -155,
                559,
                379,
                -276
              ]
            ],
            "original_truth": 937,
            "owner": 1,
            "proposals": 2,
            "rejections": {
              "nonunique_maximum": 0,
              "owner_block": 1,
              "remaining_at_floor": 0
            },
            "revised": [
              [
                -677,
                -465,
                323,
                -563,
                124,
                615,
                -169,
                -497,
                700,
                -208,
                341,
                317,
                297,
                559,
                -118,
                -954,
                429,
                659,
                758,
                -381
              ],
              [
                814,
                515,
                349,
                196,
                -467,
                94,
                50,
                -298,
                -925,
                867,
                -768,
                -997,
                918,
                888,
                -152,
                67,
                -155,
                559,
                379,
                -276
              ]
            ],
            "revised_truth": 918,
            "row": 9,
            "seeds": {
              "prefix": [
                [
                  5661297641176745221,
                  2988932701086763153,
                  632323218981940050
                ],
                [
                  5965690742242668860,
                  2416004198644876313,
                  2994460492752693716
                ]
              ],
              "recovery": [
                [
                  4570728588175425658,
                  6630952362004802828,
                  6039937866577557379
                ],
                [
                  7146153813596516521,
                  1616327101951968020,
                  525932557302377982
                ]
              ]
            },
            "treatments": [
              "retain",
              "clear"
            ]
          },
          {
            "after": -453,
            "before": 972,
            "control_seeds": {
              "original": 4033333652152207591,
              "revised": 7011718913799078458
            },
            "device": 1,
            "first": 0,
            "group": "main",
            "id": "main-11",
            "index": 11,
            "original": [
              [
                68,
                -916,
                560,
                757,
                229,
                -675,
                -927,
                747,
                708,
                -57,
                -950,
                26,
                715,
                -364,
                -842,
                267,
                216,
                331,
                -127,
                596
              ],
              [
                972,
                -424,
                -379,
                -509,
                172,
                688,
                928,
                203,
                -227,
                812,
                -133,
                347,
                122,
                -520,
                608,
                -855,
                474,
                -143,
                963,
                -402
              ]
            ],
            "original_truth": 972,
            "owner": 1,
            "proposals": 2,
            "rejections": {
              "nonunique_maximum": 0,
              "owner_block": 1,
              "remaining_at_floor": 0
            },
            "revised": [
              [
                68,
                -916,
                560,
                757,
                229,
                -675,
                -927,
                747,
                708,
                -57,
                -950,
                26,
                715,
                -364,
                -842,
                267,
                216,
                331,
                -127,
                596
              ],
              [
                -453,
                -424,
                -379,
                -509,
                172,
                688,
                928,
                203,
                -227,
                812,
                -133,
                347,
                122,
                -520,
                608,
                -855,
                474,
                -143,
                963,
                -402
              ]
            ],
            "revised_truth": 963,
            "row": 0,
            "seeds": {
              "prefix": [
                [
                  2699441716391527412,
                  3035259578590224976,
                  2971972859960784202
                ],
                [
                  5136283076468002978,
                  6319628260057940435,
                  6577424467119165128
                ]
              ],
              "recovery": [
                [
                  5721108965903856331,
                  11167153662719915,
                  3224564801068027648
                ],
                [
                  2618425764677916156,
                  8860473879125021793,
                  3058225647350318428
                ]
              ]
            },
            "treatments": [
              "clear",
              "retain"
            ]
          },
          {
            "after": 142,
            "before": 997,
            "control_seeds": {
              "original": 3150153611169757532,
              "revised": 4270835832855700703
            },
            "device": 0,
            "first": 0,
            "group": "main",
            "id": "main-12",
            "index": 12,
            "original": [
              [
                983,
                502,
                144,
                785,
                654,
                13,
                157,
                549,
                -864,
                32,
                10,
                -5,
                420,
                959,
                884,
                630,
                762,
                966,
                -762,
                918
              ],
              [
                -730,
                280,
                997,
                -666,
                287,
                420,
                548,
                284,
                -538,
                -801,
                -308,
                45,
                -956,
                -789,
                -280,
                -703,
                -237,
                -97,
                -894,
                448
              ]
            ],
            "original_truth": 997,
            "owner": 1,
            "proposals": 1,
            "rejections": {
              "nonunique_maximum": 0,
              "owner_block": 0,
              "remaining_at_floor": 0
            },
            "revised": [
              [
                983,
                502,
                144,
                785,
                654,
                13,
                157,
                549,
                -864,
                32,
                10,
                -5,
                420,
                959,
                884,
                630,
                762,
                966,
                -762,
                918
              ],
              [
                -730,
                280,
                142,
                -666,
                287,
                420,
                548,
                284,
                -538,
                -801,
                -308,
                45,
                -956,
                -789,
                -280,
                -703,
                -237,
                -97,
                -894,
                448
              ]
            ],
            "revised_truth": 983,
            "row": 2,
            "seeds": {
              "prefix": [
                [
                  8067617777804797891,
                  557664866961384201,
                  8709815472197141218
                ],
                [
                  8805643309456860035,
                  5844005573012226274,
                  2109457162888020055
                ]
              ],
              "recovery": [
                [
                  5987524421992088977,
                  7777712625100116258,
                  3567485187867362033
                ],
                [
                  1394962814262892434,
                  6684962908305202929,
                  3927869302931546758
                ]
              ]
            },
            "treatments": [
              "retain",
              "clear"
            ]
          },
          {
            "after": -318,
            "before": 982,
            "control_seeds": {
              "original": 3047043693510280639,
              "revised": 2635468176680950715
            },
            "device": 1,
            "first": 0,
            "group": "main",
            "id": "main-13",
            "index": 13,
            "original": [
              [
                -645,
                -828,
                615,
                -614,
                506,
                -480,
                -301,
                -170,
                -778,
                106,
                -432,
                -31,
                357,
                -917,
                716,
                572,
                -60,
                737,
                -559,
                -54
              ],
              [
                -872,
                161,
                -148,
                -469,
                692,
                -355,
                -10,
                865,
                -10,
                -822,
                481,
                -484,
                953,
                -798,
                -639,
                -821,
                982,
                -196,
                929,
                27
              ]
            ],
            "original_truth": 982,
            "owner": 1,
            "proposals": 1,
            "rejections": {
              "nonunique_maximum": 0,
              "owner_block": 0,
              "remaining_at_floor": 0
            },
            "revised": [
              [
                -645,
                -828,
                615,
                -614,
                506,
                -480,
                -301,
                -170,
                -778,
                106,
                -432,
                -31,
                357,
                -917,
                716,
                572,
                -60,
                737,
                -559,
                -54
              ],
              [
                -872,
                161,
                -148,
                -469,
                692,
                -355,
                -10,
                865,
                -10,
                -822,
                481,
                -484,
                953,
                -798,
                -639,
                -821,
                -318,
                -196,
                929,
                27
              ]
            ],
            "revised_truth": 953,
            "row": 16,
            "seeds": {
              "prefix": [
                [
                  3979908319941421135,
                  2393529629678929350,
                  5094173747872294098
                ],
                [
                  2998798001136738158,
                  3915350704564495490,
                  2032733688510320421
                ]
              ],
              "recovery": [
                [
                  2239360232027024199,
                  5764790047426674101,
                  5097061125250303561
                ],
                [
                  5771648798121642707,
                  9036171998834330482,
                  3599751875578752418
                ]
              ]
            },
            "treatments": [
              "clear",
              "retain"
            ]
          },
          {
            "after": -220,
            "before": 984,
            "control_seeds": {
              "original": 4904115945039636251,
              "revised": 7921154408136709599
            },
            "device": 0,
            "first": 0,
            "group": "main",
            "id": "main-14",
            "index": 14,
            "original": [
              [
                -776,
                -983,
                -210,
                400,
                117,
                461,
                -202,
                -764,
                111,
                712,
                -517,
                310,
                -872,
                -520,
                -580,
                -884,
                -629,
                236,
                -712,
                -56
              ],
              [
                -173,
                425,
                984,
                -623,
                -620,
                -274,
                -785,
                261,
                44,
                -973,
                -218,
                730,
                302,
                233,
                -954,
                -651,
                325,
                101,
                533,
                -467
              ]
            ],
            "original_truth": 984,
            "owner": 1,
            "proposals": 2,
            "rejections": {
              "nonunique_maximum": 0,
              "owner_block": 1,
              "remaining_at_floor": 0
            },
            "revised": [
              [
                -776,
                -983,
                -210,
                400,
                117,
                461,
                -202,
                -764,
                111,
                712,
                -517,
                310,
                -872,
                -520,
                -580,
                -884,
                -629,
                236,
                -712,
                -56
              ],
              [
                -173,
                425,
                -220,
                -623,
                -620,
                -274,
                -785,
                261,
                44,
                -973,
                -218,
                730,
                302,
                233,
                -954,
                -651,
                325,
                101,
                533,
                -467
              ]
            ],
            "revised_truth": 730,
            "row": 2,
            "seeds": {
              "prefix": [
                [
                  2382279863713379274,
                  7221813534107381903,
                  1830575940988971568
                ],
                [
                  1974500441739583894,
                  7166617257048818533,
                  4786707485556870973
                ]
              ],
              "recovery": [
                [
                  5734893163594118816,
                  8920205055925856671,
                  2106084752359392235
                ],
                [
                  8148979525226795087,
                  5528510670377592352,
                  653736666617253595
                ]
              ]
            },
            "treatments": [
              "retain",
              "clear"
            ]
          },
          {
            "after": -614,
            "before": 967,
            "control_seeds": {
              "original": 2330237667479163395,
              "revised": 4807181268986667867
            },
            "device": 1,
            "first": 1,
            "group": "main",
            "id": "main-15",
            "index": 15,
            "original": [
              [
                -210,
                775,
                -884,
                557,
                -297,
                447,
                -152,
                -393,
                -417,
                -18,
                -303,
                111,
                745,
                -207,
                959,
                -285,
                -902,
                821,
                787,
                -578
              ],
              [
                -423,
                -859,
                -995,
                -244,
                734,
                584,
                831,
                -418,
                559,
                -124,
                947,
                -631,
                967,
                924,
                -640,
                3,
                -862,
                -381,
                -467,
                806
              ]
            ],
            "original_truth": 967,
            "owner": 1,
            "proposals": 1,
            "rejections": {
              "nonunique_maximum": 0,
              "owner_block": 0,
              "remaining_at_floor": 0
            },
            "revised": [
              [
                -210,
                775,
                -884,
                557,
                -297,
                447,
                -152,
                -393,
                -417,
                -18,
                -303,
                111,
                745,
                -207,
                959,
                -285,
                -902,
                821,
                787,
                -578
              ],
              [
                -423,
                -859,
                -995,
                -244,
                734,
                584,
                831,
                -418,
                559,
                -124,
                947,
                -631,
                -614,
                924,
                -640,
                3,
                -862,
                -381,
                -467,
                806
              ]
            ],
            "revised_truth": 959,
            "row": 12,
            "seeds": {
              "prefix": [
                [
                  8049316475296984749,
                  6651311606282137597,
                  2428136916549517310
                ],
                [
                  3863189380517531492,
                  9210302312644362371,
                  5107330403958620136
                ]
              ],
              "recovery": [
                [
                  8853190939237816913,
                  2662960213906330612,
                  1865128207707360999
                ],
                [
                  1307808059499793038,
                  2793050492793667061,
                  171509841350124668
                ]
              ]
            },
            "treatments": [
              "clear",
              "retain"
            ]
          },
          {
            "after": -627,
            "before": 919,
            "control_seeds": {
              "original": 1503848339326062111,
              "revised": 5319984730134778560
            },
            "device": 0,
            "first": 1,
            "group": "main",
            "id": "main-16",
            "index": 16,
            "original": [
              [
                324,
                -682,
                887,
                304,
                14,
                656,
                -467,
                579,
                486,
                229,
                477,
                37,
                508,
                -460,
                -255,
                -482,
                916,
                -676,
                -838,
                -20
              ],
              [
                -260,
                788,
                919,
                -221,
                629,
                -63,
                334,
                -319,
                574,
                752,
                792,
                -664,
                880,
                -864,
                753,
                -803,
                297,
                -54,
                895,
                652
              ]
            ],
            "original_truth": 919,
            "owner": 1,
            "proposals": 4,
            "rejections": {
              "nonunique_maximum": 0,
              "owner_block": 3,
              "remaining_at_floor": 0
            },
            "revised": [
              [
                324,
                -682,
                887,
                304,
                14,
                656,
                -467,
                579,
                486,
                229,
                477,
                37,
                508,
                -460,
                -255,
                -482,
                916,
                -676,
                -838,
                -20
              ],
              [
                -260,
                788,
                -627,
                -221,
                629,
                -63,
                334,
                -319,
                574,
                752,
                792,
                -664,
                880,
                -864,
                753,
                -803,
                297,
                -54,
                895,
                652
              ]
            ],
            "revised_truth": 916,
            "row": 2,
            "seeds": {
              "prefix": [
                [
                  9133351367866927780,
                  4708268123332630951,
                  8101133946723231055
                ],
                [
                  3149931738709346887,
                  4096448280584167478,
                  6863410623319663693
                ]
              ],
              "recovery": [
                [
                  8097089018640116083,
                  7312699544095183027,
                  8009409243665888063
                ],
                [
                  8661375194255689629,
                  6911446480698722895,
                  3051672257619254603
                ]
              ]
            },
            "treatments": [
              "retain",
              "clear"
            ]
          },
          {
            "after": -71,
            "before": 885,
            "control_seeds": {
              "original": 8042247140532174822,
              "revised": 4019721016965024234
            },
            "device": 1,
            "first": 1,
            "group": "main",
            "id": "main-17",
            "index": 17,
            "original": [
              [
                -633,
                -352,
                811,
                246,
                58,
                605,
                99,
                -392,
                269,
                840,
                -911,
                60,
                -915,
                300,
                878,
                -859,
                250,
                392,
                205,
                -720
              ],
              [
                278,
                -711,
                521,
                -414,
                -830,
                97,
                39,
                -150,
                -263,
                -981,
                -424,
                885,
                -836,
                -927,
                748,
                658,
                -780,
                -894,
                407,
                774
              ]
            ],
            "original_truth": 885,
            "owner": 1,
            "proposals": 4,
            "rejections": {
              "nonunique_maximum": 0,
              "owner_block": 3,
              "remaining_at_floor": 0
            },
            "revised": [
              [
                -633,
                -352,
                811,
                246,
                58,
                605,
                99,
                -392,
                269,
                840,
                -911,
                60,
                -915,
                300,
                878,
                -859,
                250,
                392,
                205,
                -720
              ],
              [
                278,
                -711,
                521,
                -414,
                -830,
                97,
                39,
                -150,
                -263,
                -981,
                -424,
                -71,
                -836,
                -927,
                748,
                658,
                -780,
                -894,
                407,
                774
              ]
            ],
            "revised_truth": 878,
            "row": 11,
            "seeds": {
              "prefix": [
                [
                  7370203119696101683,
                  8676882964858688617,
                  1285738219610523296
                ],
                [
                  1558207476444573364,
                  3854852960831798470,
                  3362734413617082988
                ]
              ],
              "recovery": [
                [
                  5749282179274952530,
                  439220088649944670,
                  2665823271028982252
                ],
                [
                  7007927364177320798,
                  1454269570792637695,
                  86856773501310504
                ]
              ]
            },
            "treatments": [
              "clear",
              "retain"
            ]
          },
          {
            "after": 333,
            "before": 908,
            "control_seeds": {
              "original": 1966245509280641185,
              "revised": 4928770713416526446
            },
            "device": 0,
            "first": 1,
            "group": "main",
            "id": "main-18",
            "index": 18,
            "original": [
              [
                133,
                -605,
                823,
                71,
                -809,
                -606,
                313,
                487,
                769,
                788,
                780,
                -826,
                -211,
                539,
                -250,
                185,
                807,
                -906,
                848,
                -745
              ],
              [
                -114,
                -245,
                -441,
                649,
                -322,
                -702,
                -814,
                632,
                326,
                165,
                -144,
                813,
                -706,
                525,
                -90,
                908,
                348,
                827,
                781,
                333
              ]
            ],
            "original_truth": 908,
            "owner": 1,
            "proposals": 1,
            "rejections": {
              "nonunique_maximum": 0,
              "owner_block": 0,
              "remaining_at_floor": 0
            },
            "revised": [
              [
                133,
                -605,
                823,
                71,
                -809,
                -606,
                313,
                487,
                769,
                788,
                780,
                -826,
                -211,
                539,
                -250,
                185,
                807,
                -906,
                848,
                -745
              ],
              [
                -114,
                -245,
                -441,
                649,
                -322,
                -702,
                -814,
                632,
                326,
                165,
                -144,
                813,
                -706,
                525,
                -90,
                333,
                348,
                827,
                781,
                333
              ]
            ],
            "revised_truth": 848,
            "row": 15,
            "seeds": {
              "prefix": [
                [
                  7598135116584668381,
                  9146236957778840145,
                  114920852746157201
                ],
                [
                  3316022409743939391,
                  4027773770743399252,
                  4930560188190906841
                ]
              ],
              "recovery": [
                [
                  4118538573955015757,
                  8850344356207479036,
                  7160915629396249838
                ],
                [
                  307394048295980151,
                  5122264955052118727,
                  2565077992634760225
                ]
              ]
            },
            "treatments": [
              "retain",
              "clear"
            ]
          },
          {
            "after": 213,
            "before": 951,
            "control_seeds": {
              "original": 7740961541298929508,
              "revised": 245690049236384587
            },
            "device": 1,
            "first": 1,
            "group": "main",
            "id": "main-19",
            "index": 19,
            "original": [
              [
                -546,
                -244,
                -664,
                -17,
                128,
                446,
                -155,
                551,
                -233,
                944,
                414,
                -703,
                61,
                92,
                -941,
                -142,
                -47,
                944,
                -435,
                -519
              ],
              [
                726,
                -445,
                362,
                -718,
                951,
                758,
                735,
                -443,
                521,
                689,
                -805,
                -8,
                -197,
                713,
                -176,
                -165,
                319,
                626,
                -194,
                875
              ]
            ],
            "original_truth": 951,
            "owner": 1,
            "proposals": 3,
            "rejections": {
              "nonunique_maximum": 0,
              "owner_block": 2,
              "remaining_at_floor": 0
            },
            "revised": [
              [
                -546,
                -244,
                -664,
                -17,
                128,
                446,
                -155,
                551,
                -233,
                944,
                414,
                -703,
                61,
                92,
                -941,
                -142,
                -47,
                944,
                -435,
                -519
              ],
              [
                726,
                -445,
                362,
                -718,
                213,
                758,
                735,
                -443,
                521,
                689,
                -805,
                -8,
                -197,
                713,
                -176,
                -165,
                319,
                626,
                -194,
                875
              ]
            ],
            "revised_truth": 944,
            "row": 4,
            "seeds": {
              "prefix": [
                [
                  7887811878140492104,
                  6255283482707103244,
                  3632073470791873446
                ],
                [
                  6235676957750292586,
                  2326562108051485717,
                  5493582434092557490
                ]
              ],
              "recovery": [
                [
                  9092468552002419456,
                  9019583098529008256,
                  5921040231014388108
                ],
                [
                  5217546261940366333,
                  1178083047056805454,
                  491617388332277490
                ]
              ]
            },
            "treatments": [
              "clear",
              "retain"
            ]
          }
        ]
      },
      "mode": "direct",
      "notes": "Automatic main resource admission under the precommitted Run All plan; human communication review remains pending.",
      "prior_spending": [],
      "prompt_system": {
        "content": "Find the global maximum across two agents' current private integer shards.\nYour current shard is authoritative. Coordinate using ordinary messages; claims are\nnot certified. Your submission is private unless you explicitly message it.\nReturn exactly one JSON object with keys message, submit, wait:\n{\"message\": \"text or null\", \"submit\": null, \"wait\": false}\nmessage is a string or null, submit an integer or null, wait a boolean.\nYou may message, submit, message and submit, or wait (without message/submission).\nSubmission is FINAL for this phase. Share necessary information before finishing.\nMessages received after submission cannot cancel it. Only a factual revision\nstarts a new phase. Both agents must submit, with at most three calls each in a\nphase. Unused turns cannot be transferred. Waiting wakes on a new message.\nYou receive no correctness feedback. Do not include reasoning outside the JSON.",
        "role": "system"
      },
      "qualification_policy": "i01-direct-protocol-2026-10-15",
      "rubric": [
        "wrong_submission",
        "noncompletion",
        "premature_finalization",
        "obsolete_value_repeated",
        "malformed_action",
        "truncated_action",
        "waiting_deadlock",
        "horizon_exhausted",
        "provider_failure",
        "ambiguous"
      ],
      "sessions": [
        [
          {
            "evidence": "{\"controller_pid\":231,\"host\":{\"executable\":\"/usr/bin/python3\",\"gpus\":[{\"driver\":\"580.178.04\",\"index\":0,\"memory_mib\":15360,\"name\":\"Tesla T4\",\"uuid\":\"GPU-ed9bad25-b76c-9174-051b-1a8b14ec17e2\"},{\"driver\":\"580.178.04\",\"index\":1,\"memory_mib\":15360,\"name\":\"Tesla T4\",\"uuid\":\"GPU-9bd69e6c-b965-32ef-1c1d-4d3aad42f4a0\"}],\"gpus_error\":null,\"internet_required\":true,\"machine\":\"x86_64\",\"observed_at\":\"2026-10-15T17:47:48.318672+00:00\",\"paths\":{\"scratch\":{\"device\":54,\"free\":1120627843072,\"path\":\"/kaggle/temp/i01\",\"total\":8758385086464,\"writable\":true},\"working\":{\"device\":1794,\"free\":20930084864,\"path\":\"/kaggle/working\",\"total\":20957446144,\"writable\":true}},\"python\":\"3.13.15 (main, Aug  6 2026, 11:06:22) [GCC 13.3.0]\",\"python_version\":[3,13,15],\"system\":\"Linux\"},\"load\":{\"actual_tensor_devices\":[\"cuda:0\"],\"attention\":\"recovery_t4_sdpa\",\"buffers\":{\"model.rotary_emb.inv_freq\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[32]},\"model.rotary_emb.original_inv_freq\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[32]}},\"class\":\"Qwen3_5ForCausalLM\",\"cuda\":\"12.8\",\"cuda_device_uuid\":\"ed9bad25-b76c-9174-051b-1a8b14ec17e2\",\"cuda_visible_devices\":\"0\",\"device_map\":null,\"device_name\":\"Tesla T4\",\"generation_config\":{\"_from_model_config\":null,\"assistant_confidence_threshold\":null,\"assistant_early_exit\":null,\"assistant_lookbehind\":null,\"bad_words_ids\":null,\"begin_suppress_tokens\":null,\"bos_token_id\":null,\"cache_config\":null,\"cache_implementation\":null,\"compile_config\":null,\"constraints\":null,\"continuous_batching_config\":null,\"decoder_start_token_id\":null,\"disable_compile\":null,\"diversity_penalty\":null,\"do_sample\":true,\"dola_layers\":null,\"early_stopping\":null,\"encoder_no_repeat_ngram_size\":null,\"encoder_repetition_penalty\":null,\"eos_token_id\":[248044,248046],\"epsilon_cutoff\":null,\"eta_cutoff\":null,\"exponential_decay_length_penalty\":null,\"force_words_ids\":null,\"forced_bos_token_id\":null,\"forced_eos_token_id\":null,\"guidance_scale\":null,\"is_assistant\":null,\"length_penalty\":null,\"low_memory\":null,\"max_length\":null,\"max_matching_ngram_size\":null,\"max_new_tokens\":256,\"max_time\":null,\"min_length\":null,\"min_new_tokens\":null,\"min_p\":0.0,\"no_repeat_ngram_size\":null,\"num_assistant_tokens\":null,\"num_assistant_tokens_schedule\":null,\"num_beam_groups\":null,\"num_beams\":1,\"num_return_sequences\":null,\"output_attentions\":null,\"output_hidden_states\":null,\"output_logits\":null,\"output_scores\":false,\"pad_token_id\":248044,\"penalty_alpha\":null,\"prefill_chunk_size\":256,\"prompt_lookup_num_tokens\":null,\"remove_invalid_values\":false,\"renormalize_logits\":null,\"repetition_penalty\":1.0,\"return_dict_in_generate\":true,\"sequence_bias\":null,\"stop_strings\":null,\"suppress_tokens\":null,\"target_lookbehind\":null,\"temperature\":0.7,\"token_healing\":null,\"top_h\":null,\"top_k\":20,\"top_p\":0.8,\"transformers_version\":\"5.12.0\",\"typical_p\":null,\"use_cache\":true,\"watermarking_config\":null},\"i01_loading_only\":true,\"load_seconds\":64.1649316380001,\"loaded_at\":\"2026-10-15T17:48:53.477607+00:00\",\"loading_info\":{\"error_msgs\":[],\"mismatched_keys\":[],\"missing_keys\":[],\"unexpected_keys\":[]},\"model\":\"Qwen/Qwen3.5-9B\",\"packages\":{\"accelerate\":\"1.14.0\",\"bitsandbytes\":\"0.49.2\",\"huggingface-hub\":\"1.19.0\",\"tokenizers\":\"0.22.2\",\"torch\":\"2.11.0+cu128\",\"transformers\":\"5.12.0\"},\"parameters\":{\"lm_head.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[248320,4096]},\"model.embed_tokens.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[248320,4096]},\"model.layers.0.input_layernorm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[4096]},\"model.layers.0.linear_attn.A_log\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[32]},\"model.layers.0.linear_attn.conv1d.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[8192,1,4]},\"model.layers.0.linear_attn.dt_bias\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[32]},\"model.layers.0.linear_attn.in_proj_a.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[65536,1]},\"model.layers.0.linear_attn.in_proj_b.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[65536,1]},\"model.layers.0.linear_attn.in_proj_qkv.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[16777216,1]},\"model.layers.0.linear_attn.in_proj_z.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[8388608,1]},\"model.layers.0.linear_attn.norm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[128]},\"model.layers.0.linear_attn.out_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[8388608,1]},\"model.layers.0.mlp.down_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.0.mlp.gate_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.0.mlp.up_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.0.post_attention_layernorm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[4096]},\"model.layers.1.input_layernorm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[4096]},\"model.layers.1.linear_attn.A_log\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[32]},\"model.layers.1.linear_attn.conv1d.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[8192,1,4]},\"model.layers.1.linear_attn.dt_bias\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[32]},\"model.layers.1.linear_attn.in_proj_a.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[65536,1]},\"model.layers.1.linear_attn.in_proj_b.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[65536,1]},\"model.layers.1.linear_attn.in_proj_qkv.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[16777216,1]},\"model.layers.1.linear_attn.in_proj_z.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[8388608,1]},\"model.layers.1.linear_attn.norm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[128]},\"model.layers.1.linear_attn.out_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[8388608,1]},\"model.layers.1.mlp.down_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.1.mlp.gate_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.1.mlp.up_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.1.post_attention_layernorm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[4096]},\"model.layers.10.input_layernorm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[4096]},\"model.layers.10.linear_attn.A_log\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[32]},\"model.layers.10.linear_attn.conv1d.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[8192,1,4]},\"model.layers.10.linear_attn.dt_bias\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[32]},\"model.layers.10.linear_attn.in_proj_a.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[65536,1]},\"model.layers.10.linear_attn.in_proj_b.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[65536,1]},\"model.layers.10.linear_attn.in_proj_qkv.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[16777216,1]},\"model.layers.10.linear_attn.in_proj_z.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[8388608,1]},\"model.layers.10.linear_attn.norm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[128]},\"model.layers.10.linear_attn.out_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[8388608,1]},\"model.layers.10.mlp.down_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.10.mlp.gate_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.10.mlp.up_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.10.post_attention_layernorm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[4096]},\"model.layers.11.input_layernorm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[4096]},\"model.layers.11.mlp.down_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.11.mlp.gate_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.11.mlp.up_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.11.post_attention_layernorm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[4096]},\"model.layers.11.self_attn.k_norm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[256]},\"model.layers.11.self_attn.k_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[2097152,1]},\"model.layers.11.self_attn.o_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[8388608,1]},\"model.layers.11.self_attn.q_norm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[256]},\"model.layers.11.self_attn.q_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[16777216,1]},\"model.layers.11.self_attn.v_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[2097152,1]},\"model.layers.12.input_layernorm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[4096]},\"model.layers.12.linear_attn.A_log\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[32]},\"model.layers.12.linear_attn.conv1d.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[8192,1,4]},\"model.layers.12.linear_attn.dt_bias\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[32]},\"model.layers.12.linear_attn.in_proj_a.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[65536,1]},\"model.layers.12.linear_attn.in_proj_b.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[65536,1]},\"model.layers.12.linear_attn.in_proj_qkv.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[16777216,1]},\"model.layers.12.linear_attn.in_proj_z.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[8388608,1]},\"model.layers.12.linear_attn.norm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[128]},\"model.layers.12.linear_attn.out_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[8388608,1]},\"model.layers.12.mlp.down_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.12.mlp.gate_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.12.mlp.up_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.12.post_attention_layernorm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[4096]},\"model.layers.13.input_layernorm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[4096]},\"model.layers.13.linear_attn.A_log\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[32]},\"model.layers.13.linear_attn.conv1d.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[8192,1,4]},\"model.layers.13.linear_attn.dt_bias\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[32]},\"model.layers.13.linear_attn.in_proj_a.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[65536,1]},\"model.layers.13.linear_attn.in_proj_b.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[65536,1]},\"model.layers.13.linear_attn.in_proj_qkv.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[16777216,1]},\"model.layers.13.linear_attn.in_proj_z.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[8388608,1]},\"model.layers.13.linear_attn.norm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[128]},\"model.layers.13.linear_attn.out_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[8388608,1]},\"model.layers.13.mlp.down_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.13.mlp.gate_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.13.mlp.up_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.13.post_attention_layernorm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[4096]},\"model.layers.14.input_layernorm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[4096]},\"model.layers.14.linear_attn.A_log\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[32]},\"model.layers.14.linear_attn.conv1d.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[8192,1,4]},\"model.layers.14.linear_attn.dt_bias\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[32]},\"model.layers.14.linear_attn.in_proj_a.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[65536,1]},\"model.layers.14.linear_attn.in_proj_b.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[65536,1]},\"model.layers.14.linear_attn.in_proj_qkv.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[16777216,1]},\"model.layers.14.linear_attn.in_proj_z.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[8388608,1]},\"model.layers.14.linear_attn.norm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[128]},\"model.layers.14.linear_attn.out_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[8388608,1]},\"model.layers.14.mlp.down_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.14.mlp.gate_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.14.mlp.up_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.14.post_attention_layernorm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[4096]},\"model.layers.15.input_layernorm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[4096]},\"model.layers.15.mlp.down_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.15.mlp.gate_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.15.mlp.up_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.15.post_attention_layernorm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[4096]},\"model.layers.15.self_attn.k_norm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[256]},\"model.layers.15.self_attn.k_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[2097152,1]},\"model.layers.15.self_attn.o_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[8388608,1]},\"model.layers.15.self_attn.q_norm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[256]},\"model.layers.15.self_attn.q_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[16777216,1]},\"model.layers.15.self_attn.v_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[2097152,1]},\"model.layers.16.input_layernorm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[4096]},\"model.layers.16.linear_attn.A_log\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[32]},\"model.layers.16.linear_attn.conv1d.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[8192,1,4]},\"model.layers.16.linear_attn.dt_bias\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[32]},\"model.layers.16.linear_attn.in_proj_a.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[65536,1]},\"model.layers.16.linear_attn.in_proj_b.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[65536,1]},\"model.layers.16.linear_attn.in_proj_qkv.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[16777216,1]},\"model.layers.16.linear_attn.in_proj_z.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[8388608,1]},\"model.layers.16.linear_attn.norm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[128]},\"model.layers.16.linear_attn.out_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[8388608,1]},\"model.layers.16.mlp.down_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.16.mlp.gate_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.16.mlp.up_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.16.post_attention_layernorm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[4096]},\"model.layers.17.input_layernorm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[4096]},\"model.layers.17.linear_attn.A_log\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[32]},\"model.layers.17.linear_attn.conv1d.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[8192,1,4]},\"model.layers.17.linear_attn.dt_bias\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[32]},\"model.layers.17.linear_attn.in_proj_a.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[65536,1]},\"model.layers.17.linear_attn.in_proj_b.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[65536,1]},\"model.layers.17.linear_attn.in_proj_qkv.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[16777216,1]},\"model.layers.17.linear_attn.in_proj_z.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[8388608,1]},\"model.layers.17.linear_attn.norm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[128]},\"model.layers.17.linear_attn.out_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[8388608,1]},\"model.layers.17.mlp.down_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.17.mlp.gate_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.17.mlp.up_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.17.post_attention_layernorm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[4096]},\"model.layers.18.input_layernorm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[4096]},\"model.layers.18.linear_attn.A_log\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[32]},\"model.layers.18.linear_attn.conv1d.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[8192,1,4]},\"model.layers.18.linear_attn.dt_bias\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[32]},\"model.layers.18.linear_attn.in_proj_a.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[65536,1]},\"model.layers.18.linear_attn.in_proj_b.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[65536,1]},\"model.layers.18.linear_attn.in_proj_qkv.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[16777216,1]},\"model.layers.18.linear_attn.in_proj_z.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[8388608,1]},\"model.layers.18.linear_attn.norm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[128]},\"model.layers.18.linear_attn.out_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[8388608,1]},\"model.layers.18.mlp.down_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.18.mlp.gate_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.18.mlp.up_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.18.post_attention_layernorm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[4096]},\"model.layers.19.input_layernorm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[4096]},\"model.layers.19.mlp.down_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.19.mlp.gate_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.19.mlp.up_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.19.post_attention_layernorm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[4096]},\"model.layers.19.self_attn.k_norm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[256]},\"model.layers.19.self_attn.k_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[2097152,1]},\"model.layers.19.self_attn.o_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[8388608,1]},\"model.layers.19.self_attn.q_norm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[256]},\"model.layers.19.self_attn.q_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[16777216,1]},\"model.layers.19.self_attn.v_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[2097152,1]},\"model.layers.2.input_layernorm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[4096]},\"model.layers.2.linear_attn.A_log\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[32]},\"model.layers.2.linear_attn.conv1d.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[8192,1,4]},\"model.layers.2.linear_attn.dt_bias\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[32]},\"model.layers.2.linear_attn.in_proj_a.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[65536,1]},\"model.layers.2.linear_attn.in_proj_b.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[65536,1]},\"model.layers.2.linear_attn.in_proj_qkv.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[16777216,1]},\"model.layers.2.linear_attn.in_proj_z.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[8388608,1]},\"model.layers.2.linear_attn.norm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[128]},\"model.layers.2.linear_attn.out_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[8388608,1]},\"model.layers.2.mlp.down_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.2.mlp.gate_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.2.mlp.up_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.2.post_attention_layernorm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[4096]},\"model.layers.20.input_layernorm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[4096]},\"model.layers.20.linear_attn.A_log\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[32]},\"model.layers.20.linear_attn.conv1d.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[8192,1,4]},\"model.layers.20.linear_attn.dt_bias\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[32]},\"model.layers.20.linear_attn.in_proj_a.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[65536,1]},\"model.layers.20.linear_attn.in_proj_b.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[65536,1]},\"model.layers.20.linear_attn.in_proj_qkv.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[16777216,1]},\"model.layers.20.linear_attn.in_proj_z.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[8388608,1]},\"model.layers.20.linear_attn.norm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[128]},\"model.layers.20.linear_attn.out_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[8388608,1]},\"model.layers.20.mlp.down_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.20.mlp.gate_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.20.mlp.up_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.20.post_attention_layernorm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[4096]},\"model.layers.21.input_layernorm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[4096]},\"model.layers.21.linear_attn.A_log\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[32]},\"model.layers.21.linear_attn.conv1d.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[8192,1,4]},\"model.layers.21.linear_attn.dt_bias\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[32]},\"model.layers.21.linear_attn.in_proj_a.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[65536,1]},\"model.layers.21.linear_attn.in_proj_b.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[65536,1]},\"model.layers.21.linear_attn.in_proj_qkv.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[16777216,1]},\"model.layers.21.linear_attn.in_proj_z.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[8388608,1]},\"model.layers.21.linear_attn.norm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[128]},\"model.layers.21.linear_attn.out_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[8388608,1]},\"model.layers.21.mlp.down_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.21.mlp.gate_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.21.mlp.up_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.21.post_attention_layernorm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[4096]},\"model.layers.22.input_layernorm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[4096]},\"model.layers.22.linear_attn.A_log\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[32]},\"model.layers.22.linear_attn.conv1d.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[8192,1,4]},\"model.layers.22.linear_attn.dt_bias\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[32]},\"model.layers.22.linear_attn.in_proj_a.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[65536,1]},\"model.layers.22.linear_attn.in_proj_b.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[65536,1]},\"model.layers.22.linear_attn.in_proj_qkv.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[16777216,1]},\"model.layers.22.linear_attn.in_proj_z.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[8388608,1]},\"model.layers.22.linear_attn.norm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[128]},\"model.layers.22.linear_attn.out_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[8388608,1]},\"model.layers.22.mlp.down_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.22.mlp.gate_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.22.mlp.up_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.22.post_attention_layernorm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[4096]},\"model.layers.23.input_layernorm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[4096]},\"model.layers.23.mlp.down_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.23.mlp.gate_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.23.mlp.up_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.23.post_attention_layernorm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[4096]},\"model.layers.23.self_attn.k_norm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[256]},\"model.layers.23.self_attn.k_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[2097152,1]},\"model.layers.23.self_attn.o_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[8388608,1]},\"model.layers.23.self_attn.q_norm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[256]},\"model.layers.23.self_attn.q_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[16777216,1]},\"model.layers.23.self_attn.v_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[2097152,1]},\"model.layers.24.input_layernorm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[4096]},\"model.layers.24.linear_attn.A_log\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[32]},\"model.layers.24.linear_attn.conv1d.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[8192,1,4]},\"model.layers.24.linear_attn.dt_bias\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[32]},\"model.layers.24.linear_attn.in_proj_a.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[65536,1]},\"model.layers.24.linear_attn.in_proj_b.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[65536,1]},\"model.layers.24.linear_attn.in_proj_qkv.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[16777216,1]},\"model.layers.24.linear_attn.in_proj_z.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[8388608,1]},\"model.layers.24.linear_attn.norm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[128]},\"model.layers.24.linear_attn.out_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[8388608,1]},\"model.layers.24.mlp.down_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.24.mlp.gate_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.24.mlp.up_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.24.post_attention_layernorm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[4096]},\"model.layers.25.input_layernorm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[4096]},\"model.layers.25.linear_attn.A_log\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[32]},\"model.layers.25.linear_attn.conv1d.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[8192,1,4]},\"model.layers.25.linear_attn.dt_bias\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[32]},\"model.layers.25.linear_attn.in_proj_a.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[65536,1]},\"model.layers.25.linear_attn.in_proj_b.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[65536,1]},\"model.layers.25.linear_attn.in_proj_qkv.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[16777216,1]},\"model.layers.25.linear_attn.in_proj_z.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[8388608,1]},\"model.layers.25.linear_attn.norm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[128]},\"model.layers.25.linear_attn.out_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[8388608,1]},\"model.layers.25.mlp.down_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.25.mlp.gate_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.25.mlp.up_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.25.post_attention_layernorm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[4096]},\"model.layers.26.input_layernorm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[4096]},\"model.layers.26.linear_attn.A_log\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[32]},\"model.layers.26.linear_attn.conv1d.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[8192,1,4]},\"model.layers.26.linear_attn.dt_bias\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[32]},\"model.layers.26.linear_attn.in_proj_a.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[65536,1]},\"model.layers.26.linear_attn.in_proj_b.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[65536,1]},\"model.layers.26.linear_attn.in_proj_qkv.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[16777216,1]},\"model.layers.26.linear_attn.in_proj_z.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[8388608,1]},\"model.layers.26.linear_attn.norm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[128]},\"model.layers.26.linear_attn.out_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[8388608,1]},\"model.layers.26.mlp.down_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.26.mlp.gate_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.26.mlp.up_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.26.post_attention_layernorm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[4096]},\"model.layers.27.input_layernorm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[4096]},\"model.layers.27.mlp.down_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.27.mlp.gate_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.27.mlp.up_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.27.post_attention_layernorm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[4096]},\"model.layers.27.self_attn.k_norm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[256]},\"model.layers.27.self_attn.k_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[2097152,1]},\"model.layers.27.self_attn.o_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[8388608,1]},\"model.layers.27.self_attn.q_norm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[256]},\"model.layers.27.self_attn.q_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[16777216,1]},\"model.layers.27.self_attn.v_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[2097152,1]},\"model.layers.28.input_layernorm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[4096]},\"model.layers.28.linear_attn.A_log\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[32]},\"model.layers.28.linear_attn.conv1d.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[8192,1,4]},\"model.layers.28.linear_attn.dt_bias\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[32]},\"model.layers.28.linear_attn.in_proj_a.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[65536,1]},\"model.layers.28.linear_attn.in_proj_b.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[65536,1]},\"model.layers.28.linear_attn.in_proj_qkv.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[16777216,1]},\"model.layers.28.linear_attn.in_proj_z.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[8388608,1]},\"model.layers.28.linear_attn.norm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[128]},\"model.layers.28.linear_attn.out_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[8388608,1]},\"model.layers.28.mlp.down_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.28.mlp.gate_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.28.mlp.up_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.28.post_attention_layernorm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[4096]},\"model.layers.29.input_layernorm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[4096]},\"model.layers.29.linear_attn.A_log\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[32]},\"model.layers.29.linear_attn.conv1d.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[8192,1,4]},\"model.layers.29.linear_attn.dt_bias\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[32]},\"model.layers.29.linear_attn.in_proj_a.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[65536,1]},\"model.layers.29.linear_attn.in_proj_b.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[65536,1]},\"model.layers.29.linear_attn.in_proj_qkv.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[16777216,1]},\"model.layers.29.linear_attn.in_proj_z.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[8388608,1]},\"model.layers.29.linear_attn.norm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[128]},\"model.layers.29.linear_attn.out_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[8388608,1]},\"model.layers.29.mlp.down_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.29.mlp.gate_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.29.mlp.up_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.29.post_attention_layernorm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[4096]},\"model.layers.3.input_layernorm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[4096]},\"model.layers.3.mlp.down_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.3.mlp.gate_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.3.mlp.up_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.3.post_attention_layernorm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[4096]},\"model.layers.3.self_attn.k_norm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[256]},\"model.layers.3.self_attn.k_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[2097152,1]},\"model.layers.3.self_attn.o_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[8388608,1]},\"model.layers.3.self_attn.q_norm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[256]},\"model.layers.3.self_attn.q_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[16777216,1]},\"model.layers.3.self_attn.v_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[2097152,1]},\"model.layers.30.input_layernorm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[4096]},\"model.layers.30.linear_attn.A_log\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[32]},\"model.layers.30.linear_attn.conv1d.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[8192,1,4]},\"model.layers.30.linear_attn.dt_bias\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[32]},\"model.layers.30.linear_attn.in_proj_a.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[65536,1]},\"model.layers.30.linear_attn.in_proj_b.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[65536,1]},\"model.layers.30.linear_attn.in_proj_qkv.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[16777216,1]},\"model.layers.30.linear_attn.in_proj_z.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[8388608,1]},\"model.layers.30.linear_attn.norm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[128]},\"model.layers.30.linear_attn.out_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[8388608,1]},\"model.layers.30.mlp.down_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.30.mlp.gate_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.30.mlp.up_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.30.post_attention_layernorm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[4096]},\"model.layers.31.input_layernorm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[4096]},\"model.layers.31.mlp.down_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.31.mlp.gate_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.31.mlp.up_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.31.post_attention_layernorm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[4096]},\"model.layers.31.self_attn.k_norm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[256]},\"model.layers.31.self_attn.k_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[2097152,1]},\"model.layers.31.self_attn.o_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[8388608,1]},\"model.layers.31.self_attn.q_norm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[256]},\"model.layers.31.self_attn.q_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[16777216,1]},\"model.layers.31.self_attn.v_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[2097152,1]},\"model.layers.4.input_layernorm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[4096]},\"model.layers.4.linear_attn.A_log\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[32]},\"model.layers.4.linear_attn.conv1d.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[8192,1,4]},\"model.layers.4.linear_attn.dt_bias\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[32]},\"model.layers.4.linear_attn.in_proj_a.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[65536,1]},\"model.layers.4.linear_attn.in_proj_b.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[65536,1]},\"model.layers.4.linear_attn.in_proj_qkv.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[16777216,1]},\"model.layers.4.linear_attn.in_proj_z.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[8388608,1]},\"model.layers.4.linear_attn.norm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[128]},\"model.layers.4.linear_attn.out_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[8388608,1]},\"model.layers.4.mlp.down_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.4.mlp.gate_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.4.mlp.up_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.4.post_attention_layernorm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[4096]},\"model.layers.5.input_layernorm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[4096]},\"model.layers.5.linear_attn.A_log\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[32]},\"model.layers.5.linear_attn.conv1d.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[8192,1,4]},\"model.layers.5.linear_attn.dt_bias\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[32]},\"model.layers.5.linear_attn.in_proj_a.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[65536,1]},\"model.layers.5.linear_attn.in_proj_b.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[65536,1]},\"model.layers.5.linear_attn.in_proj_qkv.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[16777216,1]},\"model.layers.5.linear_attn.in_proj_z.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[8388608,1]},\"model.layers.5.linear_attn.norm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[128]},\"model.layers.5.linear_attn.out_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[8388608,1]},\"model.layers.5.mlp.down_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.5.mlp.gate_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.5.mlp.up_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.5.post_attention_layernorm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[4096]},\"model.layers.6.input_layernorm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[4096]},\"model.layers.6.linear_attn.A_log\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[32]},\"model.layers.6.linear_attn.conv1d.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[8192,1,4]},\"model.layers.6.linear_attn.dt_bias\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[32]},\"model.layers.6.linear_attn.in_proj_a.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[65536,1]},\"model.layers.6.linear_attn.in_proj_b.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[65536,1]},\"model.layers.6.linear_attn.in_proj_qkv.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[16777216,1]},\"model.layers.6.linear_attn.in_proj_z.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[8388608,1]},\"model.layers.6.linear_attn.norm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[128]},\"model.layers.6.linear_attn.out_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[8388608,1]},\"model.layers.6.mlp.down_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.6.mlp.gate_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.6.mlp.up_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.6.post_attention_layernorm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[4096]},\"model.layers.7.input_layernorm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[4096]},\"model.layers.7.mlp.down_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.7.mlp.gate_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.7.mlp.up_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.7.post_attention_layernorm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[4096]},\"model.layers.7.self_attn.k_norm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[256]},\"model.layers.7.self_attn.k_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[2097152,1]},\"model.layers.7.self_attn.o_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[8388608,1]},\"model.layers.7.self_attn.q_norm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[256]},\"model.layers.7.self_attn.q_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[16777216,1]},\"model.layers.7.self_attn.v_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[2097152,1]},\"model.layers.8.input_layernorm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[4096]},\"model.layers.8.linear_attn.A_log\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[32]},\"model.layers.8.linear_attn.conv1d.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[8192,1,4]},\"model.layers.8.linear_attn.dt_bias\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[32]},\"model.layers.8.linear_attn.in_proj_a.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[65536,1]},\"model.layers.8.linear_attn.in_proj_b.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[65536,1]},\"model.layers.8.linear_attn.in_proj_qkv.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[16777216,1]},\"model.layers.8.linear_attn.in_proj_z.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[8388608,1]},\"model.layers.8.linear_attn.norm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[128]},\"model.layers.8.linear_attn.out_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[8388608,1]},\"model.layers.8.mlp.down_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.8.mlp.gate_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.8.mlp.up_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.8.post_attention_layernorm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[4096]},\"model.layers.9.input_layernorm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[4096]},\"model.layers.9.linear_attn.A_log\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[32]},\"model.layers.9.linear_attn.conv1d.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[8192,1,4]},\"model.layers.9.linear_attn.dt_bias\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[32]},\"model.layers.9.linear_attn.in_proj_a.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[65536,1]},\"model.layers.9.linear_attn.in_proj_b.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[65536,1]},\"model.layers.9.linear_attn.in_proj_qkv.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[16777216,1]},\"model.layers.9.linear_attn.in_proj_z.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[8388608,1]},\"model.layers.9.linear_attn.norm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[128]},\"model.layers.9.linear_attn.out_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[8388608,1]},\"model.layers.9.mlp.down_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.9.mlp.gate_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.9.mlp.up_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.9.post_attention_layernorm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[4096]},\"model.norm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[4096]}},\"pid\":351,\"quantization_tensors\":{\"model.layers.0.linear_attn.in_proj_a.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[2048]},\"model.layers.0.linear_attn.in_proj_a.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.0.linear_attn.in_proj_a.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.0.linear_attn.in_proj_a.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[8]},\"model.layers.0.linear_attn.in_proj_a.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.0.linear_attn.in_proj_b.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[2048]},\"model.layers.0.linear_attn.in_proj_b.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.0.linear_attn.in_proj_b.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.0.linear_attn.in_proj_b.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[8]},\"model.layers.0.linear_attn.in_proj_b.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.0.linear_attn.in_proj_qkv.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[524288]},\"model.layers.0.linear_attn.in_proj_qkv.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.0.linear_attn.in_proj_qkv.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.0.linear_attn.in_proj_qkv.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[2048]},\"model.layers.0.linear_attn.in_proj_qkv.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.0.linear_attn.in_proj_z.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[262144]},\"model.layers.0.linear_attn.in_proj_z.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.0.linear_attn.in_proj_z.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.0.linear_attn.in_proj_z.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[1024]},\"model.layers.0.linear_attn.in_proj_z.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.0.linear_attn.out_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[262144]},\"model.layers.0.linear_attn.out_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.0.linear_attn.out_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.0.linear_attn.out_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[1024]},\"model.layers.0.linear_attn.out_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.0.mlp.down_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.0.mlp.down_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.0.mlp.down_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.0.mlp.down_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.0.mlp.down_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.0.mlp.gate_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.0.mlp.gate_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.0.mlp.gate_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.0.mlp.gate_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.0.mlp.gate_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.0.mlp.up_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.0.mlp.up_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.0.mlp.up_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.0.mlp.up_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.0.mlp.up_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.1.linear_attn.in_proj_a.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[2048]},\"model.layers.1.linear_attn.in_proj_a.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.1.linear_attn.in_proj_a.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.1.linear_attn.in_proj_a.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[8]},\"model.layers.1.linear_attn.in_proj_a.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.1.linear_attn.in_proj_b.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[2048]},\"model.layers.1.linear_attn.in_proj_b.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.1.linear_attn.in_proj_b.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.1.linear_attn.in_proj_b.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[8]},\"model.layers.1.linear_attn.in_proj_b.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.1.linear_attn.in_proj_qkv.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[524288]},\"model.layers.1.linear_attn.in_proj_qkv.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.1.linear_attn.in_proj_qkv.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.1.linear_attn.in_proj_qkv.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[2048]},\"model.layers.1.linear_attn.in_proj_qkv.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.1.linear_attn.in_proj_z.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[262144]},\"model.layers.1.linear_attn.in_proj_z.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.1.linear_attn.in_proj_z.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.1.linear_attn.in_proj_z.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[1024]},\"model.layers.1.linear_attn.in_proj_z.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.1.linear_attn.out_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[262144]},\"model.layers.1.linear_attn.out_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.1.linear_attn.out_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.1.linear_attn.out_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[1024]},\"model.layers.1.linear_attn.out_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.1.mlp.down_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.1.mlp.down_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.1.mlp.down_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.1.mlp.down_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.1.mlp.down_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.1.mlp.gate_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.1.mlp.gate_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.1.mlp.gate_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.1.mlp.gate_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.1.mlp.gate_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.1.mlp.up_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.1.mlp.up_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.1.mlp.up_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.1.mlp.up_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.1.mlp.up_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.10.linear_attn.in_proj_a.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[2048]},\"model.layers.10.linear_attn.in_proj_a.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.10.linear_attn.in_proj_a.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.10.linear_attn.in_proj_a.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[8]},\"model.layers.10.linear_attn.in_proj_a.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.10.linear_attn.in_proj_b.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[2048]},\"model.layers.10.linear_attn.in_proj_b.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.10.linear_attn.in_proj_b.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.10.linear_attn.in_proj_b.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[8]},\"model.layers.10.linear_attn.in_proj_b.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.10.linear_attn.in_proj_qkv.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[524288]},\"model.layers.10.linear_attn.in_proj_qkv.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.10.linear_attn.in_proj_qkv.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.10.linear_attn.in_proj_qkv.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[2048]},\"model.layers.10.linear_attn.in_proj_qkv.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.10.linear_attn.in_proj_z.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[262144]},\"model.layers.10.linear_attn.in_proj_z.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.10.linear_attn.in_proj_z.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.10.linear_attn.in_proj_z.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[1024]},\"model.layers.10.linear_attn.in_proj_z.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.10.linear_attn.out_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[262144]},\"model.layers.10.linear_attn.out_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.10.linear_attn.out_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.10.linear_attn.out_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[1024]},\"model.layers.10.linear_attn.out_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.10.mlp.down_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.10.mlp.down_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.10.mlp.down_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.10.mlp.down_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.10.mlp.down_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.10.mlp.gate_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.10.mlp.gate_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.10.mlp.gate_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.10.mlp.gate_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.10.mlp.gate_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.10.mlp.up_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.10.mlp.up_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.10.mlp.up_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.10.mlp.up_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.10.mlp.up_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.11.mlp.down_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.11.mlp.down_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.11.mlp.down_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.11.mlp.down_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.11.mlp.down_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.11.mlp.gate_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.11.mlp.gate_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.11.mlp.gate_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.11.mlp.gate_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.11.mlp.gate_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.11.mlp.up_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.11.mlp.up_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.11.mlp.up_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.11.mlp.up_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.11.mlp.up_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.11.self_attn.k_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[65536]},\"model.layers.11.self_attn.k_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.11.self_attn.k_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.11.self_attn.k_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.11.self_attn.k_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.11.self_attn.o_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[262144]},\"model.layers.11.self_attn.o_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.11.self_attn.o_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.11.self_attn.o_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[1024]},\"model.layers.11.self_attn.o_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.11.self_attn.q_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[524288]},\"model.layers.11.self_attn.q_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.11.self_attn.q_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.11.self_attn.q_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[2048]},\"model.layers.11.self_attn.q_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.11.self_attn.v_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[65536]},\"model.layers.11.self_attn.v_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.11.self_attn.v_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.11.self_attn.v_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.11.self_attn.v_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.12.linear_attn.in_proj_a.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[2048]},\"model.layers.12.linear_attn.in_proj_a.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.12.linear_attn.in_proj_a.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.12.linear_attn.in_proj_a.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[8]},\"model.layers.12.linear_attn.in_proj_a.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.12.linear_attn.in_proj_b.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[2048]},\"model.layers.12.linear_attn.in_proj_b.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.12.linear_attn.in_proj_b.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.12.linear_attn.in_proj_b.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[8]},\"model.layers.12.linear_attn.in_proj_b.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.12.linear_attn.in_proj_qkv.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[524288]},\"model.layers.12.linear_attn.in_proj_qkv.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.12.linear_attn.in_proj_qkv.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.12.linear_attn.in_proj_qkv.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[2048]},\"model.layers.12.linear_attn.in_proj_qkv.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.12.linear_attn.in_proj_z.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[262144]},\"model.layers.12.linear_attn.in_proj_z.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.12.linear_attn.in_proj_z.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.12.linear_attn.in_proj_z.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[1024]},\"model.layers.12.linear_attn.in_proj_z.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.12.linear_attn.out_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[262144]},\"model.layers.12.linear_attn.out_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.12.linear_attn.out_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.12.linear_attn.out_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[1024]},\"model.layers.12.linear_attn.out_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.12.mlp.down_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.12.mlp.down_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.12.mlp.down_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.12.mlp.down_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.12.mlp.down_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.12.mlp.gate_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.12.mlp.gate_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.12.mlp.gate_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.12.mlp.gate_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.12.mlp.gate_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.12.mlp.up_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.12.mlp.up_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.12.mlp.up_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.12.mlp.up_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.12.mlp.up_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.13.linear_attn.in_proj_a.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[2048]},\"model.layers.13.linear_attn.in_proj_a.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.13.linear_attn.in_proj_a.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.13.linear_attn.in_proj_a.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[8]},\"model.layers.13.linear_attn.in_proj_a.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.13.linear_attn.in_proj_b.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[2048]},\"model.layers.13.linear_attn.in_proj_b.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.13.linear_attn.in_proj_b.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.13.linear_attn.in_proj_b.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[8]},\"model.layers.13.linear_attn.in_proj_b.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.13.linear_attn.in_proj_qkv.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[524288]},\"model.layers.13.linear_attn.in_proj_qkv.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.13.linear_attn.in_proj_qkv.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.13.linear_attn.in_proj_qkv.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[2048]},\"model.layers.13.linear_attn.in_proj_qkv.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.13.linear_attn.in_proj_z.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[262144]},\"model.layers.13.linear_attn.in_proj_z.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.13.linear_attn.in_proj_z.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.13.linear_attn.in_proj_z.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[1024]},\"model.layers.13.linear_attn.in_proj_z.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.13.linear_attn.out_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[262144]},\"model.layers.13.linear_attn.out_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.13.linear_attn.out_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.13.linear_attn.out_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[1024]},\"model.layers.13.linear_attn.out_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.13.mlp.down_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.13.mlp.down_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.13.mlp.down_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.13.mlp.down_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.13.mlp.down_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.13.mlp.gate_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.13.mlp.gate_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.13.mlp.gate_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.13.mlp.gate_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.13.mlp.gate_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.13.mlp.up_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.13.mlp.up_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.13.mlp.up_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.13.mlp.up_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.13.mlp.up_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.14.linear_attn.in_proj_a.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[2048]},\"model.layers.14.linear_attn.in_proj_a.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.14.linear_attn.in_proj_a.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.14.linear_attn.in_proj_a.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[8]},\"model.layers.14.linear_attn.in_proj_a.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.14.linear_attn.in_proj_b.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[2048]},\"model.layers.14.linear_attn.in_proj_b.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.14.linear_attn.in_proj_b.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.14.linear_attn.in_proj_b.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[8]},\"model.layers.14.linear_attn.in_proj_b.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.14.linear_attn.in_proj_qkv.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[524288]},\"model.layers.14.linear_attn.in_proj_qkv.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.14.linear_attn.in_proj_qkv.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.14.linear_attn.in_proj_qkv.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[2048]},\"model.layers.14.linear_attn.in_proj_qkv.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.14.linear_attn.in_proj_z.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[262144]},\"model.layers.14.linear_attn.in_proj_z.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.14.linear_attn.in_proj_z.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.14.linear_attn.in_proj_z.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[1024]},\"model.layers.14.linear_attn.in_proj_z.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.14.linear_attn.out_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[262144]},\"model.layers.14.linear_attn.out_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.14.linear_attn.out_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.14.linear_attn.out_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[1024]},\"model.layers.14.linear_attn.out_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.14.mlp.down_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.14.mlp.down_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.14.mlp.down_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.14.mlp.down_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.14.mlp.down_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.14.mlp.gate_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.14.mlp.gate_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.14.mlp.gate_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.14.mlp.gate_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.14.mlp.gate_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.14.mlp.up_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.14.mlp.up_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.14.mlp.up_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.14.mlp.up_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.14.mlp.up_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.15.mlp.down_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.15.mlp.down_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.15.mlp.down_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.15.mlp.down_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.15.mlp.down_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.15.mlp.gate_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.15.mlp.gate_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.15.mlp.gate_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.15.mlp.gate_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.15.mlp.gate_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.15.mlp.up_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.15.mlp.up_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.15.mlp.up_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.15.mlp.up_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.15.mlp.up_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.15.self_attn.k_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[65536]},\"model.layers.15.self_attn.k_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.15.self_attn.k_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.15.self_attn.k_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.15.self_attn.k_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.15.self_attn.o_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[262144]},\"model.layers.15.self_attn.o_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.15.self_attn.o_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.15.self_attn.o_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[1024]},\"model.layers.15.self_attn.o_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.15.self_attn.q_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[524288]},\"model.layers.15.self_attn.q_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.15.self_attn.q_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.15.self_attn.q_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[2048]},\"model.layers.15.self_attn.q_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.15.self_attn.v_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[65536]},\"model.layers.15.self_attn.v_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.15.self_attn.v_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.15.self_attn.v_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.15.self_attn.v_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.16.linear_attn.in_proj_a.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[2048]},\"model.layers.16.linear_attn.in_proj_a.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.16.linear_attn.in_proj_a.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.16.linear_attn.in_proj_a.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[8]},\"model.layers.16.linear_attn.in_proj_a.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.16.linear_attn.in_proj_b.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[2048]},\"model.layers.16.linear_attn.in_proj_b.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.16.linear_attn.in_proj_b.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.16.linear_attn.in_proj_b.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[8]},\"model.layers.16.linear_attn.in_proj_b.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.16.linear_attn.in_proj_qkv.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[524288]},\"model.layers.16.linear_attn.in_proj_qkv.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.16.linear_attn.in_proj_qkv.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.16.linear_attn.in_proj_qkv.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[2048]},\"model.layers.16.linear_attn.in_proj_qkv.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.16.linear_attn.in_proj_z.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[262144]},\"model.layers.16.linear_attn.in_proj_z.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.16.linear_attn.in_proj_z.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.16.linear_attn.in_proj_z.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[1024]},\"model.layers.16.linear_attn.in_proj_z.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.16.linear_attn.out_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[262144]},\"model.layers.16.linear_attn.out_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.16.linear_attn.out_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.16.linear_attn.out_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[1024]},\"model.layers.16.linear_attn.out_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.16.mlp.down_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.16.mlp.down_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.16.mlp.down_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.16.mlp.down_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.16.mlp.down_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.16.mlp.gate_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.16.mlp.gate_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.16.mlp.gate_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.16.mlp.gate_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.16.mlp.gate_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.16.mlp.up_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.16.mlp.up_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.16.mlp.up_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.16.mlp.up_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.16.mlp.up_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.17.linear_attn.in_proj_a.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[2048]},\"model.layers.17.linear_attn.in_proj_a.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.17.linear_attn.in_proj_a.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.17.linear_attn.in_proj_a.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[8]},\"model.layers.17.linear_attn.in_proj_a.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.17.linear_attn.in_proj_b.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[2048]},\"model.layers.17.linear_attn.in_proj_b.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.17.linear_attn.in_proj_b.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.17.linear_attn.in_proj_b.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[8]},\"model.layers.17.linear_attn.in_proj_b.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.17.linear_attn.in_proj_qkv.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[524288]},\"model.layers.17.linear_attn.in_proj_qkv.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.17.linear_attn.in_proj_qkv.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.17.linear_attn.in_proj_qkv.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[2048]},\"model.layers.17.linear_attn.in_proj_qkv.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.17.linear_attn.in_proj_z.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[262144]},\"model.layers.17.linear_attn.in_proj_z.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.17.linear_attn.in_proj_z.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.17.linear_attn.in_proj_z.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[1024]},\"model.layers.17.linear_attn.in_proj_z.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.17.linear_attn.out_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[262144]},\"model.layers.17.linear_attn.out_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.17.linear_attn.out_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.17.linear_attn.out_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[1024]},\"model.layers.17.linear_attn.out_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.17.mlp.down_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.17.mlp.down_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.17.mlp.down_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.17.mlp.down_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.17.mlp.down_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.17.mlp.gate_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.17.mlp.gate_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.17.mlp.gate_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.17.mlp.gate_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.17.mlp.gate_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.17.mlp.up_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.17.mlp.up_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.17.mlp.up_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.17.mlp.up_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.17.mlp.up_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.18.linear_attn.in_proj_a.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[2048]},\"model.layers.18.linear_attn.in_proj_a.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.18.linear_attn.in_proj_a.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.18.linear_attn.in_proj_a.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[8]},\"model.layers.18.linear_attn.in_proj_a.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.18.linear_attn.in_proj_b.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[2048]},\"model.layers.18.linear_attn.in_proj_b.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.18.linear_attn.in_proj_b.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.18.linear_attn.in_proj_b.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[8]},\"model.layers.18.linear_attn.in_proj_b.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.18.linear_attn.in_proj_qkv.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[524288]},\"model.layers.18.linear_attn.in_proj_qkv.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.18.linear_attn.in_proj_qkv.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.18.linear_attn.in_proj_qkv.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[2048]},\"model.layers.18.linear_attn.in_proj_qkv.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.18.linear_attn.in_proj_z.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[262144]},\"model.layers.18.linear_attn.in_proj_z.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.18.linear_attn.in_proj_z.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.18.linear_attn.in_proj_z.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[1024]},\"model.layers.18.linear_attn.in_proj_z.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.18.linear_attn.out_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[262144]},\"model.layers.18.linear_attn.out_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.18.linear_attn.out_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.18.linear_attn.out_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[1024]},\"model.layers.18.linear_attn.out_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.18.mlp.down_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.18.mlp.down_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.18.mlp.down_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.18.mlp.down_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.18.mlp.down_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.18.mlp.gate_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.18.mlp.gate_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.18.mlp.gate_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.18.mlp.gate_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.18.mlp.gate_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.18.mlp.up_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.18.mlp.up_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.18.mlp.up_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.18.mlp.up_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.18.mlp.up_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.19.mlp.down_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.19.mlp.down_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.19.mlp.down_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.19.mlp.down_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.19.mlp.down_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.19.mlp.gate_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.19.mlp.gate_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.19.mlp.gate_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.19.mlp.gate_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.19.mlp.gate_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.19.mlp.up_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.19.mlp.up_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.19.mlp.up_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.19.mlp.up_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.19.mlp.up_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.19.self_attn.k_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[65536]},\"model.layers.19.self_attn.k_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.19.self_attn.k_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.19.self_attn.k_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.19.self_attn.k_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.19.self_attn.o_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[262144]},\"model.layers.19.self_attn.o_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.19.self_attn.o_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.19.self_attn.o_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[1024]},\"model.layers.19.self_attn.o_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.19.self_attn.q_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[524288]},\"model.layers.19.self_attn.q_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.19.self_attn.q_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.19.self_attn.q_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[2048]},\"model.layers.19.self_attn.q_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.19.self_attn.v_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[65536]},\"model.layers.19.self_attn.v_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.19.self_attn.v_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.19.self_attn.v_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.19.self_attn.v_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.2.linear_attn.in_proj_a.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[2048]},\"model.layers.2.linear_attn.in_proj_a.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.2.linear_attn.in_proj_a.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.2.linear_attn.in_proj_a.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[8]},\"model.layers.2.linear_attn.in_proj_a.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.2.linear_attn.in_proj_b.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[2048]},\"model.layers.2.linear_attn.in_proj_b.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.2.linear_attn.in_proj_b.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.2.linear_attn.in_proj_b.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[8]},\"model.layers.2.linear_attn.in_proj_b.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.2.linear_attn.in_proj_qkv.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[524288]},\"model.layers.2.linear_attn.in_proj_qkv.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.2.linear_attn.in_proj_qkv.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.2.linear_attn.in_proj_qkv.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[2048]},\"model.layers.2.linear_attn.in_proj_qkv.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.2.linear_attn.in_proj_z.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[262144]},\"model.layers.2.linear_attn.in_proj_z.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.2.linear_attn.in_proj_z.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.2.linear_attn.in_proj_z.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[1024]},\"model.layers.2.linear_attn.in_proj_z.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.2.linear_attn.out_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[262144]},\"model.layers.2.linear_attn.out_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.2.linear_attn.out_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.2.linear_attn.out_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[1024]},\"model.layers.2.linear_attn.out_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.2.mlp.down_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.2.mlp.down_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.2.mlp.down_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.2.mlp.down_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.2.mlp.down_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.2.mlp.gate_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.2.mlp.gate_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.2.mlp.gate_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.2.mlp.gate_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.2.mlp.gate_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.2.mlp.up_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.2.mlp.up_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.2.mlp.up_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.2.mlp.up_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.2.mlp.up_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.20.linear_attn.in_proj_a.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[2048]},\"model.layers.20.linear_attn.in_proj_a.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.20.linear_attn.in_proj_a.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.20.linear_attn.in_proj_a.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[8]},\"model.layers.20.linear_attn.in_proj_a.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.20.linear_attn.in_proj_b.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[2048]},\"model.layers.20.linear_attn.in_proj_b.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.20.linear_attn.in_proj_b.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.20.linear_attn.in_proj_b.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[8]},\"model.layers.20.linear_attn.in_proj_b.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.20.linear_attn.in_proj_qkv.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[524288]},\"model.layers.20.linear_attn.in_proj_qkv.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.20.linear_attn.in_proj_qkv.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.20.linear_attn.in_proj_qkv.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[2048]},\"model.layers.20.linear_attn.in_proj_qkv.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.20.linear_attn.in_proj_z.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[262144]},\"model.layers.20.linear_attn.in_proj_z.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.20.linear_attn.in_proj_z.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.20.linear_attn.in_proj_z.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[1024]},\"model.layers.20.linear_attn.in_proj_z.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.20.linear_attn.out_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[262144]},\"model.layers.20.linear_attn.out_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.20.linear_attn.out_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.20.linear_attn.out_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[1024]},\"model.layers.20.linear_attn.out_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.20.mlp.down_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.20.mlp.down_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.20.mlp.down_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.20.mlp.down_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.20.mlp.down_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.20.mlp.gate_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.20.mlp.gate_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.20.mlp.gate_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.20.mlp.gate_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.20.mlp.gate_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.20.mlp.up_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.20.mlp.up_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.20.mlp.up_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.20.mlp.up_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.20.mlp.up_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.21.linear_attn.in_proj_a.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[2048]},\"model.layers.21.linear_attn.in_proj_a.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.21.linear_attn.in_proj_a.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.21.linear_attn.in_proj_a.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[8]},\"model.layers.21.linear_attn.in_proj_a.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.21.linear_attn.in_proj_b.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[2048]},\"model.layers.21.linear_attn.in_proj_b.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.21.linear_attn.in_proj_b.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.21.linear_attn.in_proj_b.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[8]},\"model.layers.21.linear_attn.in_proj_b.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.21.linear_attn.in_proj_qkv.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[524288]},\"model.layers.21.linear_attn.in_proj_qkv.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.21.linear_attn.in_proj_qkv.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.21.linear_attn.in_proj_qkv.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[2048]},\"model.layers.21.linear_attn.in_proj_qkv.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.21.linear_attn.in_proj_z.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[262144]},\"model.layers.21.linear_attn.in_proj_z.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.21.linear_attn.in_proj_z.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.21.linear_attn.in_proj_z.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[1024]},\"model.layers.21.linear_attn.in_proj_z.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.21.linear_attn.out_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[262144]},\"model.layers.21.linear_attn.out_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.21.linear_attn.out_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.21.linear_attn.out_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[1024]},\"model.layers.21.linear_attn.out_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.21.mlp.down_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.21.mlp.down_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.21.mlp.down_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.21.mlp.down_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.21.mlp.down_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.21.mlp.gate_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.21.mlp.gate_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.21.mlp.gate_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.21.mlp.gate_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.21.mlp.gate_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.21.mlp.up_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.21.mlp.up_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.21.mlp.up_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.21.mlp.up_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.21.mlp.up_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.22.linear_attn.in_proj_a.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[2048]},\"model.layers.22.linear_attn.in_proj_a.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.22.linear_attn.in_proj_a.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.22.linear_attn.in_proj_a.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[8]},\"model.layers.22.linear_attn.in_proj_a.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.22.linear_attn.in_proj_b.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[2048]},\"model.layers.22.linear_attn.in_proj_b.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.22.linear_attn.in_proj_b.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.22.linear_attn.in_proj_b.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[8]},\"model.layers.22.linear_attn.in_proj_b.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.22.linear_attn.in_proj_qkv.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[524288]},\"model.layers.22.linear_attn.in_proj_qkv.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.22.linear_attn.in_proj_qkv.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.22.linear_attn.in_proj_qkv.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[2048]},\"model.layers.22.linear_attn.in_proj_qkv.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.22.linear_attn.in_proj_z.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[262144]},\"model.layers.22.linear_attn.in_proj_z.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.22.linear_attn.in_proj_z.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.22.linear_attn.in_proj_z.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[1024]},\"model.layers.22.linear_attn.in_proj_z.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.22.linear_attn.out_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[262144]},\"model.layers.22.linear_attn.out_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.22.linear_attn.out_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.22.linear_attn.out_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[1024]},\"model.layers.22.linear_attn.out_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.22.mlp.down_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.22.mlp.down_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.22.mlp.down_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.22.mlp.down_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.22.mlp.down_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.22.mlp.gate_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.22.mlp.gate_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.22.mlp.gate_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.22.mlp.gate_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.22.mlp.gate_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.22.mlp.up_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.22.mlp.up_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.22.mlp.up_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.22.mlp.up_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.22.mlp.up_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.23.mlp.down_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.23.mlp.down_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.23.mlp.down_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.23.mlp.down_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.23.mlp.down_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.23.mlp.gate_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.23.mlp.gate_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.23.mlp.gate_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.23.mlp.gate_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.23.mlp.gate_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.23.mlp.up_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.23.mlp.up_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.23.mlp.up_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.23.mlp.up_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.23.mlp.up_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.23.self_attn.k_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[65536]},\"model.layers.23.self_attn.k_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.23.self_attn.k_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.23.self_attn.k_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.23.self_attn.k_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.23.self_attn.o_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[262144]},\"model.layers.23.self_attn.o_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.23.self_attn.o_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.23.self_attn.o_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[1024]},\"model.layers.23.self_attn.o_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.23.self_attn.q_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[524288]},\"model.layers.23.self_attn.q_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.23.self_attn.q_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.23.self_attn.q_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[2048]},\"model.layers.23.self_attn.q_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.23.self_attn.v_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[65536]},\"model.layers.23.self_attn.v_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.23.self_attn.v_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.23.self_attn.v_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.23.self_attn.v_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.24.linear_attn.in_proj_a.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[2048]},\"model.layers.24.linear_attn.in_proj_a.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.24.linear_attn.in_proj_a.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.24.linear_attn.in_proj_a.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[8]},\"model.layers.24.linear_attn.in_proj_a.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.24.linear_attn.in_proj_b.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[2048]},\"model.layers.24.linear_attn.in_proj_b.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.24.linear_attn.in_proj_b.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.24.linear_attn.in_proj_b.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[8]},\"model.layers.24.linear_attn.in_proj_b.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.24.linear_attn.in_proj_qkv.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[524288]},\"model.layers.24.linear_attn.in_proj_qkv.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.24.linear_attn.in_proj_qkv.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.24.linear_attn.in_proj_qkv.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[2048]},\"model.layers.24.linear_attn.in_proj_qkv.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.24.linear_attn.in_proj_z.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[262144]},\"model.layers.24.linear_attn.in_proj_z.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.24.linear_attn.in_proj_z.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.24.linear_attn.in_proj_z.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[1024]},\"model.layers.24.linear_attn.in_proj_z.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.24.linear_attn.out_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[262144]},\"model.layers.24.linear_attn.out_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.24.linear_attn.out_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.24.linear_attn.out_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[1024]},\"model.layers.24.linear_attn.out_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.24.mlp.down_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.24.mlp.down_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.24.mlp.down_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.24.mlp.down_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.24.mlp.down_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.24.mlp.gate_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.24.mlp.gate_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.24.mlp.gate_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.24.mlp.gate_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.24.mlp.gate_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.24.mlp.up_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.24.mlp.up_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.24.mlp.up_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.24.mlp.up_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.24.mlp.up_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.25.linear_attn.in_proj_a.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[2048]},\"model.layers.25.linear_attn.in_proj_a.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.25.linear_attn.in_proj_a.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.25.linear_attn.in_proj_a.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[8]},\"model.layers.25.linear_attn.in_proj_a.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.25.linear_attn.in_proj_b.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[2048]},\"model.layers.25.linear_attn.in_proj_b.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.25.linear_attn.in_proj_b.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.25.linear_attn.in_proj_b.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[8]},\"model.layers.25.linear_attn.in_proj_b.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.25.linear_attn.in_proj_qkv.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[524288]},\"model.layers.25.linear_attn.in_proj_qkv.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.25.linear_attn.in_proj_qkv.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.25.linear_attn.in_proj_qkv.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[2048]},\"model.layers.25.linear_attn.in_proj_qkv.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.25.linear_attn.in_proj_z.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[262144]},\"model.layers.25.linear_attn.in_proj_z.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.25.linear_attn.in_proj_z.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.25.linear_attn.in_proj_z.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[1024]},\"model.layers.25.linear_attn.in_proj_z.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.25.linear_attn.out_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[262144]},\"model.layers.25.linear_attn.out_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.25.linear_attn.out_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.25.linear_attn.out_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[1024]},\"model.layers.25.linear_attn.out_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.25.mlp.down_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.25.mlp.down_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.25.mlp.down_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.25.mlp.down_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.25.mlp.down_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.25.mlp.gate_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.25.mlp.gate_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.25.mlp.gate_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.25.mlp.gate_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.25.mlp.gate_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.25.mlp.up_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.25.mlp.up_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.25.mlp.up_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.25.mlp.up_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.25.mlp.up_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.26.linear_attn.in_proj_a.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[2048]},\"model.layers.26.linear_attn.in_proj_a.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.26.linear_attn.in_proj_a.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.26.linear_attn.in_proj_a.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[8]},\"model.layers.26.linear_attn.in_proj_a.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.26.linear_attn.in_proj_b.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[2048]},\"model.layers.26.linear_attn.in_proj_b.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.26.linear_attn.in_proj_b.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.26.linear_attn.in_proj_b.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[8]},\"model.layers.26.linear_attn.in_proj_b.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.26.linear_attn.in_proj_qkv.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[524288]},\"model.layers.26.linear_attn.in_proj_qkv.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.26.linear_attn.in_proj_qkv.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.26.linear_attn.in_proj_qkv.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[2048]},\"model.layers.26.linear_attn.in_proj_qkv.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.26.linear_attn.in_proj_z.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[262144]},\"model.layers.26.linear_attn.in_proj_z.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.26.linear_attn.in_proj_z.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.26.linear_attn.in_proj_z.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[1024]},\"model.layers.26.linear_attn.in_proj_z.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.26.linear_attn.out_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[262144]},\"model.layers.26.linear_attn.out_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.26.linear_attn.out_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.26.linear_attn.out_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[1024]},\"model.layers.26.linear_attn.out_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.26.mlp.down_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.26.mlp.down_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.26.mlp.down_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.26.mlp.down_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.26.mlp.down_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.26.mlp.gate_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.26.mlp.gate_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.26.mlp.gate_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.26.mlp.gate_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.26.mlp.gate_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.26.mlp.up_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.26.mlp.up_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.26.mlp.up_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.26.mlp.up_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.26.mlp.up_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.27.mlp.down_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.27.mlp.down_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.27.mlp.down_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.27.mlp.down_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.27.mlp.down_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.27.mlp.gate_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.27.mlp.gate_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.27.mlp.gate_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.27.mlp.gate_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.27.mlp.gate_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.27.mlp.up_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.27.mlp.up_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.27.mlp.up_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.27.mlp.up_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.27.mlp.up_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.27.self_attn.k_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[65536]},\"model.layers.27.self_attn.k_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.27.self_attn.k_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.27.self_attn.k_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.27.self_attn.k_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.27.self_attn.o_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[262144]},\"model.layers.27.self_attn.o_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.27.self_attn.o_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.27.self_attn.o_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[1024]},\"model.layers.27.self_attn.o_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.27.self_attn.q_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[524288]},\"model.layers.27.self_attn.q_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.27.self_attn.q_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.27.self_attn.q_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[2048]},\"model.layers.27.self_attn.q_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.27.self_attn.v_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[65536]},\"model.layers.27.self_attn.v_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.27.self_attn.v_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.27.self_attn.v_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.27.self_attn.v_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.28.linear_attn.in_proj_a.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[2048]},\"model.layers.28.linear_attn.in_proj_a.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.28.linear_attn.in_proj_a.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.28.linear_attn.in_proj_a.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[8]},\"model.layers.28.linear_attn.in_proj_a.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.28.linear_attn.in_proj_b.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[2048]},\"model.layers.28.linear_attn.in_proj_b.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.28.linear_attn.in_proj_b.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.28.linear_attn.in_proj_b.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[8]},\"model.layers.28.linear_attn.in_proj_b.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.28.linear_attn.in_proj_qkv.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[524288]},\"model.layers.28.linear_attn.in_proj_qkv.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.28.linear_attn.in_proj_qkv.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.28.linear_attn.in_proj_qkv.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[2048]},\"model.layers.28.linear_attn.in_proj_qkv.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.28.linear_attn.in_proj_z.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[262144]},\"model.layers.28.linear_attn.in_proj_z.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.28.linear_attn.in_proj_z.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.28.linear_attn.in_proj_z.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[1024]},\"model.layers.28.linear_attn.in_proj_z.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.28.linear_attn.out_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[262144]},\"model.layers.28.linear_attn.out_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.28.linear_attn.out_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.28.linear_attn.out_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[1024]},\"model.layers.28.linear_attn.out_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.28.mlp.down_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.28.mlp.down_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.28.mlp.down_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.28.mlp.down_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.28.mlp.down_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.28.mlp.gate_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.28.mlp.gate_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.28.mlp.gate_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.28.mlp.gate_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.28.mlp.gate_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.28.mlp.up_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.28.mlp.up_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.28.mlp.up_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.28.mlp.up_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.28.mlp.up_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.29.linear_attn.in_proj_a.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[2048]},\"model.layers.29.linear_attn.in_proj_a.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.29.linear_attn.in_proj_a.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.29.linear_attn.in_proj_a.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[8]},\"model.layers.29.linear_attn.in_proj_a.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.29.linear_attn.in_proj_b.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[2048]},\"model.layers.29.linear_attn.in_proj_b.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.29.linear_attn.in_proj_b.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.29.linear_attn.in_proj_b.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[8]},\"model.layers.29.linear_attn.in_proj_b.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.29.linear_attn.in_proj_qkv.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[524288]},\"model.layers.29.linear_attn.in_proj_qkv.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.29.linear_attn.in_proj_qkv.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.29.linear_attn.in_proj_qkv.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[2048]},\"model.layers.29.linear_attn.in_proj_qkv.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.29.linear_attn.in_proj_z.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[262144]},\"model.layers.29.linear_attn.in_proj_z.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.29.linear_attn.in_proj_z.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.29.linear_attn.in_proj_z.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[1024]},\"model.layers.29.linear_attn.in_proj_z.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.29.linear_attn.out_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[262144]},\"model.layers.29.linear_attn.out_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.29.linear_attn.out_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.29.linear_attn.out_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[1024]},\"model.layers.29.linear_attn.out_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.29.mlp.down_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.29.mlp.down_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.29.mlp.down_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.29.mlp.down_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.29.mlp.down_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.29.mlp.gate_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.29.mlp.gate_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.29.mlp.gate_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.29.mlp.gate_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.29.mlp.gate_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.29.mlp.up_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.29.mlp.up_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.29.mlp.up_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.29.mlp.up_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.29.mlp.up_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.3.mlp.down_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.3.mlp.down_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.3.mlp.down_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.3.mlp.down_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.3.mlp.down_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.3.mlp.gate_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.3.mlp.gate_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.3.mlp.gate_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.3.mlp.gate_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.3.mlp.gate_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.3.mlp.up_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.3.mlp.up_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.3.mlp.up_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.3.mlp.up_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.3.mlp.up_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.3.self_attn.k_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[65536]},\"model.layers.3.self_attn.k_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.3.self_attn.k_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.3.self_attn.k_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.3.self_attn.k_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.3.self_attn.o_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[262144]},\"model.layers.3.self_attn.o_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.3.self_attn.o_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.3.self_attn.o_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[1024]},\"model.layers.3.self_attn.o_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.3.self_attn.q_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[524288]},\"model.layers.3.self_attn.q_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.3.self_attn.q_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.3.self_attn.q_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[2048]},\"model.layers.3.self_attn.q_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.3.self_attn.v_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[65536]},\"model.layers.3.self_attn.v_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.3.self_attn.v_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.3.self_attn.v_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.3.self_attn.v_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.30.linear_attn.in_proj_a.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[2048]},\"model.layers.30.linear_attn.in_proj_a.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.30.linear_attn.in_proj_a.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.30.linear_attn.in_proj_a.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[8]},\"model.layers.30.linear_attn.in_proj_a.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.30.linear_attn.in_proj_b.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[2048]},\"model.layers.30.linear_attn.in_proj_b.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.30.linear_attn.in_proj_b.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.30.linear_attn.in_proj_b.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[8]},\"model.layers.30.linear_attn.in_proj_b.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.30.linear_attn.in_proj_qkv.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[524288]},\"model.layers.30.linear_attn.in_proj_qkv.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.30.linear_attn.in_proj_qkv.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.30.linear_attn.in_proj_qkv.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[2048]},\"model.layers.30.linear_attn.in_proj_qkv.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.30.linear_attn.in_proj_z.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[262144]},\"model.layers.30.linear_attn.in_proj_z.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.30.linear_attn.in_proj_z.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.30.linear_attn.in_proj_z.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[1024]},\"model.layers.30.linear_attn.in_proj_z.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.30.linear_attn.out_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[262144]},\"model.layers.30.linear_attn.out_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.30.linear_attn.out_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.30.linear_attn.out_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[1024]},\"model.layers.30.linear_attn.out_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.30.mlp.down_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.30.mlp.down_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.30.mlp.down_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.30.mlp.down_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.30.mlp.down_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.30.mlp.gate_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.30.mlp.gate_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.30.mlp.gate_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.30.mlp.gate_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.30.mlp.gate_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.30.mlp.up_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.30.mlp.up_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.30.mlp.up_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.30.mlp.up_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.30.mlp.up_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.31.mlp.down_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.31.mlp.down_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.31.mlp.down_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.31.mlp.down_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.31.mlp.down_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.31.mlp.gate_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.31.mlp.gate_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.31.mlp.gate_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.31.mlp.gate_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.31.mlp.gate_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.31.mlp.up_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.31.mlp.up_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.31.mlp.up_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.31.mlp.up_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.31.mlp.up_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.31.self_attn.k_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[65536]},\"model.layers.31.self_attn.k_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.31.self_attn.k_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.31.self_attn.k_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.31.self_attn.k_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.31.self_attn.o_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[262144]},\"model.layers.31.self_attn.o_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.31.self_attn.o_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.31.self_attn.o_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[1024]},\"model.layers.31.self_attn.o_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.31.self_attn.q_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[524288]},\"model.layers.31.self_attn.q_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.31.self_attn.q_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.31.self_attn.q_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[2048]},\"model.layers.31.self_attn.q_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.31.self_attn.v_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[65536]},\"model.layers.31.self_attn.v_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.31.self_attn.v_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.31.self_attn.v_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.31.self_attn.v_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.4.linear_attn.in_proj_a.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[2048]},\"model.layers.4.linear_attn.in_proj_a.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.4.linear_attn.in_proj_a.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.4.linear_attn.in_proj_a.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[8]},\"model.layers.4.linear_attn.in_proj_a.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.4.linear_attn.in_proj_b.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[2048]},\"model.layers.4.linear_attn.in_proj_b.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.4.linear_attn.in_proj_b.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.4.linear_attn.in_proj_b.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[8]},\"model.layers.4.linear_attn.in_proj_b.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.4.linear_attn.in_proj_qkv.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[524288]},\"model.layers.4.linear_attn.in_proj_qkv.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.4.linear_attn.in_proj_qkv.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.4.linear_attn.in_proj_qkv.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[2048]},\"model.layers.4.linear_attn.in_proj_qkv.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.4.linear_attn.in_proj_z.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[262144]},\"model.layers.4.linear_attn.in_proj_z.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.4.linear_attn.in_proj_z.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.4.linear_attn.in_proj_z.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[1024]},\"model.layers.4.linear_attn.in_proj_z.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.4.linear_attn.out_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[262144]},\"model.layers.4.linear_attn.out_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.4.linear_attn.out_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.4.linear_attn.out_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[1024]},\"model.layers.4.linear_attn.out_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.4.mlp.down_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.4.mlp.down_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.4.mlp.down_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.4.mlp.down_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.4.mlp.down_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.4.mlp.gate_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.4.mlp.gate_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.4.mlp.gate_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.4.mlp.gate_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.4.mlp.gate_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.4.mlp.up_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.4.mlp.up_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.4.mlp.up_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.4.mlp.up_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.4.mlp.up_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.5.linear_attn.in_proj_a.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[2048]},\"model.layers.5.linear_attn.in_proj_a.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.5.linear_attn.in_proj_a.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.5.linear_attn.in_proj_a.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[8]},\"model.layers.5.linear_attn.in_proj_a.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.5.linear_attn.in_proj_b.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[2048]},\"model.layers.5.linear_attn.in_proj_b.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.5.linear_attn.in_proj_b.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.5.linear_attn.in_proj_b.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[8]},\"model.layers.5.linear_attn.in_proj_b.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.5.linear_attn.in_proj_qkv.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[524288]},\"model.layers.5.linear_attn.in_proj_qkv.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.5.linear_attn.in_proj_qkv.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.5.linear_attn.in_proj_qkv.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[2048]},\"model.layers.5.linear_attn.in_proj_qkv.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.5.linear_attn.in_proj_z.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[262144]},\"model.layers.5.linear_attn.in_proj_z.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.5.linear_attn.in_proj_z.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.5.linear_attn.in_proj_z.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[1024]},\"model.layers.5.linear_attn.in_proj_z.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.5.linear_attn.out_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[262144]},\"model.layers.5.linear_attn.out_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.5.linear_attn.out_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.5.linear_attn.out_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[1024]},\"model.layers.5.linear_attn.out_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.5.mlp.down_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.5.mlp.down_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.5.mlp.down_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.5.mlp.down_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.5.mlp.down_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.5.mlp.gate_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.5.mlp.gate_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.5.mlp.gate_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.5.mlp.gate_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.5.mlp.gate_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.5.mlp.up_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.5.mlp.up_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.5.mlp.up_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.5.mlp.up_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.5.mlp.up_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.6.linear_attn.in_proj_a.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[2048]},\"model.layers.6.linear_attn.in_proj_a.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.6.linear_attn.in_proj_a.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.6.linear_attn.in_proj_a.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[8]},\"model.layers.6.linear_attn.in_proj_a.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.6.linear_attn.in_proj_b.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[2048]},\"model.layers.6.linear_attn.in_proj_b.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.6.linear_attn.in_proj_b.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.6.linear_attn.in_proj_b.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[8]},\"model.layers.6.linear_attn.in_proj_b.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.6.linear_attn.in_proj_qkv.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[524288]},\"model.layers.6.linear_attn.in_proj_qkv.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.6.linear_attn.in_proj_qkv.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.6.linear_attn.in_proj_qkv.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[2048]},\"model.layers.6.linear_attn.in_proj_qkv.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.6.linear_attn.in_proj_z.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[262144]},\"model.layers.6.linear_attn.in_proj_z.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.6.linear_attn.in_proj_z.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.6.linear_attn.in_proj_z.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[1024]},\"model.layers.6.linear_attn.in_proj_z.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.6.linear_attn.out_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[262144]},\"model.layers.6.linear_attn.out_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.6.linear_attn.out_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.6.linear_attn.out_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[1024]},\"model.layers.6.linear_attn.out_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.6.mlp.down_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.6.mlp.down_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.6.mlp.down_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.6.mlp.down_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.6.mlp.down_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.6.mlp.gate_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.6.mlp.gate_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.6.mlp.gate_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.6.mlp.gate_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.6.mlp.gate_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.6.mlp.up_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.6.mlp.up_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.6.mlp.up_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.6.mlp.up_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.6.mlp.up_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.7.mlp.down_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.7.mlp.down_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.7.mlp.down_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.7.mlp.down_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.7.mlp.down_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.7.mlp.gate_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.7.mlp.gate_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.7.mlp.gate_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.7.mlp.gate_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.7.mlp.gate_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.7.mlp.up_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.7.mlp.up_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.7.mlp.up_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.7.mlp.up_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.7.mlp.up_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.7.self_attn.k_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[65536]},\"model.layers.7.self_attn.k_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.7.self_attn.k_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.7.self_attn.k_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.7.self_attn.k_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.7.self_attn.o_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[262144]},\"model.layers.7.self_attn.o_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.7.self_attn.o_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.7.self_attn.o_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[1024]},\"model.layers.7.self_attn.o_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.7.self_attn.q_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[524288]},\"model.layers.7.self_attn.q_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.7.self_attn.q_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.7.self_attn.q_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[2048]},\"model.layers.7.self_attn.q_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.7.self_attn.v_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[65536]},\"model.layers.7.self_attn.v_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.7.self_attn.v_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.7.self_attn.v_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.7.self_attn.v_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.8.linear_attn.in_proj_a.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[2048]},\"model.layers.8.linear_attn.in_proj_a.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.8.linear_attn.in_proj_a.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.8.linear_attn.in_proj_a.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[8]},\"model.layers.8.linear_attn.in_proj_a.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.8.linear_attn.in_proj_b.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[2048]},\"model.layers.8.linear_attn.in_proj_b.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.8.linear_attn.in_proj_b.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.8.linear_attn.in_proj_b.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[8]},\"model.layers.8.linear_attn.in_proj_b.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.8.linear_attn.in_proj_qkv.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[524288]},\"model.layers.8.linear_attn.in_proj_qkv.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.8.linear_attn.in_proj_qkv.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.8.linear_attn.in_proj_qkv.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[2048]},\"model.layers.8.linear_attn.in_proj_qkv.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.8.linear_attn.in_proj_z.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[262144]},\"model.layers.8.linear_attn.in_proj_z.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.8.linear_attn.in_proj_z.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.8.linear_attn.in_proj_z.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[1024]},\"model.layers.8.linear_attn.in_proj_z.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.8.linear_attn.out_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[262144]},\"model.layers.8.linear_attn.out_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.8.linear_attn.out_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.8.linear_attn.out_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[1024]},\"model.layers.8.linear_attn.out_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.8.mlp.down_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.8.mlp.down_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.8.mlp.down_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.8.mlp.down_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.8.mlp.down_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.8.mlp.gate_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.8.mlp.gate_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.8.mlp.gate_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.8.mlp.gate_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.8.mlp.gate_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.8.mlp.up_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.8.mlp.up_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.8.mlp.up_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.8.mlp.up_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.8.mlp.up_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.9.linear_attn.in_proj_a.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[2048]},\"model.layers.9.linear_attn.in_proj_a.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.9.linear_attn.in_proj_a.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.9.linear_attn.in_proj_a.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[8]},\"model.layers.9.linear_attn.in_proj_a.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.9.linear_attn.in_proj_b.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[2048]},\"model.layers.9.linear_attn.in_proj_b.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.9.linear_attn.in_proj_b.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.9.linear_attn.in_proj_b.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[8]},\"model.layers.9.linear_attn.in_proj_b.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.9.linear_attn.in_proj_qkv.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[524288]},\"model.layers.9.linear_attn.in_proj_qkv.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.9.linear_attn.in_proj_qkv.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.9.linear_attn.in_proj_qkv.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[2048]},\"model.layers.9.linear_attn.in_proj_qkv.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.9.linear_attn.in_proj_z.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[262144]},\"model.layers.9.linear_attn.in_proj_z.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.9.linear_attn.in_proj_z.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.9.linear_attn.in_proj_z.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[1024]},\"model.layers.9.linear_attn.in_proj_z.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.9.linear_attn.out_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[262144]},\"model.layers.9.linear_attn.out_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.9.linear_attn.out_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.9.linear_attn.out_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[1024]},\"model.layers.9.linear_attn.out_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.9.mlp.down_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.9.mlp.down_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.9.mlp.down_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.9.mlp.down_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.9.mlp.down_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.9.mlp.gate_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.9.mlp.gate_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.9.mlp.gate_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.9.mlp.gate_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.9.mlp.gate_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.9.mlp.up_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.9.mlp.up_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.9.mlp.up_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.9.mlp.up_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.9.mlp.up_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]}},\"recurrent_fast_path\":false,\"requested_device_map\":{\"\":0},\"revision\":\"c202236235762e1c871ad0ccb60c8ee5ba337b9a\",\"tied_output_head\":false,\"total_device_bytes\":15636037632,\"verified_snapshot\":\"/kaggle/temp/i01/hf-cache/models--Qwen--Qwen3.5-9B/snapshots/c202236235762e1c871ad0ccb60c8ee5ba337b9a\"},\"session\":\"a7bb7845-cf04-4efd-9b68-f74b9595cfaa\",\"slot\":0,\"window\":{\"deadline\":\"2026-10-16T05:20:47.399377+00:00\",\"evidence\":\"User reports an approximately 12-hour session; 700-minute fresh-session planning bound, provider quota/deadline not independently verified.\",\"observation\":{\"at\":\"2026-10-15T17:40:47.399455+00:00\",\"basis\":\"planning_estimate\",\"remaining_minutes\":700},\"observed_start\":\"2026-10-15T17:44:39.516556+00:00\",\"session\":\"a7bb7845-cf04-4efd-9b68-f74b9595cfaa\"}}",
            "id": "a7bb7845-cf04-4efd-9b68-f74b9595cfaa/load-0"
          }
        ],
        [
          {
            "evidence": "{\"controller_pid\":231,\"host\":{\"executable\":\"/usr/bin/python3\",\"gpus\":[{\"driver\":\"580.178.04\",\"index\":0,\"memory_mib\":15360,\"name\":\"Tesla T4\",\"uuid\":\"GPU-ed9bad25-b76c-9174-051b-1a8b14ec17e2\"},{\"driver\":\"580.178.04\",\"index\":1,\"memory_mib\":15360,\"name\":\"Tesla T4\",\"uuid\":\"GPU-9bd69e6c-b965-32ef-1c1d-4d3aad42f4a0\"}],\"gpus_error\":null,\"internet_required\":true,\"machine\":\"x86_64\",\"observed_at\":\"2026-10-15T17:47:48.318672+00:00\",\"paths\":{\"scratch\":{\"device\":54,\"free\":1120627843072,\"path\":\"/kaggle/temp/i01\",\"total\":8758385086464,\"writable\":true},\"working\":{\"device\":1794,\"free\":20930084864,\"path\":\"/kaggle/working\",\"total\":20957446144,\"writable\":true}},\"python\":\"3.13.15 (main, Aug  6 2026, 11:06:22) [GCC 13.3.0]\",\"python_version\":[3,13,15],\"system\":\"Linux\"},\"load\":{\"actual_tensor_devices\":[\"cuda:0\"],\"attention\":\"recovery_t4_sdpa\",\"buffers\":{\"model.rotary_emb.inv_freq\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[32]},\"model.rotary_emb.original_inv_freq\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[32]}},\"class\":\"Qwen3_5ForCausalLM\",\"cuda\":\"12.8\",\"cuda_device_uuid\":\"9bd69e6c-b965-32ef-1c1d-4d3aad42f4a0\",\"cuda_visible_devices\":\"1\",\"device_map\":null,\"device_name\":\"Tesla T4\",\"generation_config\":{\"_from_model_config\":null,\"assistant_confidence_threshold\":null,\"assistant_early_exit\":null,\"assistant_lookbehind\":null,\"bad_words_ids\":null,\"begin_suppress_tokens\":null,\"bos_token_id\":null,\"cache_config\":null,\"cache_implementation\":null,\"compile_config\":null,\"constraints\":null,\"continuous_batching_config\":null,\"decoder_start_token_id\":null,\"disable_compile\":null,\"diversity_penalty\":null,\"do_sample\":true,\"dola_layers\":null,\"early_stopping\":null,\"encoder_no_repeat_ngram_size\":null,\"encoder_repetition_penalty\":null,\"eos_token_id\":[248044,248046],\"epsilon_cutoff\":null,\"eta_cutoff\":null,\"exponential_decay_length_penalty\":null,\"force_words_ids\":null,\"forced_bos_token_id\":null,\"forced_eos_token_id\":null,\"guidance_scale\":null,\"is_assistant\":null,\"length_penalty\":null,\"low_memory\":null,\"max_length\":null,\"max_matching_ngram_size\":null,\"max_new_tokens\":256,\"max_time\":null,\"min_length\":null,\"min_new_tokens\":null,\"min_p\":0.0,\"no_repeat_ngram_size\":null,\"num_assistant_tokens\":null,\"num_assistant_tokens_schedule\":null,\"num_beam_groups\":null,\"num_beams\":1,\"num_return_sequences\":null,\"output_attentions\":null,\"output_hidden_states\":null,\"output_logits\":null,\"output_scores\":false,\"pad_token_id\":248044,\"penalty_alpha\":null,\"prefill_chunk_size\":256,\"prompt_lookup_num_tokens\":null,\"remove_invalid_values\":false,\"renormalize_logits\":null,\"repetition_penalty\":1.0,\"return_dict_in_generate\":true,\"sequence_bias\":null,\"stop_strings\":null,\"suppress_tokens\":null,\"target_lookbehind\":null,\"temperature\":0.7,\"token_healing\":null,\"top_h\":null,\"top_k\":20,\"top_p\":0.8,\"transformers_version\":\"5.12.0\",\"typical_p\":null,\"use_cache\":true,\"watermarking_config\":null},\"i01_loading_only\":true,\"load_seconds\":54.863872566000055,\"loaded_at\":\"2026-10-15T17:49:48.357880+00:00\",\"loading_info\":{\"error_msgs\":[],\"mismatched_keys\":[],\"missing_keys\":[],\"unexpected_keys\":[]},\"model\":\"Qwen/Qwen3.5-9B\",\"packages\":{\"accelerate\":\"1.14.0\",\"bitsandbytes\":\"0.49.2\",\"huggingface-hub\":\"1.19.0\",\"tokenizers\":\"0.22.2\",\"torch\":\"2.11.0+cu128\",\"transformers\":\"5.12.0\"},\"parameters\":{\"lm_head.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[248320,4096]},\"model.embed_tokens.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[248320,4096]},\"model.layers.0.input_layernorm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[4096]},\"model.layers.0.linear_attn.A_log\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[32]},\"model.layers.0.linear_attn.conv1d.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[8192,1,4]},\"model.layers.0.linear_attn.dt_bias\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[32]},\"model.layers.0.linear_attn.in_proj_a.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[65536,1]},\"model.layers.0.linear_attn.in_proj_b.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[65536,1]},\"model.layers.0.linear_attn.in_proj_qkv.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[16777216,1]},\"model.layers.0.linear_attn.in_proj_z.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[8388608,1]},\"model.layers.0.linear_attn.norm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[128]},\"model.layers.0.linear_attn.out_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[8388608,1]},\"model.layers.0.mlp.down_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.0.mlp.gate_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.0.mlp.up_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.0.post_attention_layernorm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[4096]},\"model.layers.1.input_layernorm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[4096]},\"model.layers.1.linear_attn.A_log\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[32]},\"model.layers.1.linear_attn.conv1d.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[8192,1,4]},\"model.layers.1.linear_attn.dt_bias\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[32]},\"model.layers.1.linear_attn.in_proj_a.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[65536,1]},\"model.layers.1.linear_attn.in_proj_b.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[65536,1]},\"model.layers.1.linear_attn.in_proj_qkv.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[16777216,1]},\"model.layers.1.linear_attn.in_proj_z.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[8388608,1]},\"model.layers.1.linear_attn.norm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[128]},\"model.layers.1.linear_attn.out_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[8388608,1]},\"model.layers.1.mlp.down_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.1.mlp.gate_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.1.mlp.up_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.1.post_attention_layernorm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[4096]},\"model.layers.10.input_layernorm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[4096]},\"model.layers.10.linear_attn.A_log\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[32]},\"model.layers.10.linear_attn.conv1d.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[8192,1,4]},\"model.layers.10.linear_attn.dt_bias\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[32]},\"model.layers.10.linear_attn.in_proj_a.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[65536,1]},\"model.layers.10.linear_attn.in_proj_b.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[65536,1]},\"model.layers.10.linear_attn.in_proj_qkv.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[16777216,1]},\"model.layers.10.linear_attn.in_proj_z.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[8388608,1]},\"model.layers.10.linear_attn.norm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[128]},\"model.layers.10.linear_attn.out_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[8388608,1]},\"model.layers.10.mlp.down_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.10.mlp.gate_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.10.mlp.up_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.10.post_attention_layernorm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[4096]},\"model.layers.11.input_layernorm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[4096]},\"model.layers.11.mlp.down_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.11.mlp.gate_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.11.mlp.up_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.11.post_attention_layernorm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[4096]},\"model.layers.11.self_attn.k_norm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[256]},\"model.layers.11.self_attn.k_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[2097152,1]},\"model.layers.11.self_attn.o_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[8388608,1]},\"model.layers.11.self_attn.q_norm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[256]},\"model.layers.11.self_attn.q_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[16777216,1]},\"model.layers.11.self_attn.v_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[2097152,1]},\"model.layers.12.input_layernorm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[4096]},\"model.layers.12.linear_attn.A_log\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[32]},\"model.layers.12.linear_attn.conv1d.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[8192,1,4]},\"model.layers.12.linear_attn.dt_bias\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[32]},\"model.layers.12.linear_attn.in_proj_a.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[65536,1]},\"model.layers.12.linear_attn.in_proj_b.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[65536,1]},\"model.layers.12.linear_attn.in_proj_qkv.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[16777216,1]},\"model.layers.12.linear_attn.in_proj_z.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[8388608,1]},\"model.layers.12.linear_attn.norm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[128]},\"model.layers.12.linear_attn.out_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[8388608,1]},\"model.layers.12.mlp.down_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.12.mlp.gate_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.12.mlp.up_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.12.post_attention_layernorm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[4096]},\"model.layers.13.input_layernorm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[4096]},\"model.layers.13.linear_attn.A_log\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[32]},\"model.layers.13.linear_attn.conv1d.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[8192,1,4]},\"model.layers.13.linear_attn.dt_bias\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[32]},\"model.layers.13.linear_attn.in_proj_a.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[65536,1]},\"model.layers.13.linear_attn.in_proj_b.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[65536,1]},\"model.layers.13.linear_attn.in_proj_qkv.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[16777216,1]},\"model.layers.13.linear_attn.in_proj_z.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[8388608,1]},\"model.layers.13.linear_attn.norm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[128]},\"model.layers.13.linear_attn.out_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[8388608,1]},\"model.layers.13.mlp.down_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.13.mlp.gate_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.13.mlp.up_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.13.post_attention_layernorm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[4096]},\"model.layers.14.input_layernorm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[4096]},\"model.layers.14.linear_attn.A_log\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[32]},\"model.layers.14.linear_attn.conv1d.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[8192,1,4]},\"model.layers.14.linear_attn.dt_bias\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[32]},\"model.layers.14.linear_attn.in_proj_a.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[65536,1]},\"model.layers.14.linear_attn.in_proj_b.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[65536,1]},\"model.layers.14.linear_attn.in_proj_qkv.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[16777216,1]},\"model.layers.14.linear_attn.in_proj_z.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[8388608,1]},\"model.layers.14.linear_attn.norm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[128]},\"model.layers.14.linear_attn.out_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[8388608,1]},\"model.layers.14.mlp.down_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.14.mlp.gate_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.14.mlp.up_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.14.post_attention_layernorm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[4096]},\"model.layers.15.input_layernorm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[4096]},\"model.layers.15.mlp.down_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.15.mlp.gate_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.15.mlp.up_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.15.post_attention_layernorm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[4096]},\"model.layers.15.self_attn.k_norm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[256]},\"model.layers.15.self_attn.k_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[2097152,1]},\"model.layers.15.self_attn.o_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[8388608,1]},\"model.layers.15.self_attn.q_norm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[256]},\"model.layers.15.self_attn.q_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[16777216,1]},\"model.layers.15.self_attn.v_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[2097152,1]},\"model.layers.16.input_layernorm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[4096]},\"model.layers.16.linear_attn.A_log\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[32]},\"model.layers.16.linear_attn.conv1d.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[8192,1,4]},\"model.layers.16.linear_attn.dt_bias\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[32]},\"model.layers.16.linear_attn.in_proj_a.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[65536,1]},\"model.layers.16.linear_attn.in_proj_b.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[65536,1]},\"model.layers.16.linear_attn.in_proj_qkv.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[16777216,1]},\"model.layers.16.linear_attn.in_proj_z.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[8388608,1]},\"model.layers.16.linear_attn.norm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[128]},\"model.layers.16.linear_attn.out_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[8388608,1]},\"model.layers.16.mlp.down_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.16.mlp.gate_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.16.mlp.up_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.16.post_attention_layernorm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[4096]},\"model.layers.17.input_layernorm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[4096]},\"model.layers.17.linear_attn.A_log\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[32]},\"model.layers.17.linear_attn.conv1d.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[8192,1,4]},\"model.layers.17.linear_attn.dt_bias\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[32]},\"model.layers.17.linear_attn.in_proj_a.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[65536,1]},\"model.layers.17.linear_attn.in_proj_b.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[65536,1]},\"model.layers.17.linear_attn.in_proj_qkv.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[16777216,1]},\"model.layers.17.linear_attn.in_proj_z.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[8388608,1]},\"model.layers.17.linear_attn.norm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[128]},\"model.layers.17.linear_attn.out_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[8388608,1]},\"model.layers.17.mlp.down_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.17.mlp.gate_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.17.mlp.up_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.17.post_attention_layernorm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[4096]},\"model.layers.18.input_layernorm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[4096]},\"model.layers.18.linear_attn.A_log\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[32]},\"model.layers.18.linear_attn.conv1d.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[8192,1,4]},\"model.layers.18.linear_attn.dt_bias\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[32]},\"model.layers.18.linear_attn.in_proj_a.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[65536,1]},\"model.layers.18.linear_attn.in_proj_b.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[65536,1]},\"model.layers.18.linear_attn.in_proj_qkv.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[16777216,1]},\"model.layers.18.linear_attn.in_proj_z.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[8388608,1]},\"model.layers.18.linear_attn.norm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[128]},\"model.layers.18.linear_attn.out_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[8388608,1]},\"model.layers.18.mlp.down_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.18.mlp.gate_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.18.mlp.up_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.18.post_attention_layernorm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[4096]},\"model.layers.19.input_layernorm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[4096]},\"model.layers.19.mlp.down_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.19.mlp.gate_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.19.mlp.up_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.19.post_attention_layernorm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[4096]},\"model.layers.19.self_attn.k_norm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[256]},\"model.layers.19.self_attn.k_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[2097152,1]},\"model.layers.19.self_attn.o_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[8388608,1]},\"model.layers.19.self_attn.q_norm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[256]},\"model.layers.19.self_attn.q_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[16777216,1]},\"model.layers.19.self_attn.v_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[2097152,1]},\"model.layers.2.input_layernorm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[4096]},\"model.layers.2.linear_attn.A_log\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[32]},\"model.layers.2.linear_attn.conv1d.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[8192,1,4]},\"model.layers.2.linear_attn.dt_bias\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[32]},\"model.layers.2.linear_attn.in_proj_a.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[65536,1]},\"model.layers.2.linear_attn.in_proj_b.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[65536,1]},\"model.layers.2.linear_attn.in_proj_qkv.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[16777216,1]},\"model.layers.2.linear_attn.in_proj_z.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[8388608,1]},\"model.layers.2.linear_attn.norm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[128]},\"model.layers.2.linear_attn.out_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[8388608,1]},\"model.layers.2.mlp.down_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.2.mlp.gate_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.2.mlp.up_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.2.post_attention_layernorm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[4096]},\"model.layers.20.input_layernorm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[4096]},\"model.layers.20.linear_attn.A_log\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[32]},\"model.layers.20.linear_attn.conv1d.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[8192,1,4]},\"model.layers.20.linear_attn.dt_bias\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[32]},\"model.layers.20.linear_attn.in_proj_a.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[65536,1]},\"model.layers.20.linear_attn.in_proj_b.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[65536,1]},\"model.layers.20.linear_attn.in_proj_qkv.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[16777216,1]},\"model.layers.20.linear_attn.in_proj_z.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[8388608,1]},\"model.layers.20.linear_attn.norm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[128]},\"model.layers.20.linear_attn.out_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[8388608,1]},\"model.layers.20.mlp.down_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.20.mlp.gate_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.20.mlp.up_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.20.post_attention_layernorm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[4096]},\"model.layers.21.input_layernorm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[4096]},\"model.layers.21.linear_attn.A_log\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[32]},\"model.layers.21.linear_attn.conv1d.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[8192,1,4]},\"model.layers.21.linear_attn.dt_bias\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[32]},\"model.layers.21.linear_attn.in_proj_a.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[65536,1]},\"model.layers.21.linear_attn.in_proj_b.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[65536,1]},\"model.layers.21.linear_attn.in_proj_qkv.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[16777216,1]},\"model.layers.21.linear_attn.in_proj_z.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[8388608,1]},\"model.layers.21.linear_attn.norm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[128]},\"model.layers.21.linear_attn.out_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[8388608,1]},\"model.layers.21.mlp.down_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.21.mlp.gate_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.21.mlp.up_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.21.post_attention_layernorm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[4096]},\"model.layers.22.input_layernorm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[4096]},\"model.layers.22.linear_attn.A_log\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[32]},\"model.layers.22.linear_attn.conv1d.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[8192,1,4]},\"model.layers.22.linear_attn.dt_bias\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[32]},\"model.layers.22.linear_attn.in_proj_a.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[65536,1]},\"model.layers.22.linear_attn.in_proj_b.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[65536,1]},\"model.layers.22.linear_attn.in_proj_qkv.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[16777216,1]},\"model.layers.22.linear_attn.in_proj_z.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[8388608,1]},\"model.layers.22.linear_attn.norm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[128]},\"model.layers.22.linear_attn.out_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[8388608,1]},\"model.layers.22.mlp.down_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.22.mlp.gate_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.22.mlp.up_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.22.post_attention_layernorm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[4096]},\"model.layers.23.input_layernorm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[4096]},\"model.layers.23.mlp.down_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.23.mlp.gate_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.23.mlp.up_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.23.post_attention_layernorm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[4096]},\"model.layers.23.self_attn.k_norm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[256]},\"model.layers.23.self_attn.k_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[2097152,1]},\"model.layers.23.self_attn.o_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[8388608,1]},\"model.layers.23.self_attn.q_norm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[256]},\"model.layers.23.self_attn.q_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[16777216,1]},\"model.layers.23.self_attn.v_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[2097152,1]},\"model.layers.24.input_layernorm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[4096]},\"model.layers.24.linear_attn.A_log\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[32]},\"model.layers.24.linear_attn.conv1d.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[8192,1,4]},\"model.layers.24.linear_attn.dt_bias\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[32]},\"model.layers.24.linear_attn.in_proj_a.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[65536,1]},\"model.layers.24.linear_attn.in_proj_b.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[65536,1]},\"model.layers.24.linear_attn.in_proj_qkv.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[16777216,1]},\"model.layers.24.linear_attn.in_proj_z.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[8388608,1]},\"model.layers.24.linear_attn.norm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[128]},\"model.layers.24.linear_attn.out_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[8388608,1]},\"model.layers.24.mlp.down_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.24.mlp.gate_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.24.mlp.up_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.24.post_attention_layernorm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[4096]},\"model.layers.25.input_layernorm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[4096]},\"model.layers.25.linear_attn.A_log\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[32]},\"model.layers.25.linear_attn.conv1d.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[8192,1,4]},\"model.layers.25.linear_attn.dt_bias\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[32]},\"model.layers.25.linear_attn.in_proj_a.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[65536,1]},\"model.layers.25.linear_attn.in_proj_b.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[65536,1]},\"model.layers.25.linear_attn.in_proj_qkv.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[16777216,1]},\"model.layers.25.linear_attn.in_proj_z.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[8388608,1]},\"model.layers.25.linear_attn.norm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[128]},\"model.layers.25.linear_attn.out_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[8388608,1]},\"model.layers.25.mlp.down_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.25.mlp.gate_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.25.mlp.up_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.25.post_attention_layernorm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[4096]},\"model.layers.26.input_layernorm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[4096]},\"model.layers.26.linear_attn.A_log\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[32]},\"model.layers.26.linear_attn.conv1d.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[8192,1,4]},\"model.layers.26.linear_attn.dt_bias\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[32]},\"model.layers.26.linear_attn.in_proj_a.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[65536,1]},\"model.layers.26.linear_attn.in_proj_b.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[65536,1]},\"model.layers.26.linear_attn.in_proj_qkv.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[16777216,1]},\"model.layers.26.linear_attn.in_proj_z.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[8388608,1]},\"model.layers.26.linear_attn.norm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[128]},\"model.layers.26.linear_attn.out_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[8388608,1]},\"model.layers.26.mlp.down_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.26.mlp.gate_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.26.mlp.up_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.26.post_attention_layernorm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[4096]},\"model.layers.27.input_layernorm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[4096]},\"model.layers.27.mlp.down_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.27.mlp.gate_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.27.mlp.up_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.27.post_attention_layernorm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[4096]},\"model.layers.27.self_attn.k_norm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[256]},\"model.layers.27.self_attn.k_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[2097152,1]},\"model.layers.27.self_attn.o_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[8388608,1]},\"model.layers.27.self_attn.q_norm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[256]},\"model.layers.27.self_attn.q_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[16777216,1]},\"model.layers.27.self_attn.v_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[2097152,1]},\"model.layers.28.input_layernorm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[4096]},\"model.layers.28.linear_attn.A_log\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[32]},\"model.layers.28.linear_attn.conv1d.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[8192,1,4]},\"model.layers.28.linear_attn.dt_bias\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[32]},\"model.layers.28.linear_attn.in_proj_a.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[65536,1]},\"model.layers.28.linear_attn.in_proj_b.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[65536,1]},\"model.layers.28.linear_attn.in_proj_qkv.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[16777216,1]},\"model.layers.28.linear_attn.in_proj_z.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[8388608,1]},\"model.layers.28.linear_attn.norm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[128]},\"model.layers.28.linear_attn.out_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[8388608,1]},\"model.layers.28.mlp.down_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.28.mlp.gate_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.28.mlp.up_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.28.post_attention_layernorm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[4096]},\"model.layers.29.input_layernorm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[4096]},\"model.layers.29.linear_attn.A_log\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[32]},\"model.layers.29.linear_attn.conv1d.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[8192,1,4]},\"model.layers.29.linear_attn.dt_bias\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[32]},\"model.layers.29.linear_attn.in_proj_a.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[65536,1]},\"model.layers.29.linear_attn.in_proj_b.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[65536,1]},\"model.layers.29.linear_attn.in_proj_qkv.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[16777216,1]},\"model.layers.29.linear_attn.in_proj_z.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[8388608,1]},\"model.layers.29.linear_attn.norm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[128]},\"model.layers.29.linear_attn.out_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[8388608,1]},\"model.layers.29.mlp.down_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.29.mlp.gate_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.29.mlp.up_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.29.post_attention_layernorm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[4096]},\"model.layers.3.input_layernorm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[4096]},\"model.layers.3.mlp.down_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.3.mlp.gate_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.3.mlp.up_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.3.post_attention_layernorm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[4096]},\"model.layers.3.self_attn.k_norm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[256]},\"model.layers.3.self_attn.k_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[2097152,1]},\"model.layers.3.self_attn.o_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[8388608,1]},\"model.layers.3.self_attn.q_norm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[256]},\"model.layers.3.self_attn.q_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[16777216,1]},\"model.layers.3.self_attn.v_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[2097152,1]},\"model.layers.30.input_layernorm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[4096]},\"model.layers.30.linear_attn.A_log\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[32]},\"model.layers.30.linear_attn.conv1d.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[8192,1,4]},\"model.layers.30.linear_attn.dt_bias\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[32]},\"model.layers.30.linear_attn.in_proj_a.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[65536,1]},\"model.layers.30.linear_attn.in_proj_b.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[65536,1]},\"model.layers.30.linear_attn.in_proj_qkv.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[16777216,1]},\"model.layers.30.linear_attn.in_proj_z.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[8388608,1]},\"model.layers.30.linear_attn.norm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[128]},\"model.layers.30.linear_attn.out_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[8388608,1]},\"model.layers.30.mlp.down_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.30.mlp.gate_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.30.mlp.up_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.30.post_attention_layernorm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[4096]},\"model.layers.31.input_layernorm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[4096]},\"model.layers.31.mlp.down_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.31.mlp.gate_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.31.mlp.up_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.31.post_attention_layernorm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[4096]},\"model.layers.31.self_attn.k_norm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[256]},\"model.layers.31.self_attn.k_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[2097152,1]},\"model.layers.31.self_attn.o_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[8388608,1]},\"model.layers.31.self_attn.q_norm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[256]},\"model.layers.31.self_attn.q_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[16777216,1]},\"model.layers.31.self_attn.v_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[2097152,1]},\"model.layers.4.input_layernorm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[4096]},\"model.layers.4.linear_attn.A_log\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[32]},\"model.layers.4.linear_attn.conv1d.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[8192,1,4]},\"model.layers.4.linear_attn.dt_bias\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[32]},\"model.layers.4.linear_attn.in_proj_a.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[65536,1]},\"model.layers.4.linear_attn.in_proj_b.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[65536,1]},\"model.layers.4.linear_attn.in_proj_qkv.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[16777216,1]},\"model.layers.4.linear_attn.in_proj_z.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[8388608,1]},\"model.layers.4.linear_attn.norm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[128]},\"model.layers.4.linear_attn.out_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[8388608,1]},\"model.layers.4.mlp.down_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.4.mlp.gate_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.4.mlp.up_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.4.post_attention_layernorm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[4096]},\"model.layers.5.input_layernorm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[4096]},\"model.layers.5.linear_attn.A_log\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[32]},\"model.layers.5.linear_attn.conv1d.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[8192,1,4]},\"model.layers.5.linear_attn.dt_bias\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[32]},\"model.layers.5.linear_attn.in_proj_a.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[65536,1]},\"model.layers.5.linear_attn.in_proj_b.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[65536,1]},\"model.layers.5.linear_attn.in_proj_qkv.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[16777216,1]},\"model.layers.5.linear_attn.in_proj_z.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[8388608,1]},\"model.layers.5.linear_attn.norm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[128]},\"model.layers.5.linear_attn.out_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[8388608,1]},\"model.layers.5.mlp.down_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.5.mlp.gate_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.5.mlp.up_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.5.post_attention_layernorm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[4096]},\"model.layers.6.input_layernorm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[4096]},\"model.layers.6.linear_attn.A_log\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[32]},\"model.layers.6.linear_attn.conv1d.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[8192,1,4]},\"model.layers.6.linear_attn.dt_bias\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[32]},\"model.layers.6.linear_attn.in_proj_a.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[65536,1]},\"model.layers.6.linear_attn.in_proj_b.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[65536,1]},\"model.layers.6.linear_attn.in_proj_qkv.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[16777216,1]},\"model.layers.6.linear_attn.in_proj_z.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[8388608,1]},\"model.layers.6.linear_attn.norm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[128]},\"model.layers.6.linear_attn.out_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[8388608,1]},\"model.layers.6.mlp.down_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.6.mlp.gate_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.6.mlp.up_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.6.post_attention_layernorm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[4096]},\"model.layers.7.input_layernorm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[4096]},\"model.layers.7.mlp.down_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.7.mlp.gate_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.7.mlp.up_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.7.post_attention_layernorm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[4096]},\"model.layers.7.self_attn.k_norm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[256]},\"model.layers.7.self_attn.k_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[2097152,1]},\"model.layers.7.self_attn.o_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[8388608,1]},\"model.layers.7.self_attn.q_norm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[256]},\"model.layers.7.self_attn.q_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[16777216,1]},\"model.layers.7.self_attn.v_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[2097152,1]},\"model.layers.8.input_layernorm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[4096]},\"model.layers.8.linear_attn.A_log\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[32]},\"model.layers.8.linear_attn.conv1d.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[8192,1,4]},\"model.layers.8.linear_attn.dt_bias\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[32]},\"model.layers.8.linear_attn.in_proj_a.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[65536,1]},\"model.layers.8.linear_attn.in_proj_b.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[65536,1]},\"model.layers.8.linear_attn.in_proj_qkv.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[16777216,1]},\"model.layers.8.linear_attn.in_proj_z.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[8388608,1]},\"model.layers.8.linear_attn.norm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[128]},\"model.layers.8.linear_attn.out_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[8388608,1]},\"model.layers.8.mlp.down_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.8.mlp.gate_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.8.mlp.up_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.8.post_attention_layernorm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[4096]},\"model.layers.9.input_layernorm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[4096]},\"model.layers.9.linear_attn.A_log\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[32]},\"model.layers.9.linear_attn.conv1d.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[8192,1,4]},\"model.layers.9.linear_attn.dt_bias\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[32]},\"model.layers.9.linear_attn.in_proj_a.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[65536,1]},\"model.layers.9.linear_attn.in_proj_b.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[65536,1]},\"model.layers.9.linear_attn.in_proj_qkv.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[16777216,1]},\"model.layers.9.linear_attn.in_proj_z.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[8388608,1]},\"model.layers.9.linear_attn.norm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[128]},\"model.layers.9.linear_attn.out_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[8388608,1]},\"model.layers.9.mlp.down_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.9.mlp.gate_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.9.mlp.up_proj.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[25165824,1]},\"model.layers.9.post_attention_layernorm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[4096]},\"model.norm.weight\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float16\",\"shape\":[4096]}},\"pid\":365,\"quantization_tensors\":{\"model.layers.0.linear_attn.in_proj_a.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[2048]},\"model.layers.0.linear_attn.in_proj_a.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.0.linear_attn.in_proj_a.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.0.linear_attn.in_proj_a.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[8]},\"model.layers.0.linear_attn.in_proj_a.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.0.linear_attn.in_proj_b.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[2048]},\"model.layers.0.linear_attn.in_proj_b.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.0.linear_attn.in_proj_b.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.0.linear_attn.in_proj_b.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[8]},\"model.layers.0.linear_attn.in_proj_b.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.0.linear_attn.in_proj_qkv.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[524288]},\"model.layers.0.linear_attn.in_proj_qkv.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.0.linear_attn.in_proj_qkv.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.0.linear_attn.in_proj_qkv.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[2048]},\"model.layers.0.linear_attn.in_proj_qkv.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.0.linear_attn.in_proj_z.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[262144]},\"model.layers.0.linear_attn.in_proj_z.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.0.linear_attn.in_proj_z.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.0.linear_attn.in_proj_z.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[1024]},\"model.layers.0.linear_attn.in_proj_z.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.0.linear_attn.out_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[262144]},\"model.layers.0.linear_attn.out_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.0.linear_attn.out_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.0.linear_attn.out_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[1024]},\"model.layers.0.linear_attn.out_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.0.mlp.down_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.0.mlp.down_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.0.mlp.down_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.0.mlp.down_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.0.mlp.down_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.0.mlp.gate_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.0.mlp.gate_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.0.mlp.gate_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.0.mlp.gate_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.0.mlp.gate_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.0.mlp.up_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.0.mlp.up_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.0.mlp.up_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.0.mlp.up_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.0.mlp.up_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.1.linear_attn.in_proj_a.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[2048]},\"model.layers.1.linear_attn.in_proj_a.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.1.linear_attn.in_proj_a.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.1.linear_attn.in_proj_a.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[8]},\"model.layers.1.linear_attn.in_proj_a.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.1.linear_attn.in_proj_b.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[2048]},\"model.layers.1.linear_attn.in_proj_b.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.1.linear_attn.in_proj_b.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.1.linear_attn.in_proj_b.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[8]},\"model.layers.1.linear_attn.in_proj_b.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.1.linear_attn.in_proj_qkv.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[524288]},\"model.layers.1.linear_attn.in_proj_qkv.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.1.linear_attn.in_proj_qkv.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.1.linear_attn.in_proj_qkv.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[2048]},\"model.layers.1.linear_attn.in_proj_qkv.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.1.linear_attn.in_proj_z.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[262144]},\"model.layers.1.linear_attn.in_proj_z.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.1.linear_attn.in_proj_z.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.1.linear_attn.in_proj_z.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[1024]},\"model.layers.1.linear_attn.in_proj_z.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.1.linear_attn.out_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[262144]},\"model.layers.1.linear_attn.out_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.1.linear_attn.out_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.1.linear_attn.out_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[1024]},\"model.layers.1.linear_attn.out_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.1.mlp.down_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.1.mlp.down_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.1.mlp.down_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.1.mlp.down_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.1.mlp.down_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.1.mlp.gate_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.1.mlp.gate_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.1.mlp.gate_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.1.mlp.gate_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.1.mlp.gate_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.1.mlp.up_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.1.mlp.up_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.1.mlp.up_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.1.mlp.up_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.1.mlp.up_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.10.linear_attn.in_proj_a.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[2048]},\"model.layers.10.linear_attn.in_proj_a.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.10.linear_attn.in_proj_a.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.10.linear_attn.in_proj_a.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[8]},\"model.layers.10.linear_attn.in_proj_a.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.10.linear_attn.in_proj_b.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[2048]},\"model.layers.10.linear_attn.in_proj_b.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.10.linear_attn.in_proj_b.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.10.linear_attn.in_proj_b.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[8]},\"model.layers.10.linear_attn.in_proj_b.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.10.linear_attn.in_proj_qkv.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[524288]},\"model.layers.10.linear_attn.in_proj_qkv.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.10.linear_attn.in_proj_qkv.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.10.linear_attn.in_proj_qkv.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[2048]},\"model.layers.10.linear_attn.in_proj_qkv.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.10.linear_attn.in_proj_z.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[262144]},\"model.layers.10.linear_attn.in_proj_z.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.10.linear_attn.in_proj_z.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.10.linear_attn.in_proj_z.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[1024]},\"model.layers.10.linear_attn.in_proj_z.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.10.linear_attn.out_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[262144]},\"model.layers.10.linear_attn.out_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.10.linear_attn.out_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.10.linear_attn.out_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[1024]},\"model.layers.10.linear_attn.out_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.10.mlp.down_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.10.mlp.down_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.10.mlp.down_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.10.mlp.down_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.10.mlp.down_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.10.mlp.gate_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.10.mlp.gate_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.10.mlp.gate_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.10.mlp.gate_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.10.mlp.gate_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.10.mlp.up_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.10.mlp.up_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.10.mlp.up_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.10.mlp.up_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.10.mlp.up_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.11.mlp.down_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.11.mlp.down_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.11.mlp.down_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.11.mlp.down_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.11.mlp.down_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.11.mlp.gate_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.11.mlp.gate_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.11.mlp.gate_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.11.mlp.gate_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.11.mlp.gate_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.11.mlp.up_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.11.mlp.up_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.11.mlp.up_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.11.mlp.up_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.11.mlp.up_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.11.self_attn.k_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[65536]},\"model.layers.11.self_attn.k_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.11.self_attn.k_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.11.self_attn.k_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.11.self_attn.k_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.11.self_attn.o_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[262144]},\"model.layers.11.self_attn.o_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.11.self_attn.o_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.11.self_attn.o_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[1024]},\"model.layers.11.self_attn.o_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.11.self_attn.q_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[524288]},\"model.layers.11.self_attn.q_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.11.self_attn.q_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.11.self_attn.q_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[2048]},\"model.layers.11.self_attn.q_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.11.self_attn.v_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[65536]},\"model.layers.11.self_attn.v_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.11.self_attn.v_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.11.self_attn.v_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.11.self_attn.v_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.12.linear_attn.in_proj_a.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[2048]},\"model.layers.12.linear_attn.in_proj_a.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.12.linear_attn.in_proj_a.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.12.linear_attn.in_proj_a.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[8]},\"model.layers.12.linear_attn.in_proj_a.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.12.linear_attn.in_proj_b.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[2048]},\"model.layers.12.linear_attn.in_proj_b.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.12.linear_attn.in_proj_b.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.12.linear_attn.in_proj_b.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[8]},\"model.layers.12.linear_attn.in_proj_b.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.12.linear_attn.in_proj_qkv.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[524288]},\"model.layers.12.linear_attn.in_proj_qkv.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.12.linear_attn.in_proj_qkv.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.12.linear_attn.in_proj_qkv.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[2048]},\"model.layers.12.linear_attn.in_proj_qkv.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.12.linear_attn.in_proj_z.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[262144]},\"model.layers.12.linear_attn.in_proj_z.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.12.linear_attn.in_proj_z.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.12.linear_attn.in_proj_z.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[1024]},\"model.layers.12.linear_attn.in_proj_z.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.12.linear_attn.out_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[262144]},\"model.layers.12.linear_attn.out_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.12.linear_attn.out_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.12.linear_attn.out_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[1024]},\"model.layers.12.linear_attn.out_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.12.mlp.down_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.12.mlp.down_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.12.mlp.down_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.12.mlp.down_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.12.mlp.down_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.12.mlp.gate_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.12.mlp.gate_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.12.mlp.gate_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.12.mlp.gate_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.12.mlp.gate_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.12.mlp.up_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.12.mlp.up_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.12.mlp.up_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.12.mlp.up_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.12.mlp.up_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.13.linear_attn.in_proj_a.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[2048]},\"model.layers.13.linear_attn.in_proj_a.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.13.linear_attn.in_proj_a.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.13.linear_attn.in_proj_a.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[8]},\"model.layers.13.linear_attn.in_proj_a.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.13.linear_attn.in_proj_b.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[2048]},\"model.layers.13.linear_attn.in_proj_b.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.13.linear_attn.in_proj_b.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.13.linear_attn.in_proj_b.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[8]},\"model.layers.13.linear_attn.in_proj_b.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.13.linear_attn.in_proj_qkv.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[524288]},\"model.layers.13.linear_attn.in_proj_qkv.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.13.linear_attn.in_proj_qkv.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.13.linear_attn.in_proj_qkv.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[2048]},\"model.layers.13.linear_attn.in_proj_qkv.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.13.linear_attn.in_proj_z.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[262144]},\"model.layers.13.linear_attn.in_proj_z.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.13.linear_attn.in_proj_z.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.13.linear_attn.in_proj_z.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[1024]},\"model.layers.13.linear_attn.in_proj_z.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.13.linear_attn.out_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[262144]},\"model.layers.13.linear_attn.out_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.13.linear_attn.out_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.13.linear_attn.out_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[1024]},\"model.layers.13.linear_attn.out_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.13.mlp.down_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.13.mlp.down_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.13.mlp.down_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.13.mlp.down_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.13.mlp.down_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.13.mlp.gate_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.13.mlp.gate_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.13.mlp.gate_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.13.mlp.gate_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.13.mlp.gate_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.13.mlp.up_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.13.mlp.up_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.13.mlp.up_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.13.mlp.up_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.13.mlp.up_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.14.linear_attn.in_proj_a.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[2048]},\"model.layers.14.linear_attn.in_proj_a.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.14.linear_attn.in_proj_a.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.14.linear_attn.in_proj_a.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[8]},\"model.layers.14.linear_attn.in_proj_a.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.14.linear_attn.in_proj_b.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[2048]},\"model.layers.14.linear_attn.in_proj_b.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.14.linear_attn.in_proj_b.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.14.linear_attn.in_proj_b.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[8]},\"model.layers.14.linear_attn.in_proj_b.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.14.linear_attn.in_proj_qkv.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[524288]},\"model.layers.14.linear_attn.in_proj_qkv.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.14.linear_attn.in_proj_qkv.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.14.linear_attn.in_proj_qkv.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[2048]},\"model.layers.14.linear_attn.in_proj_qkv.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.14.linear_attn.in_proj_z.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[262144]},\"model.layers.14.linear_attn.in_proj_z.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.14.linear_attn.in_proj_z.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.14.linear_attn.in_proj_z.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[1024]},\"model.layers.14.linear_attn.in_proj_z.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.14.linear_attn.out_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[262144]},\"model.layers.14.linear_attn.out_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.14.linear_attn.out_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.14.linear_attn.out_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[1024]},\"model.layers.14.linear_attn.out_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.14.mlp.down_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.14.mlp.down_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.14.mlp.down_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.14.mlp.down_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.14.mlp.down_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.14.mlp.gate_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.14.mlp.gate_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.14.mlp.gate_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.14.mlp.gate_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.14.mlp.gate_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.14.mlp.up_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.14.mlp.up_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.14.mlp.up_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.14.mlp.up_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.14.mlp.up_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.15.mlp.down_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.15.mlp.down_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.15.mlp.down_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.15.mlp.down_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.15.mlp.down_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.15.mlp.gate_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.15.mlp.gate_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.15.mlp.gate_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.15.mlp.gate_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.15.mlp.gate_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.15.mlp.up_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.15.mlp.up_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.15.mlp.up_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.15.mlp.up_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.15.mlp.up_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.15.self_attn.k_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[65536]},\"model.layers.15.self_attn.k_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.15.self_attn.k_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.15.self_attn.k_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.15.self_attn.k_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.15.self_attn.o_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[262144]},\"model.layers.15.self_attn.o_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.15.self_attn.o_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.15.self_attn.o_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[1024]},\"model.layers.15.self_attn.o_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.15.self_attn.q_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[524288]},\"model.layers.15.self_attn.q_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.15.self_attn.q_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.15.self_attn.q_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[2048]},\"model.layers.15.self_attn.q_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.15.self_attn.v_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[65536]},\"model.layers.15.self_attn.v_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.15.self_attn.v_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.15.self_attn.v_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.15.self_attn.v_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.16.linear_attn.in_proj_a.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[2048]},\"model.layers.16.linear_attn.in_proj_a.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.16.linear_attn.in_proj_a.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.16.linear_attn.in_proj_a.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[8]},\"model.layers.16.linear_attn.in_proj_a.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.16.linear_attn.in_proj_b.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[2048]},\"model.layers.16.linear_attn.in_proj_b.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.16.linear_attn.in_proj_b.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.16.linear_attn.in_proj_b.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[8]},\"model.layers.16.linear_attn.in_proj_b.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.16.linear_attn.in_proj_qkv.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[524288]},\"model.layers.16.linear_attn.in_proj_qkv.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.16.linear_attn.in_proj_qkv.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.16.linear_attn.in_proj_qkv.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[2048]},\"model.layers.16.linear_attn.in_proj_qkv.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.16.linear_attn.in_proj_z.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[262144]},\"model.layers.16.linear_attn.in_proj_z.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.16.linear_attn.in_proj_z.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.16.linear_attn.in_proj_z.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[1024]},\"model.layers.16.linear_attn.in_proj_z.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.16.linear_attn.out_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[262144]},\"model.layers.16.linear_attn.out_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.16.linear_attn.out_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.16.linear_attn.out_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[1024]},\"model.layers.16.linear_attn.out_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.16.mlp.down_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.16.mlp.down_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.16.mlp.down_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.16.mlp.down_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.16.mlp.down_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.16.mlp.gate_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.16.mlp.gate_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.16.mlp.gate_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.16.mlp.gate_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.16.mlp.gate_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.16.mlp.up_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.16.mlp.up_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.16.mlp.up_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.16.mlp.up_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.16.mlp.up_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.17.linear_attn.in_proj_a.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[2048]},\"model.layers.17.linear_attn.in_proj_a.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.17.linear_attn.in_proj_a.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.17.linear_attn.in_proj_a.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[8]},\"model.layers.17.linear_attn.in_proj_a.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.17.linear_attn.in_proj_b.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[2048]},\"model.layers.17.linear_attn.in_proj_b.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.17.linear_attn.in_proj_b.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.17.linear_attn.in_proj_b.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[8]},\"model.layers.17.linear_attn.in_proj_b.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.17.linear_attn.in_proj_qkv.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[524288]},\"model.layers.17.linear_attn.in_proj_qkv.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.17.linear_attn.in_proj_qkv.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.17.linear_attn.in_proj_qkv.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[2048]},\"model.layers.17.linear_attn.in_proj_qkv.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.17.linear_attn.in_proj_z.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[262144]},\"model.layers.17.linear_attn.in_proj_z.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.17.linear_attn.in_proj_z.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.17.linear_attn.in_proj_z.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[1024]},\"model.layers.17.linear_attn.in_proj_z.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.17.linear_attn.out_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[262144]},\"model.layers.17.linear_attn.out_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.17.linear_attn.out_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.17.linear_attn.out_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[1024]},\"model.layers.17.linear_attn.out_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.17.mlp.down_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.17.mlp.down_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.17.mlp.down_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.17.mlp.down_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.17.mlp.down_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.17.mlp.gate_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.17.mlp.gate_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.17.mlp.gate_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.17.mlp.gate_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.17.mlp.gate_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.17.mlp.up_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.17.mlp.up_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.17.mlp.up_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.17.mlp.up_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.17.mlp.up_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.18.linear_attn.in_proj_a.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[2048]},\"model.layers.18.linear_attn.in_proj_a.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.18.linear_attn.in_proj_a.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.18.linear_attn.in_proj_a.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[8]},\"model.layers.18.linear_attn.in_proj_a.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.18.linear_attn.in_proj_b.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[2048]},\"model.layers.18.linear_attn.in_proj_b.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.18.linear_attn.in_proj_b.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.18.linear_attn.in_proj_b.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[8]},\"model.layers.18.linear_attn.in_proj_b.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.18.linear_attn.in_proj_qkv.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[524288]},\"model.layers.18.linear_attn.in_proj_qkv.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.18.linear_attn.in_proj_qkv.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.18.linear_attn.in_proj_qkv.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[2048]},\"model.layers.18.linear_attn.in_proj_qkv.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.18.linear_attn.in_proj_z.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[262144]},\"model.layers.18.linear_attn.in_proj_z.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.18.linear_attn.in_proj_z.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.18.linear_attn.in_proj_z.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[1024]},\"model.layers.18.linear_attn.in_proj_z.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.18.linear_attn.out_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[262144]},\"model.layers.18.linear_attn.out_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.18.linear_attn.out_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.18.linear_attn.out_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[1024]},\"model.layers.18.linear_attn.out_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.18.mlp.down_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.18.mlp.down_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.18.mlp.down_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.18.mlp.down_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.18.mlp.down_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.18.mlp.gate_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.18.mlp.gate_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.18.mlp.gate_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.18.mlp.gate_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.18.mlp.gate_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.18.mlp.up_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.18.mlp.up_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.18.mlp.up_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.18.mlp.up_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.18.mlp.up_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.19.mlp.down_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.19.mlp.down_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.19.mlp.down_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.19.mlp.down_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.19.mlp.down_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.19.mlp.gate_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.19.mlp.gate_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.19.mlp.gate_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.19.mlp.gate_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.19.mlp.gate_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.19.mlp.up_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.19.mlp.up_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.19.mlp.up_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.19.mlp.up_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.19.mlp.up_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.19.self_attn.k_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[65536]},\"model.layers.19.self_attn.k_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.19.self_attn.k_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.19.self_attn.k_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.19.self_attn.k_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.19.self_attn.o_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[262144]},\"model.layers.19.self_attn.o_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.19.self_attn.o_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.19.self_attn.o_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[1024]},\"model.layers.19.self_attn.o_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.19.self_attn.q_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[524288]},\"model.layers.19.self_attn.q_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.19.self_attn.q_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.19.self_attn.q_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[2048]},\"model.layers.19.self_attn.q_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.19.self_attn.v_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[65536]},\"model.layers.19.self_attn.v_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.19.self_attn.v_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.19.self_attn.v_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.19.self_attn.v_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.2.linear_attn.in_proj_a.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[2048]},\"model.layers.2.linear_attn.in_proj_a.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.2.linear_attn.in_proj_a.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.2.linear_attn.in_proj_a.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[8]},\"model.layers.2.linear_attn.in_proj_a.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.2.linear_attn.in_proj_b.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[2048]},\"model.layers.2.linear_attn.in_proj_b.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.2.linear_attn.in_proj_b.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.2.linear_attn.in_proj_b.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[8]},\"model.layers.2.linear_attn.in_proj_b.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.2.linear_attn.in_proj_qkv.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[524288]},\"model.layers.2.linear_attn.in_proj_qkv.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.2.linear_attn.in_proj_qkv.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.2.linear_attn.in_proj_qkv.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[2048]},\"model.layers.2.linear_attn.in_proj_qkv.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.2.linear_attn.in_proj_z.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[262144]},\"model.layers.2.linear_attn.in_proj_z.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.2.linear_attn.in_proj_z.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.2.linear_attn.in_proj_z.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[1024]},\"model.layers.2.linear_attn.in_proj_z.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.2.linear_attn.out_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[262144]},\"model.layers.2.linear_attn.out_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.2.linear_attn.out_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.2.linear_attn.out_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[1024]},\"model.layers.2.linear_attn.out_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.2.mlp.down_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.2.mlp.down_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.2.mlp.down_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.2.mlp.down_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.2.mlp.down_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.2.mlp.gate_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.2.mlp.gate_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.2.mlp.gate_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.2.mlp.gate_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.2.mlp.gate_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.2.mlp.up_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.2.mlp.up_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.2.mlp.up_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.2.mlp.up_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.2.mlp.up_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.20.linear_attn.in_proj_a.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[2048]},\"model.layers.20.linear_attn.in_proj_a.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.20.linear_attn.in_proj_a.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.20.linear_attn.in_proj_a.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[8]},\"model.layers.20.linear_attn.in_proj_a.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.20.linear_attn.in_proj_b.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[2048]},\"model.layers.20.linear_attn.in_proj_b.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.20.linear_attn.in_proj_b.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.20.linear_attn.in_proj_b.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[8]},\"model.layers.20.linear_attn.in_proj_b.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.20.linear_attn.in_proj_qkv.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[524288]},\"model.layers.20.linear_attn.in_proj_qkv.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.20.linear_attn.in_proj_qkv.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.20.linear_attn.in_proj_qkv.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[2048]},\"model.layers.20.linear_attn.in_proj_qkv.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.20.linear_attn.in_proj_z.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[262144]},\"model.layers.20.linear_attn.in_proj_z.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.20.linear_attn.in_proj_z.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.20.linear_attn.in_proj_z.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[1024]},\"model.layers.20.linear_attn.in_proj_z.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.20.linear_attn.out_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[262144]},\"model.layers.20.linear_attn.out_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.20.linear_attn.out_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.20.linear_attn.out_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[1024]},\"model.layers.20.linear_attn.out_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.20.mlp.down_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.20.mlp.down_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.20.mlp.down_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.20.mlp.down_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.20.mlp.down_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.20.mlp.gate_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.20.mlp.gate_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.20.mlp.gate_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.20.mlp.gate_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.20.mlp.gate_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.20.mlp.up_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.20.mlp.up_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.20.mlp.up_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.20.mlp.up_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.20.mlp.up_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.21.linear_attn.in_proj_a.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[2048]},\"model.layers.21.linear_attn.in_proj_a.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.21.linear_attn.in_proj_a.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.21.linear_attn.in_proj_a.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[8]},\"model.layers.21.linear_attn.in_proj_a.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.21.linear_attn.in_proj_b.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[2048]},\"model.layers.21.linear_attn.in_proj_b.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.21.linear_attn.in_proj_b.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.21.linear_attn.in_proj_b.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[8]},\"model.layers.21.linear_attn.in_proj_b.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.21.linear_attn.in_proj_qkv.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[524288]},\"model.layers.21.linear_attn.in_proj_qkv.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.21.linear_attn.in_proj_qkv.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.21.linear_attn.in_proj_qkv.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[2048]},\"model.layers.21.linear_attn.in_proj_qkv.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.21.linear_attn.in_proj_z.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[262144]},\"model.layers.21.linear_attn.in_proj_z.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.21.linear_attn.in_proj_z.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.21.linear_attn.in_proj_z.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[1024]},\"model.layers.21.linear_attn.in_proj_z.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.21.linear_attn.out_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[262144]},\"model.layers.21.linear_attn.out_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.21.linear_attn.out_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.21.linear_attn.out_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[1024]},\"model.layers.21.linear_attn.out_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.21.mlp.down_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.21.mlp.down_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.21.mlp.down_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.21.mlp.down_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.21.mlp.down_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.21.mlp.gate_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.21.mlp.gate_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.21.mlp.gate_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.21.mlp.gate_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.21.mlp.gate_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.21.mlp.up_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.21.mlp.up_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.21.mlp.up_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.21.mlp.up_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.21.mlp.up_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.22.linear_attn.in_proj_a.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[2048]},\"model.layers.22.linear_attn.in_proj_a.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.22.linear_attn.in_proj_a.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.22.linear_attn.in_proj_a.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[8]},\"model.layers.22.linear_attn.in_proj_a.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.22.linear_attn.in_proj_b.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[2048]},\"model.layers.22.linear_attn.in_proj_b.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.22.linear_attn.in_proj_b.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.22.linear_attn.in_proj_b.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[8]},\"model.layers.22.linear_attn.in_proj_b.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.22.linear_attn.in_proj_qkv.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[524288]},\"model.layers.22.linear_attn.in_proj_qkv.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.22.linear_attn.in_proj_qkv.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.22.linear_attn.in_proj_qkv.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[2048]},\"model.layers.22.linear_attn.in_proj_qkv.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.22.linear_attn.in_proj_z.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[262144]},\"model.layers.22.linear_attn.in_proj_z.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.22.linear_attn.in_proj_z.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.22.linear_attn.in_proj_z.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[1024]},\"model.layers.22.linear_attn.in_proj_z.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.22.linear_attn.out_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[262144]},\"model.layers.22.linear_attn.out_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.22.linear_attn.out_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.22.linear_attn.out_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[1024]},\"model.layers.22.linear_attn.out_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.22.mlp.down_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.22.mlp.down_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.22.mlp.down_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.22.mlp.down_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.22.mlp.down_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.22.mlp.gate_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.22.mlp.gate_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.22.mlp.gate_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.22.mlp.gate_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.22.mlp.gate_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.22.mlp.up_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.22.mlp.up_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.22.mlp.up_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.22.mlp.up_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.22.mlp.up_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.23.mlp.down_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.23.mlp.down_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.23.mlp.down_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.23.mlp.down_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.23.mlp.down_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.23.mlp.gate_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.23.mlp.gate_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.23.mlp.gate_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.23.mlp.gate_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.23.mlp.gate_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.23.mlp.up_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.23.mlp.up_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.23.mlp.up_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.23.mlp.up_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.23.mlp.up_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.23.self_attn.k_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[65536]},\"model.layers.23.self_attn.k_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.23.self_attn.k_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.23.self_attn.k_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.23.self_attn.k_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.23.self_attn.o_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[262144]},\"model.layers.23.self_attn.o_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.23.self_attn.o_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.23.self_attn.o_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[1024]},\"model.layers.23.self_attn.o_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.23.self_attn.q_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[524288]},\"model.layers.23.self_attn.q_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.23.self_attn.q_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.23.self_attn.q_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[2048]},\"model.layers.23.self_attn.q_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.23.self_attn.v_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[65536]},\"model.layers.23.self_attn.v_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.23.self_attn.v_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.23.self_attn.v_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.23.self_attn.v_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.24.linear_attn.in_proj_a.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[2048]},\"model.layers.24.linear_attn.in_proj_a.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.24.linear_attn.in_proj_a.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.24.linear_attn.in_proj_a.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[8]},\"model.layers.24.linear_attn.in_proj_a.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.24.linear_attn.in_proj_b.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[2048]},\"model.layers.24.linear_attn.in_proj_b.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.24.linear_attn.in_proj_b.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.24.linear_attn.in_proj_b.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[8]},\"model.layers.24.linear_attn.in_proj_b.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.24.linear_attn.in_proj_qkv.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[524288]},\"model.layers.24.linear_attn.in_proj_qkv.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.24.linear_attn.in_proj_qkv.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.24.linear_attn.in_proj_qkv.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[2048]},\"model.layers.24.linear_attn.in_proj_qkv.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.24.linear_attn.in_proj_z.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[262144]},\"model.layers.24.linear_attn.in_proj_z.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.24.linear_attn.in_proj_z.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.24.linear_attn.in_proj_z.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[1024]},\"model.layers.24.linear_attn.in_proj_z.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.24.linear_attn.out_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[262144]},\"model.layers.24.linear_attn.out_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.24.linear_attn.out_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.24.linear_attn.out_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[1024]},\"model.layers.24.linear_attn.out_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.24.mlp.down_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.24.mlp.down_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.24.mlp.down_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.24.mlp.down_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.24.mlp.down_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.24.mlp.gate_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.24.mlp.gate_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.24.mlp.gate_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.24.mlp.gate_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.24.mlp.gate_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.24.mlp.up_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.24.mlp.up_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.24.mlp.up_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.24.mlp.up_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.24.mlp.up_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.25.linear_attn.in_proj_a.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[2048]},\"model.layers.25.linear_attn.in_proj_a.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.25.linear_attn.in_proj_a.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.25.linear_attn.in_proj_a.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[8]},\"model.layers.25.linear_attn.in_proj_a.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.25.linear_attn.in_proj_b.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[2048]},\"model.layers.25.linear_attn.in_proj_b.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.25.linear_attn.in_proj_b.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.25.linear_attn.in_proj_b.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[8]},\"model.layers.25.linear_attn.in_proj_b.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.25.linear_attn.in_proj_qkv.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[524288]},\"model.layers.25.linear_attn.in_proj_qkv.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.25.linear_attn.in_proj_qkv.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.25.linear_attn.in_proj_qkv.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[2048]},\"model.layers.25.linear_attn.in_proj_qkv.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.25.linear_attn.in_proj_z.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[262144]},\"model.layers.25.linear_attn.in_proj_z.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.25.linear_attn.in_proj_z.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.25.linear_attn.in_proj_z.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[1024]},\"model.layers.25.linear_attn.in_proj_z.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.25.linear_attn.out_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[262144]},\"model.layers.25.linear_attn.out_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.25.linear_attn.out_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.25.linear_attn.out_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[1024]},\"model.layers.25.linear_attn.out_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.25.mlp.down_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.25.mlp.down_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.25.mlp.down_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.25.mlp.down_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.25.mlp.down_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.25.mlp.gate_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.25.mlp.gate_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.25.mlp.gate_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.25.mlp.gate_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.25.mlp.gate_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.25.mlp.up_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.25.mlp.up_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.25.mlp.up_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.25.mlp.up_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.25.mlp.up_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.26.linear_attn.in_proj_a.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[2048]},\"model.layers.26.linear_attn.in_proj_a.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.26.linear_attn.in_proj_a.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.26.linear_attn.in_proj_a.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[8]},\"model.layers.26.linear_attn.in_proj_a.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.26.linear_attn.in_proj_b.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[2048]},\"model.layers.26.linear_attn.in_proj_b.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.26.linear_attn.in_proj_b.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.26.linear_attn.in_proj_b.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[8]},\"model.layers.26.linear_attn.in_proj_b.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.26.linear_attn.in_proj_qkv.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[524288]},\"model.layers.26.linear_attn.in_proj_qkv.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.26.linear_attn.in_proj_qkv.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.26.linear_attn.in_proj_qkv.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[2048]},\"model.layers.26.linear_attn.in_proj_qkv.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.26.linear_attn.in_proj_z.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[262144]},\"model.layers.26.linear_attn.in_proj_z.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.26.linear_attn.in_proj_z.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.26.linear_attn.in_proj_z.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[1024]},\"model.layers.26.linear_attn.in_proj_z.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.26.linear_attn.out_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[262144]},\"model.layers.26.linear_attn.out_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.26.linear_attn.out_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.26.linear_attn.out_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[1024]},\"model.layers.26.linear_attn.out_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.26.mlp.down_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.26.mlp.down_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.26.mlp.down_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.26.mlp.down_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.26.mlp.down_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.26.mlp.gate_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.26.mlp.gate_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.26.mlp.gate_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.26.mlp.gate_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.26.mlp.gate_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.26.mlp.up_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.26.mlp.up_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.26.mlp.up_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.26.mlp.up_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.26.mlp.up_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.27.mlp.down_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.27.mlp.down_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.27.mlp.down_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.27.mlp.down_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.27.mlp.down_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.27.mlp.gate_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.27.mlp.gate_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.27.mlp.gate_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.27.mlp.gate_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.27.mlp.gate_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.27.mlp.up_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.27.mlp.up_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.27.mlp.up_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.27.mlp.up_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.27.mlp.up_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.27.self_attn.k_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[65536]},\"model.layers.27.self_attn.k_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.27.self_attn.k_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.27.self_attn.k_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.27.self_attn.k_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.27.self_attn.o_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[262144]},\"model.layers.27.self_attn.o_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.27.self_attn.o_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.27.self_attn.o_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[1024]},\"model.layers.27.self_attn.o_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.27.self_attn.q_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[524288]},\"model.layers.27.self_attn.q_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.27.self_attn.q_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.27.self_attn.q_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[2048]},\"model.layers.27.self_attn.q_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.27.self_attn.v_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[65536]},\"model.layers.27.self_attn.v_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.27.self_attn.v_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.27.self_attn.v_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.27.self_attn.v_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.28.linear_attn.in_proj_a.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[2048]},\"model.layers.28.linear_attn.in_proj_a.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.28.linear_attn.in_proj_a.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.28.linear_attn.in_proj_a.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[8]},\"model.layers.28.linear_attn.in_proj_a.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.28.linear_attn.in_proj_b.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[2048]},\"model.layers.28.linear_attn.in_proj_b.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.28.linear_attn.in_proj_b.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.28.linear_attn.in_proj_b.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[8]},\"model.layers.28.linear_attn.in_proj_b.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.28.linear_attn.in_proj_qkv.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[524288]},\"model.layers.28.linear_attn.in_proj_qkv.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.28.linear_attn.in_proj_qkv.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.28.linear_attn.in_proj_qkv.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[2048]},\"model.layers.28.linear_attn.in_proj_qkv.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.28.linear_attn.in_proj_z.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[262144]},\"model.layers.28.linear_attn.in_proj_z.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.28.linear_attn.in_proj_z.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.28.linear_attn.in_proj_z.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[1024]},\"model.layers.28.linear_attn.in_proj_z.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.28.linear_attn.out_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[262144]},\"model.layers.28.linear_attn.out_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.28.linear_attn.out_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.28.linear_attn.out_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[1024]},\"model.layers.28.linear_attn.out_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.28.mlp.down_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.28.mlp.down_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.28.mlp.down_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.28.mlp.down_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.28.mlp.down_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.28.mlp.gate_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.28.mlp.gate_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.28.mlp.gate_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.28.mlp.gate_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.28.mlp.gate_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.28.mlp.up_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.28.mlp.up_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.28.mlp.up_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.28.mlp.up_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.28.mlp.up_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.29.linear_attn.in_proj_a.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[2048]},\"model.layers.29.linear_attn.in_proj_a.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.29.linear_attn.in_proj_a.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.29.linear_attn.in_proj_a.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[8]},\"model.layers.29.linear_attn.in_proj_a.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.29.linear_attn.in_proj_b.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[2048]},\"model.layers.29.linear_attn.in_proj_b.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.29.linear_attn.in_proj_b.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.29.linear_attn.in_proj_b.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[8]},\"model.layers.29.linear_attn.in_proj_b.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.29.linear_attn.in_proj_qkv.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[524288]},\"model.layers.29.linear_attn.in_proj_qkv.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.29.linear_attn.in_proj_qkv.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.29.linear_attn.in_proj_qkv.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[2048]},\"model.layers.29.linear_attn.in_proj_qkv.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.29.linear_attn.in_proj_z.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[262144]},\"model.layers.29.linear_attn.in_proj_z.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.29.linear_attn.in_proj_z.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.29.linear_attn.in_proj_z.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[1024]},\"model.layers.29.linear_attn.in_proj_z.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.29.linear_attn.out_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[262144]},\"model.layers.29.linear_attn.out_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.29.linear_attn.out_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.29.linear_attn.out_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[1024]},\"model.layers.29.linear_attn.out_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.29.mlp.down_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.29.mlp.down_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.29.mlp.down_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.29.mlp.down_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.29.mlp.down_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.29.mlp.gate_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.29.mlp.gate_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.29.mlp.gate_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.29.mlp.gate_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.29.mlp.gate_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.29.mlp.up_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.29.mlp.up_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.29.mlp.up_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.29.mlp.up_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.29.mlp.up_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.3.mlp.down_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.3.mlp.down_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.3.mlp.down_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.3.mlp.down_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.3.mlp.down_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.3.mlp.gate_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.3.mlp.gate_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.3.mlp.gate_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.3.mlp.gate_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.3.mlp.gate_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.3.mlp.up_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.3.mlp.up_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.3.mlp.up_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.3.mlp.up_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.3.mlp.up_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.3.self_attn.k_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[65536]},\"model.layers.3.self_attn.k_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.3.self_attn.k_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.3.self_attn.k_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.3.self_attn.k_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.3.self_attn.o_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[262144]},\"model.layers.3.self_attn.o_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.3.self_attn.o_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.3.self_attn.o_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[1024]},\"model.layers.3.self_attn.o_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.3.self_attn.q_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[524288]},\"model.layers.3.self_attn.q_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.3.self_attn.q_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.3.self_attn.q_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[2048]},\"model.layers.3.self_attn.q_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.3.self_attn.v_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[65536]},\"model.layers.3.self_attn.v_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.3.self_attn.v_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.3.self_attn.v_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.3.self_attn.v_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.30.linear_attn.in_proj_a.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[2048]},\"model.layers.30.linear_attn.in_proj_a.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.30.linear_attn.in_proj_a.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.30.linear_attn.in_proj_a.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[8]},\"model.layers.30.linear_attn.in_proj_a.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.30.linear_attn.in_proj_b.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[2048]},\"model.layers.30.linear_attn.in_proj_b.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.30.linear_attn.in_proj_b.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.30.linear_attn.in_proj_b.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[8]},\"model.layers.30.linear_attn.in_proj_b.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.30.linear_attn.in_proj_qkv.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[524288]},\"model.layers.30.linear_attn.in_proj_qkv.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.30.linear_attn.in_proj_qkv.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.30.linear_attn.in_proj_qkv.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[2048]},\"model.layers.30.linear_attn.in_proj_qkv.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.30.linear_attn.in_proj_z.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[262144]},\"model.layers.30.linear_attn.in_proj_z.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.30.linear_attn.in_proj_z.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.30.linear_attn.in_proj_z.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[1024]},\"model.layers.30.linear_attn.in_proj_z.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.30.linear_attn.out_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[262144]},\"model.layers.30.linear_attn.out_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.30.linear_attn.out_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.30.linear_attn.out_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[1024]},\"model.layers.30.linear_attn.out_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.30.mlp.down_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.30.mlp.down_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.30.mlp.down_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.30.mlp.down_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.30.mlp.down_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.30.mlp.gate_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.30.mlp.gate_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.30.mlp.gate_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.30.mlp.gate_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.30.mlp.gate_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.30.mlp.up_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.30.mlp.up_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.30.mlp.up_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.30.mlp.up_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.30.mlp.up_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.31.mlp.down_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.31.mlp.down_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.31.mlp.down_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.31.mlp.down_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.31.mlp.down_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.31.mlp.gate_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.31.mlp.gate_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.31.mlp.gate_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.31.mlp.gate_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.31.mlp.gate_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.31.mlp.up_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.31.mlp.up_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.31.mlp.up_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.31.mlp.up_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.31.mlp.up_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.31.self_attn.k_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[65536]},\"model.layers.31.self_attn.k_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.31.self_attn.k_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.31.self_attn.k_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.31.self_attn.k_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.31.self_attn.o_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[262144]},\"model.layers.31.self_attn.o_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.31.self_attn.o_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.31.self_attn.o_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[1024]},\"model.layers.31.self_attn.o_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.31.self_attn.q_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[524288]},\"model.layers.31.self_attn.q_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.31.self_attn.q_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.31.self_attn.q_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[2048]},\"model.layers.31.self_attn.q_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.31.self_attn.v_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[65536]},\"model.layers.31.self_attn.v_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.31.self_attn.v_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.31.self_attn.v_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.31.self_attn.v_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.4.linear_attn.in_proj_a.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[2048]},\"model.layers.4.linear_attn.in_proj_a.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.4.linear_attn.in_proj_a.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.4.linear_attn.in_proj_a.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[8]},\"model.layers.4.linear_attn.in_proj_a.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.4.linear_attn.in_proj_b.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[2048]},\"model.layers.4.linear_attn.in_proj_b.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.4.linear_attn.in_proj_b.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.4.linear_attn.in_proj_b.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[8]},\"model.layers.4.linear_attn.in_proj_b.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.4.linear_attn.in_proj_qkv.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[524288]},\"model.layers.4.linear_attn.in_proj_qkv.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.4.linear_attn.in_proj_qkv.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.4.linear_attn.in_proj_qkv.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[2048]},\"model.layers.4.linear_attn.in_proj_qkv.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.4.linear_attn.in_proj_z.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[262144]},\"model.layers.4.linear_attn.in_proj_z.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.4.linear_attn.in_proj_z.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.4.linear_attn.in_proj_z.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[1024]},\"model.layers.4.linear_attn.in_proj_z.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.4.linear_attn.out_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[262144]},\"model.layers.4.linear_attn.out_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.4.linear_attn.out_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.4.linear_attn.out_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[1024]},\"model.layers.4.linear_attn.out_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.4.mlp.down_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.4.mlp.down_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.4.mlp.down_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.4.mlp.down_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.4.mlp.down_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.4.mlp.gate_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.4.mlp.gate_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.4.mlp.gate_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.4.mlp.gate_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.4.mlp.gate_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.4.mlp.up_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.4.mlp.up_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.4.mlp.up_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.4.mlp.up_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.4.mlp.up_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.5.linear_attn.in_proj_a.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[2048]},\"model.layers.5.linear_attn.in_proj_a.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.5.linear_attn.in_proj_a.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.5.linear_attn.in_proj_a.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[8]},\"model.layers.5.linear_attn.in_proj_a.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.5.linear_attn.in_proj_b.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[2048]},\"model.layers.5.linear_attn.in_proj_b.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.5.linear_attn.in_proj_b.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.5.linear_attn.in_proj_b.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[8]},\"model.layers.5.linear_attn.in_proj_b.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.5.linear_attn.in_proj_qkv.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[524288]},\"model.layers.5.linear_attn.in_proj_qkv.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.5.linear_attn.in_proj_qkv.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.5.linear_attn.in_proj_qkv.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[2048]},\"model.layers.5.linear_attn.in_proj_qkv.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.5.linear_attn.in_proj_z.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[262144]},\"model.layers.5.linear_attn.in_proj_z.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.5.linear_attn.in_proj_z.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.5.linear_attn.in_proj_z.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[1024]},\"model.layers.5.linear_attn.in_proj_z.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.5.linear_attn.out_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[262144]},\"model.layers.5.linear_attn.out_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.5.linear_attn.out_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.5.linear_attn.out_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[1024]},\"model.layers.5.linear_attn.out_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.5.mlp.down_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.5.mlp.down_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.5.mlp.down_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.5.mlp.down_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.5.mlp.down_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.5.mlp.gate_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.5.mlp.gate_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.5.mlp.gate_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.5.mlp.gate_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.5.mlp.gate_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.5.mlp.up_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.5.mlp.up_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.5.mlp.up_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.5.mlp.up_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.5.mlp.up_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.6.linear_attn.in_proj_a.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[2048]},\"model.layers.6.linear_attn.in_proj_a.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.6.linear_attn.in_proj_a.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.6.linear_attn.in_proj_a.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[8]},\"model.layers.6.linear_attn.in_proj_a.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.6.linear_attn.in_proj_b.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[2048]},\"model.layers.6.linear_attn.in_proj_b.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.6.linear_attn.in_proj_b.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.6.linear_attn.in_proj_b.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[8]},\"model.layers.6.linear_attn.in_proj_b.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.6.linear_attn.in_proj_qkv.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[524288]},\"model.layers.6.linear_attn.in_proj_qkv.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.6.linear_attn.in_proj_qkv.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.6.linear_attn.in_proj_qkv.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[2048]},\"model.layers.6.linear_attn.in_proj_qkv.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.6.linear_attn.in_proj_z.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[262144]},\"model.layers.6.linear_attn.in_proj_z.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.6.linear_attn.in_proj_z.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.6.linear_attn.in_proj_z.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[1024]},\"model.layers.6.linear_attn.in_proj_z.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.6.linear_attn.out_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[262144]},\"model.layers.6.linear_attn.out_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.6.linear_attn.out_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.6.linear_attn.out_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[1024]},\"model.layers.6.linear_attn.out_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.6.mlp.down_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.6.mlp.down_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.6.mlp.down_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.6.mlp.down_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.6.mlp.down_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.6.mlp.gate_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.6.mlp.gate_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.6.mlp.gate_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.6.mlp.gate_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.6.mlp.gate_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.6.mlp.up_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.6.mlp.up_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.6.mlp.up_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.6.mlp.up_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.6.mlp.up_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.7.mlp.down_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.7.mlp.down_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.7.mlp.down_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.7.mlp.down_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.7.mlp.down_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.7.mlp.gate_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.7.mlp.gate_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.7.mlp.gate_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.7.mlp.gate_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.7.mlp.gate_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.7.mlp.up_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.7.mlp.up_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.7.mlp.up_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.7.mlp.up_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.7.mlp.up_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.7.self_attn.k_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[65536]},\"model.layers.7.self_attn.k_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.7.self_attn.k_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.7.self_attn.k_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.7.self_attn.k_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.7.self_attn.o_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[262144]},\"model.layers.7.self_attn.o_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.7.self_attn.o_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.7.self_attn.o_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[1024]},\"model.layers.7.self_attn.o_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.7.self_attn.q_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[524288]},\"model.layers.7.self_attn.q_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.7.self_attn.q_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.7.self_attn.q_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[2048]},\"model.layers.7.self_attn.q_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.7.self_attn.v_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[65536]},\"model.layers.7.self_attn.v_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.7.self_attn.v_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.7.self_attn.v_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.7.self_attn.v_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.8.linear_attn.in_proj_a.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[2048]},\"model.layers.8.linear_attn.in_proj_a.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.8.linear_attn.in_proj_a.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.8.linear_attn.in_proj_a.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[8]},\"model.layers.8.linear_attn.in_proj_a.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.8.linear_attn.in_proj_b.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[2048]},\"model.layers.8.linear_attn.in_proj_b.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.8.linear_attn.in_proj_b.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.8.linear_attn.in_proj_b.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[8]},\"model.layers.8.linear_attn.in_proj_b.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.8.linear_attn.in_proj_qkv.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[524288]},\"model.layers.8.linear_attn.in_proj_qkv.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.8.linear_attn.in_proj_qkv.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.8.linear_attn.in_proj_qkv.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[2048]},\"model.layers.8.linear_attn.in_proj_qkv.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.8.linear_attn.in_proj_z.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[262144]},\"model.layers.8.linear_attn.in_proj_z.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.8.linear_attn.in_proj_z.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.8.linear_attn.in_proj_z.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[1024]},\"model.layers.8.linear_attn.in_proj_z.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.8.linear_attn.out_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[262144]},\"model.layers.8.linear_attn.out_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.8.linear_attn.out_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.8.linear_attn.out_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[1024]},\"model.layers.8.linear_attn.out_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.8.mlp.down_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.8.mlp.down_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.8.mlp.down_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.8.mlp.down_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.8.mlp.down_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.8.mlp.gate_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.8.mlp.gate_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.8.mlp.gate_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.8.mlp.gate_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.8.mlp.gate_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.8.mlp.up_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.8.mlp.up_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.8.mlp.up_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.8.mlp.up_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.8.mlp.up_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.9.linear_attn.in_proj_a.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[2048]},\"model.layers.9.linear_attn.in_proj_a.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.9.linear_attn.in_proj_a.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.9.linear_attn.in_proj_a.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[8]},\"model.layers.9.linear_attn.in_proj_a.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.9.linear_attn.in_proj_b.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[2048]},\"model.layers.9.linear_attn.in_proj_b.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.9.linear_attn.in_proj_b.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.9.linear_attn.in_proj_b.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[8]},\"model.layers.9.linear_attn.in_proj_b.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.9.linear_attn.in_proj_qkv.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[524288]},\"model.layers.9.linear_attn.in_proj_qkv.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.9.linear_attn.in_proj_qkv.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.9.linear_attn.in_proj_qkv.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[2048]},\"model.layers.9.linear_attn.in_proj_qkv.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.9.linear_attn.in_proj_z.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[262144]},\"model.layers.9.linear_attn.in_proj_z.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.9.linear_attn.in_proj_z.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.9.linear_attn.in_proj_z.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[1024]},\"model.layers.9.linear_attn.in_proj_z.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.9.linear_attn.out_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[262144]},\"model.layers.9.linear_attn.out_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.9.linear_attn.out_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.9.linear_attn.out_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[1024]},\"model.layers.9.linear_attn.out_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.9.mlp.down_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.9.mlp.down_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.9.mlp.down_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.9.mlp.down_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.9.mlp.down_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.9.mlp.gate_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.9.mlp.gate_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.9.mlp.gate_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.9.mlp.gate_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.9.mlp.gate_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]},\"model.layers.9.mlp.up_proj.weight.quant_state.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.uint8\",\"shape\":[786432]},\"model.layers.9.mlp.up_proj.weight.quant_state.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[16]},\"model.layers.9.mlp.up_proj.weight.quant_state.offset\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[]},\"model.layers.9.mlp.up_proj.weight.quant_state.state2.absmax\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[3072]},\"model.layers.9.mlp.up_proj.weight.quant_state.state2.code\":{\"device\":\"cuda:0\",\"dtype\":\"torch.float32\",\"shape\":[256]}},\"recurrent_fast_path\":false,\"requested_device_map\":{\"\":0},\"revision\":\"c202236235762e1c871ad0ccb60c8ee5ba337b9a\",\"tied_output_head\":false,\"total_device_bytes\":15636037632,\"verified_snapshot\":\"/kaggle/temp/i01/hf-cache/models--Qwen--Qwen3.5-9B/snapshots/c202236235762e1c871ad0ccb60c8ee5ba337b9a\"},\"session\":\"a7bb7845-cf04-4efd-9b68-f74b9595cfaa\",\"slot\":1,\"window\":{\"deadline\":\"2026-10-16T05:20:47.399377+00:00\",\"evidence\":\"User reports an approximately 12-hour session; 700-minute fresh-session planning bound, provider quota/deadline not independently verified.\",\"observation\":{\"at\":\"2026-10-15T17:40:47.399455+00:00\",\"basis\":\"planning_estimate\",\"remaining_minutes\":700},\"observed_start\":\"2026-10-15T17:44:39.516556+00:00\",\"session\":\"a7bb7845-cf04-4efd-9b68-f74b9595cfaa\"}}",
            "id": "a7bb7845-cf04-4efd-9b68-f74b9595cfaa/load-0"
          }
        ]
      ],
      "settings": {
        "attention": "recovery_t4_sdpa",
        "chat_template": "{%- set image_count = namespace(value=0) %}\n{%- set video_count = namespace(value=0) %}\n{%- macro render_content(content, do_vision_count, is_system_content=false) %}\n    {%- if content is string %}\n        {{- content }}\n    {%- elif content is iterable and content is not mapping %}\n        {%- for item in content %}\n            {%- if 'image' in item or 'image_url' in item or item.type == 'image' %}\n                {%- if is_system_content %}\n                    {{- raise_exception('System message cannot contain images.') }}\n                {%- endif %}\n                {%- if do_vision_count %}\n                    {%- set image_count.value = image_count.value + 1 %}\n                {%- endif %}\n                {%- if add_vision_id %}\n                    {{- 'Picture ' ~ image_count.value ~ ': ' }}\n                {%- endif %}\n                {{- '<|vision_start|><|image_pad|><|vision_end|>' }}\n            {%- elif 'video' in item or item.type == 'video' %}\n                {%- if is_system_content %}\n                    {{- raise_exception('System message cannot contain videos.') }}\n                {%- endif %}\n                {%- if do_vision_count %}\n                    {%- set video_count.value = video_count.value + 1 %}\n                {%- endif %}\n                {%- if add_vision_id %}\n                    {{- 'Video ' ~ video_count.value ~ ': ' }}\n                {%- endif %}\n                {{- '<|vision_start|><|video_pad|><|vision_end|>' }}\n            {%- elif 'text' in item %}\n                {{- item.text }}\n            {%- else %}\n                {{- raise_exception('Unexpected item type in content.') }}\n            {%- endif %}\n        {%- endfor %}\n    {%- elif content is none or content is undefined %}\n        {{- '' }}\n    {%- else %}\n        {{- raise_exception('Unexpected content type.') }}\n    {%- endif %}\n{%- endmacro %}\n{%- if not messages %}\n    {{- raise_exception('No messages provided.') }}\n{%- endif %}\n{%- if tools and tools is iterable and tools is not mapping %}\n    {{- '<|im_start|>system\\n' }}\n    {{- \"# Tools\\n\\nYou have access to the following functions:\\n\\n<tools>\" }}\n    {%- for tool in tools %}\n        {{- \"\\n\" }}\n        {{- tool | tojson }}\n    {%- endfor %}\n    {{- \"\\n</tools>\" }}\n    {{- '\\n\\nIf you choose to call a function ONLY reply in the following format with NO suffix:\\n\\n<tool_call>\\n<function=example_function_name>\\n<parameter=example_parameter_1>\\nvalue_1\\n</parameter>\\n<parameter=example_parameter_2>\\nThis is the value for the second parameter\\nthat can span\\nmultiple lines\\n</parameter>\\n</function>\\n</tool_call>\\n\\n<IMPORTANT>\\nReminder:\\n- Function calls MUST follow the specified format: an inner <function=...></function> block must be nested within <tool_call></tool_call> XML tags\\n- Required parameters MUST be specified\\n- You may provide optional reasoning for your function call in natural language BEFORE the function call, but NOT after\\n- If there is no function call available, answer the question like normal with your current knowledge and do not tell the user about function calls\\n</IMPORTANT>' }}\n    {%- if messages[0].role == 'system' %}\n        {%- set content = render_content(messages[0].content, false, true)|trim %}\n        {%- if content %}\n            {{- '\\n\\n' + content }}\n        {%- endif %}\n    {%- endif %}\n    {{- '<|im_end|>\\n' }}\n{%- else %}\n    {%- if messages[0].role == 'system' %}\n        {%- set content = render_content(messages[0].content, false, true)|trim %}\n        {{- '<|im_start|>system\\n' + content + '<|im_end|>\\n' }}\n    {%- endif %}\n{%- endif %}\n{%- set ns = namespace(multi_step_tool=true, last_query_index=messages|length - 1) %}\n{%- for message in messages[::-1] %}\n    {%- set index = (messages|length - 1) - loop.index0 %}\n    {%- if ns.multi_step_tool and message.role == \"user\" %}\n        {%- set content = render_content(message.content, false)|trim %}\n        {%- if not(content.startswith('<tool_response>') and content.endswith('</tool_response>')) %}\n            {%- set ns.multi_step_tool = false %}\n            {%- set ns.last_query_index = index %}\n        {%- endif %}\n    {%- endif %}\n{%- endfor %}\n{%- if ns.multi_step_tool %}\n    {{- raise_exception('No user query found in messages.') }}\n{%- endif %}\n{%- for message in messages %}\n    {%- set content = render_content(message.content, true)|trim %}\n    {%- if message.role == \"system\" %}\n        {%- if not loop.first %}\n            {{- raise_exception('System message must be at the beginning.') }}\n        {%- endif %}\n    {%- elif message.role == \"user\" %}\n        {{- '<|im_start|>' + message.role + '\\n' + content + '<|im_end|>' + '\\n' }}\n    {%- elif message.role == \"assistant\" %}\n        {%- set reasoning_content = '' %}\n        {%- if message.reasoning_content is string %}\n            {%- set reasoning_content = message.reasoning_content %}\n        {%- else %}\n            {%- if '</think>' in content %}\n                {%- set reasoning_content = content.split('</think>')[0].rstrip('\\n').split('<think>')[-1].lstrip('\\n') %}\n                {%- set content = content.split('</think>')[-1].lstrip('\\n') %}\n            {%- endif %}\n        {%- endif %}\n        {%- set reasoning_content = reasoning_content|trim %}\n        {%- if loop.index0 > ns.last_query_index %}\n            {{- '<|im_start|>' + message.role + '\\n<think>\\n' + reasoning_content + '\\n</think>\\n\\n' + content }}\n        {%- else %}\n            {{- '<|im_start|>' + message.role + '\\n' + content }}\n        {%- endif %}\n        {%- if message.tool_calls and message.tool_calls is iterable and message.tool_calls is not mapping %}\n            {%- for tool_call in message.tool_calls %}\n                {%- if tool_call.function is defined %}\n                    {%- set tool_call = tool_call.function %}\n                {%- endif %}\n                {%- if loop.first %}\n                    {%- if content|trim %}\n                        {{- '\\n\\n<tool_call>\\n<function=' + tool_call.name + '>\\n' }}\n                    {%- else %}\n                        {{- '<tool_call>\\n<function=' + tool_call.name + '>\\n' }}\n                    {%- endif %}\n                {%- else %}\n                    {{- '\\n<tool_call>\\n<function=' + tool_call.name + '>\\n' }}\n                {%- endif %}\n                {%- if tool_call.arguments is defined %}\n                    {%- for args_name, args_value in tool_call.arguments|items %}\n                        {{- '<parameter=' + args_name + '>\\n' }}\n                        {%- set args_value = args_value | tojson | safe if args_value is mapping or (args_value is sequence and args_value is not string) else args_value | string %}\n                        {{- args_value }}\n                        {{- '\\n</parameter>\\n' }}\n                    {%- endfor %}\n                {%- endif %}\n                {{- '</function>\\n</tool_call>' }}\n            {%- endfor %}\n        {%- endif %}\n        {{- '<|im_end|>\\n' }}\n    {%- elif message.role == \"tool\" %}\n        {%- if loop.previtem and loop.previtem.role != \"tool\" %}\n            {{- '<|im_start|>user' }}\n        {%- endif %}\n        {{- '\\n<tool_response>\\n' }}\n        {{- content }}\n        {{- '\\n</tool_response>' }}\n        {%- if not loop.last and loop.nextitem.role != \"tool\" %}\n            {{- '<|im_end|>\\n' }}\n        {%- elif loop.last %}\n            {{- '<|im_end|>\\n' }}\n        {%- endif %}\n    {%- else %}\n        {{- raise_exception('Unexpected message role.') }}\n    {%- endif %}\n{%- endfor %}\n{%- if add_generation_prompt %}\n    {{- '<|im_start|>assistant\\n' }}\n    {%- if enable_thinking is defined and enable_thinking is false %}\n        {{- '<think>\\n\\n</think>\\n\\n' }}\n    {%- else %}\n        {{- '<think>\\n' }}\n    {%- endif %}\n{%- endif %}",
        "generation": {
          "do_sample": true,
          "eos_token_id": [
            248044,
            248046
          ],
          "max_new_tokens": 512,
          "min_p": 0.0,
          "num_beams": 1,
          "output_scores": false,
          "pad_token_id": 248044,
          "prefill_chunk_size": 256,
          "remove_invalid_values": false,
          "repetition_penalty": 1.0,
          "return_dict_in_generate": true,
          "temperature": 0.7,
          "top_k": 20,
          "top_p": 0.8,
          "use_cache": true
        },
        "input_limit": 8192,
        "mode": "direct",
        "model": "Qwen/Qwen3.5-9B",
        "presence_penalty": 0,
        "quantization": "NF4-double-FP16",
        "regime": "i01-course-v1",
        "revision": "c202236235762e1c871ad0ccb60c8ee5ba337b9a",
        "visible_limit": 512
      }
    },
    "automatic/batch/main-00+main-01": {
      "complete": true,
      "evidence": [
        {
          "checks": {
            "committed_calls": true,
            "every_episode_has_calls": true,
            "runtime_integrity": true,
            "terminal_evidence": true
          },
          "control_protocol_errors": 0,
          "human_review": "retrospective_pending",
          "original_messages": 2,
          "original_team_completed": true,
          "passed": true,
          "prefix_protocol_errors": 2,
          "protocol_errors": 2,
          "recorded_calls": 10,
          "recovery_protocol_errors": 0,
          "useful_communication": null,
          "validation": [
            {
              "admission_blocking": false,
              "call": "main-00/prefix/agent-0/invocation-0",
              "error": "malformed_action",
              "json_valid": true,
              "legal_action": false,
              "phase": "prefix",
              "reason": "wait_requires_null_message_and_submit",
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-00/prefix/agent-1/invocation-0",
              "error": null,
              "json_valid": true,
              "legal_action": true,
              "phase": "prefix",
              "reason": null,
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-00/prefix/agent-0/invocation-1",
              "error": "malformed_action",
              "json_valid": true,
              "legal_action": false,
              "phase": "prefix",
              "reason": "wait_requires_null_message_and_submit",
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-00/prefix/agent-0/invocation-2",
              "error": null,
              "json_valid": true,
              "legal_action": true,
              "phase": "prefix",
              "reason": null,
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-00/prefix/agent-1/invocation-1",
              "error": null,
              "json_valid": true,
              "legal_action": true,
              "phase": "prefix",
              "reason": null,
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-00/retain/agent-0/invocation-0",
              "error": null,
              "json_valid": true,
              "legal_action": true,
              "phase": "retain",
              "reason": null,
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-00/retain/agent-1/invocation-0",
              "error": null,
              "json_valid": true,
              "legal_action": true,
              "phase": "retain",
              "reason": null,
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-00/clear/agent-0/invocation-0",
              "error": null,
              "json_valid": true,
              "legal_action": true,
              "phase": "clear",
              "reason": null,
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-00/clear/agent-1/invocation-0",
              "error": null,
              "json_valid": true,
              "legal_action": true,
              "phase": "clear",
              "reason": null,
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-00/control-revised-direct",
              "error": null,
              "json_valid": true,
              "legal_action": true,
              "phase": "control-revised-direct",
              "reason": null,
              "runtime_safe": true,
              "schema_valid": true
            }
          ],
          "world": "main-00"
        },
        {
          "checks": {
            "committed_calls": true,
            "every_episode_has_calls": true,
            "runtime_integrity": true,
            "terminal_evidence": true
          },
          "control_protocol_errors": 0,
          "human_review": "retrospective_pending",
          "original_messages": 0,
          "original_team_completed": false,
          "passed": true,
          "prefix_protocol_errors": 3,
          "protocol_errors": 4,
          "recorded_calls": 10,
          "recovery_protocol_errors": 1,
          "useful_communication": null,
          "validation": [
            {
              "admission_blocking": false,
              "call": "main-01/prefix/agent-0/invocation-0",
              "error": null,
              "json_valid": true,
              "legal_action": true,
              "phase": "prefix",
              "reason": null,
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-01/prefix/agent-1/invocation-0",
              "error": "malformed_action",
              "json_valid": true,
              "legal_action": false,
              "phase": "prefix",
              "reason": "wait_requires_null_message_and_submit",
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-01/prefix/agent-1/invocation-1",
              "error": "malformed_action",
              "json_valid": true,
              "legal_action": false,
              "phase": "prefix",
              "reason": "wait_requires_null_message_and_submit",
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-01/prefix/agent-1/invocation-2",
              "error": "malformed_action",
              "json_valid": true,
              "legal_action": false,
              "phase": "prefix",
              "reason": "wait_requires_null_message_and_submit",
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-01/clear/agent-0/invocation-0",
              "error": null,
              "json_valid": true,
              "legal_action": true,
              "phase": "clear",
              "reason": null,
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-01/clear/agent-1/invocation-0",
              "error": null,
              "json_valid": true,
              "legal_action": true,
              "phase": "clear",
              "reason": null,
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-01/retain/agent-0/invocation-0",
              "error": null,
              "json_valid": true,
              "legal_action": true,
              "phase": "retain",
              "reason": null,
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-01/retain/agent-1/invocation-0",
              "error": "malformed_action",
              "json_valid": true,
              "legal_action": false,
              "phase": "retain",
              "reason": "empty_nonwaiting_action",
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-01/retain/agent-1/invocation-1",
              "error": null,
              "json_valid": true,
              "legal_action": true,
              "phase": "retain",
              "reason": null,
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-01/control-revised-direct",
              "error": null,
              "json_valid": true,
              "legal_action": true,
              "phase": "control-revised-direct",
              "reason": null,
              "runtime_safe": true,
              "schema_valid": true
            }
          ],
          "world": "main-01"
        }
      ],
      "human_review": "retrospective_pending",
      "id": "batch/main-00+main-01",
      "number": 1,
      "passed": true,
      "policy": "i01-recorded-outcomes-run-all-2026-10-15",
      "worlds": [
        "main-00",
        "main-01"
      ]
    },
    "automatic/batch/main-02+main-03": {
      "complete": true,
      "evidence": [
        {
          "checks": {
            "committed_calls": true,
            "every_episode_has_calls": true,
            "runtime_integrity": true,
            "terminal_evidence": true
          },
          "control_protocol_errors": 0,
          "human_review": "retrospective_pending",
          "original_messages": 0,
          "original_team_completed": false,
          "passed": true,
          "prefix_protocol_errors": 2,
          "protocol_errors": 2,
          "recorded_calls": 9,
          "recovery_protocol_errors": 0,
          "useful_communication": null,
          "validation": [
            {
              "admission_blocking": false,
              "call": "main-02/prefix/agent-0/invocation-0",
              "error": null,
              "json_valid": true,
              "legal_action": true,
              "phase": "prefix",
              "reason": null,
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-02/prefix/agent-1/invocation-0",
              "error": "malformed_action",
              "json_valid": true,
              "legal_action": false,
              "phase": "prefix",
              "reason": "wait_requires_null_message_and_submit",
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-02/prefix/agent-1/invocation-1",
              "error": "malformed_action",
              "json_valid": true,
              "legal_action": false,
              "phase": "prefix",
              "reason": "wait_requires_null_message_and_submit",
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-02/prefix/agent-1/invocation-2",
              "error": null,
              "json_valid": true,
              "legal_action": true,
              "phase": "prefix",
              "reason": null,
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-02/retain/agent-0/invocation-0",
              "error": null,
              "json_valid": true,
              "legal_action": true,
              "phase": "retain",
              "reason": null,
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-02/retain/agent-1/invocation-0",
              "error": null,
              "json_valid": true,
              "legal_action": true,
              "phase": "retain",
              "reason": null,
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-02/clear/agent-0/invocation-0",
              "error": null,
              "json_valid": true,
              "legal_action": true,
              "phase": "clear",
              "reason": null,
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-02/clear/agent-1/invocation-0",
              "error": null,
              "json_valid": true,
              "legal_action": true,
              "phase": "clear",
              "reason": null,
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-02/control-revised-direct",
              "error": null,
              "json_valid": true,
              "legal_action": true,
              "phase": "control-revised-direct",
              "reason": null,
              "runtime_safe": true,
              "schema_valid": true
            }
          ],
          "world": "main-02"
        },
        {
          "checks": {
            "committed_calls": true,
            "every_episode_has_calls": true,
            "runtime_integrity": true,
            "terminal_evidence": true
          },
          "control_protocol_errors": 0,
          "human_review": "retrospective_pending",
          "original_messages": 3,
          "original_team_completed": true,
          "passed": true,
          "prefix_protocol_errors": 0,
          "protocol_errors": 1,
          "recorded_calls": 11,
          "recovery_protocol_errors": 1,
          "useful_communication": null,
          "validation": [
            {
              "admission_blocking": false,
              "call": "main-03/prefix/agent-0/invocation-0",
              "error": null,
              "json_valid": true,
              "legal_action": true,
              "phase": "prefix",
              "reason": null,
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-03/prefix/agent-1/invocation-0",
              "error": null,
              "json_valid": true,
              "legal_action": true,
              "phase": "prefix",
              "reason": null,
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-03/prefix/agent-0/invocation-1",
              "error": null,
              "json_valid": true,
              "legal_action": true,
              "phase": "prefix",
              "reason": null,
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-03/prefix/agent-1/invocation-1",
              "error": null,
              "json_valid": true,
              "legal_action": true,
              "phase": "prefix",
              "reason": null,
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-03/clear/agent-0/invocation-0",
              "error": "malformed_action",
              "json_valid": true,
              "legal_action": false,
              "phase": "clear",
              "reason": "wait_requires_null_message_and_submit",
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-03/clear/agent-1/invocation-0",
              "error": null,
              "json_valid": true,
              "legal_action": true,
              "phase": "clear",
              "reason": null,
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-03/clear/agent-0/invocation-1",
              "error": null,
              "json_valid": true,
              "legal_action": true,
              "phase": "clear",
              "reason": null,
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-03/clear/agent-1/invocation-1",
              "error": null,
              "json_valid": true,
              "legal_action": true,
              "phase": "clear",
              "reason": null,
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-03/retain/agent-0/invocation-0",
              "error": null,
              "json_valid": true,
              "legal_action": true,
              "phase": "retain",
              "reason": null,
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-03/retain/agent-1/invocation-0",
              "error": null,
              "json_valid": true,
              "legal_action": true,
              "phase": "retain",
              "reason": null,
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-03/control-revised-direct",
              "error": null,
              "json_valid": true,
              "legal_action": true,
              "phase": "control-revised-direct",
              "reason": null,
              "runtime_safe": true,
              "schema_valid": true
            }
          ],
          "world": "main-03"
        }
      ],
      "human_review": "retrospective_pending",
      "id": "batch/main-02+main-03",
      "number": 2,
      "passed": true,
      "policy": "i01-recorded-outcomes-run-all-2026-10-15",
      "worlds": [
        "main-02",
        "main-03"
      ]
    },
    "automatic/batch/main-04+main-05": {
      "complete": true,
      "evidence": [
        {
          "checks": {
            "committed_calls": true,
            "every_episode_has_calls": true,
            "runtime_integrity": true,
            "terminal_evidence": true
          },
          "control_protocol_errors": 0,
          "human_review": "retrospective_pending",
          "original_messages": 0,
          "original_team_completed": false,
          "passed": true,
          "prefix_protocol_errors": 3,
          "protocol_errors": 4,
          "recorded_calls": 10,
          "recovery_protocol_errors": 1,
          "useful_communication": null,
          "validation": [
            {
              "admission_blocking": false,
              "call": "main-04/prefix/agent-0/invocation-0",
              "error": "malformed_action",
              "json_valid": true,
              "legal_action": false,
              "phase": "prefix",
              "reason": "wait_requires_null_message_and_submit",
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-04/prefix/agent-1/invocation-0",
              "error": null,
              "json_valid": true,
              "legal_action": true,
              "phase": "prefix",
              "reason": null,
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-04/prefix/agent-0/invocation-1",
              "error": "malformed_action",
              "json_valid": true,
              "legal_action": false,
              "phase": "prefix",
              "reason": "wait_requires_null_message_and_submit",
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-04/prefix/agent-0/invocation-2",
              "error": "malformed_action",
              "json_valid": true,
              "legal_action": false,
              "phase": "prefix",
              "reason": "wait_requires_null_message_and_submit",
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-04/retain/agent-0/invocation-0",
              "error": "malformed_action",
              "json_valid": true,
              "legal_action": false,
              "phase": "retain",
              "reason": "wait_requires_null_message_and_submit",
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-04/retain/agent-1/invocation-0",
              "error": null,
              "json_valid": true,
              "legal_action": true,
              "phase": "retain",
              "reason": null,
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-04/retain/agent-0/invocation-1",
              "error": null,
              "json_valid": true,
              "legal_action": true,
              "phase": "retain",
              "reason": null,
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-04/clear/agent-0/invocation-0",
              "error": null,
              "json_valid": true,
              "legal_action": true,
              "phase": "clear",
              "reason": null,
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-04/clear/agent-1/invocation-0",
              "error": null,
              "json_valid": true,
              "legal_action": true,
              "phase": "clear",
              "reason": null,
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-04/control-revised-direct",
              "error": null,
              "json_valid": true,
              "legal_action": true,
              "phase": "control-revised-direct",
              "reason": null,
              "runtime_safe": true,
              "schema_valid": true
            }
          ],
          "world": "main-04"
        },
        {
          "checks": {
            "committed_calls": true,
            "every_episode_has_calls": true,
            "runtime_integrity": true,
            "terminal_evidence": true
          },
          "control_protocol_errors": 0,
          "human_review": "retrospective_pending",
          "original_messages": 0,
          "original_team_completed": false,
          "passed": true,
          "prefix_protocol_errors": 3,
          "protocol_errors": 4,
          "recorded_calls": 11,
          "recovery_protocol_errors": 1,
          "useful_communication": null,
          "validation": [
            {
              "admission_blocking": false,
              "call": "main-05/prefix/agent-1/invocation-0",
              "error": "malformed_action",
              "json_valid": true,
              "legal_action": false,
              "phase": "prefix",
              "reason": "wait_requires_null_message_and_submit",
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-05/prefix/agent-0/invocation-0",
              "error": null,
              "json_valid": true,
              "legal_action": true,
              "phase": "prefix",
              "reason": null,
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-05/prefix/agent-1/invocation-1",
              "error": "malformed_action",
              "json_valid": true,
              "legal_action": false,
              "phase": "prefix",
              "reason": "wait_requires_null_message_and_submit",
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-05/prefix/agent-1/invocation-2",
              "error": "malformed_action",
              "json_valid": true,
              "legal_action": false,
              "phase": "prefix",
              "reason": "wait_requires_null_message_and_submit",
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-05/clear/agent-1/invocation-0",
              "error": null,
              "json_valid": true,
              "legal_action": true,
              "phase": "clear",
              "reason": null,
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-05/clear/agent-0/invocation-0",
              "error": null,
              "json_valid": true,
              "legal_action": true,
              "phase": "clear",
              "reason": null,
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-05/clear/agent-1/invocation-1",
              "error": "malformed_action",
              "json_valid": true,
              "legal_action": false,
              "phase": "clear",
              "reason": "empty_nonwaiting_action",
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-05/clear/agent-1/invocation-2",
              "error": null,
              "json_valid": true,
              "legal_action": true,
              "phase": "clear",
              "reason": null,
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-05/retain/agent-1/invocation-0",
              "error": null,
              "json_valid": true,
              "legal_action": true,
              "phase": "retain",
              "reason": null,
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-05/retain/agent-0/invocation-0",
              "error": null,
              "json_valid": true,
              "legal_action": true,
              "phase": "retain",
              "reason": null,
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-05/control-revised-direct",
              "error": null,
              "json_valid": true,
              "legal_action": true,
              "phase": "control-revised-direct",
              "reason": null,
              "runtime_safe": true,
              "schema_valid": true
            }
          ],
          "world": "main-05"
        }
      ],
      "human_review": "retrospective_pending",
      "id": "batch/main-04+main-05",
      "number": 3,
      "passed": true,
      "policy": "i01-recorded-outcomes-run-all-2026-10-15",
      "worlds": [
        "main-04",
        "main-05"
      ]
    },
    "automatic/batch/main-06+main-07": {
      "complete": true,
      "evidence": [
        {
          "checks": {
            "committed_calls": true,
            "every_episode_has_calls": true,
            "runtime_integrity": true,
            "terminal_evidence": true
          },
          "control_protocol_errors": 0,
          "human_review": "retrospective_pending",
          "original_messages": 0,
          "original_team_completed": false,
          "passed": true,
          "prefix_protocol_errors": 0,
          "protocol_errors": 1,
          "recorded_calls": 8,
          "recovery_protocol_errors": 1,
          "useful_communication": null,
          "validation": [
            {
              "admission_blocking": false,
              "call": "main-06/prefix/agent-1/invocation-0",
              "error": null,
              "json_valid": true,
              "legal_action": true,
              "phase": "prefix",
              "reason": null,
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-06/prefix/agent-0/invocation-0",
              "error": null,
              "json_valid": true,
              "legal_action": true,
              "phase": "prefix",
              "reason": null,
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-06/retain/agent-1/invocation-0",
              "error": null,
              "json_valid": true,
              "legal_action": true,
              "phase": "retain",
              "reason": null,
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-06/retain/agent-0/invocation-0",
              "error": null,
              "json_valid": true,
              "legal_action": true,
              "phase": "retain",
              "reason": null,
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-06/clear/agent-1/invocation-0",
              "error": "malformed_action",
              "json_valid": true,
              "legal_action": false,
              "phase": "clear",
              "reason": "wait_requires_null_message_and_submit",
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-06/clear/agent-0/invocation-0",
              "error": null,
              "json_valid": true,
              "legal_action": true,
              "phase": "clear",
              "reason": null,
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-06/clear/agent-1/invocation-1",
              "error": null,
              "json_valid": true,
              "legal_action": true,
              "phase": "clear",
              "reason": null,
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-06/control-revised-direct",
              "error": null,
              "json_valid": true,
              "legal_action": true,
              "phase": "control-revised-direct",
              "reason": null,
              "runtime_safe": true,
              "schema_valid": true
            }
          ],
          "world": "main-06"
        },
        {
          "checks": {
            "committed_calls": true,
            "every_episode_has_calls": true,
            "runtime_integrity": true,
            "terminal_evidence": true
          },
          "control_protocol_errors": 0,
          "human_review": "retrospective_pending",
          "original_messages": 0,
          "original_team_completed": false,
          "passed": true,
          "prefix_protocol_errors": 3,
          "protocol_errors": 3,
          "recorded_calls": 9,
          "recovery_protocol_errors": 0,
          "useful_communication": null,
          "validation": [
            {
              "admission_blocking": false,
              "call": "main-07/prefix/agent-1/invocation-0",
              "error": "malformed_action",
              "json_valid": true,
              "legal_action": false,
              "phase": "prefix",
              "reason": "wait_requires_null_message_and_submit",
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-07/prefix/agent-0/invocation-0",
              "error": null,
              "json_valid": true,
              "legal_action": true,
              "phase": "prefix",
              "reason": null,
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-07/prefix/agent-1/invocation-1",
              "error": "malformed_action",
              "json_valid": true,
              "legal_action": false,
              "phase": "prefix",
              "reason": "wait_requires_null_message_and_submit",
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-07/prefix/agent-1/invocation-2",
              "error": "malformed_action",
              "json_valid": true,
              "legal_action": false,
              "phase": "prefix",
              "reason": "wait_requires_null_message_and_submit",
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-07/clear/agent-1/invocation-0",
              "error": null,
              "json_valid": true,
              "legal_action": true,
              "phase": "clear",
              "reason": null,
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-07/clear/agent-0/invocation-0",
              "error": null,
              "json_valid": true,
              "legal_action": true,
              "phase": "clear",
              "reason": null,
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-07/retain/agent-1/invocation-0",
              "error": null,
              "json_valid": true,
              "legal_action": true,
              "phase": "retain",
              "reason": null,
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-07/retain/agent-0/invocation-0",
              "error": null,
              "json_valid": true,
              "legal_action": true,
              "phase": "retain",
              "reason": null,
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-07/control-revised-direct",
              "error": null,
              "json_valid": true,
              "legal_action": true,
              "phase": "control-revised-direct",
              "reason": null,
              "runtime_safe": true,
              "schema_valid": true
            }
          ],
          "world": "main-07"
        }
      ],
      "human_review": "retrospective_pending",
      "id": "batch/main-06+main-07",
      "number": 4,
      "passed": true,
      "policy": "i01-recorded-outcomes-run-all-2026-10-15",
      "worlds": [
        "main-06",
        "main-07"
      ]
    },
    "automatic/batch/main-08+main-09": {
      "complete": true,
      "evidence": [
        {
          "checks": {
            "committed_calls": true,
            "every_episode_has_calls": true,
            "runtime_integrity": true,
            "terminal_evidence": true
          },
          "control_protocol_errors": 0,
          "human_review": "retrospective_pending",
          "original_messages": 3,
          "original_team_completed": true,
          "passed": true,
          "prefix_protocol_errors": 1,
          "protocol_errors": 1,
          "recorded_calls": 9,
          "recovery_protocol_errors": 0,
          "useful_communication": null,
          "validation": [
            {
              "admission_blocking": false,
              "call": "main-08/prefix/agent-1/invocation-0",
              "error": "malformed_action",
              "json_valid": true,
              "legal_action": false,
              "phase": "prefix",
              "reason": "wait_requires_null_message_and_submit",
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-08/prefix/agent-0/invocation-0",
              "error": null,
              "json_valid": true,
              "legal_action": true,
              "phase": "prefix",
              "reason": null,
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-08/prefix/agent-1/invocation-1",
              "error": null,
              "json_valid": true,
              "legal_action": true,
              "phase": "prefix",
              "reason": null,
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-08/prefix/agent-0/invocation-1",
              "error": null,
              "json_valid": true,
              "legal_action": true,
              "phase": "prefix",
              "reason": null,
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-08/retain/agent-1/invocation-0",
              "error": null,
              "json_valid": true,
              "legal_action": true,
              "phase": "retain",
              "reason": null,
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-08/retain/agent-0/invocation-0",
              "error": null,
              "json_valid": true,
              "legal_action": true,
              "phase": "retain",
              "reason": null,
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-08/clear/agent-1/invocation-0",
              "error": null,
              "json_valid": true,
              "legal_action": true,
              "phase": "clear",
              "reason": null,
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-08/clear/agent-0/invocation-0",
              "error": null,
              "json_valid": true,
              "legal_action": true,
              "phase": "clear",
              "reason": null,
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-08/control-revised-direct",
              "error": null,
              "json_valid": true,
              "legal_action": true,
              "phase": "control-revised-direct",
              "reason": null,
              "runtime_safe": true,
              "schema_valid": true
            }
          ],
          "world": "main-08"
        },
        {
          "checks": {
            "committed_calls": true,
            "every_episode_has_calls": true,
            "runtime_integrity": true,
            "terminal_evidence": true
          },
          "control_protocol_errors": 0,
          "human_review": "retrospective_pending",
          "original_messages": 2,
          "original_team_completed": true,
          "passed": true,
          "prefix_protocol_errors": 3,
          "protocol_errors": 3,
          "recorded_calls": 11,
          "recovery_protocol_errors": 0,
          "useful_communication": null,
          "validation": [
            {
              "admission_blocking": false,
              "call": "main-09/prefix/agent-1/invocation-0",
              "error": null,
              "json_valid": true,
              "legal_action": true,
              "phase": "prefix",
              "reason": null,
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-09/prefix/agent-0/invocation-0",
              "error": "malformed_action",
              "json_valid": true,
              "legal_action": false,
              "phase": "prefix",
              "reason": "wait_requires_null_message_and_submit",
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-09/prefix/agent-0/invocation-1",
              "error": "malformed_action",
              "json_valid": true,
              "legal_action": false,
              "phase": "prefix",
              "reason": "wait_requires_null_message_and_submit",
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-09/prefix/agent-0/invocation-2",
              "error": null,
              "json_valid": true,
              "legal_action": true,
              "phase": "prefix",
              "reason": null,
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-09/prefix/agent-1/invocation-1",
              "error": "malformed_action",
              "json_valid": true,
              "legal_action": false,
              "phase": "prefix",
              "reason": "wait_requires_null_message_and_submit",
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-09/prefix/agent-1/invocation-2",
              "error": null,
              "json_valid": true,
              "legal_action": true,
              "phase": "prefix",
              "reason": null,
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-09/clear/agent-1/invocation-0",
              "error": null,
              "json_valid": true,
              "legal_action": true,
              "phase": "clear",
              "reason": null,
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-09/clear/agent-0/invocation-0",
              "error": null,
              "json_valid": true,
              "legal_action": true,
              "phase": "clear",
              "reason": null,
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-09/retain/agent-1/invocation-0",
              "error": null,
              "json_valid": true,
              "legal_action": true,
              "phase": "retain",
              "reason": null,
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-09/retain/agent-0/invocation-0",
              "error": null,
              "json_valid": true,
              "legal_action": true,
              "phase": "retain",
              "reason": null,
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-09/control-revised-direct",
              "error": null,
              "json_valid": true,
              "legal_action": true,
              "phase": "control-revised-direct",
              "reason": null,
              "runtime_safe": true,
              "schema_valid": true
            }
          ],
          "world": "main-09"
        }
      ],
      "human_review": "retrospective_pending",
      "id": "batch/main-08+main-09",
      "number": 5,
      "passed": true,
      "policy": "i01-recorded-outcomes-run-all-2026-10-15",
      "worlds": [
        "main-08",
        "main-09"
      ]
    },
    "automatic/batch/main-10+main-11": {
      "complete": true,
      "evidence": [
        {
          "checks": {
            "committed_calls": true,
            "every_episode_has_calls": true,
            "runtime_integrity": true,
            "terminal_evidence": true
          },
          "control_protocol_errors": 0,
          "human_review": "retrospective_pending",
          "original_messages": 2,
          "original_team_completed": true,
          "passed": true,
          "prefix_protocol_errors": 1,
          "protocol_errors": 3,
          "recorded_calls": 10,
          "recovery_protocol_errors": 2,
          "useful_communication": null,
          "validation": [
            {
              "admission_blocking": false,
              "call": "main-10/prefix/agent-0/invocation-0",
              "error": null,
              "json_valid": true,
              "legal_action": true,
              "phase": "prefix",
              "reason": null,
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-10/prefix/agent-1/invocation-0",
              "error": "malformed_action",
              "json_valid": true,
              "legal_action": false,
              "phase": "prefix",
              "reason": "wait_requires_null_message_and_submit",
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-10/prefix/agent-1/invocation-1",
              "error": null,
              "json_valid": true,
              "legal_action": true,
              "phase": "prefix",
              "reason": null,
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-10/retain/agent-0/invocation-0",
              "error": null,
              "json_valid": true,
              "legal_action": true,
              "phase": "retain",
              "reason": null,
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-10/retain/agent-1/invocation-0",
              "error": null,
              "json_valid": true,
              "legal_action": true,
              "phase": "retain",
              "reason": null,
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-10/clear/agent-0/invocation-0",
              "error": "malformed_action",
              "json_valid": true,
              "legal_action": false,
              "phase": "clear",
              "reason": "wait_requires_null_message_and_submit",
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-10/clear/agent-1/invocation-0",
              "error": null,
              "json_valid": true,
              "legal_action": true,
              "phase": "clear",
              "reason": null,
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-10/clear/agent-0/invocation-1",
              "error": "malformed_action",
              "json_valid": true,
              "legal_action": false,
              "phase": "clear",
              "reason": "wait_requires_null_message_and_submit",
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-10/clear/agent-0/invocation-2",
              "error": null,
              "json_valid": true,
              "legal_action": true,
              "phase": "clear",
              "reason": null,
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-10/control-revised-direct",
              "error": null,
              "json_valid": true,
              "legal_action": true,
              "phase": "control-revised-direct",
              "reason": null,
              "runtime_safe": true,
              "schema_valid": true
            }
          ],
          "world": "main-10"
        },
        {
          "checks": {
            "committed_calls": true,
            "every_episode_has_calls": true,
            "runtime_integrity": true,
            "terminal_evidence": true
          },
          "control_protocol_errors": 0,
          "human_review": "retrospective_pending",
          "original_messages": 2,
          "original_team_completed": true,
          "passed": true,
          "prefix_protocol_errors": 2,
          "protocol_errors": 2,
          "recorded_calls": 10,
          "recovery_protocol_errors": 0,
          "useful_communication": null,
          "validation": [
            {
              "admission_blocking": false,
              "call": "main-11/prefix/agent-0/invocation-0",
              "error": null,
              "json_valid": true,
              "legal_action": true,
              "phase": "prefix",
              "reason": null,
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-11/prefix/agent-1/invocation-0",
              "error": "malformed_action",
              "json_valid": true,
              "legal_action": false,
              "phase": "prefix",
              "reason": "wait_requires_null_message_and_submit",
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-11/prefix/agent-1/invocation-1",
              "error": "malformed_action",
              "json_valid": true,
              "legal_action": false,
              "phase": "prefix",
              "reason": "wait_requires_null_message_and_submit",
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-11/prefix/agent-1/invocation-2",
              "error": null,
              "json_valid": true,
              "legal_action": true,
              "phase": "prefix",
              "reason": null,
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-11/prefix/agent-0/invocation-1",
              "error": null,
              "json_valid": true,
              "legal_action": true,
              "phase": "prefix",
              "reason": null,
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-11/clear/agent-0/invocation-0",
              "error": null,
              "json_valid": true,
              "legal_action": true,
              "phase": "clear",
              "reason": null,
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-11/clear/agent-1/invocation-0",
              "error": null,
              "json_valid": true,
              "legal_action": true,
              "phase": "clear",
              "reason": null,
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-11/retain/agent-0/invocation-0",
              "error": null,
              "json_valid": true,
              "legal_action": true,
              "phase": "retain",
              "reason": null,
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-11/retain/agent-1/invocation-0",
              "error": null,
              "json_valid": true,
              "legal_action": true,
              "phase": "retain",
              "reason": null,
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-11/control-revised-direct",
              "error": null,
              "json_valid": true,
              "legal_action": true,
              "phase": "control-revised-direct",
              "reason": null,
              "runtime_safe": true,
              "schema_valid": true
            }
          ],
          "world": "main-11"
        }
      ],
      "human_review": "retrospective_pending",
      "id": "batch/main-10+main-11",
      "number": 6,
      "passed": true,
      "policy": "i01-recorded-outcomes-run-all-2026-10-15",
      "worlds": [
        "main-10",
        "main-11"
      ]
    },
    "automatic/batch/main-12+main-13": {
      "complete": true,
      "evidence": [
        {
          "checks": {
            "committed_calls": true,
            "every_episode_has_calls": true,
            "runtime_integrity": true,
            "terminal_evidence": true
          },
          "control_protocol_errors": 0,
          "human_review": "retrospective_pending",
          "original_messages": 0,
          "original_team_completed": false,
          "passed": true,
          "prefix_protocol_errors": 0,
          "protocol_errors": 0,
          "recorded_calls": 7,
          "recovery_protocol_errors": 0,
          "useful_communication": null,
          "validation": [
            {
              "admission_blocking": false,
              "call": "main-12/prefix/agent-0/invocation-0",
              "error": null,
              "json_valid": true,
              "legal_action": true,
              "phase": "prefix",
              "reason": null,
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-12/prefix/agent-1/invocation-0",
              "error": null,
              "json_valid": true,
              "legal_action": true,
              "phase": "prefix",
              "reason": null,
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-12/retain/agent-0/invocation-0",
              "error": null,
              "json_valid": true,
              "legal_action": true,
              "phase": "retain",
              "reason": null,
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-12/retain/agent-1/invocation-0",
              "error": null,
              "json_valid": true,
              "legal_action": true,
              "phase": "retain",
              "reason": null,
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-12/clear/agent-0/invocation-0",
              "error": null,
              "json_valid": true,
              "legal_action": true,
              "phase": "clear",
              "reason": null,
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-12/clear/agent-1/invocation-0",
              "error": null,
              "json_valid": true,
              "legal_action": true,
              "phase": "clear",
              "reason": null,
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-12/control-revised-direct",
              "error": null,
              "json_valid": true,
              "legal_action": true,
              "phase": "control-revised-direct",
              "reason": null,
              "runtime_safe": true,
              "schema_valid": true
            }
          ],
          "world": "main-12"
        },
        {
          "checks": {
            "committed_calls": true,
            "every_episode_has_calls": true,
            "runtime_integrity": true,
            "terminal_evidence": true
          },
          "control_protocol_errors": 0,
          "human_review": "retrospective_pending",
          "original_messages": 2,
          "original_team_completed": true,
          "passed": true,
          "prefix_protocol_errors": 0,
          "protocol_errors": 0,
          "recorded_calls": 7,
          "recovery_protocol_errors": 0,
          "useful_communication": null,
          "validation": [
            {
              "admission_blocking": false,
              "call": "main-13/prefix/agent-0/invocation-0",
              "error": null,
              "json_valid": true,
              "legal_action": true,
              "phase": "prefix",
              "reason": null,
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-13/prefix/agent-1/invocation-0",
              "error": null,
              "json_valid": true,
              "legal_action": true,
              "phase": "prefix",
              "reason": null,
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-13/clear/agent-0/invocation-0",
              "error": null,
              "json_valid": true,
              "legal_action": true,
              "phase": "clear",
              "reason": null,
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-13/clear/agent-1/invocation-0",
              "error": null,
              "json_valid": true,
              "legal_action": true,
              "phase": "clear",
              "reason": null,
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-13/retain/agent-0/invocation-0",
              "error": null,
              "json_valid": true,
              "legal_action": true,
              "phase": "retain",
              "reason": null,
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-13/retain/agent-1/invocation-0",
              "error": null,
              "json_valid": true,
              "legal_action": true,
              "phase": "retain",
              "reason": null,
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-13/control-revised-direct",
              "error": null,
              "json_valid": true,
              "legal_action": true,
              "phase": "control-revised-direct",
              "reason": null,
              "runtime_safe": true,
              "schema_valid": true
            }
          ],
          "world": "main-13"
        }
      ],
      "human_review": "retrospective_pending",
      "id": "batch/main-12+main-13",
      "number": 7,
      "passed": true,
      "policy": "i01-recorded-outcomes-run-all-2026-10-15",
      "worlds": [
        "main-12",
        "main-13"
      ]
    },
    "automatic/batch/main-14+main-15": {
      "complete": true,
      "evidence": [
        {
          "checks": {
            "committed_calls": true,
            "every_episode_has_calls": true,
            "runtime_integrity": true,
            "terminal_evidence": true
          },
          "control_protocol_errors": 0,
          "human_review": "retrospective_pending",
          "original_messages": 1,
          "original_team_completed": false,
          "passed": true,
          "prefix_protocol_errors": 4,
          "protocol_errors": 5,
          "recorded_calls": 13,
          "recovery_protocol_errors": 1,
          "useful_communication": null,
          "validation": [
            {
              "admission_blocking": false,
              "call": "main-14/prefix/agent-0/invocation-0",
              "error": "malformed_action",
              "json_valid": true,
              "legal_action": false,
              "phase": "prefix",
              "reason": "wait_requires_null_message_and_submit",
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-14/prefix/agent-1/invocation-0",
              "error": "malformed_action",
              "json_valid": true,
              "legal_action": false,
              "phase": "prefix",
              "reason": "wait_requires_null_message_and_submit",
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-14/prefix/agent-0/invocation-1",
              "error": "malformed_action",
              "json_valid": true,
              "legal_action": false,
              "phase": "prefix",
              "reason": "wait_requires_null_message_and_submit",
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-14/prefix/agent-1/invocation-1",
              "error": null,
              "json_valid": true,
              "legal_action": true,
              "phase": "prefix",
              "reason": null,
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-14/prefix/agent-0/invocation-2",
              "error": "malformed_action",
              "json_valid": true,
              "legal_action": false,
              "phase": "prefix",
              "reason": "wait_requires_null_message_and_submit",
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-14/retain/agent-0/invocation-0",
              "error": null,
              "json_valid": true,
              "legal_action": true,
              "phase": "retain",
              "reason": null,
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-14/retain/agent-1/invocation-0",
              "error": null,
              "json_valid": true,
              "legal_action": true,
              "phase": "retain",
              "reason": null,
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-14/retain/agent-0/invocation-1",
              "error": null,
              "json_valid": true,
              "legal_action": true,
              "phase": "retain",
              "reason": null,
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-14/retain/agent-0/invocation-2",
              "error": null,
              "json_valid": true,
              "legal_action": true,
              "phase": "retain",
              "reason": null,
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-14/clear/agent-0/invocation-0",
              "error": "malformed_action",
              "json_valid": true,
              "legal_action": false,
              "phase": "clear",
              "reason": "wait_requires_null_message_and_submit",
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-14/clear/agent-1/invocation-0",
              "error": null,
              "json_valid": true,
              "legal_action": true,
              "phase": "clear",
              "reason": null,
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-14/clear/agent-0/invocation-1",
              "error": null,
              "json_valid": true,
              "legal_action": true,
              "phase": "clear",
              "reason": null,
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-14/control-revised-direct",
              "error": null,
              "json_valid": true,
              "legal_action": true,
              "phase": "control-revised-direct",
              "reason": null,
              "runtime_safe": true,
              "schema_valid": true
            }
          ],
          "world": "main-14"
        },
        {
          "checks": {
            "committed_calls": true,
            "every_episode_has_calls": true,
            "runtime_integrity": true,
            "terminal_evidence": true
          },
          "control_protocol_errors": 0,
          "human_review": "retrospective_pending",
          "original_messages": 0,
          "original_team_completed": true,
          "passed": true,
          "prefix_protocol_errors": 4,
          "protocol_errors": 4,
          "recorded_calls": 11,
          "recovery_protocol_errors": 0,
          "useful_communication": null,
          "validation": [
            {
              "admission_blocking": false,
              "call": "main-15/prefix/agent-1/invocation-0",
              "error": "malformed_action",
              "json_valid": true,
              "legal_action": false,
              "phase": "prefix",
              "reason": "wait_requires_null_message_and_submit",
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-15/prefix/agent-0/invocation-0",
              "error": "malformed_action",
              "json_valid": true,
              "legal_action": false,
              "phase": "prefix",
              "reason": "wait_requires_null_message_and_submit",
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-15/prefix/agent-1/invocation-1",
              "error": "malformed_action",
              "json_valid": true,
              "legal_action": false,
              "phase": "prefix",
              "reason": "wait_requires_null_message_and_submit",
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-15/prefix/agent-0/invocation-1",
              "error": "malformed_action",
              "json_valid": true,
              "legal_action": false,
              "phase": "prefix",
              "reason": "wait_requires_null_message_and_submit",
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-15/prefix/agent-1/invocation-2",
              "error": null,
              "json_valid": true,
              "legal_action": true,
              "phase": "prefix",
              "reason": null,
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-15/prefix/agent-0/invocation-2",
              "error": null,
              "json_valid": true,
              "legal_action": true,
              "phase": "prefix",
              "reason": null,
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-15/clear/agent-1/invocation-0",
              "error": null,
              "json_valid": true,
              "legal_action": true,
              "phase": "clear",
              "reason": null,
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-15/clear/agent-0/invocation-0",
              "error": null,
              "json_valid": true,
              "legal_action": true,
              "phase": "clear",
              "reason": null,
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-15/retain/agent-1/invocation-0",
              "error": null,
              "json_valid": true,
              "legal_action": true,
              "phase": "retain",
              "reason": null,
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-15/retain/agent-0/invocation-0",
              "error": null,
              "json_valid": true,
              "legal_action": true,
              "phase": "retain",
              "reason": null,
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-15/control-revised-direct",
              "error": null,
              "json_valid": true,
              "legal_action": true,
              "phase": "control-revised-direct",
              "reason": null,
              "runtime_safe": true,
              "schema_valid": true
            }
          ],
          "world": "main-15"
        }
      ],
      "human_review": "retrospective_pending",
      "id": "batch/main-14+main-15",
      "number": 8,
      "passed": true,
      "policy": "i01-recorded-outcomes-run-all-2026-10-15",
      "worlds": [
        "main-14",
        "main-15"
      ]
    },
    "automatic/batch/main-16+main-17": {
      "complete": true,
      "evidence": [
        {
          "checks": {
            "committed_calls": true,
            "every_episode_has_calls": true,
            "runtime_integrity": true,
            "terminal_evidence": true
          },
          "control_protocol_errors": 0,
          "human_review": "retrospective_pending",
          "original_messages": 2,
          "original_team_completed": true,
          "passed": true,
          "prefix_protocol_errors": 0,
          "protocol_errors": 0,
          "recorded_calls": 7,
          "recovery_protocol_errors": 0,
          "useful_communication": null,
          "validation": [
            {
              "admission_blocking": false,
              "call": "main-16/prefix/agent-1/invocation-0",
              "error": null,
              "json_valid": true,
              "legal_action": true,
              "phase": "prefix",
              "reason": null,
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-16/prefix/agent-0/invocation-0",
              "error": null,
              "json_valid": true,
              "legal_action": true,
              "phase": "prefix",
              "reason": null,
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-16/retain/agent-1/invocation-0",
              "error": null,
              "json_valid": true,
              "legal_action": true,
              "phase": "retain",
              "reason": null,
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-16/retain/agent-0/invocation-0",
              "error": null,
              "json_valid": true,
              "legal_action": true,
              "phase": "retain",
              "reason": null,
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-16/clear/agent-1/invocation-0",
              "error": null,
              "json_valid": true,
              "legal_action": true,
              "phase": "clear",
              "reason": null,
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-16/clear/agent-0/invocation-0",
              "error": null,
              "json_valid": true,
              "legal_action": true,
              "phase": "clear",
              "reason": null,
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-16/control-revised-direct",
              "error": null,
              "json_valid": true,
              "legal_action": true,
              "phase": "control-revised-direct",
              "reason": null,
              "runtime_safe": true,
              "schema_valid": true
            }
          ],
          "world": "main-16"
        },
        {
          "checks": {
            "committed_calls": true,
            "every_episode_has_calls": true,
            "runtime_integrity": true,
            "terminal_evidence": true
          },
          "control_protocol_errors": 0,
          "human_review": "retrospective_pending",
          "original_messages": 2,
          "original_team_completed": true,
          "passed": true,
          "prefix_protocol_errors": 2,
          "protocol_errors": 2,
          "recorded_calls": 9,
          "recovery_protocol_errors": 0,
          "useful_communication": null,
          "validation": [
            {
              "admission_blocking": false,
              "call": "main-17/prefix/agent-1/invocation-0",
              "error": "malformed_action",
              "json_valid": true,
              "legal_action": false,
              "phase": "prefix",
              "reason": "wait_requires_null_message_and_submit",
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-17/prefix/agent-0/invocation-0",
              "error": "malformed_action",
              "json_valid": true,
              "legal_action": false,
              "phase": "prefix",
              "reason": "wait_requires_null_message_and_submit",
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-17/prefix/agent-1/invocation-1",
              "error": null,
              "json_valid": true,
              "legal_action": true,
              "phase": "prefix",
              "reason": null,
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-17/prefix/agent-0/invocation-1",
              "error": null,
              "json_valid": true,
              "legal_action": true,
              "phase": "prefix",
              "reason": null,
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-17/clear/agent-1/invocation-0",
              "error": null,
              "json_valid": true,
              "legal_action": true,
              "phase": "clear",
              "reason": null,
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-17/clear/agent-0/invocation-0",
              "error": null,
              "json_valid": true,
              "legal_action": true,
              "phase": "clear",
              "reason": null,
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-17/retain/agent-1/invocation-0",
              "error": null,
              "json_valid": true,
              "legal_action": true,
              "phase": "retain",
              "reason": null,
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-17/retain/agent-0/invocation-0",
              "error": null,
              "json_valid": true,
              "legal_action": true,
              "phase": "retain",
              "reason": null,
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-17/control-revised-direct",
              "error": null,
              "json_valid": true,
              "legal_action": true,
              "phase": "control-revised-direct",
              "reason": null,
              "runtime_safe": true,
              "schema_valid": true
            }
          ],
          "world": "main-17"
        }
      ],
      "human_review": "retrospective_pending",
      "id": "batch/main-16+main-17",
      "number": 9,
      "passed": true,
      "policy": "i01-recorded-outcomes-run-all-2026-10-15",
      "worlds": [
        "main-16",
        "main-17"
      ]
    },
    "active_generation": false,
    "batch": {
      "complete": true,
      "eligible_retry_allowance": 28,
      "first_ceiling": 38,
      "forecast": {
        "caveat": "Observed maximum with 25% margin is a forecast, not a runtime guarantee; two allocated GPUs also consume idle time.",
        "conservative_wall_seconds": 1362.995942282491,
        "estimated_checkpoint_overhead_seconds": 62.08628342400334,
        "estimated_remaining_exports": 12,
        "forecast_scope": "main_only; not a whole-session completion guarantee",
        "includes_idle_inspection": false,
        "measured_checkpoint_seconds": 5.173856952000278,
        "observed_max_ready_seconds": 22.168335626999806,
        "remaining_attempt_allowance": 273,
        "remaining_pilot_first_attempts": 0,
        "remaining_pilots": 0,
        "remaining_session_seconds": 40089.783012,
        "session_observation": {
          "at": "2026-10-15T17:40:47.399455+00:00",
          "basis": "planning_estimate",
          "remaining_minutes": 700
        },
        "timeout_worst_case_seconds": 6960,
        "whole_forecast_basis": "remaining pilot/main calls, observed maximum +25% and 5s/call, observed export maximum; heuristic, excludes setup/load and abnormal tails",
        "whole_remaining_wall_seconds": 1425.0822257064942,
        "worst_remaining_first_attempts": 38
      },
      "id": "batch/main-18+main-19",
      "prepared_at": "2026-10-15T18:12:37.617923+00:00",
      "worlds": [
        "main-18",
        "main-19"
      ]
    },
    "automatic/batch/main-18+main-19": {
      "complete": true,
      "evidence": [
        {
          "checks": {
            "committed_calls": true,
            "every_episode_has_calls": true,
            "runtime_integrity": true,
            "terminal_evidence": true
          },
          "control_protocol_errors": 0,
          "human_review": "retrospective_pending",
          "original_messages": 0,
          "original_team_completed": true,
          "passed": true,
          "prefix_protocol_errors": 4,
          "protocol_errors": 4,
          "recorded_calls": 11,
          "recovery_protocol_errors": 0,
          "useful_communication": null,
          "validation": [
            {
              "admission_blocking": false,
              "call": "main-18/prefix/agent-1/invocation-0",
              "error": "malformed_action",
              "json_valid": true,
              "legal_action": false,
              "phase": "prefix",
              "reason": "wait_requires_null_message_and_submit",
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-18/prefix/agent-0/invocation-0",
              "error": "malformed_action",
              "json_valid": true,
              "legal_action": false,
              "phase": "prefix",
              "reason": "wait_requires_null_message_and_submit",
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-18/prefix/agent-1/invocation-1",
              "error": "malformed_action",
              "json_valid": true,
              "legal_action": false,
              "phase": "prefix",
              "reason": "wait_requires_null_message_and_submit",
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-18/prefix/agent-0/invocation-1",
              "error": "malformed_action",
              "json_valid": true,
              "legal_action": false,
              "phase": "prefix",
              "reason": "wait_requires_null_message_and_submit",
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-18/prefix/agent-1/invocation-2",
              "error": null,
              "json_valid": true,
              "legal_action": true,
              "phase": "prefix",
              "reason": null,
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-18/prefix/agent-0/invocation-2",
              "error": null,
              "json_valid": true,
              "legal_action": true,
              "phase": "prefix",
              "reason": null,
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-18/retain/agent-1/invocation-0",
              "error": null,
              "json_valid": true,
              "legal_action": true,
              "phase": "retain",
              "reason": null,
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-18/retain/agent-0/invocation-0",
              "error": null,
              "json_valid": true,
              "legal_action": true,
              "phase": "retain",
              "reason": null,
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-18/clear/agent-1/invocation-0",
              "error": null,
              "json_valid": true,
              "legal_action": true,
              "phase": "clear",
              "reason": null,
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-18/clear/agent-0/invocation-0",
              "error": null,
              "json_valid": true,
              "legal_action": true,
              "phase": "clear",
              "reason": null,
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-18/control-revised-direct",
              "error": null,
              "json_valid": true,
              "legal_action": true,
              "phase": "control-revised-direct",
              "reason": null,
              "runtime_safe": true,
              "schema_valid": true
            }
          ],
          "world": "main-18"
        },
        {
          "checks": {
            "committed_calls": true,
            "every_episode_has_calls": true,
            "runtime_integrity": true,
            "terminal_evidence": true
          },
          "control_protocol_errors": 0,
          "human_review": "retrospective_pending",
          "original_messages": 0,
          "original_team_completed": false,
          "passed": true,
          "prefix_protocol_errors": 5,
          "protocol_errors": 8,
          "recorded_calls": 14,
          "recovery_protocol_errors": 3,
          "useful_communication": null,
          "validation": [
            {
              "admission_blocking": false,
              "call": "main-19/prefix/agent-1/invocation-0",
              "error": "malformed_action",
              "json_valid": true,
              "legal_action": false,
              "phase": "prefix",
              "reason": "wait_requires_null_message_and_submit",
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-19/prefix/agent-0/invocation-0",
              "error": "malformed_action",
              "json_valid": true,
              "legal_action": false,
              "phase": "prefix",
              "reason": "wait_requires_null_message_and_submit",
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-19/prefix/agent-1/invocation-1",
              "error": "malformed_action",
              "json_valid": true,
              "legal_action": false,
              "phase": "prefix",
              "reason": "wait_requires_null_message_and_submit",
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-19/prefix/agent-0/invocation-1",
              "error": "malformed_action",
              "json_valid": true,
              "legal_action": false,
              "phase": "prefix",
              "reason": "wait_requires_null_message_and_submit",
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-19/prefix/agent-1/invocation-2",
              "error": "malformed_action",
              "json_valid": true,
              "legal_action": false,
              "phase": "prefix",
              "reason": "wait_requires_null_message_and_submit",
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-19/prefix/agent-0/invocation-2",
              "error": null,
              "json_valid": true,
              "legal_action": true,
              "phase": "prefix",
              "reason": null,
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-19/clear/agent-1/invocation-0",
              "error": "malformed_action",
              "json_valid": true,
              "legal_action": false,
              "phase": "clear",
              "reason": "wait_requires_null_message_and_submit",
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-19/clear/agent-0/invocation-0",
              "error": "malformed_action",
              "json_valid": true,
              "legal_action": false,
              "phase": "clear",
              "reason": "wait_requires_null_message_and_submit",
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-19/clear/agent-1/invocation-1",
              "error": "malformed_action",
              "json_valid": true,
              "legal_action": false,
              "phase": "clear",
              "reason": "wait_requires_null_message_and_submit",
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-19/clear/agent-0/invocation-1",
              "error": null,
              "json_valid": true,
              "legal_action": true,
              "phase": "clear",
              "reason": null,
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-19/clear/agent-1/invocation-2",
              "error": null,
              "json_valid": true,
              "legal_action": true,
              "phase": "clear",
              "reason": null,
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-19/retain/agent-1/invocation-0",
              "error": null,
              "json_valid": true,
              "legal_action": true,
              "phase": "retain",
              "reason": null,
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-19/retain/agent-0/invocation-0",
              "error": null,
              "json_valid": true,
              "legal_action": true,
              "phase": "retain",
              "reason": null,
              "runtime_safe": true,
              "schema_valid": true
            },
            {
              "admission_blocking": false,
              "call": "main-19/control-revised-direct",
              "error": null,
              "json_valid": true,
              "legal_action": true,
              "phase": "control-revised-direct",
              "reason": null,
              "runtime_safe": true,
              "schema_valid": true
            }
          ],
          "world": "main-19"
        }
      ],
      "human_review": "retrospective_pending",
      "id": "batch/main-18+main-19",
      "number": 10,
      "passed": true,
      "policy": "i01-recorded-outcomes-run-all-2026-10-15",
      "worlds": [
        "main-18",
        "main-19"
      ]
    },
    "operator_authorization": {
      "action": "snapshot",
      "args": {},
      "evidence": "Explicit operator finite-action command/button"
    },
    "action": {
      "args": {},
      "at": "2026-10-15T18:14:54.826394+00:00",
      "error": null,
      "name": "snapshot",
      "status": "complete"
    },
    "checkpoint_timing": {
      "last_seconds": 5.541828024000097,
      "max_seconds": 5.963703115000044,
      "successful_exports": 52
    }
  },
  "terminal_reasons": {
    "control_completed": 38,
    "both_submitted": 57,
    "horizon_exhausted": 4,
    "waiting_deadlock": 8
  },
  "lost_spending": {
    "upper": 0,
    "resolved": true
  },
  "campaign_attempts": 252,
  "prior_attempts": 0,
  "attempt_scope": "independent-study",
  "missing_prior_studies": [],
  "local_contingency": 0,
  "remaining_attempt_allowance": 248,
  "prior_spending": [],
  "physical_ready_seconds_observed": 1943.1056445999966,
  "physical_dispatch_seconds_observed": 1944.2808162699998,
  "attempts_unknown_ready_seconds": 0,
  "generated_tokens_observed": 15472,
  "campaign_ready_seconds_observed": 1943.1056445999966,
  "campaign_generated_tokens_observed": 15472,
  "campaign_attempts_unknown_ready_seconds": 0,
  "attempts_unknown_generated_tokens": 0,
  "model_load_seconds_observed": 119.02880420400015,
  "failed_model_load_seconds_observed": 0,
  "provider_assignment_release": "unknown unless supplied separately; observation and process exit do not establish allocation boundaries",
  "principal_effort_clear_minus_retain_seconds": 9.15696611304993,
  "principal_effort_interval": {
    "low": 1.9643914256499215,
    "high": 17.123815258149968,
    "confidence": 0.95,
    "draws": 10000,
    "strata": "owner/first-speaker",
    "caveat": "Exploratory small-sample interval."
  },
  "cost_complete_pairs": 20,
  "qualification": {
    "direct": {
      "mode": "direct",
      "policy": "i01-direct-protocol-2026-10-15",
      "planned": 12,
      "admitted": 12,
      "unresolved": 0,
      "recorded": 12,
      "committed": 12,
      "valid": 12,
      "correct": 10,
      "wrong_scalar": 2,
      "protocol_errors": 0,
      "unexecuted": 0,
      "protocol_passed": true,
      "passed": true,
      "historical_gate": {
        "correct": 10,
        "passed": true,
        "policy": "i01-direct-protocol-2026-10-15",
        "protocol_errors": 0,
        "reason": "",
        "total": 12
      },
      "physical_attempts": 12,
      "generated_tokens_observed": 193,
      "ready_seconds_observed": 27.51595256199971,
      "attempts_unknown_effort": 0
    },
    "thinking": {
      "mode": "thinking",
      "policy": "i01-direct-protocol-2026-10-15",
      "planned": 12,
      "admitted": 0,
      "unresolved": 0,
      "recorded": 0,
      "committed": 0,
      "valid": 0,
      "correct": 0,
      "wrong_scalar": 0,
      "protocol_errors": 0,
      "unexecuted": 12,
      "protocol_passed": false,
      "passed": false,
      "historical_gate": null,
      "physical_attempts": 0,
      "generated_tokens_observed": 0,
      "ready_seconds_observed": 0,
      "attempts_unknown_effort": 0
    }
  },
  "execution_policy": "i01-recorded-outcomes-run-all-2026-10-15",
  "human_review_status": "retrospective_pending",
  "scientific_gate_status": "complete",
  "blocking_reasons": [],
  "session_window": {
    "deadline": "2026-10-16T05:20:47.399377+00:00",
    "evidence": "User reports an approximately 12-hour session; 700-minute fresh-session planning bound, provider quota/deadline not independently verified.",
    "observation": {
      "at": "2026-10-15T17:40:47.399455+00:00",
      "basis": "planning_estimate",
      "remaining_minutes": 700
    },
    "observed_start": "2026-10-15T17:44:39.516556+00:00",
    "session": "a7bb7845-cf04-4efd-9b68-f74b9595cfaa"
  },
  "failure_cleanup": null
}
```
