import doctest
import pytest
import math

###########################################################

class array_deque:

    def __init__(self):                   # constructor for empty container
        '''your documentation here'''
        self._size = 0                    # no item has been inserted yet
        self._capacity = 1                # we reserve memory for at least one item
        self._data = [None]               # internal memory (init one free cell)
        self._startindex = 0              
        self._endindex = 0                
        
    def size(self):
        '''your documentation here'''
        return self._size
        
    def capacity(self):
        '''your documentation here'''
        return self._capacity                       # your code here
        
    def push(self, item):                 # add item at the end
        '''your documentation here'''
        if self._capacity == self._size:  # internal memory is full
            new_data= [0]*(self._capacity*2)            # your code to double the memory
            for i in range(self._size+1):
                new_data[i]=self._data[i]
            self._capacity= self._capacity*2 #Größe anpassen
            self._data = new_data

        elif self._endindex == self._capacity-1:
            self._endindex = 0
            self._data[-self._startindex] = item
        else:
            self._data[self._size]=item 
        self._size += 1
                                 # your code to insert the new item
        
    def pop_first(self):
        '''your documentation here'''
        if self._size == 0:
            raise RuntimeError("pop_first() on empty container")
        else:
            self._data[self._startindex %(self._capacity) -self._startindex] = 0 #hier reicht zugriff [0]
            self._startindex += 1 
            self._size -= 1          
        
    def pop_last(self):
        '''your documentation here'''
        if self._size == 0:
            raise RuntimeError("pop_last() on empty container")
        else:
            self._data[self._endindex %(self._capacity) -self._startindex] = 0
            self._endindex -= 1
            self._size -= 1
        
    def __getitem__(self, index):         # __getitem__ implements v = c[index]
        '''your documentation here'''
        if index < 0 or index >= self._size:
            raise RuntimeError("index out of range")
        return self._data[index + self._startindex]
        
    def __setitem__(self, index, v):      # __setitem__ implements c[index] = v
        '''your documentation here'''
        if index < 0 or index >= self._size:
            raise RuntimeError("index out of range")
        else: 
            for i in range (self._size , index-1,-1):
                self._data[i+self._startindex +1] = self._data[i+self._startindex]
            self._data[index + self._startindex] = v
            self._size += 1
            self._endindex +=1

        
    def first(self):
        '''your documentation here'''
        return self._data[self._startindex]                        # your code here
        
    def last(self):
        '''your documentation here'''
        return self._data[self._endindex]                        # your code here
        
    def __eq__(self, other):
        '''returns True if self and other have same size and elements'''
        if (self._size == other._size):
            for i in range (self._size):
                if (self._data[i] != other._data[i]):
                    return False
            return True
        else:
            return False
        ...                               # your code here

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
    ...                                   # your tests here
