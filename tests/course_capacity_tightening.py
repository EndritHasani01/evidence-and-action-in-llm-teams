"""Native proof-only tightening; runtime bytes/caps and old capacity stay intact."""

import argparse
import gzip
import hashlib
import json
from pathlib import Path
import re
import unittest

from tests.capacity_bound import byte_alphabet, piece_upper, scalar_parts
from tests.tokenizer_course_capacity import metadata_support

ROOT = Path(__file__).resolve().parent.parent
ASCII_REGIONS = re.compile(r"[A-Za-z]+|([\x00-\x7f])\1{7,}")


def hangul(scalar):
    return 0xAC00 <= ord(scalar) <= 0xD7A3


def proof_decomposition(text, nfd):
    # Complete syllables contain only CCC=0 L/V[/T] internally. Ordering
    # cannot insert a later mark there; LV+T may compose to one 3-byte syllable.
    return "".join(c if hangul(c) else nfd.normalize_str(c) for c in text)


def scalar_cost(scalar, byte_pairs):
    raw = scalar.encode("utf-8")
    return len(raw) - int(len(raw) >= 3 and not hangul(scalar) and tuple(raw[:2]) in byte_pairs)


def piece_cost(text, byte_pairs, ladders):
    upper = sum(scalar_cost(c, byte_pairs) for c in text)
    for region in ASCII_REGIONS.finditer(text):
        raw = region.group().encode("ascii")
        selected = 0
        previous = -9
        # Skip three starting characters (native contraction/regex boundary)
        # and two ending characters (edge plus a composable ASCII starter).
        for offset in range(3, len(raw)-2):
            if offset-previous >= 3 and tuple(raw[offset:offset+2]) in byte_pairs:
                selected += 1
                previous = offset
        # Independent alternatives over this same ASCII region, not additive.
        old_run_savings = len(raw) - piece_upper(region.group(), ladders)
        upper -= max(old_run_savings, selected)
    return upper


def byte_pairs(metadata):
    inverse = byte_alphabet()
    pairs = [p.split(" ") if isinstance(p,str) else p for p in metadata["model"]["merges"]]
    return {(inverse[left],inverse[right]) for left,right in pairs if len(left)==len(right)==1}


def audit(directory, tokenizer):
    import tokenizers
    from tokenizers.normalizers import NFD, NFC
    support = metadata_support(directory, tokenizer)
    metadata = json.loads((directory/"tokenizer.json").read_bytes())
    original = json.loads(gzip.decompress((ROOT/"tests/fixtures/course_capacity.json.gz").read_bytes()))
    prior = original["tokenizer_bound_audit"]
    pairs = byte_pairs(metadata)
    # The pinned regex isolates digits. They must never get a byte-pair credit.
    if any(48 <= a <= 57 and 48 <= b <= 57 for a, b in pairs):
        raise ValueError("digit merge requires a renewed regex-boundary argument")
    nfd, nfc = NFD(), NFC()
    scalars = 0
    for code in range(0x110000):
        if 0xD800 <= code <= 0xDFFF:
            continue
        text = chr(code)
        decomposition = proof_decomposition(text,nfd)
        normal = nfc.normalize_str(text)
        if sum(scalar_cost(c,pairs) for c in normal) > sum(scalar_cost(c,pairs) for c in decomposition):
            raise ValueError(f"Unicode composition potential grows: {code}")
        if nfc.normalize_str(decomposition) != normal:
            raise ValueError(f"proof decomposition is not canonically equivalent: {code}")
        if hangul(text) and scalar_cost(text,pairs) > sum(scalar_cost(c,pairs) for c in nfd.normalize_str(text)):
            raise ValueError(f"Jamo composition potential grows: {code}")
        scalars += 1
    # Retain the original exhaustive three-byte partial/invalid allowance.
    if prior["max_nfd_byte_ratio_ceiling"] != 3:
        raise ValueError("renew the original partial UTF-8 proof")
    inverse = byte_alphabet()
    added = {i:str(t) for i,t in tokenizer.added_tokens_decoder.items()}
    rows = []
    for symbol, token_id in tokenizer.get_vocab().items():
        raw = added[token_id].encode() if token_id in added else bytes(inverse[c] for c in symbol)
        parts, partial = scalar_parts(raw)
        own = 3*partial + sum(piece_cost(proof_decomposition(p,nfd),pairs,prior["ascii_doubling_ladders"]) for p in parts)
        prose = 3*partial + sum(piece_cost(p,pairs,prior["ascii_doubling_ladders"]) for p in parts)
        rows.append((token_id,own,prose))
    if len(rows) != prior["audited_entries"]:
        raise ValueError("loaded vocabulary coverage differs")
    own = max(r[1] for r in rows)
    prose = max(r[2] for r in rows)
    accounting = []
    for original_row in original["accounting"]:
        row = {k:original_row[k] for k in ("task","size","nontext_bytes","template_wrapper_bytes")}
        row.update(own_payload_tokens_upper=7*256*own, prose_payload_tokens_upper=21*64*prose)
        row["input_tokens_upper"] = row["nontext_bytes"]+row["template_wrapper_bytes"]+row["own_payload_tokens_upper"]+row["prose_payload_tokens_upper"]
        row["resident_tokens_upper"] = row["input_tokens_upper"]+256
        accounting.append(row)
    return dict(model=original["model"],revision=original["revision"],limits=original["limits"],
        tokenizer_sha256=hashlib.sha256((directory/"tokenizer.json").read_bytes()).hexdigest(),
        tokenizers=tokenizers.__version__,
        source_capacity_sha256=hashlib.sha256((ROOT/"tests/fixtures/course_capacity.json.gz").read_bytes()).hexdigest(),
        audited_entries=len(rows), unicode_scalars=scalars, eligible_byte_pairs=len(pairs),
        unassigned_output_ids_decoding_empty=len(support["unassigned_output_ids_decoding_empty"]),
        own_tokens_per_physical_token_upper=own, prose_tokens_per_counted_token_upper=prose,
        largest_own=sorted(rows,key=lambda r:(-r[1],r[0]))[:12],
        largest_prose=sorted(rows,key=lambda r:(-r[2],r[0]))[:12], accounting=accounting,
        input_tokens_upper=max(r["input_tokens_upper"] for r in accounting),
        resident_tokens_upper=max(r["resident_tokens_upper"] for r in accounting),
        original_resident_tokens_upper=original["resident_tokens_upper"],
        scope="Supplemental complete native capacity argument only; no runtime bytes/caps changed or model/GPU admission.",
        model_weights_loaded=False,gpu_execution=False,memory_preparation_admitted=False)


class TighteningChecks(unittest.TestCase):
    directory = tokenizer = report = None

    def test_exhaustive_identity_arithmetic_and_complete_family_coverage(self):
        self.assertEqual((self.report["audited_entries"],self.report["unicode_scalars"]),(248077,1112064))
        self.assertEqual((self.report["own_tokens_per_physical_token_upper"],
                          self.report["prose_tokens_per_counted_token_upper"]),(32,32))
        self.assertEqual((self.report["input_tokens_upper"],self.report["resident_tokens_upper"]),(109851,110107))
        self.assertEqual(len({r["task"] for r in self.report["accounting"]}),5)
        self.assertEqual(self.report["original_resident_tokens_upper"],156251)

    def test_all_original_adversarial_requests_remain_literal_and_within_bound(self):
        from scripts.m5_course_preparation import peer_view
        from recovery.prompts import COURSE_LIMITS, render_request, tokenize_request
        original = json.loads(gzip.decompress((ROOT/"tests/fixtures/course_capacity.json.gz").read_bytes()))
        bounds = {r["task"]:r["input_tokens_upper"] for r in self.report["accounting"]}
        for row in original["rendered_fixtures"]:
            view = peer_view(row["view"])
            native = tokenize_request(render_request(view,limits=COURSE_LIMITS),self.tokenizer,limits=COURSE_LIMITS)
            self.assertLessEqual(native.input_tokens,bounds[row["task"]])
            self.assertEqual(native.input_tokens,row["input_tokens"])
            for entry in view.history:
                if hasattr(entry,"text"):
                    self.assertIn(entry.text,native.text)

    def test_induced_byte_edges_survive_native_regex_contractions_and_boundaries(self):
        from tokenizers.normalizers import NFD
        pairs = byte_pairs(json.loads((self.directory/"tokenizer.json").read_bytes()))
        prior = json.loads(gzip.decompress((ROOT/"tests/fixtures/course_capacity.json.gz").read_bytes()))["tokenizer_bound_audit"]
        cases = ["'rest'", "'st'", "'llong'", "a'*", "ASCIIStarter\u0323\u0301",
            "\uac00\u11a8", "\uac00\u0301\u11a8", "\uac00\uac00", "\u1f82\u0301",
            "e\u0301", "\u2014"*16, " "*20+"\n"+" "*20+"\n", "\ufffd"*10,
            ".translatesAutoresizingMaskIntoConstraints", "<|im_start|>letters<|im_end|>"]
        for text in cases:
            with self.subTest(text=text):
                # Include native regex/template neighboring fragments; charge
                # their bytes separately, never presume BPE subadditivity.
                for left,right in (("\n","\n"),("'","."),(" ","\u0301")):
                    actual = self.tokenizer.encode(left+text+right,add_special_tokens=False)
                    upper = piece_cost(proof_decomposition(text,NFD()),pairs,prior["ascii_doubling_ladders"])
                    self.assertLessEqual(len(actual),upper+3*len((left+right).encode()))

    def test_ascii_certificates_are_inside_native_pretokenizer_pieces(self):
        from tokenizers.normalizers import NFC
        metadata = json.loads((self.directory/"tokenizer.json").read_bytes())
        pairs = byte_pairs(metadata)
        split = self.tokenizer.backend_tokenizer.pre_tokenizer
        inverse = byte_alphabet()
        # Exhaust the byte alphabet, all protected run lengths and native
        # contraction/whitespace/punctuation neighbors. Reuse the old run
        # certificate separately; this challenges the new pair certificate.
        for value in range(128):
            for length in (8, 9, 16, 32, 64, 128):
                for left, right in (("'", "\u0301"), ("x", "!"), ("\n", "\n"), (" ", "\r\n")):
                    text = NFC().normalize_str(left+chr(value)*length+right)
                    pieces = [bytes(inverse[c] for c in p) for p, _ in split.pre_tokenize_str(text)]
                    boundaries = set()
                    offset = 0
                    for p in pieces:
                        offset += len(p)
                        boundaries.add(offset)
                    self.assertEqual(b"".join(pieces), text.encode())
                    for region in ASCII_REGIONS.finditer(text):
                        raw = region.group().encode()
                        start = len(text[:region.start()].encode())
                        previous = -9
                        for offset in range(3, len(raw)-2):
                            if offset-previous >= 3 and tuple(raw[offset:offset+2]) in pairs:
                                self.assertNotIn(start+offset+1, boundaries)
                                previous = offset

    def test_cross_token_normalization_and_largest_payloads(self):
        from tokenizers.normalizers import NFD
        metadata = json.loads((self.directory/"tokenizer.json").read_bytes())
        pairs = byte_pairs(metadata)
        prior = json.loads(gzip.decompress((ROOT/"tests/fixtures/course_capacity.json.gz").read_bytes()))["tokenizer_bound_audit"]
        # Complete Hangul syllables followed by T, scalar fragments split at
        # physical token boundaries, and composing/reordered marks are legal
        # invalid own replies too. They retain the three-byte fragment charge.
        sequences = [(i,)*256 for i, _, _ in self.report["largest_own"]]
        fragments = ["\uac00\u11a8", "e\u0301\u0323", "\uac00\u0301\u11a8", "A\u0344", "\u1f82\u0301"]
        sequences += [tuple(self.tokenizer.encode(t,add_special_tokens=False))*32 for t in fragments]
        added = {i:str(t) for i,t in self.tokenizer.added_tokens_decoder.items()}
        symbols = {i:s for s,i in self.tokenizer.get_vocab().items()}
        inverse = byte_alphabet()
        for ids in sequences:
            allowance = 0
            for i in ids:
                raw = added[i].encode() if i in added else bytes(inverse[c] for c in symbols[i])
                parts, partial = scalar_parts(raw)
                allowance += 3*partial+sum(piece_cost(proof_decomposition(p,NFD()),pairs,prior["ascii_doubling_ladders"]) for p in parts)
            text = self.tokenizer.decode(ids,skip_special_tokens=False,clean_up_tokenization_spaces=False)
            self.assertLessEqual(len(self.tokenizer.encode("\n"+text+"\n",add_special_tokens=False)),allowance+2)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tokenizer",required=True,type=Path)
    parser.add_argument("--output",required=True,type=Path)
    args = parser.parse_args()
    if args.output.exists():
        parser.error("use a fresh report; retain earlier evidence")
    from transformers import AutoTokenizer
    tokenizer = AutoTokenizer.from_pretrained(args.tokenizer,local_files_only=True)
    report = audit(args.tokenizer,tokenizer)
    TighteningChecks.directory,TighteningChecks.tokenizer,TighteningChecks.report = args.tokenizer,tokenizer,report
    result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(TighteningChecks))
    if not result.wasSuccessful():
        return 1
    with args.output.open("x",encoding="utf-8",newline="\n") as output:
        json.dump(report,output,indent=2)
        output.write("\n")
    print(json.dumps({k:report[k] for k in ("audited_entries","unicode_scalars","input_tokens_upper","resident_tokens_upper","gpu_execution")},indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
