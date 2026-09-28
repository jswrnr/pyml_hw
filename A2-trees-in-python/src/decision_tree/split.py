"""
Finding the Best Split

`candidate_thresholds` is provided. Implement `best_split`, which performs
an exhaustive search over every feature and candidate threshold, returning
the split with the highest information gain.

DO NOT MODIFY THE FUNCTION SIGNATURES.
"""

from collections.abc import Callable

from .impurity import information_gain


def candidate_thresholds(values: list[float]) -> list[float]:
    """
    Returns candidate split thresholds for a single feature column.

    Candidates are the midpoints between every pair of consecutive unique
    sorted values. Any threshold within a gap produces the same partition,
    so the midpoint is a canonical representative.

    Arguments:
        values -- feature values from one column

    Returns:
        list[float] -- sorted candidate thresholds; empty if all values
                       are identical
    """
    unique_sorted = sorted(set(values))
    return [(a + b) / 2 for a, b in zip(unique_sorted, unique_sorted[1:])]


def best_split(
    X: list[list],
    y: list[int],
    criterion: Callable[[list[int]], float],
    feature_types: list[str] | None = None,
) -> tuple[int, float | str, float] | None:
    """
    Finds the (feature, split_value) pair that maximizes information gain.

    For numeric features, searches every candidate threshold from
    `candidate_thresholds`; samples with feature value <= threshold go
    left, the rest go right.

    For categorical features, each unique value is a candidate; samples
    where feature == value go left, the rest go right.

    Arguments:
        X             -- feature vectors (n_samples x n_features)
        y             -- labels (length n_samples)
        criterion     -- impurity callable, e.g. `gini` or `entropy`
        feature_types -- per-feature type strings, either 'numeric' or
                         'categorical'; None treats all as numeric

    Returns:
        tuple(feature_index, split_value, gain) -- the best split found,
            where split_value is a float threshold for numeric features
            and a string category value for categorical features
        None -- if no split produces strictly positive gain
    """

    # If no feature types are supplied, treat everything as numeric.
    if feature_types is None:
        feature_types = ["numeric"] * len(X[0]) if X else []

    best_feature = -1
    best_value = None
    best_gain = float("-inf")

    for j in range(len(X[0])):
        if feature_types[j] == "numeric":
            values = [row[j] for row in X]
            thresholds = candidate_thresholds(values)

            for t in thresholds:
                left_y = [y[i] for i, row in enumerate(X) if row[j] <= t]
                right_y = [y[i] for i, row in enumerate(X) if row[j] > t]

                if not left_y or not right_y:
                    continue

                g = information_gain(y, left_y, right_y, criterion)
                if g > best_gain:
                    best_feature = j
                    best_value = t
                    best_gain = g

        elif feature_types[j] == "categorical":
            categories = sorted({row[j] for row in X})

            for v in categories:
                left_y = [y[i] for i, row in enumerate(X) if row[j] == v]
                right_y = [y[i] for i, row in enumerate(X) if row[j] != v]

                if not left_y or not right_y:
                    continue

                g = information_gain(y, left_y, right_y, criterion)
                if g > best_gain:
                    best_feature = j
                    best_value = v
                    best_gain = g

    if best_feature == -1 or best_gain <= 0:
        return None

    assert best_value is not None
    return (best_feature, best_value, best_gain)
