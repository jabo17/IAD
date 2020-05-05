import math

def sieb(n):
     #wir gehen davon aus: alle Zahlen sind PZ
     #Länge n+1, denn: wir wollen PZ bis n nicht n-1
    feld = [True]*(n+1) 
    primfeld = list()
    for i in range(2,n):
        if feld[i]==True:
            primfeld.append(i)
            j=i
            #streiche nun alle Vielfachen der PZ:
            while i*j<=n:
                feld[j*i] = False
                j=j+1
                
                
    return primfeld
 






