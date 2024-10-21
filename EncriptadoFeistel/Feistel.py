# Primero creamos la función que nos regrese el k de los que es el multiplo de la cadena
# de bits
import numpy as np

#Declaramos la llave de encriptado como global
#tenemos que recordar que nuestra llave de encriptado tiene que ser del mismo
#orden o mayor de bits que el mensaje que vamos a encriptar.

w = 65580



def kfun(a:int):
    '''
    :param a: la cadena a cifrar
    :return: el multiplo de 16 que mide la cadena de bits
    '''

    for i in range(1,6):
        if( a <= (2**(16*i)) -1  ):
            return i

#Definimos la función con la cual vamos a obtener las llaves

def llaves(a:int):
    '''

    :param a: Mandamos a w para obtener las llaves
    :return: retornamos todas las llaves
    '''

    global w
    i = kfun(a)
    llave = []
    for j in range(i):
        llave.append(0)

    a = 0

    for j in range(1,i+1):

        llave[j-1] = w & ( 2 **(16*j)-1 - a )
        a = 2 **(16*j)-1
        llave[j-1] = llave[j-1] >>( 16*(j-1))
        llave[j-1] = llave[j-1] & ((2**(8))-1)



    return llave



def encriptado(a:int ):

    '''

    :param a: El mensaje a encriptar
    :return: el mensaje encriptado
    '''

    i = kfun(a)
    m = []
    for j in range(i):
        m.append(0)

    llave = llaves(a)

    b = 0

    for j in range(1,i+1):


        m1 = a & ( ( 2 **(16 * j) ) - 1 - b)

        b = (2 ** (16 * j)) - 1

        m1 = m1 >> (16*(j-1))


        L = m1 & ( (2**(16))- 1  - ((2**(8))-1)   )
        L = L >> 8


        R = m1 & ((2**(8))-1)


        R = R ^ llave[j-1]




        R = (L ^ R) << 8

        m[j-1] = R | L

    #M es un arreglo el cual tiene m1 , m2 y m3 encriptados
    #Ahora buscamos pegarlo m4,m3,m2,m1 de esta forma.
    #Funcion pegado
    mf = FuncionDePegado(m,i)

    return mf





def FuncionDePegado(m,i):
    '''

    :param m: Es el arreglo que contiene a m4 m3 m2 m1
    :return: vamos a regresar el entero que representa concatenar estos bits
    '''

    #Vamos a pegar m3m2m1
    #primero vamos a convertirlos al orden de bits que corresponden

    m1 = []
    for j in range(i):
        m1.append(0)
    m2 = m[0]

    for j in range(i):
        m1[j] = m[j] * (2 **(16*j))


    for j in range(1,i):
        m2 = m2 | ( m1[j] * (2 **(16*j)) )



        
    return m2

def desencriptado(a):
    global w
    i = kfun(a)

    m = []
    for j in range(i):
        m.append(0)

    llave = llaves(w)

    b = 0

    for j in range(1, i+1):
        m1 = a & ( (2 ** (16 * j)) - 1 - b)

        b = (2 ** (16 * j)) - 1
        m1 = m1 >> 16 * (j - 1)
        L = m1 & ((2 ** (16)) - 1)
        L = L >>8
        R = m1 & ((2 ** (8)) - 1)
        L = L  ^ R

        L = L ^ llave[j-1]



        R << 8


        m[j - 1] = R | L





    mf = FuncionDePegado(m,i)


    return mf


if __name__ == '__main__':

    a = 65616
    print("Mensaje encriptado")
    mf = encriptado(a)
    print(mf)

    md = desencriptado(mf)
    i = kfun(a)
    j = kfun(md)
    if i > j:
        print("Fallo")
        md = md | (2**(16*(i-j)))
    print("Mensaje desencriptado")
    print(md)






