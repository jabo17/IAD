import pytest
import random
from random import randint

#(a) Ein Fixture ist Hilfscode, der ausgeführt wird, bevor die Testfunktion ausgeführt wird,
#  um nicht so viel extra code zu schreiben und das Testen besser von der Initalisierung der Vorbedingungen zu trennen.
# Man benutzt es, indem man über die Funktion @pytest.fixture schreibt, welche dann vor dem Aufruf einer Testfunktion von pytest aufgerufen wird.
# Wenn man mit pytest eine Datei aufruft, muss pytest die Testfunktionen festellen können. Hierfuer dient das Prefix test_, alle anderen Funktionen werden nur
# aufgerufen, falls test_<name> sie aufruft. check_<name> hat für pytest in diesem Sinne keine spezielle Bedeutung, sondern dient uns nur als Hilfe
# Ergebnisse zu verifizieren und steht somit mehreren beispielsweise Testfunktionen zur Verfügung


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
            #we changed < to <=
            #otherwise (<): if equal: current's new pos is before the el at j-i
            if key(a[j-1]) < key(current):
                break
            else:
                a[j] = a[j-1]
            j -= 1
        a[j] = current

##################################################################

def insertion_sort(a, key=lambda x: x):
    '''
    Sort the array 'a' in-place.

    Parameter 'key' must hold a function that, given a complicated
    object, extracts the property to sort by. By default, this
    is the object itself (useful to sort integers). To sort Students
    by name, you call:
        insertion_sort(students, key=Student.get_name)
    whereas to sort by mark, you use
        insertion_sort(students, key=Student.get_mark)
    This corresponds to the behavior of Python's built-in sorting functions.
    '''
    for i in range(1, len(a)):
        current = a[i]
        j = i
        while j > 0:
            #we changed < to <=
            #otherwise (<): if equal: current's new pos is before the el at j-i
            if key(a[j-1]) <= key(current):
                break
            else:
                a[j] = a[j-1]
            j -= 1
        a[j] = current

##################################################################

def merge(left, right, key=lambda x: x):
    '''
        Merge Elements of left and right in new array
    '''
    res = []
    i, j = 0, 0
    while i < len(left) and j < len(right):
        if key(left[i]) <= key(right[j]):
            res.append(left[i])
            i += 1
        else:
            res.append(right[j])
            j += 1
    while i < len(left):
        res.append(left[i])
        i += 1
    while j < len(right):
        res.append(right[j])
        j += 1
    return res

def merge_sort(a, key=lambda x: x):
    '''
    Sort the array 'a' in-place.

    Parameter 'key' must hold a function that, given a complicated
    object, extracts the property to sort by. By default, this
    is the object itself (useful to sort integers). To sort Students
    by name, you call:
        merge_sort(students, key=Student.get_name)
    whereas to sort by mark, you use
        merge_sort(students, key=Student.get_mark)
    This corresponds to the behavior of Python's built-in sorting functions.
    '''
    N = len(a)
    if N <= 1:
        return a
    else:
        left = a[0:N//2]
        right = a[N//2:N]
        leftSorted = merge_sort(left, key)
        rightSorted = merge_sort(right, key)
        return merge(leftSorted, rightSorted, key)

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

@pytest.mark.xfail(reason="jedes Beispiel in test_checks soll einen Fehler erzeugen, der abgefangen wird.")
def test_checks():
    #fehler für länge
    check_integer_sorting([3,4],[1])
    #fehler für nicht sortiertes Ergebnis
    check_integer_sorting([5,3,7],[3,7,5])
    #fehler für nicht enthaltensein
    check_integer_sorting([1,2,3],[1,1,2])
    #habe ich noch hinzugefuegt
    #fehler für: element zu wenig enthalten sein
    check_integer_sorting([1,3,3],[1,1,3])

def test_builtin_sort(arrays):
    # test the integer arrays
    for original in arrays['int_arrays']:
        result = list(original)
        result.sort()
        check_integer_sorting(original, result)

    # test the Student arrays
    for original in arrays['student_arrays']:
        result1 = list(original)
        result1.sort(key=Student.get_name)
        check_student_sorting(original, result1, Student.get_name)
        result2 = list(original)
        result2.sort(key=Student.get_mark)
        check_student_sorting(original, result2, Student.get_mark)

#wir erwarten dass ein Fehler auftritt, da insertion_sort_1 nicht stabil sortiert und wir dies in dem Test pruefen
@pytest.mark.xfail(reason="insertion_sort_1 is not stable yet and would not pass the test for a stable-check")
def test_insertion_sort(arrays):
    # test the integer arrays
    for original in arrays['int_arrays']:
        result = list(original)
        insertion_sort_1(result)
        check_integer_sorting(original, result)
        # test new insertion sort
        result2 = list(original)
        insertion_sort(result2)
        check_integer_sorting(original, result2)

    # test the Student arrays
    for original in arrays['student_arrays']:
        result1 = list(original)
        insertion_sort_1(result1, Student.get_name)
        check_student_sorting(original, result1, Student.get_name)
        result2 = list(original)
        insertion_sort_1(result2, Student.get_mark)
        check_student_sorting(original, result2, Student.get_mark)
        #test new insertion sort
        result3 = list(original)
        insertion_sort(result3, Student.get_name)
        check_student_sorting(original, result3, Student.get_name)
        result4 = list(original)
        insertion_sort(result4, Student.get_mark)
        check_student_sorting(original, result4, Student.get_mark)

def test_merge_sort(arrays):
    for original in arrays['int_arrays']:
        result = merge_sort(original)
        check_integer_sorting(original, result)
    for original in arrays['student_arrays']:
        result = merge_sort(original, Student.get_name)
        check_student_sorting(original, result, Student.get_name)
        result2 = merge_sort(original, Student.get_mark)
        check_student_sorting(original, result2, Student.get_mark)

def test_hierarchical_sort(arrays):
    for original in arrays['student_arrays']:
        #wir testen zuerst merge_sort
        result = merge_sort(original, Student.get_name)
        #in result sollten alle Studenten nach Namen sortiert sein
        #wir testen dies natuerlich nochmal
        check_student_sorting(original, result, Student.get_name)
        #dann sortieren wir result nach noten
        result2 = merge_sort(result, Student.get_mark)
        #und pruefen, ob von result nach result2 stabil sortiert wurde
        #was genau dann der fall ist, falls alle Studenten mit gleicher Note nach Namen sortiert sind
        check_student_sorting(result, result2, Student.get_mark)
        #und weil das so toll (hoffentlich :D) klappt, machen wir das nochmal mit dem tollen Insertionsort
        result3 = list(original)
        insertion_sort(result3, Student.get_name)
        check_student_sorting(original, result, Student.get_name)
        result4 = list(result3)
        insertion_sort(result4, Student.get_mark)
        check_student_sorting(result3, result4, Student.get_mark)

def check_integer_sorting(original, result):
    '''Parameter 'original' contains the array before sorting,
    parameter 'result' contains the output of the sorting algorithm.'''
    #gleiche länge
    assert len(original)== len(result)
    #sortiertes Ergebnis:
    for i in range(0,len(result)-1):
        assert result[i]<= result[i+1]
    #gleiche Elemente:
    result_c = list(result)
    for i in range(0,len(result_c)):
        a = original[i]
        assert a in result_c
        result_c.remove(a) #hier hat Jannick noch etwas verändert

def check_student_sorting(original, result, key):
    '''Parameter 'original' contains the array before sorting,
    parameter 'result' contains the output of the sorting algorithm.
    'key' is the attribute defining the order.
    '''
    #gleiche länge
    assert len(original) == len(result)
    #sortiertes Ergebnis:
    for i in range(0,len(result)-1):
        assert key(result[i])<= key(result[i+1])
    #gleiche Elemente und stable
    result_c = list(result)
    for i in range(0, len(result_c)):
        a = original[i]
        assert a in result_c #ist el in sorted array?
        j = result_c.index(a) #get index of first match
        assert j==0 or key(result_c[j-1])<key(a) #assert is was stable sorted // falls eq => a was not stable sorted
        result_c.remove(a)