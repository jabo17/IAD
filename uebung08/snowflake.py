import math
#Berechnung der neuen Punkte:
#Q_11 = (a_1 + 1/3 (b_1-a_1))
# Q_12 = (a_2+ 1/3 (b_2-a_2))
# analog für Q_2
#
#die Spitze des Dreiecks wird brechenet duch die euklidische Norm:
# v = b - a
# L = \lver v \rvert _2 = sqrt((b_1-a_1)**2 + (b_2-a_2)**2)
# v_senkrecht = (v_11, -v_12)
#
# Pythagoras: ermittle die gewünschte Länge von v(wie alpha gewählt wird, damit |alpha*v|_2 = gewünschte Länge)
# gewünschte Länge = (L/3)**2 - (L/6)**2
# a = sqrt(N/(vsenkrecht_11**2 + vsenkrecht_12**2))
#
#nun können wir mittels des Mittelpunktes Q_3 ermitteln:
#MP = ((a_1+b_1)/2, (b_2+a_2)/2)
#Q_3 = ((Ma_1 + a*vsenkrecht_11), (Ma_2 + alpha*vseknrecht_12))

def koch_snowflake(level):
    result_x = []
    result_y = []
    a = (0.,0.)
    b = (1.,0.)
    c = (1./2, math.sqrt(3)/2)
    print(c)
    result_x, result_y = snow_help(a,b, level, result_x, result_y)
    result_x, result_y = snow_help(b,c, level, result_x, result_y)
    result_x, result_y = snow_help(c,a, level, result_x, result_y)
    return result_x, result_y

def snow_help(a, b, level, result_x, result_y):
    if level == 0:
        result_x.append(a[0])
        result_x.append(b[0])
        result_y.append(a[1])
        result_y.append(b[1])
        #print(result_x,result_y)
    else:
        #print("a: ", a,b)
        v = (b[0]-a[0], b[1]-a[1])
        v_vertical = (v[1], -v[0])
        length = math.sqrt(v[0]**2 + v[1]**2)
        searched_length = (length/3)**2 - (length/6)**2 

        Q_1 = (a[0]+1./3* v[0], a[1]+1./3* v[1] )
        result_x, result_y = snow_help(a, Q_1, level -1, result_x, result_y)
       

        alpha = math.sqrt(searched_length / (v_vertical[0]**2 + v_vertical[1]**2))
        MP = ((a[0]+b[0])/2, (b[1]+a[1])/2)
        Q_3 = ((MP[0] + alpha*v_vertical[0]), (MP[1] + alpha*v_vertical[1]))


        result_x, result_y = snow_help( Q_1, Q_3, level -1, result_x, result_y)
        
        Q_2 = (a[0]+2./3* v[0], a[1]+2./3* v[1] )

        result_x, result_y = snow_help( Q_3, Q_2, level -1, result_x, result_y)

        result_x, result_y = snow_help(Q_2, b, level -1, result_x, result_y)
    return result_x, result_y

def test_snowflake(): 
    koch_snowflake(2)

#main
# import matplotlib.pyplot as plt
points_x, points_y = koch_snowflake(4)
# plt.plot(points_x, points_y) # zeichne die Punkte aus Teilaufgabe b)
# plt.gca().set_aspect('equal') # skaliere x- und y-Achse gleich
# plt.savefig('snowflake.svg') # speichere die Zeichnung

#in txt datei abspeichern
data = open("snowflake.txt", "w")
for zx,zy in zip(points_x, points_y):
    data.write('{} {}\n'.format(zx, zy))
data.close()
