import pytest
import random
from sortalgorithm import insertion_sort
from random import randint

#(a) ein Fixture ist Hilfscode, den man ausführt,bevor die testfunktion  ausgeführt wird,
#  um nicht so viel extra code zu schreiben
#   man benutzt es, indem man über die funktion @pytest.fixture schreibt und die funktion dann über die 
# testfunktion aufruft 


class Student:
    def __init__(self, name, mark):
        '''Construct new Student object with given 'name' and 'mark'.'''
        self._name = name
        self._mark = mark

    def get_name(self):
        '''Access the name.'''
        return self._name

    def get_mark(self):
        '''Access the mark.'''
        return self._mark

    def __repr__(self):
        '''Convert Student object to a string.'''
        return "%s: %3.1f" % (self._name, self._mark)

    def __eq__(self, other):
        '''Check if two Student objects are equal.'''
        return self._name == other._name and self._mark == other._mark

##################################################################

def insertion_sort_1(a, key=lambda x: x):
    '''
    Sort the array 'a' in-place.

    Parameter 'key' must hold a function that, given a complicated
    object, extracts the property to sort by. By default, this
    is the object itself (useful to sort integers). To sort Students
    by name, you call:
        insertion_sort_1(students, key=Student.get_name)
    whereas to sort by mark, you use
        insertion_sort_1(students, key=Student.get_mark)
    This corresponds to the behavior of Python's built-in sorting functions.
    
    NOTE: THIS IMPLEMENTATION INTENTIONALLY CONTAINS A BUG, 
    WHICH YOUR TESTS ARE SUPPOSED TO DETECT.
    '''
    for i in range(1, len(a)):
        current = a[i]
        j = i
        while j > 0:
            if key(a[j-1]) < key(current):
                break
            else:
                a[j] = a[j-1]
            j -= 1
        a[j] = current

##################################################################

@pytest.fixture
def arrays():
    '''Create a dictionary holding test data.'''

    data = dict()
    
    # integer arrays
    data['int_arrays'] = [
        [],           # empty array
        [1],          # one element
        [2,1],        # two elements
        [3,2,3,1],    # the array from the exercise text
        [randint(0, 4) for k in range(10)], # 10 random ints
        [randint(0, 4) for k in range(10)]  # another 10 random ints
    ]

    # Student arrays
    data['student_arrays'] = [
       [Student('Adam', 1.3),
        Student('Bert', 2.0),
        Student('Elsa', 1.0),
        Student('Greg', 1.7),
        Student('Jill', 2.7),
        Student('Judy', 3.0),
        Student('Mike', 2.3),
        Student('Patt', 5.0)], # without replicated marks

       [Student('Adam', 1.3),
        Student('Bert', 2.0),
        Student('Elsa', 1.3),
        Student('Greg', 1.0),
        Student('Jill', 1.7),
        Student('Judy', 1.0),
        Student('Mike', 2.3),
        Student('Patt', 1.3)], # with replicated marks, alphabetic

       [Student('Bert', 2.0),
        Student('Mike', 2.3),
        Student('Elsa', 1.3),
        Student('Judy', 1.0),
        Student('Patt', 2.0),
        Student('Greg', 1.0),
        Student('Jill', 1.7),
        Student('Adam', 1.3)] # with replicated marks, random order
    ]
    
    return data

##################################################################

#stuff for test functions

@pytest.fixture
def original():
    return [4,7,2,10]


@pytest.fixture
def result ():
    return insertion_sort(original())

#################################################################

def test_checks():
    #fehler für länge
    check_integer_sorting([3,4],[1])
    #fehler für nicht sortiertes Ergebnis
    check_integer_sorting([5,3,7],[3,7,5])
    #fehler für nicht enthaltensein
    check_integer_sorting([1,2,3],[1,1,2])

def test_builtin_sort(arrays):
    # test the integer arrays
    for original in arrays['int_arrays']:
        ... # your code here (test that array is sorted)

    # test the Student arrays
    for original in arrays['student_arrays']:
        ... # your code here (test that array is stably sorted)

def test_insertion_sort(arrays):
    # test the integer arrays
    for original in arrays['int_arrays']:
        ... # your code here (test that array is sorted)

    # test the Student arrays
    for original in arrays['student_arrays']:
        ... # your code here (test that array is stably sorted)

def check_integer_sorting(original, result):
    '''Parameter 'original' contains the array before sorting,
    parameter 'result' contains the output of the sorting algorithm.'''
    #gleiche länge
    assert len(original)== len(result)
    #sortiertes Ergebnis:
    for i in range(0,len(result)-1):
        assert result[i]<= result[i+1]
    #gleiche Elemente:
    for i in range(0,len(result)):
        a = original[i]
        assert a in result

def check_student_sorting(original, result, key):
    '''Parameter 'original' contains the array before sorting,
    parameter 'result' contains the output of the sorting algorithm.
    'key' is the attribute defining the order.
    '''
    ... # your code here

#main
#test_checks()
