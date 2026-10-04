# Belief revision, slicing and consistent snapshots

Additional primary-source checks on 2026-09-30. These sharpen the conceptual boundaries; they do not imply a new algorithm.

## Belief revision and truth maintenance

[AGM, On the Logic of Theory Change (1985), primary-paper PDF](https://fitelson.org/piksi/piksi_22/agm.pdf). Abstract, introductory definitions and contraction/revision formulation inspected. It studies principled change to logical theories, including partial-meet constructions. Preserving as much old information as possible is therefore not a new objective. The assumptions concern logical consequence and selection among belief sets; they do not prescribe how to reconstruct opaque distributed agent execution or price tool acquisition.

[de Kleer, An Assumption-Based TMS (1986)](https://doi.org/10.1016/0004-3702(86)90080-9). Publisher abstract inspected, not full algorithm. It represents assumption environments and multiple potential solutions, so alternate-support preservation and keeping competing contexts are established.

[Morris and Nado, Representing Actions with an ATMS (AAAI 1986)](https://cdn.aaai.org/AAAI/1986/AAAI86-003.pdf). Abstract/introduction and context discussion inspected. Explicitly distinguishes inferential truth maintenance from actions/world changes and explores context merges. The fact that a fact was once valid does not mean it should be inherited into every future context. This strengthens the case for separating historical record, current source state and operational commitments.

## Program slicing

[Agrawal and Horgan, Dynamic Program Slicing (1990)](https://www.cs.purdue.edu/homes/xyzhang/fall07/Papers/p246-agrawal.pdf). Abstract, introduction and dependence-graph discussion inspected. Dynamic slices concern a particular executed program/input; static slices conservatively cover possible influence. Neither is equivalent to model-written citations. The analogy supports measuring coarse exposure versus fine reported dependencies, but does not establish that every token in an LLM context actually influenced the output.

## Snapshots

[Chandy and Lamport, Distributed Snapshots (1985)](https://lamport.azurewebsites.net/pubs/chandy.pdf). System model and recording rules inspected. A distributed state includes communication channels as well as process states; arbitrary separate snapshots can create inconsistent histories. In this project, immutable synchronous phase cuts simplify this requirement. The native SILO read-cursor mutations are precisely why copying agent text alone cannot guarantee matched branches. The research does not invent an asynchronous snapshot algorithm.

## Incremental search

[Koenig, Likhachev and Furcy, Lifelong Planning A* (2004)](https://idm-lab.org/bib/abstracts/papers/aij04.pdf). Overview, local-consistency explanation and algorithm update/termination passages inspected; formal proofs not fully rederived. Its reuse and reopening follow explicit graph-cost semantics and inconsistent search state. The current proposal cannot claim to invent revisiting previously searched regions. The unanswered implementation question is what adequate state an opaque agent can expose without such a specified search algorithm.
