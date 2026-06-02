"""
Fill out the code below so that they perform the mathematical operations
that are described in the docstring.

DO NOT MODIFY THE FUNCTION SIGNATURES.
"""


def gram_schmidt(vectors: list[list[float]]) -> list[list[float]]:
    """
    Orthonormalizes a set of linearly independent vectors using the
    Gram-Schmidt process.

    More about this method can be found here:

        https://en.wikipedia.org/wiki/Gram%E2%80%93Schmidt_process

    TIP: Write several helper functions within the body of this function.

    Arguments:
        vectors -- a list of linearly independent vectors, each represented
            as a list of floats of equal length

    Returns:
        list[list[float]] -- a list of orthonormal vectors spanning the same
            subspace as the input vectors

    Raises:
        ValueError -- if the vectors are not all the same length
        ValueError -- if the vectors are linearly dependent
    """

    # ------ SOLUTION GOES HERE!  ------


def gaussian_elimination(A: list[list[float]], b: list[float]) -> list[float]:
    """
    Solves the linear system Ax = b using Gaussian elimination
    with partial pivoting.

    More about this method can be found here:

        https://en.wikipedia.org/wiki/Gaussian_elimination

    Arguments:
        A -- an n x n matrix represented as a list of lists of floats
        b -- a list of n floats representing the right-hand side vector

    Returns:
        list[float] -- the solution vector x such that Ax = b

    Raises:
        ValueError -- if A is not square or dimensions are incompatible
        ValueError -- if the system is singular (no unique solution exists)

    (_Hint: Partial pivoting — before eliminating column `col`, find the row
    in `range(col, n)` with the largest absolute value in that column and swap
    it into the pivot position. This keeps the algorithm numerically stable._)
    """

    # ------ SOLUTION GOES HERE!  ------


if __name__ == "__main__":
    # Orthonormalize two non-orthogonal vectors in R^2
    basis = gram_schmidt([[3, 0], [1, 1]])
    print("gram_schmidt:", [f"[{', '.join(f'{x:.4f}' for x in v)}]" for v in basis])

    # Solve 2x + y = 5, x + 3y = 10  →  x=1.0, y=3.0
    x = gaussian_elimination([[2, 1], [1, 3]], [5, 10])
    print("gaussian_elimination:", [round(v, 4) for v in x])
