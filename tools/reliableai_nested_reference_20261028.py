"""Authored exact witnesses; never import or execute acquired software."""
from fractions import Fraction


def endpoint_keys(edges, inspected=False):
    result = set()
    for u, v, left, right in edges:
        if left == 'arrow':
            result.add((u, v))
        if right == 'arrow':
            result.add((v, v) if inspected else (v, u))
    return result


def score(predicted, truth):
    return Fraction(2 * len(predicted & truth), len(predicted) + len(truth)) if predicted or truth else Fraction(1)


def rising(a, n):
    out = Fraction(1)
    for i in range(n):
        out *= a + i
    return out


def binary_marginal(alpha, counts):
    return rising(alpha / 2, counts[0]) * rising(alpha / 2, counts[1]) / rising(alpha, sum(counts))


def calculate():
    truth = [('A', 'B', 'tail', 'arrow')]
    wrong_neighbor = [('C', 'B', 'tail', 'arrow')]
    reversed_storage = [('B', 'A', 'arrow', 'tail')]
    star = [('A', 'C', 'tail', 'arrow'), ('B', 'C', 'tail', 'arrow')]
    collision = score(endpoint_keys(wrong_neighbor, True), endpoint_keys(truth, True))
    corrected = score(endpoint_keys(wrong_neighbor), endpoint_keys(truth))
    reversed_score = score(endpoint_keys(reversed_storage, True), endpoint_keys(truth, True))
    reversed_corrected = score(endpoint_keys(reversed_storage), endpoint_keys(truth))
    assert (collision, corrected, reversed_score, reversed_corrected) == (1, 0, 0, 1)
    assert len(endpoint_keys(star, True)) == 1 and len(endpoint_keys(star)) == 2
    a2, a10 = binary_marginal(Fraction(2), (1, 1)), binary_marginal(Fraction(10), (1, 1))
    assert a2 == Fraction(1, 6) and a10 == Fraction(5, 22)
    def comparator(a, b):
        return 1 if a < b else -1
    assert comparator(3, 3) == -1 and comparator(2, 3) == 1 and comparator(3, 2) == -1
    return dict(
        kind='authored_exact_logical_witnesses_not_native_execution',
        endpoint_neighbor_collision=dict(inspected_arrowhead_f1=str(collision), neighbor_preserving_f1=str(corrected), skeleton_match=False),
        endpoint_storage_reversal=dict(inspected_arrowhead_f1=str(reversed_score), neighbor_preserving_f1=str(reversed_corrected), same_semantic_edge=True),
        incoming_star=dict(inspected_keys=len(endpoint_keys(star, True)), neighbor_preserving_keys=len(endpoint_keys(star))),
        score_prior=dict(binary_counts=[1, 1], alpha_2_marginal=str(a2), alpha_10_marginal=str(a10), constructor_zero_maps_to=10, scores='Natural logarithms of these positive marginal factors; no causal interpretation.'),
        comparator=dict(equal_score_result=comparator(3, 3), required_equality_result=0, empirical_tree_behavior='not executed'),
        native_execution=False, bank_qualification=False)


if __name__ == '__main__':
    import json
    print(json.dumps(calculate(), indent=2))
