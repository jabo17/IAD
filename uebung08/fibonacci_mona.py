#(a)
#exponentially
def fib1(n):
    if n <= 1:
        return n
    return fib1(n-1) + fib1(n-2)

#Course of values recursion
#linear-recursive, we call the function fib3Impl only once per call
def fib3(n):
    f1, f2 = fib3Impl(n)
    return f2

def fib3Impl(n):
    if n == 0:
        return 1,0
    else:
        f1, f2 = fib3Impl(n-1)
    return f1 + f2, f1

#iterative
def fib5(n):
    f1, f2, = 1,0
    while n > 0:
        f1, f2, = f1 + f2, f1
        n -= 1
    return f2

#(b)
def mul2x2(A,B):
    # A = [a_11, a_12, a_21, a_22]
    C = [0] * 4
    C[0] = A[0] * B[0] + A[1] * B[2]
    C[1] = A[0] * B[1] + A[1] * B[3]
    C[2] = A[2] * B[0] + A[3] * B[2]
    C[3] = A[2] * B[1] + A[3] * B[3]
    return C

def fib6(n):
    F = [1,1,1,0]
    Result = [1,1,1,0]
    if n == 0:
        return 0
    elif n == 1:
        return Result[1]
    while n > 1:
        Result = mul2x2(Result,F)
        n -= 1
    return Result[1]

def fib7(n):
    X = [1,1,1,0]
    Y = mul2x2(X,X)
    if n == 0:
        return 0
    elif n == 1:
        return 1
    elif n %2 == 0:
        return fib7Impl(Y,n/2)[1]
    elif n %2 == 1:
        Y = mul2x2(X,fib7Impl(Y,n/2-1))
        return Y[1]
    else:
        raise ValueError("number must be an unsigned integer!")

def fib7Impl(Y, n):
    Result = list(Y)
    while n > 1:
        Result = mul2x2(Result,Y)
        n -= 1
    return Result
    

##### tests ########
def test_fib ():
    assert fib1(0) == 0
    assert fib3(0) == 0
    assert fib5(0) == 0

    #print(fib1(38)) 12 sec
    #print(fib3(956)) else: maximum recursion depth
    #print(fib5(10500)) #500 000 was possible

def test_mult ():
    A = [1,0,0,1]
    assert mul2x2(A,A) == [1,0,0,1] 
    B = [6,1,9,1]
    assert mul2x2(A,B) == [6,1,9,1]

def test_fib6():
    assert fib6(0) == 0
    assert fib6(1) == 1
    for i in range(10):
        assert fib6(i) == fib5(i)

def test_fib7():
    assert fib7(0) == 0
    assert fib7(1) == 1
    for i in range(10):
        assert fib7(i) == fib5(i)
    
    #print(fib7(100000)) danach schmiert mir wieder mein programm ab