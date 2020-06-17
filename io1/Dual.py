from Controlador import *
import numpy as np

matrizTrans = [] #matriz a usar como transpuesta
matrizNueva = [] #matriz que se va usar para agregar las de holgura y artificial 
listaZFase1 = [] #lista donde se guarda el resultado de Z con las variables agregadas 
listaNueva = []
masHolgura=0 #variable para llevar un contador de cuantas variables de holgura positivas se debe agregar 
menosHolgura=0 #variable para llevar un contador de cuantas variables de holgura negativas se debe agregar
artificial=0 #variable para llevar un contador de cuantas variables de artificial se debe agregar


#funcion que crea la matriz transpuesta vacia a partir del numero de variables y restricciones    
def crearMatrizTrans(variables, restricciones):
    #Creacion de una matriz vacia
    for i in range(variables):
        matrizTrans.append([])
        for j in range(restricciones+2):
            matrizTrans[i].append(None)   

#Agarra la funcion objetivo y cada una de las restricciones y le agrega las de holgura y artificial que llevan cada una 
def agregarHA(variables,restricciones):
    global menosHolgura
    global masHolgura
    global artificial
    #agrega la fila de Z mas las variables de holgura y artificiales 
    for i in range(restricciones):
        listaZFase1.append(listaNueva[i])
    for j in range(masHolgura):
        listaZFase1.append(0)#agrega 0 porque las de holgura llevan 0 
    for i in range(menosHolgura):
        listaZFase1.append(0)#agrega 0 porque las de holgura llevan 0 
    for y in range(artificial):
        listaZFase1.append(-1)#agrega -1 porque las artificiales en Z llevan -1 al pasar del otro lado 
    listaZFase1.append(0)
    matrizNueva.append(listaZFase1)#Anade esa lista a la matriz que se va imprimir 

    #agrega cada restriccion en una lista con las variables de holgut=ra y artificial en 0 y las mete a la matriz
    for i in range(variables):
        listaRestriccion = []
        for j in range(restricciones):
            listaRestriccion.append(int(matrizTrans[i][j]))
        for x in range(menosHolgura):
            listaRestriccion.append(0)
        for x in range(masHolgura):
            listaRestriccion.append(0)
        for x in range(artificial):
            listaRestriccion.append(0)
        listaRestriccion.append(int(matrizTrans[i][restricciones]))
        listaRestriccion.append(matrizTrans[i][restricciones+1])
        matrizNueva.append(listaRestriccion)

    #agregar los 1 de holgura y artificial
    for i in range(menosHolgura):
        matrizNueva[i+1][restricciones+i]=-1
    for i in range(masHolgura):
        matrizNueva[i+1][restricciones+menosHolgura+i]=1
    for i in range(artificial):
        matrizNueva[i+1][restricciones+menosHolgura+masHolgura+i]=1

#Lleva los contadores de la cantidad de variables que se deben agregar y sino hay imprime que no hay signos 
def evaluarRestricciones(restricciones, variables):
    global menosHolgura
    global masHolgura
    global artificial
    for i in range(variables):
        if(matrizTrans[i][restricciones+1] == ">="):
            artificial = artificial +1
            menosHolgura = menosHolgura +1
        elif(matrizTrans[i][restricciones+1] == "<="):
            masHolgura = masHolgura +1
        elif(matrizTrans[i][restricciones+1] == "="):
            artificial = artificial +1
        else:
            pass

#Funcion de max que recibe las variables, restricciones, listaVariables que es la que contiene la fila de Z
# y tambien matrizX que es la que nos manda la interfaz 
def dualMax(variables, restricciones,matrizX, listaVariables):

    for i in range(restricciones):
        if matrizX[i][variables+1] == ">=":

            matrizX[i][variables+1] = "<="
            for j in range(variables+1):
                try:
                    aux = int(matrizX[i][j])
                    aux = -aux;
                    matrizX[i][j] = str(aux)
                except:
                    pass

    #listaNueva contiene la nueva Min W
    for x in range(0,restricciones):
        listaNueva.append(matrizX[x][variables])#Le asigno a listaNueva los nuevos valores de Z

    #Con este for se tranpone la matriz con los datos de Z que estaban en listaVariables 
    for x in range(variables):
        matrizTrans[x][restricciones]=listaVariables[x]
        matrizTrans[x][restricciones+1]=">="

    #Con este for transpone la matrizX en la matrizTrans que sera la que vamos a utilizar 
    for w in range(variables):
        for y in range(restricciones):
            matrizTrans[w][y]=matrizX[y][w]       
    

    evaluarRestricciones(restricciones, variables)#Funcion oara evaluar las restricciones y sumas las variables 
    agregarHA(variables,restricciones)#Funcion que agrega las variables a cada fila 

    
    for y in range(variables+1):
        if(y==0):
            print("Z: " + str(matrizNueva[y]))
        else:
            print("R: " + str(matrizNueva[y]))

    for i in range(variables):
        for j in range(restricciones+1):
            try:
                matrizTrans[i][j] =  float(matrizTrans[i][j])
            except:
                pass

    for i in range(len(listaNueva)):
        try:
            listaNueva[i] =  float(listaNueva[i])
        except:
            pass


    controlador = Controlador(True,listaNueva,matrizTrans,restricciones)
    controlador.inicioControlador()
    
#Funcion de min que recibe las variables, restricciones, listaVariables que es la que contiene la fila de Z
# y tambien matrizX que es la que nos manda la interfaz 
def dualMin(variables, restricciones,matrizX, listaVariables):


    for i in range(restricciones):
        if matrizX[i][variables+1] == "<=":

            matrizX[i][variables+1] = ">="
            for j in range(variables+1):
                try:
                    aux = int(matrizX[i][j])
                    aux = -aux;
                    matrizX[i][j] = str(aux)
                except:
                    pass

    #listaNueva contiene la nueva Min W
    for x in range(restricciones):
        listaNueva.append(matrizX[x][variables])#Le asigno a listaNueva los nuevos valores de Z

    #Con este for transpone la matrizX en la matrizTrans que sera la que vamos a utilizar 
    for w in range(variables):
        for y in range(restricciones):
            matrizTrans[w][y]=matrizX[y][w]       

    #Con este for se tranpone la matriz con los datos de Z que estaban en listaVariables y depende de signo lo cambia ya que es la funcion de MIN
    for x in range(variables):
        matrizTrans[x][restricciones]=listaVariables[x]
        matrizTrans[x][restricciones+1]= "<="

    evaluarRestricciones(restricciones, variables)
    agregarHA(variables,restricciones)

    #imprimir matriz en forma ordenada
    for y in range(variables+1):
        if(y==0):
            print("Z: " + str(matrizNueva[y]))
        else:
            print("R: " + str(matrizNueva[y]))


    for i in range(variables):
        for j in range(restricciones+1):
            try:
                matrizTrans[i][j] =  float(matrizTrans[i][j])
            except:
                pass

    for i in range(len(listaNueva)):
        try:
            listaNueva[i] =  float(listaNueva[i])
        except:
            pass
    

    controlador = Controlador(False,listaNueva,matrizTrans,restricciones)
    controlador.inicioControlador()