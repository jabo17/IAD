import pytest
import timeit
import copy

###########################################################

class array_deque:

    def __init__(self):
        '''
            Initialisation of array_deque

            Example for new instance and init check
            >>> c = array_deque()
            >>> c.size()
            0
            >>> c.capacity()
            1


        '''
        self._size = 0                    # no item has been inserted yet
        self._capacity = 1                # we reserve memory for at least one item
        self._data = [None]               # internal memory (init one free cell)
        self._begin = 0                   # first element in dynamic list
        self._end = 0                     # last element in dynamic list
        
    def size(self):
        '''
            Size of Items in Deque

            >>> c = array_deque()
            >>> c.size()
            0
        '''
        return self._size
        
    def capacity(self):
        '''Capacity of Deques internal memory
        
            >>> c = array_deque()
            >>> c.capacity()
            1
        '''
        return self._capacity                       # your code here
        
    def push(self, item):                 # add item at the end
        '''
            Pushes an element to the end with constant complexity

            #Example for adding an element
            >>> c = array_deque()
            >>> c.push(0)
            >>> c[0] == 0
            True
        '''
        if self._capacity == self._size:

            #allocating new memory
            self._data = self._data[self._begin:self._capacity] + self._data[0:(self._end+1)%self._capacity] + [None] * (self._capacity + self._capacity-self._size)

            #new position of old list
            #if assignments are more expensive than comparision, uncomment the next line 
            #if self._end < self._begin:
            self._begin = 0
            self._end = self.size()-1
            #end if

            self._capacity *= 2

        #we only increment end, if size was not empty, otherwise the last points already to position 0
        if self.size() != 0 :
            self._end = (self._end + 1) % self._capacity
        self._size += 1 
        self._data[self._end] = item
        
        
    def pop_first(self):
        '''
            Removes the first element
            
            Example for adding two elemnts and removing the first one
            >>> c = array_deque()
            >>> c.push(0)
            >>> c.push(1)
            >>> c.pop_first()
            >>> c.first() == 1
            True
        '''
        if self._size == 0:
            raise RuntimeError("pop_first() on empty container")
        self._data[self._begin] = None
        #we use a modulo calc to handle index overflow
        self._begin = (self._begin + 1) % self._capacity
        self._size -= 1
        
    def pop_last(self):
        '''
            Removes the last element

            Example for adding two element and removing the last one
            >>> c = array_deque()
            >>> c.push(0)
            >>> c.push(1) 
            >>> c.pop_last()
            >>> c.last() == 0
            True
            
        '''
        if self._size == 0:
            raise RuntimeError("pop_last() on empty container")
        self._data[self._end] = None
        #we use a modulo calc to handle index overflow
        self._end = (self._end - 1) % self._capacity
        self._size -= 1
        
    # __getitem__ implements v = c[index]
    def __getitem__(self, index):
        '''
            Get item at index position

            Example for adding two elements and receive these elements at the index
            >>> c = array_deque()
            >>> c.push(0)
            >>> c.push(1)
            >>> c[0]== 0
            True

            Example for Index out of range
            >>> d = array_deque()
            >>> d.size()
            0
            >>> d[0] == 0
            Traceback (most recent call last):
                ...
            RuntimeError: index out of range

        '''
        if index < 0 or index >= self._size:
            raise RuntimeError("index out of range")
        #we use a modulo calc to handle index overflow
        return self._data[(self._begin+index)% self._capacity]

    # __setitem__ implements c[index] = v    
    def __setitem__(self, index, v):      
        '''
            Set item at index position

            Example for setting an element at a position 
            >>> c = array_deque()
            >>> c.push(0)
            >>> c[0]=1
            >>> c[0]== 1
            True

            Example for Index out of range
            >>> d = array_deque()
            >>> d.size()
            0
            >>> d[1] = 0
            Traceback (most recent call last):
                ...
            RuntimeError: index out of range
            
        '''
        if index < 0 or index >= self._size:
            raise RuntimeError("index out of range")
        #we use a modulo calc to handle index overflow
        self._data[(self._begin+index)% self._capacity] = v
        
    def first(self):
        '''
            Get first element

            append one element and check whether it is the first
            >>> c = array_deque()
            >>> c.push(0)
            >>> c.first() == 0
            True
            
        '''
        return self._data[self._begin]
        
    def last(self):
        '''
            Get last element

            >>> c= array_deque()
            >>> c.push(0)
            >>> c.last() == 0
            True    
        '''
        return self._data[self._end]
        
    def __eq__(self, other):
        '''
            returns True if self and other have same size and elements
            
            example for two equal array_deque
            >>> c = array_deque()
            >>> c.push(0)
            >>> d = array_deque()
            >>> d.push(0)
            >>> c == d
            True
        '''
        if self.size() != other.size():
            return False
        for i in range(0,self.size()):
            if self[i] != other[i]:
                return False
        return True

    def __ne__(self, other):
        '''
            returns True if self and other have different size or elements
            
            example for two arraydeques with different elements
            >>> c= array_deque()
            >>> c.push(0) 
            >>> d= array_deque()
            >>> d.push(1)
            >>> c!= d
            True   
        '''
        return not (self == other)

###########################################################

class slow_array_deque(array_deque):

    def push(self, item):                 # add item at the end
        '''
            Pushes an element to the end with linear complexity
            
            >>> s = slow_array_deque()
            >>> s.push(0)
            >>> s[0] == 0
            True
        '''
        if self._capacity == self._size:

            #allocating new memory
            self._data = self._data[self._begin:self._capacity] + self._data[0:(self._end+1)%self._capacity] + [None] 

            #new position of old list
            #if assignments are more expensive than comparision, uncomment the next line 
            #if self._end < self._begin:
            self._begin = 0
            self._end = self.size()-1
            #end if

            self._capacity +=1
        if self.size() != 0 :
            self._end = (self._end + 1) % self._capacity
        self._size += 1
        self._data[self._end] = item

###########################################################

#verifies axiomes for a empty deque for n elements
def check_procedure(deque, n):
    
    #size check
    # axiome 1
    assert deque.size() == 0

    lastsize = 0
    #we try to push elements
    for i in range(n):
        #copy for axiome 3 (v)
        old = copy.deepcopy(deque)

        #push
        deque.push(i)

        #axiome 3 (ii)
        assert deque.last() == i

        #axiome 7 (ii)
        assert check_last_is_last(deque)

        #axiome 3 (iv)
        assert deque.first() == 0

        #axiome 7 (i)
        assert check_first_is_first(deque)

        #axiome 3 (i)
        assert deque.size() == lastsize+1
        lastsize += 1

        #axiome 3 (iii)
        for j in range(0, i):
            deque[j] = j

        #axiome 2
        assert deque.size() <= deque.capacity()

        #axiome 3 (v) and axiome 5 (i),(ii)
        old2 = copy.deepcopy(deque)
        old2.pop_last()
        assert old == old2 #equals regarding __eq__

        if(lastsize-1 > 0):
            #axiome 7 (i)
            assert check_first_is_first(old2)
            #axiome 7 (ii)
            assert check_last_is_last(old2)

    #axiome 4
    for i in range(n,2*n):
        assert deque[i-n] != i

        #copy for axiome 4 (iii)
        old = copy.deepcopy(deque)

        deque[i-n] = i
        #axiome 4 (i)
        assert deque.size() == lastsize
        #axiome 4 (ii)
        assert deque[i-n] == i

        #axiome 4 (iii)
        for j in range(0,n):
            if ( j != i-n):
                assert old[j] == deque[j]

    for i in range(0,n):

        #copy for axiome 6 (ii)
        old = copy.deepcopy(deque)

        deque.pop_first()

        if(lastsize-1 > 0):
            #axiome 7 (i)
            assert check_first_is_first(deque)
            #axiome 7 (ii)
            assert check_last_is_last(deque)

        #axiome 6 (i)
        assert deque.size() == lastsize - 1
        lastsize -= 1

        #axiome 6 (ii)
        for j in range(lastsize):
            assert deque[j] == old[j+1]

    assert deque.size() == 0

    #expections
    with pytest.raises(RuntimeError):
        assert(deque[0])
    with pytest.raises(RuntimeError):
        assert(deque.pop_first())
    with pytest.raises(RuntimeError):
        assert(deque.pop_last())

#helper functions    
def check_first_is_first(deque):
    return deque.first() == deque[0]

def check_last_is_last(deque):
    return deque.last() == deque[deque.size()-1]

#test slow_array_deque and array_deque
def test_array_deque():
    check_procedure(array_deque(), 20)
    check_procedure(array_deque(), 30)
    check_procedure(slow_array_deque(), 20)
    check_procedure(slow_array_deque(), 30)

#to watch output: pytest file.py -s
def test_complexity_deque():
    #we fill n lists with sizes 1 to n
    n = 1000
    time_avg = 0
    minT = -1
    maxT = -1
    for i in range(1,n+1):
        #print(i)
        #t is average time per push in the current measurement
        t = timeit.Timer(stmt="deque.push(0)", setup="from array_deque_jannick import array_deque; deque = array_deque();").timeit(number=i)/i
        if t < minT or minT == -1: minT = t
        if t > maxT: maxT = t
        time_avg += t
    time_avg = time_avg / n
    #values should be nearly equal, if push has amortised constant complexity
    print("array_deque [if constant: values should be almost equal]:")
    print("MinT: " + str(minT))
    print("MaxT: " + str(maxT))
    print("AvgT: " + str(time_avg))
    print("N: " + str(n))

def test_complexity_slow_deque():
    #we fill n lists with sizes 1 to n
    n = 1000
    time_avg = 0
    minT = -1
    maxT = -1
    for i in range(1,n+1):
        #print(i)
        #t is average time per push in the current measurement
        t = timeit.Timer(stmt="deque.push(0)", setup="from array_deque_jannick import slow_array_deque; deque = slow_array_deque();").timeit(number=i)/i
        # we assume an amortized linear complexity, so t is proportional to n
        if t < minT or minT == -1: minT = t / n
        if t > maxT: maxT = t / n
        time_avg += t / n 
    time_avg = time_avg / n
    #values should be nearly equal, if push has amortized linear complexity
    print("slow array_deque [if linear: values should be almost equal]:")
    print("MinT: " + str(minT))
    print("MaxT: " + str(maxT))
    print("AvgT: " + str(time_avg))
    print("N: " + str(n))


if __name__ == '__main__':
    import doctest
    doctest.testmod()
    #doctest.testmod(extraglobs={'c': array_deque()})