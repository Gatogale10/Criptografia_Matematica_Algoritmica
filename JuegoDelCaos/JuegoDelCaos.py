import numpy as np
import math
import random
import matplotlib.pyplot as plt


#En el siguiente codigo veremos como realizar el juego del caos


def juego(puntos1, p0):

    p1 = dist(p0,puntos1[random.randint(0, len(puntos1) - 1)] )

    return p1


def dist(x,y):
    return [(x[0]+y[0])/2,(x[1]+y[1])/2]


if __name__ == '__main__':

    # Definimos los puntos en R^2 del juegos y su probabilidad.

    puntos = [  [0,0] , [0,8] , [4,4]   ]
    xp = []
    yp = []
    for i in range(len(puntos)):
        xp.append(puntos[i][0])
        yp.append(puntos[i][1])


    #Damos el punto mayor y menor en x y el punto mayor y menor en y.
    xp.sort()
    yp.sort()
    xmin = xp[0]
    xmax = xp[-1]
    ymin = yp[0]
    ymax = yp[-1]

    #Generamos un numero aleatorio entre los maximos y minimos de estos puntos

    rx =  xmax - (xmax-xmin)*random.random()
    ry = ymax - (ymax - ymin) * random.random()

    #Punto inicial en R^2
    p0 = [rx,ry]

    #La probabilidad es la misma para todos los puntos

    p = 1/ len(puntos)




    #Numero de iteraciones
    n =  200000
    #Arreglo donde guardamos los puntos
    punt = juego(puntos,p0)
    Ar = []
    Ar.append(punt)

    for i in range(n):
        punt = juego(puntos,punt)
        Ar.append(punt)


    #Graficamos los puntos
    # Graficamos los puntos
    Ar = np.array(Ar)
    plt.figure(figsize=(10, 8))
    plt.scatter(Ar[:, 0], Ar[:, 1], s=0.01, color='black', alpha=0.6)
    plt.title("Juego del Caos - Puntos Generados")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.grid(alpha=0.3)
    plt.show()

















