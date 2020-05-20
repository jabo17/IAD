from math import sqrt
import pytest

def archimedes1(k):
    '''
        approximate pi with the archimedes algorithm
        k is the number of doubles
    '''
    #we start with four edges
    n = 4
    s_2n = sqrt(2)
    t_2n = 2.0
    print("n:", n, "pi:", (n*(s_2n+t_2n))/4, "diff:", t_2n-s_2n, sep=" ")
    for i in range(k):
        #Rundungsfehler pflanzen sich in der Iteration fort
        #Dadurch wird t_2n unsinnigerweise groesser als s_2n aber einem gewissen anzahl von verdopplungen
        s_2n = sqrt(2-sqrt(4-s_2n**2))
        t_2n = (2/t_2n)*(sqrt(4+t_2n**2)-2)
        n *= 2
        print("n:", n, "i:", i, "pi:", (n*(s_2n+t_2n))/4, "diff:", t_2n-s_2n, sep=" ")
    return (n, (n*(s_2n+t_2n))/4, s_2n, t_2n)

def archimedes2(k):
    '''
        approximate pi with the archimedes algorithm
        k is the number of doubles
    '''
    #we start with four edges
    n = 4
    s_2n = sqrt(2)
    t_2n = 2.0
    print("n:", n, "pi:", (n*(s_2n+t_2n))/4, "diff:", t_2n-s_2n, sep=" ")
    for i in range(k):
        #Rundungsfehler pflanzen sich in der Iteration fort
        #Dadurch wird t_2n unsinnigerweise groesser als s_2n aber einem gewissen anzahl von verdopplungen   
        s_2n = s_2n/(sqrt(2+sqrt(4-s_2n**2)))
        #t_2n = (2*s_2n)/sqrt(4-s_2n**2)
        t_2n = (2*t_2n)/(sqrt(4+t_2n**2)+2)
        n *= 2
        print("n:", n, "i:", i, "pi:", (n*(s_2n+t_2n))/4, "diff:", t_2n-s_2n, sep=" ")
    return (n, (n*(s_2n+t_2n))/4, s_2n, t_2n)

@pytest.fixture(scope="module")
def k():
    return 29

@pytest.fixture(scope="module")
def t_n(k):
    s_2n = sqrt(2)
    for i in range(k):
        s_2n = s_2n/(sqrt(2+sqrt(4-s_2n**2)))
    return (2*s_2n)/sqrt(4-s_2n**2)


def test_archimedes1(k, t_n):
    n, pi, s, t = archimedes1(k)
    assert t_n == t

def test_archimedes2(k, t_n):
    print(t_n)
    n, pi, s, t = archimedes2(k)
    assert t_n == t