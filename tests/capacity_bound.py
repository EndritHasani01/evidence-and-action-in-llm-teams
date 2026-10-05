"""CPU-only proof audit for the pinned native literal-history tokenizer.

The argument is in docs/implementation-research/m2-t06-capacity-proof.md.
This is capacity evidence, never a renderer, inference tool or budget repair.
"""

import math
import re

RUN = re.compile(r"([\x00-\x7f])\1{7,}")
SPLIT = (r"(?i:'s|'t|'re|'ve|'m|'ll|'d)|[^\r\n\p{L}\p{N}]?[\p{L}\p{M}]+|\p{N}|"
         r" ?[^\s\p{L}\p{M}\p{N}]+[\r\n]*|\s*[\r\n]+|\s+(?!\S)|\s+")


def byte_alphabet():
    # The standard ByteLevel bijection: vocabulary glyph UTF-8 size is not
    # decoded payload byte size.
    values = list(range(33, 127)) + list(range(161, 173)) + list(range(174, 256))
    glyphs = values[:]
    extra = 0
    for value in range(256):
        if value not in values:
            values.append(value)
            glyphs.append(256 + extra)
            extra += 1
    return {chr(glyph): value for value, glyph in zip(values, glyphs)}


def scalar_parts(raw):
    """Complete scalars plus a per-byte allowance for invalid/partial UTF-8.

    Do not independently lossy-decode a multi-byte fragment as one replacement:
    it can join the neighboring token into a scalar with a larger decomposition.
    """
    offset, parts, incomplete = 0, [], 0
    while offset < len(raw):
        try:
            parts.append(raw[offset:].decode("utf-8"))
            break
        except UnicodeDecodeError as error:
            parts.append(raw[offset:offset + error.start].decode("utf-8"))
            incomplete += error.end - error.start
            offset += error.end
    return parts, incomplete


def piece_upper(text, ladders, *, nfd=None, em_dash=False):
    """A weighted byte bound, not sampled canonical re-encoding ratios.

    Every byte costs one token except audited homogeneous ASCII merge ladders.
    Two boundary fragments per level and two peeled regex-edge characters are
    paid explicitly. Protect the last ASCII starter against NFC composition.
    For already-NFC prose, separated E2-80 pairs in em dashes each force at
    least one merge (or an overlapping merge of equal or greater saving).
    """
    text = nfd.normalize_str(text) if nfd is not None else text
    upper = len(text.encode("utf-8"))
    if em_dash:
        upper -= text.count("\u2014")
    for match in RUN.finditer(text):
        size = len(match.group())
        chunk = ladders.get(match.group(1), 1)
        if chunk >= 8:
            cost = math.ceil((size - 1) / chunk) + 2 * int(math.log2(chunk)) + 5
            upper -= max(0, size - cost)
    return upper


def audit_tokenizer(metadata, tokenizer):
    from tokenizers.normalizers import NFD, NFC
    from tokenizers.pre_tokenizers import ByteLevel

    model = metadata["model"]
    expected_pretokenizer = {"type": "Sequence", "pretokenizers": [
        {"type": "Split", "pattern": {"Regex": SPLIT}, "behavior": "Isolated", "invert": False},
        {"type": "ByteLevel", "add_prefix_space": False, "trim_offsets": False, "use_regex": False}]}
    if (model["type"] != "BPE" or model.get("dropout") is not None
            or model.get("unk_token") is not None or model.get("ignore_merges", False)
            or model.get("continuing_subword_prefix") or model.get("end_of_word_suffix")
            or metadata["normalizer"] != {"type": "NFC"}
            or metadata["decoder"]["type"] != "ByteLevel"
            or metadata["pre_tokenizer"] != expected_pretokenizer):
        raise ValueError("bound requires the pinned deterministic NFC ByteLevel BPE")
    inverse = byte_alphabet()
    forward = {value: glyph for glyph, value in inverse.items()}
    if set(ByteLevel.alphabet()) != set(inverse) or not set(inverse) <= model["vocab"].keys():
        raise ValueError("all 256 unmerged byte symbols must be available")
    pairs = [tuple(pair.split(" ")) if isinstance(pair, str) else tuple(pair)
             for pair in model["merges"]]
    ranks = {pair: rank for rank, pair in enumerate(pairs)}
    outputs = {left + right: rank for rank, (left, right) in enumerate(pairs)}
    if len(outputs) != len(pairs):
        raise ValueError("run proof requires unique merge productions")
    # Only homogeneous ASCII productions are used by the run proof. Some
    # unrelated multilingual merges reference a later production; do not infer
    # globally monotone ranks or canonical-encoding subadditivity from this audit.
    pure = 0
    for rank, (left, right) in enumerate(pairs):
        raw = bytes(inverse[c] for c in left + right)
        if raw and raw[0] < 128 and len(set(raw)) == 1:
            pure += 1
            if any(outputs.get(part, -1) >= rank for part in (left, right)):
                raise ValueError("homogeneous ASCII merge dependency must precede its use")
    ladders = {}
    for value in range(128):
        symbol, size, previous = forward[value], 1, -1
        while (symbol * size, symbol * size) in ranks:
            rank = ranks[symbol * size, symbol * size]
            if rank <= previous:
                raise ValueError("ASCII doubling ladder ranks must increase")
            previous, size = rank, size * 2
        if size >= 8:
            ladders[chr(value)] = size
    if (forward[0xE2], forward[0x80]) not in ranks:
        raise ValueError("em-dash UTF-8 prefix pair is needed for the prose bound")
    # AutoTokenizer adds seven further special tokens from tokenizer_config.
    # Audit the loaded boundary, not just tokenizer.json's added-token list.
    loaded_added = [dict(id=token_id, content=str(token), lstrip=token.lstrip,
                         rstrip=token.rstrip, normalized=token.normalized)
                    for token_id, token in sorted(tokenizer.added_tokens_decoder.items())]
    for token in loaded_added:
        text = token["content"]
        if (not text.isascii() or RUN.search(text)
                or (len(set(text)) == 1 and text[0] in ladders)
                or token["lstrip"] or token["rstrip"]
                or token["normalized"]):
            raise ValueError("added-token boundary is outside the audited contract")
    nfd, nfc = NFD(), NFC()
    max_scalars, max_ratio = 0, 0
    for value in range(0x110000):
        if 0xD800 <= value <= 0xDFFF:
            continue
        scalar = chr(value)
        decomposed = nfd.normalize_str(scalar)
        before, after = len(scalar.encode()), len(decomposed.encode())
        max_scalars = max(max_scalars, len(decomposed))
        max_ratio = max(max_ratio, math.ceil(after / before))
        if len(nfc.normalize_str(decomposed).encode()) > after:
            raise ValueError("canonical composition must not increase the byte allowance")
    if max_ratio > 3:
        raise ValueError("partial UTF-8 bytes need a renewed decomposition allowance")
    rows = []
    added = {token["id"]: token["content"] for token in loaded_added}
    for symbol, token_id in model["vocab"].items():
        raw = (added[token_id].encode() if token_id in added else
               bytes(inverse[c] for c in symbol))
        parts, incomplete = scalar_parts(raw)
        own = 3 * incomplete + sum(piece_upper(part, ladders, nfd=nfd) for part in parts)
        prose = 3 * incomplete + sum(piece_upper(part, ladders, em_dash=True) for part in parts)
        rows.append((token_id, own, prose, len(raw)))
    model_ids = set(model["vocab"].values())
    for token_id, content in added.items():
        if token_id not in model_ids:
            own = piece_upper(content, ladders, nfd=nfd)
            prose = piece_upper(content, ladders, em_dash=True)
            rows.append((token_id, own, prose, len(content.encode())))
    loaded_vocab = tokenizer.get_vocab()
    if ({row[0] for row in rows} != set(loaded_vocab.values())
            or any(loaded_vocab.get(symbol) != token_id
                   for symbol, token_id in model["vocab"].items())):
        raise ValueError("audit must cover the exact loaded vocabulary")
    return {"model_vocabulary_entries": len(model["vocab"]), "audited_entries": len(rows),
            "configuration_added_tokens": [token for token in loaded_added
                if token["id"] not in {item["id"] for item in metadata["added_tokens"]}],
            "homogeneous_ascii_productions": pure,
            "ascii_doubling_ladders": ladders, "max_nfd_scalars": max_scalars,
            "max_nfd_byte_ratio_ceiling": max_ratio,
            "own_tokens_per_physical_token_upper": max(row[1] for row in rows),
            "prose_tokens_per_counted_token_upper": max(row[2] for row in rows),
            "payload_bytes_per_token_upper": max(row[3] for row in rows),
            "largest_own": sorted(rows, key=lambda row: (-row[1], row[0]))[:12],
            "largest_prose": sorted(rows, key=lambda row: (-row[2], row[0]))[:12]}
