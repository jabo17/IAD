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
            new_data= [0]*(self._capacity*2)            #to double the memory
            for i in range(self._size):               
                new_data[i]=self._data[i]
            self._capacity= self._capacity*2 #Größe anpassen
            self._data = new_data
            self._endindex += 1

        elif self._endindex == self._capacity-1:
            self._endindex = 0
            self._data[-self._startindex] = item
        else:
            self._data[self._size]=item 
            self._endindex += 1
        self._size += 1
                                 # your code to insert the new item
        
    def pop_first(self):
        '''your documentation here'''
        if self._size == 0:
            raise RuntimeError("pop_first() on empty container")
        else:
            self._data[0] = 0 #hier reicht zugriff [0]
            self._startindex += 1 
            self._size -= 1          
        
    def pop_last(self):
        '''your documentation here'''
        if self._size == 0:
            raise RuntimeError("pop_last() on empty container")
        else:
            self._data[self._endindex -self._startindex] = 0
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
            self._data[index] = v

        
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
            new_data= [0]*(self._capacity+1)            #to enlarge the memory
            for i in range(self._size):               
                new_data[i]=self._data[i]
            self._capacity= self._capacity+1 #Größe anpassen
            self._data = new_data
            self._endindex += 1

        elif self._endindex == self._capacity-1:
            self._endindex = 0
            self._data[-self._startindex] = item
        else:
            self._data[self._size]=item 
            self._endindex += 1                           # code to enlarge the memory by one
        self._size += 1

###########################################################

def test_array_deque():
    a= array_deque()
    assert a.size() == 0      #neuer Container hat Größe 0
    assert a.size() <= a.capacity()         #zu jeder Zeit, da könnte man noch was verändern
                                    
                                     #vorbereitung für den Test unten: wir müssen uns den vorherigen
    oldarray = [0]*a.size()         #Zustand merken können
    for i in range (a.size()):
        oldarray[i] = a[i]

    a.push(3)
    assert a.size() == len(oldarray)+1         #Größe hat sich um 1 erhöht
    assert a[a.size()-1] == 3              #grade eingefügtes Element ist das letzte
    for i in range (a.size()-1):
        assert oldarray[i] == a[i]       #alle anderen Elemente haben sich nicht verändert
    
    if(len(oldarray)==0):                #das eingefügte element ist das erste
        assert a[0] == 3
    else:
        assert oldarray[0]== a[0]       #das vorherig erste ist auch jetzt das erste element
    
    a.pop_last()
    for i in range(a.size()):
        assert oldarray[i]== a[i]       #nach pop_last reproduziert container vor dem push
    
    a.push(4)
    a.push(5)
    oldarray = [0]*a.size()         #Zustand merken können
    for i in range (a.size()):
        oldarray[i] = a[i]
    a[1]= 8
    oldarray[1]= 8
    assert len(oldarray)==a.size()      #größe unverändert
    assert a[1]== 8                     #an indes k steht element v
    for i in range(a.size()):           #vorherige elemente haben sich nicht verändert
        assert oldarray[i]== a[i]


    oldarray = [0]*a.size()         #Zustand merken können
    for i in range (a.size()):
        oldarray[i] = a[i]

    if(a.size()==0):                #Hier weiß ich noch nicht recht
        with pytest.raises(Exception):    
            a.pop_last()
    else:
        a.pop_last()

    assert a.size() == len(oldarray)-1      #Größe hat sich um 1 verringert
    for i in range(a.size()):
        assert oldarray[i]== a[i]
    
    oldarray = [0]*a.size()         #Zustand merken können
    for i in range (a.size()):
        oldarray[i] = a[i]
    
    if(a.size()==0):                
        with pytest.raises(Exception):    
            a.pop_first()
    else:
        a.pop_first()
    
    assert a.size()== len(oldarray)-1
    for i in range(a.size()):
        assert a[i]== oldarray[i+1]
    
    if(a.size()!=0):
        assert a.first()== a[0]
        assert a.last()== a[a.size()-1]

#####################################################################

#Hier wollen wir zeigen, dass push die amortisierte konstante Komplexität hat
import timeit
import random
code_to_be_measured = '''
a.push(4)
'''
initialisation = '''
from __main__ import array_deque
a = array_deque()
'''
t = timeit.Timer(code_to_be_measured, initialisation)

M = 100
time = t.timeit(M)# run ’code_to_be_measured’ M times
print("average execution time original array_deque:", time / M)

####################################################################

#Hier wollen wir dasselbe für slow_push() zeigen:
code_to_be_measured = '''
a.push(4)
'''
initialisation = '''
from __main__ import slow_array_deque
a = slow_array_deque()
'''
t = timeit.Timer(code_to_be_measured, initialisation)

M = 100
time = t.timeit(M)# run ’code_to_be_measured’ M times
print("average execution time slow_array_deque:", time / M)
    

