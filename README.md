# Recovering Distributed LLM Teams After Information Changes

**Endrit Hasani** | Faculty of Computer Science & Engineering, Ss. Cyril and Methodius University in Skopje

Mentors: Prof. Sonja Gievska, Ph.D.; Martina Toshevska, M.Sc.

**[Read the final report (PDF)](report/recovering-distributed-llm-teams.pdf)** for the complete methodology, results, discussion and references.

## Study overview

This study examines how a team of language-model agents recovers when information changes. Two agents have private lists of integers and collaborate to find the global maximum. The largest record is then replaced with a lower value. Two independent continuations either **retain** or **clear** the previous visible conversation. Success requires both agents to submit the correct revised maximum.

The final assisted experiment used Qwen3.5-9B and completed **20 paired main trials**. Retaining history succeeded in **2/20 trials (10%)**, while clearing it succeeded in **3/20 (15%)**. The clear-minus-retain difference was +5 percentage points, with an exploratory 95% bootstrap interval of -15 to +25 points. These results do not establish a generally preferable history policy.

The central finding is that **improved initial collaboration and more compliant communication did not produce reliable recovery after information changed**. Improvements relative to the preliminary experiment are descriptive: different inputs and several methodological changes prevent attributing them to assistance alone.

## Main study materials

| Material | Where to find it |
|---|---|
| Executed notebook | [executed-notebook.ipynb](experiments/assisted-experiment/executed-notebook.ipynb), including saved outputs |
| Kaggle experiment code | [Python scripts](scripts/assisted-experiment/recovery/i01/) and [frozen configuration](scripts/assisted-experiment/configs/), copied from the recorded checkpoint |
| Complete downloaded results | [Original Kaggle ZIP](experiments/assisted-experiment/kaggle-results.zip), including the databases, raw records, logs and source snapshot |
| Browsable results | [Tables, figures and conversations](results/assisted-experiment/) and [all main outcomes](results/assisted-experiment-main-outcomes.csv) |

The executed notebooks and Kaggle downloads are preserved unchanged. The preliminary experiment's [notebook and download](experiments/preliminary-experiment/), [source code](scripts/preliminary-experiment/) and [results](results/preliminary-experiment/) are retained separately for the comparison discussed in the report.
