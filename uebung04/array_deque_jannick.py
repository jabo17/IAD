import doctest
import pytest
import timeit

###########################################################

class array_deque:

    def __init__(self):                   # constructor for empty container
        '''Initialisation of array_deque'''
        self._size = 0                    # no item has been inserted yet
        self._capacity = 1                # we reserve memory for at least one item
        self._data = [None]               # internal memory (init one free cell)
        self._begin = 0                   # first element in dynamic list
        self._end = 0                     # last element in dynamic list
        
    def size(self):
        '''Size of Items in Deque'''
        return self._size
        
    def capacity(self):
        '''Capacity of Deques internal memory'''
        return self._capacity                       # your code here
        
    def push(self, item):                 # add item at the end
        '''Pushes an element to the end'''
        if self._capacity == self._size:
            if self._end < self._begin:
                end = self._capacity
                self._data = self._data[self._begin:end] + self._data[0:self._end+1] + [None] * (self._capacity + self._capacity-self._size)
                #new position of old list
                self._begin = 0
                self._end = self.size()-1
            else:
                print(len(self._data[self._begin:self._end+1]))
                self._data = self._data[self._begin:self._end+1] + [None] * (self._capacity + self._capacity-self._size)
            #wir kopieren die relative Liste an den Begin der neuen Liste und allokieren +capacity Speicher
            print(len(self._data))
            self._capacity *= 2
        self._size += 1
        if self.size() != 0 :
            self._end = (self._end + 1) % self._capacity
        self._data[self._end] = item
        
        
    def pop_first(self):
        '''Removes the first element'''
        if self._size == 0:
            raise RuntimeError("pop_first() on empty container")
        self._data[self._begin] = None
        self._begin = (self._begin + 1) % self._capacity
        self._size -= 1
        
    def pop_last(self):
        '''Removes the last element'''
        if self._size == 0:
            raise RuntimeError("pop_last() on empty container")
        self._data[self._end] = None
        self._end = (self._end - 1) % self._capacity
        self._size -= 1
        
    def __getitem__(self, index):         # __getitem__ implements v = c[index]
        '''Get item at index position'''
        if index < 0 or index >= self._size:
            raise RuntimeError("index out of range")
        return self._data[self._begin+index]                        # your code here
        
    def __setitem__(self, index, v):      # __setitem__ implements c[index] = v
        '''Set item at index position'''
        if index < 0 or index >= self._size:
            raise RuntimeError("index out of range")
        self._data[self._begin+index] = v                               # your code here
        
    def first(self):
        '''Get first element of Deque'''
        return self._data[self._begin]                        # your code here
        
    def last(self):
        '''Get last element of Deque'''
        return self._data[self._end]                        # your code here
        
    def __eq__(self, other):
        '''returns True if self and other have same size and elements'''
        if self.size != other.size:
            return False
        for i in range(0,self.size):
            if self[i] != other[i]:
                return False
        return True

    def __ne__(self, other):
        '''returns True if self and other have different size or elements'''
        return not (self == other)

###########################################################

class slow_array_deque(array_deque):

    def push(self, item):                 # add item at the end
        if self._capacity == self._size:  # internal memory is full
            ...                           # code to enlarge the memory by one
        self._size += 1
        ...                               # your code to insert the new item

###########################################################

def test_array_deque():
    deque = array_deque()
    
    # size check
    deque.push(0)
    assert deque.size() == 1
    assert deque._end == 0

    # re-alloc check
    deque.push(1)
    assert deque.size() == 2
    assert deque._end == 1
    assert deque.capacity() == 2

    #queue properties
    assert 0 == deque.first()
    deque.pop_first()
    assert deque._begin == 1
    assert 1 == deque.first()
    assert 1 == deque.last()
    deque.pop_last()
    assert deque._begin == 1
    assert deque._end == 0
    assert deque.size() == 0
    
    # testing _begin index overflow
    assert deque.capacity() == 2
    deque.push(2)
    assert deque._begin == 1
    assert deque._end == 1
    deque.push(3)
    assert deque._begin == 1
    assert deque._end == 0 #because (_end+1)%2=0

    #reallocation
    deque.push(4)
    assert deque.capacity() == 4
    #after realloc. _begin is 0 and _end is size-1
    assert deque._begin == 0
    assert deque[deque._begin] == 2  # first element is 2
    assert deque._end == deque.size()-1
    assert deque[deque._end] == 4 # last element is 4

def test_complexity():
    timeit.Timer(stmt="deque.push(0)", setup="from __main__ import array_deque; deque = array_deque();").timeit(number=10000000)