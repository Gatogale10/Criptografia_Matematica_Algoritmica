

#Declaramos la llave

l = 189

#Declaramos las cajas como variables globales
S1=[[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
    [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
    [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
    [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]]

S2=[[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
    [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
    [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
    [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]]


#Declaramos la permutacion
perm = [0,1,2,3,4,6,5,7,8,9,10,11]
#perm = [0,1,2,3,4,5,6,7,8,9,10,11]

#Algoritmo de extension

def extension(d):

    #Extendemos la longitud del lado derecho a 12 bits
    l = (d & ( ((2**(8)) -1) - ((2**(4))-1) ) ) >> 4
    r = d & ( ( 2**(4)) -1 )

    b0 = (r & 1) << 5
    b3 = r & 8
    b3 = b3 >> 3

    b4 = ( l & 1) << 5
    b7 = l & 8
    b7 = b7 >> 3

    r = r << 1
    r = r | b4 | b7

    l = l<<1
    l = l | b0 | b3
    l = l << 6
    dext = l | r


    m = []
    m.append(l)
    m.append(r)

    #dext = FuncionDePegado(m,2)


    return dext


#Funcion para pegar dos mensajes
def FuncionDePegado(m, i):
    '''
    :param m: Es el arreglo que contiene a m4 m3 m2 m1
    :return: vamos a regresar el entero que representa concatenar estos bits
    '''

    # Vamos a pegar m3m2m1
    # primero vamos a convertirlos al orden de bits que corresponden

    m1 = []
    for j in range(i):
        m1.append(0)
    m2 = m[0]

    for j in range(i):
        m1[j] = m[j] * (2 ** (6 * j))

    for j in range(1, i):
        m2 = m2 | (m2[j] * (2 ** (6 * j)))

    return m2

#Funcion que aplica la permutación dada
def permutacion(ED):
    global perm

    # Vamos a aplicar la permutacion
    a = [12]

    for i in range(len(perm)):

        if perm[i] != i and (i not in a) :
            a.append(i)
            a.append(perm[i])

            s = ED & ( 2**(i))
            s1 = ED & ( 2**(perm[i]) )

            ED = ED  -s - s1

            s1 = (s1 >> ( 2**(perm[i]-i)) )
            s =  (s  << ( 2**(perm[i]-i)) )
            ED = ED + s + s1
    return ED


#Funcion para cortar el bit 3,7, 11 y 15
def cortarbits(k1):

    #Cortamos de 4 en 4 posiciones
    b1 = (k1 &  ( ( (2**4) -1 ) - (2**3)  ) )
    b2 = (k1 & ( ((2 ** 8) - 1) - ( (2**4)- 1 ) - (2**7) ) ) >> 1
    b3 = (k1 & ( ((2 ** 12) - 1) - ((2**8) - 1) - (2**11) )) >> 2
    b4 = (k1 & ( ((2 ** 16) - 1) - ((2 ** 12) - 1) - (2**15) ) ) >> 3
    k2 = b1 | b2 | b3 | b4

    return k2

#Vamos a generar las 4 llaves con la llave original
def llaves():

    global l

    l1 = l

    #Primero vamos a partir la llave en dos

    C =( (l1 & ( ((2 ** (16)) - 1) - ( (2 ** (8)) - 1) )) >> 8)
    D = l1 & ( (2 ** (8)) - 1 )

    # Vamos a generar las 4 llaves
    llave = []

    for i in range(4):
         llaves1 = []

         #Primero generamos la rotación hacia la derecha en dos posiciones
         # de esta misma rotacion o traslacion se generara las siguiente llave
         # y asi sucesivamente hasta llegar a la llave original.

         dk1 = (C & ( (2 **(6) ) - 1 ) ) << 2
         dk2 = (D & ( (2 **(6) ) - 1 ) ) << 2
         ck1 = (C & ( (2**7) + (2**6) )) >> 6
         ck2 = (D & ( (2**7) + (2**6) )) >> 6
         #Rotamos dos posiciones a la izquierda cada lado
         C = ((dk1 | ck1) << 8)
         D =  dk2 | ck2

         #Ahora esta es la nueva llave
         l1 = C | D

         #Ahora vamos a cortar el bit 3,7, 11 ,15

         k1 = cortarbits(l1)

         #print("llave 16")
         #print(l1)
         #print("Llave 12")
         #print(k1)
         # Declaremos a los nuevos C y D

         C = ((l1 & (((2 ** (16)) - 1) - ((2 ** (8)) - 1))) >> 8)
         D = l1 & ((2 ** (8)) - 1)

         llave.append(k1)

    return llave


#Buscamos la fila y las columnas
def box(a):

    b1 = a & 1
    b6 =(a & (2**5)) >> 4

    n = b1 | b6
    b25 = (a & ( 30 ) ) >> 1

    return n, b25


#Aplicamos las s-box a los dos lados
def sbox(L,R):
    global S1, S2

    n1 , b1 = box(L)
    n2 , b2 = box(R)

    return S2[n1][b1], S1[n2][b2]

#Funcion para encriptar el mensaje
def encriptado(a:int):

    #Primero separamos el mensaje en 8-bits y 8-bits
    C = (a & (   ((2**(16)) - 1) - ((2**(8))-1)      ) ) >> 8
    D = ( a & ( (2**(8)) -1 ) )


    #Realizamos el algoritmo de extension para el lado derecho de 8 a 12 bits

    #Vamos a realizar 4 permutaciones
    llav = llaves()

    #Realizamos la extension de 8 a 12 bits de lado derecho
    ED = extension(D)


    # Aplicamos la permutación
    EDp = permutacion(ED)



    for i in llav:

        # Realizamos el XOR con la llave
        EDp = EDp ^ i


        # Partimos en dos mitades
        L = (EDp & ( ((2**12) - 1) - ( (2**6) - 1  ) ) ) >> 6
        #L = L & (2**6 -1)
        R = EDp & (2**6 -1)

        # Imprimimos la s-box


        # Aplicamos la s-box a cada mitad
        L , R = sbox(L,R)

        # Imprimimos despues de aplicar las s-box


        # I
        L = L << 4



        # Pegamos a ambas y obtenemos a lado derecho
        EDp = (L | R)

        #Hacemos XOR con el lado izquiero
        EDp = ( (EDp ^ C ) << 8 )

        # Finalmente intercambiamos y pegamos
        a = EDp | C


        # Volvemos a realizar el algoritmo
        C = (a & (((2 ** (16)) - 1) - ((2 ** (8)) - 1))) >> 8
        EDp = (a & ((2 ** (8)) - 1))


        # Realizamos la extension
        ED = extension(EDp)


        # Aplicamos la permutacion
        EDp = permutacion(ED)


    #Tenemos el mensaje encriptado

    return a


# Ahora aplicamos

def desencriptado(a:int):
    a = 1


if __name__ == '__main__':
    #Decimos el mensaje a encriptar

    a = 23
    b = encriptado(a)
    print("----------------------------------------------------------------Encriptaddo--------------------------------------------------------------")

    print(f"Vamos a encriptar el mensaje: {a} ")
    print(f"Con la llave {l}")
    print(f"Mensaje encriptado : {b}")














