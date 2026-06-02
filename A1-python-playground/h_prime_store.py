"""
`PrimeStore` Class

Write a python class called `PrimeStore` that can return an iterator which
outputs prime numbers ad infinitum starting from 2.

- `PrimeStore` has a **class variable** that holds previously generated primes.
  It is initialized with only the first prime `2`. Because it is a class
  variable, all `PrimeStore` instances share the same list.

- There should be a method which is able to generate primes by iterating
  through natural numbers and testing each one to see if it is a prime number.
  This method should be as efficient as possible. Be sure to store results to
  the internal class variable `_primes`. (_Hint: Use the @classmethod decorator
  (https://docs.python.org/3/library/functions.html#classmethod) and consider
  even numbers. Consider splitting this into two classmethods — one that tests
  whether a number is prime and one that generates the next prime; it is fine
  for them to call each other._)

- `PrimeStore` should be iterable, but itself should not be an iterator. It
  should be feasible to iterate through `PrimeStore` consecutively, with each
  instance of iteration having its own index. It should only halt once a
  `break` statement is reached. Generate new primes if need be.

- `__getitem__` is implemented such that, given it has argument `i` it will
  return the i-th prime, with 2 being the 0th prime. If the i-th prime has
  not yet been found, generate primes until it is encountered.
    - Raise a `TypeError` if `i` is not an `int` or a `slice`.
    - Raise a `ValueError` if a `slice` has no stop index given a positive step size.
    - Raise a `ValueError` if a `slice` has no start index given a negative step size.
    - Raise an `IndexError` if either an `int` or a `slice` uses a negative index.
  (_Note: A Python `slice` object has `.start`, `.stop`, and `.step` attributes
  that are `None` when not specified by the caller — e.g. `s[3:]` gives
  `slice(3, None, None)`._)

- `__iter__` returns a unique iterator object that outputs prime numbers in
  increasing order starting from 2. This iterator should not have a stopping
  point and should only halt once a `break` statement is encountered. Generate
  new prime numbers if need be. (_Hint: Use generator functions._)
- `__len__` returns the number of primes generated so far.
"""

import math
from typing import Iterator, Union


class PrimeStore:
    _primes = [2]

    # ------ SOLUTION GOES HERE!  ------


if __name__ == "__main__":
    ps = PrimeStore()

    # Iterate through primes, stopping before 30
    primes_under_30 = []
    for p in ps:
        if p >= 30:
            break
        primes_under_30.append(p)
    print("Primes under 30:", primes_under_30)

    # Index and slice access
    print("5th prime (index 4):", ps[4])  # 11
    print("First five primes:  ", ps[0:5])  # [2, 3, 5, 7, 11]
    print("Primes generated so far:", len(ps))
