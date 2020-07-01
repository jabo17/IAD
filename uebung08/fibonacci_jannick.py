"""
    Implementation of fibonacci
"""
import pytest
import timeit

import matplotlib
import matplotlib.pyplot as plt
import numpy as np


def fib1(N):
    """
        tree-recursive fib impl
        complexity: O(2^d) with d depth of recursive tree

    Args:
        N: fib of N

    Returns: fib of N

    """
    if N <= 1: return N
    return fib1(N - 1) + fib1(N - 2)


def fib3Impl(N):
    if N == 0:
        return 1, 0
    else:
        f1, f2 = fib3Impl(N - 1)
        return f1 + f2, f1


def fib3(N):
    f1, f2 = fib3Impl(N)
    return f2


def fib5(N):
    f1, f2 = 1, 0
    while N > 0:
        f1, f2 = f1 * f2, f1
        N -= 1
    return f2


def mul2x2(A, B):
    # matr [0,1,
    #       2,3]
    return [A[0] * B[0] + A[2] * B[1], A[0] * B[1] + A[1] * B[3],
            A[2] * B[0] + A[3] * B[1], A[2] * B[1] + A[3] * B[3]]


def fib6(N):
    f1 = [1, 1, 1, 0]
    fn = [1, 0, 0, 1]
    while N > 0:
        fn = mul2x2(fn, f1)
        N -= 1
    return fn[1]


def fib7(N):
    return fib7Impl([1, 1, 1, 0], N)[1]


def fib7Impl(X, N):
    if N == 0: return [1, 0, 0, 1]
    if N == 1: return X
    if N % 2 == 0:
        return fib7Impl(mul2x2(X, X), N / 2)
    else:
        return mul2x2(X, fib7Impl(mul2x2(X, X), (N - 1) / 2))


# Pytests

def test_fib6():
    assert fib6(0) == 0
    assert fib6(1) == 1
    assert fib6(2) == 1
    assert fib6(3) == 2
    assert fib6(4) == 3
    assert fib6(5) == 5
    assert fib6(6) == 8
    assert fib6(7) == 13


@pytest.mark.skip
def test_fib6_for_big_numbers():
    # N=2000000 takes 9.4 s
    t = timeit.Timer(stmt="fib6(200000)", globals=globals()).timeit(1)
    print(t)
    assert t < 10


def test_fib7_against_fib6():
    for i in range(20):
        assert fib6(i) == fib7(i)

@pytest.mark.skip
def test_plot_complexity_fib5_aigainst_fib7():
    M = 1000
    precision = 4
    map = {5: [], 7: []}

    for algo in [5,7]:
        limit = M if algo != 1 else 12
        for i in range(limit):
            map[algo].append(timeit.Timer(stmt=f"fib{algo}({i})", globals=globals()).timeit(number=precision)*1000/precision)

    fig, ax = plt.subplots()
    x = np.arange(0, M, 1)
    for algo in [5,7]:
        ax.plot(x, map[algo], label = f"fib{algo}(N)")

    ax.set(xlabel='fib(N)', ylabel="time (s)", title="Complexity of fib(N)")
    ax.legend(loc='upper left')
    ax.grid()

    fig.savefig("fib_complexity_5vs7.png")
    plt.show()

@pytest.mark.skip
def test_plot_complexity_all():
    M = 500
    precision = 4
    map = {1: [], 3: [], 5: [], 6: [], 7: []}

    for algo in [1,3,5,6,7]:
        #we limit fib1
        limit = M if algo != 1 else 12
        for i in range(limit):
            map[algo].append(timeit.Timer(stmt=f"fib{algo}({i})", globals=globals()).timeit(number=precision)*1000/precision)

    #fill res for fib1 with zeros
    for i in range(M - 12): map[1].append(0)

    fig, ax = plt.subplots()
    x = np.arange(0, M, 1)
    for algo in [1,3,5,6,7]:
        ax.plot(x, map[algo], label = f"fib{algo}(N)")

    ax.set(xlabel='fib(N)', ylabel="time (s)", title="Complexity of fib(N)")
    ax.legend(loc='upper left')
    ax.grid()

    fig.savefig("fib_complexity.png")
    plt.show()

def test_fib7_big_number():
    # 4000000 takes round about 9s
    t = timeit.Timer(stmt="fib7(4000000)", globals=globals()).timeit(1)
    print(t)
    assert t < 10