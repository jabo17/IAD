#insertionsort gibt geordnetes array zurück
def insertion_sort(a):
        for i in range(len(a)):
                j=i
                while j>0:
                        if a[j-1] > a[j]:
                                a[j-1], a[j] = a[j], a[j-1]
                                j= j-1
                        else: break
        return a

import random

def quick_sort(a):
    return quicksortImpl (a,0,len(a)-1)
    
def quicksortImpl(a,l,r):
    counter = 0
    if r > l:
        k, part_counter = partition(a, l, r)

        counter += part_counter
        counter += quicksortImpl(a,l, k-1)
        counter += quicksortImpl(a,k+1, r)
    return counter

def partition (a,l,r):
    counter = 0

    m=random.randint(l,r)
    a[m], a[r] = a[r], a[m]
    pivot = a[r]
    i= l
    j= r-1
    while True:
        while i < r:
            counter+=1
            if a[i]<= pivot:
                i= i+1
            else: break
        while j > l:
            counter+=1
            if a[j]>= pivot:
                j= j-1
            else: break
        if i<j:
            a[i], a[j]= a[j], a[i]
        else: 
            break        
    a[r]= a[i]

    a[i]= pivot
    return i, counter
