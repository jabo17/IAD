import math

def sieve(n):
     #wir gehen davon aus: alle Zahlen sind PZ
    feld = [True]*n 
    primfeld = list()
    for i in range(2,n):
        if feld[i]==True:
            primfeld.append(i)
            j=i
            #streiche nun alle Vielfachen der PZ:
            while i*j<n:
                feld[j*i] = False
                j=j+1
                
    return primfeld
 
print(sieve(1000))





