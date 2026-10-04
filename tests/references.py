"""Small independent references; no imports from the production package."""


def insertion_order(values):
    result = []
    for value in values:
        i = 0
        while i < len(result) and result[i] <= value:
            i += 1
        result.insert(i, value)
    return result


def numeric_reference(task, values):
    if task == "top_k":
        return list(reversed(insertion_order(values)))[:10]
    if task == "prefix_sum":
        return [sum(values[:j + 1]) for j in range(len(values))]
    if task == "difference_array":
        # Independent coefficient-vector definition, rather than neighbor slicing.
        return [sum(value * ((k == j) - (k == j - 1))
                    for k, value in enumerate(values))
                for j in range(1, len(values))]
    if task == "distributed_sort":
        return insertion_order(values)
    raise ValueError(task)


def relaxation_distances(node_count, edges):
    """Synchronous edge relaxation, with no queue/adjacency traversal."""

    infinity = node_count + 1
    distances = [0] + [infinity] * (node_count - 1)
    for _ in range(node_count - 1):
        previous = distances[:]
        for u, v in edges:
            distances[u] = min(distances[u], previous[v] + 1)
            distances[v] = min(distances[v], previous[u] + 1)
    return {str(i): (-1 if value == infinity else value)
            for i, value in enumerate(distances)}
