"""Verify changed handoff documents and inbound links to their Markdown headings."""

from collections import Counter
import json
from pathlib import Path
import re
import unicodedata
from urllib.parse import unquote

from verify_handoff import DOCUMENTS, ROOT


def anchors(path):
    result = set()
    repeated = Counter()
    fenced = False
    for line in path.read_text(encoding="utf-8").splitlines():
        if re.match(r"^\s*(```|~~~)", line):
            fenced = not fenced
        match = re.match(r"^#{1,6}\s+(.+?)\s*#*\s*$", line)
        if fenced or not match:
            continue
        title = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", match.group(1)).lower()
        slug = "".join(c for c in title if c in " _-" or unicodedata.category(c)[0] in "LN")
        slug = slug.replace(" ", "-")
        result.add(slug if not repeated[slug] else f"{slug}-{repeated[slug]}")
        repeated[slug] += 1
    return result


def main():
    output = Path(__file__).resolve().parent / "link-validation.json"
    assert not output.exists(), "Preserve earlier link evidence"
    changed = {(ROOT / name).resolve() for name in DOCUMENTS}
    user_edit = (ROOT / "docs/validation/m5-inference-preparation.md").resolve()
    sources = sorted(set(ROOT.glob("docs/**/*.md")) | {ROOT / "README.md"})
    checked = fragments = inbound = 0
    for source in sources:
        for target in re.findall(r"\[[^\]]+\]\(([^()\n]+)\)", source.read_text(encoding="utf-8")):
            target = target.strip().strip("<>")
            if re.match(r"[a-z]+://|mailto:", target):
                continue
            name, _, fragment = target.partition("#")
            resolved = (source.parent / unquote(name)).resolve() if name else source.resolve()
            in_scope = source.resolve() in changed or source.resolve() == user_edit
            if not in_scope and resolved not in changed:
                continue
            assert resolved.exists(), (source, target)
            checked += 1
            inbound += not in_scope
            if fragment and resolved.suffix == ".md":
                assert unquote(fragment) in anchors(resolved), (source, target)
                fragments += 1
    report = {"status": "passed", "changed_documents": len(changed),
        "existing_user_edit_links_also_checked": True,
        "local_references_checked": checked, "markdown_fragments_checked": fragments,
        "other_document_inbound_links_checked": inbound,
        "scope": "Changed handoffs, existing user edit, and inbound links to changed handoffs; no remote links or GPU execution."}
    output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
