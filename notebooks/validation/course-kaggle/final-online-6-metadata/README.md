# Final-online-6 native metadata evidence

Collected on 13 October 2026 using small read-only HTTP requests. No tensor
payloads were downloaded and no model/GPU execution occurred.

- `4B-hub.json`: original response from the
  [pinned 4B revision API](https://huggingface.co/api/models/Qwen/Qwen3.5-4B/revision/851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a?blobs=true).
- `9B-hub.json`: original response from the
  [pinned 9B revision API](https://huggingface.co/api/models/Qwen/Qwen3.5-9B/revision/c202236235762e1c871ad0ccb60c8ee5ba337b9a?blobs=true).
- Each `*.header.json` contains only the native 4B Safetensors JSON header,
  including its original trailing whitespace. It was fetched with two strict
  HTTP 206 range requests: the first eight length bytes, then the header.
- Each `*.header-receipt.json` records the immutable source URL, Content-Range,
  native total size, header/prefix bytes and derived payload size. The original
  length prefix is represented by its parsed unsigned little-endian value.

The headers plus their two eight-byte length prefixes total **90,240 bytes**.
The tensor payload total is **9,319,737,856**; complete shard files total
**9,319,828,096**. The native model index itself stays unchanged.
See the [official Safetensors format](https://github.com/safetensors/safetensors#format)
and [pinned 4B index](https://huggingface.co/Qwen/Qwen3.5-4B/raw/851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a/model.safetensors.index.json).

The [read-only analysis](../analyse_final_online_6.py) consumes these fixtures
offline, verifies the revision/native file identities and exact header arithmetic,
and executes the archived inventory function to reproduce the failure. These
files are technical diagnostic evidence, not new scientific requirements or
downloaded model checkpoints.
