"""Write notebooks/thesis_kaggle.ipynb: settings + one facade call per cell.

Usage: python scripts/build_thesis_notebook.py
The notebook holds no scientific logic; every cell calls recovery.thesis.notebook.
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPOSITORY = "EndritHasani01/evidence-and-action-in-llm-teams"

INTRO = """# Thesis study: recovering two-agent LLM teams after one private change

This notebook runs the adopted thesis regime `thesis-recovery-v1`
(PROJECT_SPECIFICATION.md section 13). All logic is in the `recovery.thesis`
Python package; each cell below makes one call into it.

**Settings (cell 1).** `SCOPE` decides what may run:

| SCOPE | Runs | GPU |
|---|---|---|
| `cpu` | install, open or restore the study, CPU checks, report | no |
| `rehearsal` | the whole pipeline on 2+2 worlds with a scripted model, in a separate `-rehearsal` study | no |
| `development` | readiness and 16 development worlds per model, then the gate report | T4 x2 |
| `main` | freeze (needs `MAIN_AUTHORIZATION` = the gate-report ID) and main worlds until done or out of time | T4 x2 |

Run All never crosses a scope. GPU scopes need your explicit authorization.

**Every session:** settings and source -> install -> open (restores the newest
checkpoint automatically) -> CPU checks -> development -> freeze -> main -> report -> finish.
Completed work is never repeated; a rerun continues where the study stopped.

**Durability.** Raw replies are saved before their effects; a checkpoint is written
every 20 minutes and after every cell. For an off-session copy either set
`CHECKPOINT_REPO` (private Hugging Face dataset; add your write token as the Kaggle
secret `HF_TOKEN`), or use *Save Version -> Save & Run All* so Kaggle keeps
`/kaggle/working`, or download the newest checkpoint from cell 9. For the next
session attach the previous version's output (or rely on the mirror).

**Kaggle settings:** Internet on; accelerator GPU T4 x2 for GPU scopes; after the
first run pin the notebook environment to its original image.
"""

SETTINGS = f'''# 1. Settings and source (edit, then Run All; use Save & Run All for main sessions)
SOURCE_COMMIT = "PUT-THE-FULL-40-CHARACTER-COMMIT-HERE"
STUDY_ID = "thesis-recovery-v1"
SCOPE = "cpu"                # "cpu" | "rehearsal" | "development" | "main"
START_NEW_STUDY = False      # True only for the very first run of STUDY_ID (or of its rehearsal)
MAIN_AUTHORIZATION = ""      # paste the development gate-report ID (dev-...) to authorize main
SESSION_HOURS = 11.0         # hours this session may use from now; a fresh GPU session allows 12
CHECKPOINT_REPO = ""         # optional private HF dataset, e.g. "your-name/thesis-checkpoints"

import io, pathlib, sys, tarfile, urllib.request, zipfile
SRC = pathlib.Path("/kaggle/temp/thesis") / f"src-{{SOURCE_COMMIT[:12]}}"
if not (SRC / ".source-commit").exists():
    SRC.mkdir(parents=True, exist_ok=True)
    packets = sorted(pathlib.Path("/kaggle/input").rglob(f"thesis-source-{{SOURCE_COMMIT[:12]}}.zip"))
    if packets:  # fallback: source packet attached as a private dataset
        with zipfile.ZipFile(packets[0]) as packet:
            packet.extractall(SRC)
    else:
        url = f"https://codeload.github.com/{REPOSITORY}/tar.gz/{{SOURCE_COMMIT}}"
        print("Downloading source", SOURCE_COMMIT[:12], "from GitHub ...", flush=True)
        data = urllib.request.urlopen(url, timeout=300).read()
        with tarfile.open(fileobj=io.BytesIO(data), mode="r:gz") as tar:
            assert tar.pax_headers.get("comment") == SOURCE_COMMIT, "GitHub archive is not SOURCE_COMMIT"
            keep = [m for m in tar.getmembers() if "/" in m.name
                    and m.name.split("/", 1)[1].split("/")[0] in ("recovery", "configs", "pyproject.toml")]
            for member in keep:
                member.name = member.name.split("/", 1)[1]
            tar.extractall(SRC, members=keep, filter="data")
        (SRC / ".source-commit").write_text(SOURCE_COMMIT)
sys.path.insert(0, str(SRC))
from recovery.thesis import notebook as nb
nb.start(source_commit=SOURCE_COMMIT, study=STUDY_ID, scope=SCOPE, session_hours=SESSION_HOURS,
         start_new_study=START_NEW_STUDY, main_authorization=MAIN_AUTHORIZATION,
         checkpoint_repo=CHECKPOINT_REPO, source_root=SRC)'''

CELLS = [
    ("## 2. Install the pinned environment\nHash-pinned packages into a scratch virtual environment (about 3 minutes; reused within the session).",
     "nb.install()"),
    ("## 3. Open the study\nRestores the newest checkpoint from attached inputs or the mirror, reopens a local study, or creates it on the very first run.",
     "nb.open_study()"),
    ("## 4. CPU checks\nWorld manifest, input separation, protocol, analysis and checkpoint checks, and the token-capacity proof (tokenizer files only).",
     "nb.cpu_checks()"),
    ("## 5. Development (GPU)\nReadiness, then 16 development worlds per model. Prints the gate report and its ID.",
     "nb.develop()"),
    ("## 6. Freeze\nOnly with `SCOPE = \"main\"` and `MAIN_AUTHORIZATION` equal to the gate-report ID.",
     "nb.freeze()"),
    ("## 7. Main (GPU)\nContinues the frozen main worlds until complete or until the session cutoff. Outcomes stay hidden until main is complete.",
     "nb.main()"),
    ("## 8. Report\nRebuilt from the canonical store only.",
     "nb.report()"),
    ("## 9. Save and finish\nFinal checkpoint, mirror upload and download links. Then stop the Kaggle session to release the GPU.",
     "nb.finish()"),
    ("## Optional: inspect one episode\nUncomment to print exact requests and replies.",
     '# nb.show(model="qwen", world="main-000", cell="RV")'),
]


def cell(kind, text):
    lines = text.split("\n")
    source = [line + "\n" for line in lines[:-1]] + [lines[-1]]
    if kind == "markdown":
        return dict(cell_type="markdown", metadata={}, source=source)
    return dict(cell_type="code", metadata={}, execution_count=None, outputs=[], source=source)


def build():
    cells = [cell("markdown", INTRO), cell("code", SETTINGS)]
    for markdown, code in CELLS:
        cells += [cell("markdown", markdown), cell("code", code)]
    return dict(cells=cells, metadata=dict(kernelspec=dict(display_name="Python 3", language="python", name="python3"),
                                           language_info=dict(name="python")), nbformat=4, nbformat_minor=5)


def main():
    path = ROOT / "notebooks" / "thesis_kaggle.ipynb"
    path.write_text(json.dumps(build(), indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(path)


if __name__ == "__main__":
    main()
