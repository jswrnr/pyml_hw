import numpy as np
import pytest
from a_movement import (
    batch_flatten,
    split_into_patches,
    channels_first_to_last,
    interleave_rows,
    tile_vector,
)

# ---------------------------------------------------------------------------
# batch_flatten
# ---------------------------------------------------------------------------


def test_batch_flatten_3d():
    X = np.arange(24).reshape(2, 3, 4)

    result = batch_flatten(X)

    assert result.shape == (2, 12)


def test_batch_flatten_4d():
    X = np.zeros((4, 3, 8, 8))

    assert batch_flatten(X).shape == (4, 192)


def test_batch_flatten_2d():
    X = np.arange(12).reshape(3, 4)

    result = batch_flatten(X)

    assert result.shape == (3, 4)


def test_batch_flatten_values():
    X = np.arange(24).reshape(2, 3, 4)

    np.testing.assert_array_equal(batch_flatten(X), X.reshape(2, 12))


def test_batch_flatten_raises_1d():
    with pytest.raises(ValueError):
        batch_flatten(np.arange(4))


# ---------------------------------------------------------------------------
# split_into_patches
# ---------------------------------------------------------------------------


def test_split_into_patches_shape():
    X = np.arange(24).reshape(4, 6)

    result = split_into_patches(X, 2, 3)

    assert result.shape == (2, 2, 2, 3)


def test_split_into_patches_top_left():
    X = np.arange(16).reshape(4, 4)

    np.testing.assert_array_equal(
        split_into_patches(X, 2, 2)[0, 0],
        np.array([[0, 1], [4, 5]]),
    )


def test_split_into_patches_top_right():
    X = np.arange(16).reshape(4, 4)

    np.testing.assert_array_equal(
        split_into_patches(X, 2, 2)[0, 1],
        np.array([[2, 3], [6, 7]]),
    )


def test_split_into_patches_bottom_left():
    X = np.arange(16).reshape(4, 4)

    np.testing.assert_array_equal(
        split_into_patches(X, 2, 2)[1, 0],
        np.array([[8, 9], [12, 13]]),
    )


def test_split_into_patches_reconstructable():
    X = np.arange(48).reshape(6, 8)
    patches = split_into_patches(X, 2, 4)

    reconstructed = patches.transpose(0, 2, 1, 3).reshape(X.shape)

    np.testing.assert_array_equal(reconstructed, X)


def test_split_into_patches_raises_non_divisible():
    with pytest.raises(ValueError):
        split_into_patches(np.zeros((5, 4)), 2, 2)

    with pytest.raises(ValueError):
        split_into_patches(np.zeros((4, 5)), 2, 2)


def test_split_into_patches_raises_non_2d():
    with pytest.raises(ValueError):
        split_into_patches(np.zeros((2, 4, 4)), 2, 2)


# ---------------------------------------------------------------------------
# channels_first_to_last
# ---------------------------------------------------------------------------


def test_channels_first_to_last_shape():
    X = np.zeros((2, 3, 4, 5))

    assert channels_first_to_last(X).shape == (2, 4, 5, 3)


def test_channels_first_to_last_values():
    X = np.arange(24).reshape(1, 3, 2, 4)

    expected = X.transpose(0, 2, 3, 1)

    np.testing.assert_array_equal(channels_first_to_last(X), expected)


def test_channels_first_to_last_raises():
    with pytest.raises(ValueError):
        channels_first_to_last(np.zeros((3, 4, 5)))

    with pytest.raises(ValueError):
        channels_first_to_last(np.zeros((1, 2, 3, 4, 5)))


# ---------------------------------------------------------------------------
# interleave_rows
# ---------------------------------------------------------------------------


def test_interleave_rows_shape():
    A = np.zeros((3, 2))
    B = np.ones((3, 2))

    assert interleave_rows(A, B).shape == (6, 2)


def test_interleave_rows_order():
    A = np.array([[1, 2], [3, 4]])
    B = np.array([[10, 20], [30, 40]])
    expected = np.array([[1, 2], [10, 20], [3, 4], [30, 40]])

    np.testing.assert_array_equal(interleave_rows(A, B), expected)


def test_interleave_rows_raises_shape_mismatch():
    with pytest.raises(ValueError):
        interleave_rows(np.zeros((2, 3)), np.zeros((3, 2)))

    with pytest.raises(ValueError):
        interleave_rows(np.zeros(3), np.zeros(3))


# ---------------------------------------------------------------------------
# tile_vector
# ---------------------------------------------------------------------------


def test_tile_vector_shape():
    assert tile_vector(np.array([1, 2, 3]), 4).shape == (4, 3)


def test_tile_vector_values():
    vector = np.array([1, 2, 3])

    np.testing.assert_array_equal(
        tile_vector(vector, 4),
        np.array([[1, 2, 3], [1, 2, 3], [1, 2, 3], [1, 2, 3]]),
    )


def test_tile_vector_raises_non_1d():
    with pytest.raises(ValueError):
        tile_vector(np.zeros((2, 2)), 3)


def test_tile_vector_raises_n_zero():
    with pytest.raises(ValueError):
        tile_vector(np.array([1, 2]), 0)
