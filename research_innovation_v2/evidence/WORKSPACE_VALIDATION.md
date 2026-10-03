# Workspace validation

Executed 2026-10-04 after final scientific review. These checks establish artifact consistency and preservation, not model performance, hardware feasibility or exhaustive novelty.

- All **15** required synthesis/state artifacts exist.
- All **38** files in the prior investigation have documented read coverage, including programmatic inspection of the complete audit JSON.
- Checked **127** local Markdown links: zero broken links; no Unicode replacement characters or unbalanced fenced code blocks.
- Re-ran the strengthened protocol probe successfully: 8,748 finite update cases, five numeric ambiguous-view pairs, one BFS pair, two complete scripted B-state pairs with receipt sufficiency, temporal-order examples and 256 routing patterns.
- Budget arithmetic checks agree: original 5,856/4,488; focused extension 6,368/4,872; rejected all-six sweep 7,392/5,640; pilot 652 plus at most 24 smoke calls.
- Independent final review is closed; its two interpretation corrections were applied and verified.
- Specification SHA256: `D6DA776F73B6AD03874DC17DF546B6662DB3569C9F0B80780179CDFFE44FBC00`, identical to the prior recorded baseline.
- Git comparison against start-of-investigation commit `1f9bed5` finds no changes to PROJECT_SPECIFICATION.md, research_innovation/, or acl26-silo-bench/. The protocol probe additionally verified all 36 prior source hashes and 180 stored-case hashes.

No LLM/GPU inference was run. No production runtime, original specification or previous research record was modified. New Python files are deterministic research probes only. External paper results were inspected, not reproduced. The theoretical examples are constructed, not natural model observations.

Reproduction: run the two scripts linked in [README](../README.md). Search/read limitations and paper-version discrepancies remain documented in the source notes.
