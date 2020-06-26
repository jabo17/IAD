"""
    This file contains an implementation of Bucket Sort

    Jannick Borowitz
    Email: ak238@stud.uni-heidelberg.de
"""
import pytest
import random
import math
import copy
import timeit


def quantize(r: int, M: int) -> int:
    '''
    Maps key r in [0,1) to a bucket [0,M-1]

    Args:
        r: the key
        M: bucket size

    Returns:
        int: the index of keys's bucket
    '''
    return int((r ** 2) * M)


def create_data(size: int) -> list:
    '''
    Creates sampling data for the example unit circle

    Args:
        size: size of random test data

    Returns:
        list: sampling test data
    '''
    a = []
    while len(a) < size:
        x, y = random.uniform(-1, 1), random.uniform(-1, 1)
        r = math.sqrt(x ** 2 + y ** 2)
        if r < 1.0:
            a.append(r)
    return a


def insertion_sort(elements: list) -> None:
    '''

    Args:
        elements: a list of elements to be sorted

    Returns:
        None: (Call by reference / insito)
    '''
    j = 1

    while j < len(elements):
        current = j
        while elements[current - 1] > elements[current] and current > 0:
            elements[current - 1], elements[current] = elements[current], elements[current - 1]
            current -= 1
        j += 1


def bucket_sort(a: list, bucketMap: callable, d: int) -> list:
    '''
    Sorts a in constant complexity

    Args:
        a: a list of elements
        bucketMap: a mapper function Keys(a)-->[0, M-1]
        d: N/M

    Returns:
        list: a sorted list
    '''
    N = len(a)
    M = N // d
    if M == 0: M = 1

    buckets = [[] for x in range(M)]
    for r in a:
        buckets[bucketMap(r, M)].append(r)

    for k in range(M):
        insertion_sort(buckets[k])

    return [r for k in range(M) for r in buckets[k]]


# Helper Functions

def chi_squared(buckets: list) -> bool:
    chiSquared = 0
    N = 0
    M = len(buckets)
    for k in range(0, M):
        N += len(buckets[k])
    c = N / M
    for k in range(0, M):
        chiSquared += ((len(buckets[k]) - c) ** 2) / c

    tau = math.sqrt(2 * chiSquared) - math.sqrt(2 * M - 3)

    if abs(tau) > 3:
        return False
    return True


# PyTests
@pytest.mark.skip
def test_quantize():
    max = 1000
    min = 500
    failed = 0
    success = 0
    tolerance = 0.03
    for size in range(min, max):
        sampleData = create_data(size)
        # we await buckets between 10 and 3 elements
        for M in range(size // 10, size // 3):
            buckets = [[] for i in range(0, M)]
            for r in sampleData:
                buckets[quantize(r, M)].append(r)
                # buckets[int(r*M)].append(r)
            if chi_squared(buckets):
                success += 1
            else:
                failed += 1
    if failed / (failed + success) > tolerance:
        print("Failed : ", failed)
        print("Success : ", success)
        raise AssertionError("FailRate is bigger than tolerance")


def test_insertion_sort():
    a = [random.random() for x in range(100)]

    b = copy.copy(a)

    insertion_sort(a)
    b.sort()
    assert a == b


def test_bucket_sort():
    a = create_data(100)

    result = bucket_sort(a, quantize, 3)
    result2 = bucket_sort(a, lambda r, M: int(r * M), 3)

    a.sort()

    assert a == result
    assert a == result2


def test_complexity():
    max_c = -1
    min_c = -1
    for N in range(1, 1000):

        scope = globals()
        t = timeit.Timer(stmt=f"bucket_sort(a,quantize,3)", setup=f"a=create_data({N})", globals=scope).timeit(number=5) / 5
        c = t / N

        if c < min_c or min_c == -1:
            min_c = c
        elif c > max_c or min_c == -1:
            max_c = c

    print(f"{max_c=}")
    print(f"{min_c=}")

def test_complexity_naive():
    max_c = -1
    min_c = -1
    for N in range(1, 1000):

        scope = globals()
        t = timeit.Timer(stmt=f"bucket_sort(a,lambda r, M: int(r*M),3)", setup=f"a=create_data({N})", globals=scope).timeit(number=5) / 5
        c = t / N

        if c < min_c or min_c == -1:
            min_c = c
        elif c > max_c or min_c == -1:
            max_c = c

    print(f"{max_c=}")
    print(f"{min_c=}")