"""
Sensor Data Preprocessing — Functional Utilities

A common step in ML pipelines is cleaning and transforming raw time-series
data before it reaches a model. In this problem you will implement a small
library of higher-order utility functions and use them to build a sensor
data preprocessing pipeline.

The four functions below are general-purpose; they know nothing about sensors.
The __main__ block at the bottom wires them together for a concrete task:
cleaning a stream of noisy float readings from a temperature sensor.

DO NOT MODIFY THE FUNCTION SIGNATURES.
"""

import random

# ---------------------------------------------------------------------------
# 1. compose
# ---------------------------------------------------------------------------


def compose(*fns):
    """
    Returns a new function that applies each function in *fns right-to-left
    to a single argument. That is, compose(f, g, h)(x) == f(g(h(x))).

    Arguments:
        *fns -- one or more callables, each accepting a single argument

    Returns:
        callable -- a new function that is the composition of the inputs

    Raises:
        TypeError  -- if any element of fns is not callable
        ValueError -- if no functions are provided

    Example:
        >>> double = lambda x: x * 2
        >>> add_one = lambda x: x + 1
        >>> f = compose(double, add_one)   # f(x) = 2 * (x + 1)
        >>> f(3)
        8

    (_Hint: Python's built-in `reversed()` works on any sequence, including
    a tuple like `fns`._)
    """

    # ------ SOLUTION GOES HERE!  ------
    if not fns:
        raise ValueError("no functions")
    fns = list(fns)
    not_fns = [x for x in fns if not callable(x)]
    # filter(callable, fns)
    if any(not_fns):
        raise TypeError("not all callable")
    fns = reversed(fns)

    def composed(x):
        for f in fns:
            x = f(x)
        return x

    return composed


# ---------------------------------------------------------------------------
# 2. pipeline
# ---------------------------------------------------------------------------


def pipeline(data, *transforms):
    """
    Passes data through a sequence of transformation stages left-to-right.

    Each stage is a tuple of (fn, kwargs) where fn accepts the current value
    as its first positional argument and kwargs is a dict of keyword arguments
    forwarded to fn on that call.

    Arguments:
        data       -- the initial value to transform
        *transforms -- one or more (callable, dict) pairs

    Returns:
        the final transformed value after all stages have been applied

    Raises:
        TypeError -- if any stage is not a (callable, dict) pair

    Example:
        >>> def scale(x, factor=1.0): return [v * factor for v in x]
        >>> def offset(x, amount=0.0): return [v + amount for v in x]
        >>> pipeline([1.0, 2.0], (scale, {"factor": 2.0}), (offset, {"amount": -1.0}))
        [1.0, 3.0]
    """

    # ------ SOLUTION GOES HERE!  ------
    istuple = lambda x: not (callable(x[0]) and isinstance(x[1], dict))
    if any(filter(istuple, transforms)):
        raise TypeError("tuple err")
    for fn, d in transforms:
        data = fn(data, **d)
    return data


# ---------------------------------------------------------------------------
# 3. apply_if
# ---------------------------------------------------------------------------


def apply_if(data, predicate, transform, default=None):
    """
    Applies transform to each element of data that satisfies predicate,
    substituting default for elements that do not.

    Arguments:
        data      -- an iterable of values
        predicate -- a callable(x) -> bool that decides whether to transform x
        transform -- a callable(x) -> value applied when predicate is True
        default   -- the value substituted when predicate is False (default None)

    Returns:
        list -- a list the same length as data where each element is either
                transform(x) or default

    Raises:
        TypeError -- if predicate or transform are not callable

    Example:
        >>> apply_if([0.001, 0.5, 0.002, 0.8], lambda x: x > 0.01,
        ...          lambda x: round(x, 2), default=0.0)
        [0.0, 0.5, 0.0, 0.8]
    """

    # ------ SOLUTION GOES HERE!  ------
    if not callable(predicate) or not callable(transform):
        raise TypeError("fucked up")

    def apply(d):
        if predicate(d):
            return transform(d)
        else:
            return default

    return list(map(apply, data))


# ---------------------------------------------------------------------------
# 4. window_filter
# ---------------------------------------------------------------------------


def window_filter(data, size, predicate, default=None):
    """
    Slides a window of length `size` across data one step at a time.
    For each window, returns the window (as a list) if predicate(window)
    is True, otherwise returns default.

    A window is a contiguous subsequence of `size` consecutive elements.
    The first window is data[0:size], the second data[1:size+1], and so on.
    The number of windows is len(data) - size + 1.

    Arguments:
        data      -- a sequence of values
        size      -- the number of consecutive elements per window (int >= 1)
        predicate -- a callable(window: list) -> bool
        default   -- value returned in place of a window that fails the
                     predicate (default None)

    Returns:
        list -- one entry per window position: either the window list or default

    Raises:
        ValueError -- if size < 1 or size > len(data)
        TypeError  -- if predicate is not callable

    Example:
        >>> data = [0.2, 0.4, 0.3, 0.5, 1.6]
        >>> window_filter(data, 3, lambda w: max(w) - min(w) <= 1.0)
        [[0.2, 0.4, 0.3], [0.4, 0.3, 0.5], None]
        # window[0]: [0.2, 0.4, 0.3]  range=0.2  → OK
        # window[1]: [0.4, 0.3, 0.5]  range=0.2  → OK
        # window[2]: [0.3, 0.5, 1.6]  range=1.3  → None  (fails predicate)
    """

    # ------ SOLUTION GOES HERE!  ------
    if size < 1 or size > len(data):
        raise ValueError("size error")
    if not callable(predicate):
        raise TypeError("error")
    pos: int = 0
    l: list = []
    while len(data) - 1 >= pos + size:
        t = data[pos : pos + size]
        if predicate(t):
            l.append(t)
        else:
            l.append(default)
        pos += 1
    return l


# ---------------------------------------------------------------------------
# Preprocessing helpers  (provided — do not modify)
# ---------------------------------------------------------------------------


def _center(readings, mean=0.0):
    """Subtracts mean from every reading."""
    return [x - mean for x in readings]


def _scale(readings, factor=1.0):
    """Multiplies every reading by factor."""
    return [x * factor for x in readings]


def _clip(readings, lo=-1.0, hi=1.0):
    """Clamps every reading to [lo, hi]."""
    return [max(lo, min(hi, x)) for x in readings]


def _smooth(readings, window_size=3):
    """Replaces each reading with the mean of its surrounding window."""
    half = window_size // 2
    out = []
    for i in range(len(readings)):
        lo = max(0, i - half)
        hi = min(len(readings), i + half + 1)
        out.append(sum(readings[lo:hi]) / (hi - lo))
    return out


def _round_readings(readings, decimals=3):
    """Rounds every reading to `decimals` decimal places."""
    return [round(x, decimals) for x in readings]


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    random.seed(42)

    # Simulate 20 raw temperature sensor readings (Celsius, with noise).
    raw = [
        20.0 + random.gauss(0, 0.5) + random.choice([0] * 9 + [5]) for _ in range(20)
    ]

    print("=== Raw readings ===")
    print([round(x, 3) for x in raw])

    # --- Step 1: compose a per-reading normalizer ----------------------------
    # Build a single function that: subtracts the mean, scales to [-1, 1],
    # then clips. Because compose applies right-to-left, pass the functions
    # in reverse application order: the last argument is applied first.
    sample_mean = sum(raw) / len(raw)
    sample_range = max(raw) - min(raw)

    normalize = compose(
        lambda readings: _clip(readings, lo=-1.0, hi=1.0),
        lambda readings: _scale(readings, factor=2.0 / sample_range),
        lambda readings: _center(readings, mean=sample_mean),
    )

    normalized = normalize(raw)
    print("\n=== After compose: centered → scaled → clipped ===")
    print([round(x, 3) for x in normalized])

    # --- Step 2: pipeline of named stages ------------------------------------
    # Each stage is (fn, kwargs). Stages run left-to-right.
    preprocessed = pipeline(
        normalized,
        (_smooth, {"window_size": 3}),
        (_round_readings, {"decimals": 3}),
    )

    print("\n=== After pipeline: smoothed → rounded ===")
    print(preprocessed)

    # --- Step 3: apply_if — suppress near-zero noise -------------------------
    # Any reading with absolute value <= 0.05 is likely noise; zero it out.
    denoised = apply_if(
        preprocessed,
        lambda x: abs(x) > 0.05,
        lambda x: x,
        default=0.0,
    )

    print("\n=== After apply_if: noise floor zeroed ===")
    print(denoised)

    # --- Step 4: window_filter — flag glitch windows -------------------------
    # A window is suspicious if its peak-to-peak range exceeds 0.5.
    # Glitch windows are replaced with None for downstream handling.
    glitch_threshold = 0.5
    filtered = window_filter(
        denoised,
        size=3,
        predicate=lambda w: max(w) - min(w) <= glitch_threshold,
        default=None,
    )

    print("\n=== After window_filter: glitch windows replaced with None ===")
    for i, window in enumerate(filtered):
        status = "OK  " if window is not None else "GLITCH"
        print(f"  window[{i:02d}]: {status}  {window}")
