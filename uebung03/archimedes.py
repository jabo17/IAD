import math

#seitenlänge inneres n-eck
def innereseck(k):
    if (k > 1):
        return math.sqrt(2-math.sqrt(4-innereseck(k-1)**2))
    else: 
        return math.sqrt(2-math.sqrt(4-math.sqrt(2)**2))

#seitenlänge #äußeres n-eck
def aessereseck(k):
    if (k > 1):
        return (2/aessereseck(k-1))*(math.sqrt(4+aessereseck(k-1)**2)-2)
    else:
        return (2/4)*(math.sqrt(4+4**2)-2)

def archimedes1(k):
    eckenzahl = 2**k *4
    obereschranke = eckenzahl/2 * aessereseck(k)
    untereschranke = eckenzahl/2 * innereseck(k)

    print("var1:")
    print("Anzahl der Verdopplungen:", k)
    print("Anzahl der Ecken:", eckenzahl )
    print("oberer Schätzwert:", obereschranke)
    print("unterer Schätzwert:", untereschranke)
    print("Differenz der Schranken:", obereschranke -untereschranke)
#(b)
#folgende Beobachtungen für große n:
#für n=27 obere Schätzwert =0.0
#         unterer Schätzwert = 4.0,
#  wir haben eine Auslöschung, denn: 
# in aessereseck wird in der Klammer (sqr(4+(t_n)^2)-2) berechnet. Für ein hinreichend kleines n wird 
# durch die Addition mit 4, der 64 Bit Speicher für float nicht mehr ausreichen, um die kleinen Nachkommastellen
#(in unserem Fall: die Zahl 2.6374*10^(-16)) noch darzustellen. Sie werden einfach abgeschnitten und
#wir erhalten sqr(4)-2 = 0 und damit insgesamt 0 als Ergebnis

#(c) besser Version

def innercorner (k):
    if (k>1):
        return innercorner((k-1))/(math.sqrt(2+math.sqrt(4-innercorner((k-1))**2)))
    else:
        return math.sqrt(2)/math.sqrt(2+math.sqrt(4-2))

def outsidecorner(k):
    if (k>1):
        return (2*outsidecorner(k-1))/(math.sqrt(4+outsidecorner(k-1)**2)+2)
    else:
        return (2*4)/(math.sqrt(4+4**2)+2)

#zweite Variante von Archimedes:
def archimedes2(k):
    eckenzahl = 2**k *4
    obereschranke = eckenzahl/2 * outsidecorner(k)
    untereschranke = eckenzahl/2 * innercorner(k)

    print("var2:")
    print("Anzahl der Verdopplungen:", k)
    print("Anzahl der Ecken:", eckenzahl )
    print("oberer Schätzwert:", obereschranke)
    print("unterer Schätzwert:", untereschranke)
    print("Differenz der Schranken:", obereschranke -untereschranke)

#die neuen Formeln sind besser, weil wir fast nur + operationen auführen und so keine Auslöschung 
#durch subtraktion entstehen kann, an dre einzigen Stelle, an der - operation (in s_n)ausgeführt wird, kann
#keine Null entstehen, weil anschließend wieder addiert. (blah hier bitte noch einfügen)

#pro Verdopplung bekommt man in etwa 1 zusätzliche Dezimalstelle für kleine n von pi

#(d)


        

#main
archimedes2(7)
