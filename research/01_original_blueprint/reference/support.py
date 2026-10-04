"""Finite justification algebra, independent exhaustive oracle, and scope policies.

Recursive labels are complete for the unate Boolean formulas used in this study.
An atom cannot occur with both polarities; unknown evidence is not false.
"""
from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations, product
from typing import Mapping, Iterable

from .contracts import Expr

Proof = frozenset[str]
Family = frozenset[Proof]


@dataclass(frozen=True)
class Obs:
    evidence_id: str
    value: bool


def atom(name: str) -> Expr:
    return Expr(op="atom", name=name)


def AND(*xs: Expr) -> Expr:
    return Expr(op="and", children=xs)


def OR(*xs: Expr) -> Expr:
    return Expr(op="or", children=xs)


def NOT(x: Expr) -> Expr:
    return Expr(op="not", children=(x,))


def names(expr: Expr) -> set[str]:
    return {expr.name} if expr.op == "atom" else set().union(*(names(c) for c in expr.children))


def ensure_unate(expr: Expr, sign: bool = True, seen=None):
    seen = {} if seen is None else seen
    if expr.op == "atom":
        if expr.name in seen and seen[expr.name] != sign:
            raise ValueError("Mixed-polarity atom is outside the generator contract")
        seen[expr.name] = sign
    else:
        for child in expr.children:
            ensure_unate(child, not sign if expr.op == "not" else sign, seen)


def truth(expr: Expr, assignment: Mapping[str, bool]) -> bool:
    if expr.op == "atom":
        return assignment[expr.name]
    if expr.op == "const":
        return expr.constant
    if expr.op == "not":
        return not truth(expr.children[0], assignment)
    vals = [truth(c, assignment) for c in expr.children]
    return all(vals) if expr.op == "and" else any(vals)


def antichain(sets: Iterable[Iterable[str]]) -> Family:
    unique = {frozenset(s) for s in sets}
    return frozenset(s for s in unique if not any(t < s for t in unique))


def alternatives(families: Iterable[Family]) -> Family:
    return antichain(s for f in families for s in f)


def conjunction(families: Iterable[Family]) -> Family:
    out: Family = frozenset({frozenset()})
    for f in families:
        out = antichain(a | b for a in out for b in f)
    return out


def labels(expr: Expr, wanted: bool, observed: Mapping[str, Obs]) -> Family:
    ensure_unate(expr)
    ids = [o.evidence_id for o in observed.values()]
    if len(ids) != len(set(ids)):
        raise ValueError("One evidence version per atom; duplicate IDs are forbidden")

    def visit(e, v):
        if e.op == "atom":
            ob = observed.get(e.name)
            return frozenset({frozenset({ob.evidence_id})}) if ob and ob.value == v else frozenset()
        if e.op == "const":
            return frozenset({frozenset()}) if e.constant == v else frozenset()
        if e.op == "not":
            return visit(e.children[0], not v)
        sub = [visit(c, v) for c in e.children]
        require_all = (e.op == "and" and v) or (e.op == "or" and not v)
        return conjunction(sub) if require_all else alternatives(sub)

    return visit(expr, wanted)


def entails(expr: Expr, wanted: bool, partial: Mapping[str, bool]) -> bool:
    unknown = sorted(names(expr) - partial.keys())
    for bits in product((False, True), repeat=len(unknown)):
        assignment = dict(partial)
        assignment.update(zip(unknown, bits))
        if truth(expr, assignment) != wanted:
            return False
    return True


def exhaustive_labels(expr: Expr, wanted: bool, observed: Mapping[str, Obs]) -> Family:
    """Independent enumeration of subsets and ALL compatible completions."""
    items = sorted((k, o) for k, o in observed.items() if k in names(expr))
    proofs = []
    for n in range(len(items) + 1):
        for subset in combinations(items, n):
            ids = frozenset(o.evidence_id for _, o in subset)
            if any(p <= ids for p in proofs):
                continue
            if entails(expr, wanted, {k: o.value for k, o in subset}):
                proofs.append(ids)
    return frozenset(proofs)


def survives(family: Family, current_ids: set[str]) -> bool:
    return any(proof <= current_ids for proof in family)


def descendants(seeds: set[str], edges: Iterable[tuple[str, str]]) -> set[str]:
    children = {}
    for a, b in edges:
        children.setdefault(a, set()).add(b)
    reached, todo = set(seeds), list(seeds)
    while todo:
        for nxt in children.get(todo.pop(), ()):
            if nxt not in reached:
                reached.add(nxt)
                todo.append(nxt)
    return reached


def estimated_mask(active: set[str], corrected: set[str], edges,
                   estimates: Mapping[str, Family | None], current_ids: set[str]) -> set[str]:
    """Missing labels fall back to exposure withdrawal; empty proof is disallowed."""
    candidates = active & descendants(corrected, edges)
    return {n for n in candidates if not any(p and p <= current_ids for p in (estimates.get(n) or ())) }


def exact_mask(assertions: Mapping[str, tuple[Expr, bool]],
               observed_by_node: Mapping[str, Mapping[str, Obs]]) -> set[str]:
    return {n for n, (expr, wanted) in assertions.items()
            if not labels(expr, wanted, observed_by_node[n])}


def serialize(family: Family) -> list[list[str]]:
    return [sorted(p) for p in sorted(family, key=lambda x: (len(x), tuple(sorted(x))))]
