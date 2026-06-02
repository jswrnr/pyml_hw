"""
RunningStats Class

Write a class called `RunningStats` that computes a running mean and
unbiased sample variance from a stream of numbers, without storing the
individual values.

This is useful in ML contexts where you may be processing data in batches
or reading from a stream too large to hold in memory — for instance,
computing dataset statistics during a single pass over a training set.

The algorithm you must use is Welford's online algorithm:

    https://en.wikipedia.org/wiki/Algorithms_for_calculating_variance#Welford's_online_algorithm

Each call to `.update(x)` incorporates a new value x into the running
statistics using the recurrences:

    n    <- n + 1
    delta  = x - mean
    mean <- mean + delta / n
    delta2 = x - mean          # note: uses the *updated* mean
    M2   <- M2 + delta * delta2

where M2 accumulates the sum of squared deviations. The unbiased sample
variance is M2 / (n - 1) for n >= 2.

Additionally, use the `@property` decorator when implementing the properties
in the requirements. For more information on the `@property` decorator, read
this blog post:

    https://www.stratascratch.com/blog/how-to-use-python-property-decorator-with-examples

--------------------------------------------------------------------------
Requirements
--------------------------------------------------------------------------

- `RunningStats()` initializes with no observations (n=0, mean=0.0, M2=0.0).

- `.update(x)` incorporates a single new value into the running statistics.
  Raises a TypeError if x is not an int or float.

- `.mean` property returns the current running mean.
  Raises a StatisticsError if no values have been added yet.

- `.variance` property returns the current unbiased sample variance (M2 / (n-1)).
  Raises a StatisticsError if fewer than two values have been added.

- `.std` property returns the square root of variance.
  Raises a StatisticsError if fewer than two values have been added.

- `.__len__` returns the number of values seen so far.

- `.__repr__` returns a string of the form:
      RunningStats(n=3, mean=2.000, std=1.000)
  using an f-string. If fewer than two values have been seen, std is
  shown as 'N/A' instead of a number. If no values have been seen, mean
  is also shown as 'N/A'.

- `.reset()` restores the object to its initial state.

DO NOT MODIFY THE FUNCTION SIGNATURES OR THE IMPORTS.
"""

import math
from statistics import StatisticsError


class RunningStats:
    # ------ SOLUTION GOES HERE!  ------
    def __init__(self, n: int = 0, mean: float = 0.0, m2: float = 0.0):
        self._n = n
        self._mean = mean
        self._m2 = m2

    @property
    def mean(self):
        if self._n == 0:
            raise StatisticsError("can't get mean while n is 0")
        return self._mean

    @property
    def variance(self):
        if self._n < 2:
            raise StatisticsError("can't get var while n is less than 2")
        return self._m2 / (self._n - 1)

    @property
    def std(self):
        if self._n < 2:
            raise StatisticsError("can't get std while n is less than 2")
        return math.sqrt(self.variance)

    def update(self, x: int | float):
        if not (type(x) is int or type(x) is float):
            raise TypeError("update needs int or float")
        self._n += 1
        diff_old = x - self._mean
        self._mean = self._mean + diff_old / self._n
        self._m2 = self._m2 + (diff_old * (x - self._mean))

    def __len__(self) -> int:
        return self._n

    def __repr__(self) -> str:
        std = f"{self.std:.3f}" if self._n > 1 else "N/A"
        mean = f"{self.mean:.3f}" if self._n > 0 else "N/A"
        return f"RunningStats(n={self._n}, mean={mean}, std={std})"

    def reset(self):
        self._n = 0
        self._mean = 0
        self._m2 = 0


if __name__ == "__main__":
    import random

    random.seed(0)
    stream = [random.gauss(mu=10.0, sigma=2.0) for _ in range(1000)]

    rs = RunningStats()
    print("Before any updates:", rs)

    for x in stream:
        rs.update(x)

    print("After 1000 updates:", rs)
    print("  n        :", len(rs))
    print(f"  mean     : {rs.mean:.4f}")
    print(f"  variance : {rs.variance:.4f}")
    print(f"  std      : {rs.std:.4f}")

    rs.reset()
    print("After reset:", rs)
