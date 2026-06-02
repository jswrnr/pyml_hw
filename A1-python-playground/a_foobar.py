"""
The classic interview hazing ritual, now with extra chaos.

Rules:
  - For multiples of 3:           print "Foo"
  - For multiples of 5:           print "Bar"
  - For multiples of 7:           print "Bop"
  - For multiples of 3 AND 5:     print "FooBar"
  - For multiples of 3 AND 7:     print "FooBop"
  - For multiples of 5 AND 7:     print "BarBop"
  - For multiples of 3, 5, AND 7: print "FooBarBop"
  - For multiples of 11:          append "Bap" to whatever you would print
                                  (or print "Bap" alone if no other rule fires)
  - For everything else:          print the number itself

Example: foobar(1, 16) should print:
    1
    2
    Foo
    4
    Bar
    Foo
    Bop
    8
    Foo
    Bar
    Bap
    Foo
    13
    14
    FooBar

DO NOT MODIFY THE FUNCTION SIGNATURES.
"""


def foobar_word(n: int) -> str:
    """
    Returns the foobar string for a single integer n.

    Applies the rules above in order: build a word from the 3/5/7 divisors,
    append "Bap" if divisible by 11, and fall back to str(n) if the word
    would otherwise be empty.

    Arguments:
        n -- any integer

    Returns:
        str -- the word to print for n
    """
    s: str = ""
    if n % 3 == 0:
        s += "Foo"
    if n % 5 == 0:
        s += "Bar"
    if n % 7 == 0:
        s += "Bop"
    if n % 11 == 0:
        s += "Bap"
    if len(s) == 0:
        return str(n)
    return s
    # ------ SOLUTION GOES HERE!  ------


def foobar(start: int, stop: int) -> None:
    """
    Prints one foobar_word per line for each integer in [start, stop).

    Arguments:
        start -- inclusive lower bound
        stop  -- exclusive upper bound
    """

    # ------ SOLUTION GOES HERE!  ------
    for i in range(start, stop):
        print(foobar_word(i))


# ---------------------------------------------------------------------------
# Prompt / demo
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=== FooBarBop(Bap) ===")
    print("Rules: Foo=÷3  Bar=÷5  Bop=÷7  Bap=÷11  (combined for multiple divisors)\n")

    try:
        start = int(input("Start (inclusive): "))
        stop = int(input("Stop  (exclusive): "))
    except ValueError:
        print("Please enter integers.")
        raise SystemExit(1)

    print()
    foobar(start, stop)
