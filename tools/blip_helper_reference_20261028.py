"""Exact proposal-owned witnesses; never imports or executes acquired Java."""
from fractions import Fraction


def rising(x, n):
    value = Fraction(1)
    for i in range(n):
        value *= x + i
    return value


def marginal(alpha, counts, denominator_count):
    value = Fraction(1)
    for count in counts:
        value *= rising(Fraction(alpha, len(counts)), count)
    return value / rising(Fraction(alpha), denominator_count)


def merge_count(left, right):
    i = j = count = 0
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            i += 1
        elif right[j] < left[i]:
            j += 1
        else:
            count += 1
            i += 1
            j += 1
    return count


def java_int_product(values):
    product = 1
    for value in values:
        product = ((product * value + 2**31) % 2**32) - 2**31
    return product


def calculate():
    complete = marginal(2, [1, 1], 2)
    mismatched = marginal(2, [1, 1], 3)
    assert complete == Fraction(1, 6) and mismatched == Fraction(1, 24)
    assert mismatched / complete == Fraction(1, 4)
    unsorted = merge_count([2, 0], [0, 2])
    sorted_count = merge_count([0, 2], [0, 2])
    assert unsorted == 1 and sorted_count == 2
    assert java_int_product([65536, 65536]) == 0
    assert java_int_product([46341, 46341]) < 0
    # In the inspected branches neither nextLine nor the reader position changes.
    # Record an abstract state transition, not a native thread or timeout result.
    stalling = [dict(line='', read_missing=False), dict(line='0,?', read_missing=True)]
    transitions = [dict(before=x, after=dict(x), advances=False) for x in stalling]
    tolerance = Fraction(1, 2**5)
    assert Fraction(1, 100) < tolerance and not (tolerance < tolerance)
    default_dat = dict(route='dat', read_missing=False, row='0,?', disposition='drop_entire_row_and_advance')
    default_data = dict(route='data', read_missing=False, row='0,?', disposition='retain_row_with_separate_missing_index')
    return dict(status='pass', kind='independent exact arithmetic and inspected control-flow witnesses',
        missing_target=dict(alpha=2, observed_counts=[1, 1], retained_rows=3,
                            complete_case_factor=str(complete), inspected_total_denominator_factor=str(mismatched),
                            ratio=str(mismatched / complete), interpretation='Illustrative retained target-missing row; no native likelihood or statistical calibration claim.'),
        intersection=dict(unsorted_left=[2, 0], right=[0, 2], two_pointer_count=unsorted,
                          sorted_count=sorted_count, required='Strictly ordered unique nonnegative row identities.'),
        cardinality=dict(exact_product_65536_squared=65536**2, java_int_product=0,
                         product_46341_squared=46341**2, java_int_product_negative=java_int_product([46341, 46341]),
                         required='Check multiplication before array allocation and prior division; also bound short-coded states.'),
        reader_progress=transitions, default_missingness_routes=[default_dat, default_data],
        comparison=dict(default_absolute_tolerance=str(tolerance), small_error_accepted=True,
                        error_equal_to_tolerance_rejected=True, returned_boolean_requires_assertion=True),
        native_execution=False, bank_data=False)


if __name__ == '__main__':
    import json
    print(json.dumps(calculate(), indent=2))
