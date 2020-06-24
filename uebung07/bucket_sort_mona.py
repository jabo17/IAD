import random
import math
import timeit

def create_data(size):
    a = []
    while len(a) < size:
        x, y = random.uniform(-1, 1), random.uniform(-1, 1)
        r = math.sqrt(x**2 + y**2)
        if r < 1.0: # der Punkt (x,y) liegt im Einheitskreis
            a.append(r)
    return a 

def insertionSort(a):
    N = len(a)

    for i in range(N):
        current = a[i]
        j = i
        while j > 0:
            if current < a[j-1]:
                a[j] = a[j-1]
            else:
                break
            j -= 1
        a[j] = current

#(a)
def quantize(r,M):
    #Anteil der Punkte innerhalb des Kreises mit Radius r ist gerade Flächeninhalt Kreis Radius r / Flächeninhalt Einheitskreis = r**2
    return int(r**2*M)

#(b)
def chi_squared(buckets):
    #wir erhalten ein Array bestehend aus einzelnen arrays, den jeweiligen buckets
    M = len(buckets)

    #Gesamtanzahl der einzelen bucketelemente ist die Lände des ursprünglichen arrays a
    N = 0
    for index in range(M):
        N += len(buckets[index])
    
    c= N/M
    chi_sum = 0
    # chi^2 = sum_{k=0}^{M-1} \frac{(n_k-c)^2}{c}
    for index in range(M):
        chi_sum += ((len(buckets[index])-c)**2 ) / c
    
    tau = math.sqrt(2* chi_sum)- math.sqrt(2*M-3)
    if abs(tau) > 3:
        return False
    return True

def quantize_naive(r,M):
    return int(r*M)


#besonders für den Einheitskreis: a[k]._key == a[k]
#(c)
def bucketSort(a,quantize, d):
    N = len(a)
    M = int(N/float(d))

    #M leere Buckets erzeugen
    buckets = [[] for k in range(M)]

    #Daten auf die Buckets verteilen
    for k in range(len(a)):
        #bucket index berechnen
        index = quantize(a[k], M)
        buckets[index].append(a[k])
    
    start = 0
    for k in range(M):
        insertionSort(buckets[k])
        end = start + len(buckets[k])
        a[start:end] = buckets[k]
        start += len(buckets[k])



############# tests ##########
def test_bucket_sort():

    #random array with size N
    N = 500
    a = create_data(N)
    d = 3

    #check bucketsort
    bucketSort(a,quantize, d )
    for i in range(len(a)-1):
        assert a[i] <= a[i+1]
    
    #for chi function

    #the better quantize function
    assert check_chi(a,quantize, d) == True

    #naive implementation
    b = create_data(N)
    assert check_chi(b,quantize_naive,d) == False


def check_chi (a,quantize, d):
    N = len(a)
    M = int(N/float(d))

    #M leere Buckets erzeugen
    buckets = [[] for k in range(M)]

    #Daten auf die Buckets verteilen
    for k in range(len(a)):
        #bucket index berechnen
        index = quantize(a[k], M)
        buckets[index].append(a[k])
    
    return chi_squared(buckets)

#(c)
def test_linear_runtime_quantize():
    max_c = -1
    min_c = -1

    for i in range(200,500):
        #get runtime

        t = timeit.Timer(stmt="bucketSort(a,quantize,d)", setup="from bucket_sort_mona import create_data;from bucket_sort_mona import quantize; from bucket_sort_mona import bucketSort; N = "+ str(i)+";  a = create_data(N ); d = 3;").timeit(number=100)/100
        
        #is runtime approx linear?
        const = t / i
        if const < min_c or min_c == -1:
            min_c = const
        elif const> max_c or max_c == -1:
            max_c = const
    
    print("Min_c with quantize: ", min_c)
    print("Max_c with quantize", max_c)
    #now see the diff
    #assert max_c - min_c <= 5

def test_linear_runtime_quantize_naive():
    max_c = -1
    min_c = -1

    for i in range(200,500):
        #get runtime

        t = timeit.Timer(stmt="bucketSort(a,quantize_naive,d)", setup="from bucket_sort_mona import create_data;from bucket_sort_mona import quantize_naive; from bucket_sort_mona import bucketSort; N = "+ str(i)+";  a = create_data(N ); d = 3;").timeit(number=100)/100
        
        #is runtime approx linear?
        const = t / i
        if const < min_c or min_c == -1:
            min_c = const
        elif const> max_c or max_c == -1:
            max_c = const
    
    print("Min_c with quantize_naive: ", min_c)
    print("Max_c with quantize_naive", max_c)
        