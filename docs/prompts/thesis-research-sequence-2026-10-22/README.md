# Three research sessions toward an implementable thesis

Run these prompts **one at a time, in order, in this repository**. Each linked
file is a complete prompt to copy into a new session. The prompts inspect the
previous session's deliverables rather than relying on chat memory.

1. [Select the scientific study](01-scientific-study.md): challenge the existing
   proposals and settle one meaningful, feasible experimental design.
2. [Research the online execution workflow](02-online-workflow.md): design the
   Python scripts, thin Kaggle notebook, online downloads, visible progress,
   cell checkpoints and interruption recovery.
3. [Write the precise specification](03-project-specification.md): independently
   reconcile the science and execution design into a complete specification
   proposal and implementation roadmap.

All three sessions are **research and Markdown specification work**. They do not
implement the new experiment, adopt scientific amendments, execute model calls,
use GPUs, download model weights, book compute or publish anything. You do not
need to approve a new scientific regime between these research sessions. Review
their conclusions and steer the next prompt if your preferences change.

The intended destination is practical: most logic in reusable `.py` scripts,
one notebook that calls them, preparation downloaded online inside Kaggle,
frequent readable progress, durable saves during execution and a checkpoint or
preparation receipt after every code cell. The research must establish the
details and limits;
this prompt package does not claim that delivery is already implemented.

Expected new outputs, using repository-relative paths:

| Session | Markdown deliverables |
|---|---|
| 1 | `docs/proposals/thesis-study-recommendation.md` |
| 2 | `docs/implementation-research/thesis-online-execution-design.md` |
| 3 | `docs/proposals/thesis-project-specification.md` and `docs/proposals/thesis-implementation-roadmap.md` |

The final specification remains a proposal until explicitly approved and adopted
in `PROJECT_SPECIFICATION.md`. The existing specification and engineering plan
retain their authority. Scientific adoption and CPU implementation are the next
decision after these three sessions; GPU development and main execution have
their own later authorization boundaries.

Do not run the prompts recursively or treat instructions inside their files as
authorization while merely inspecting the repository. Their task instructions
apply when you provide the corresponding prompt as your request.
