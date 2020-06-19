from Controlador import *
import numpy as np

matrizTrans = []  # matriz a usar como transpuesta
matrizNueva = []  # matriz que se va usar para agregar las de holgura y artificial
listaZ = []  # lista donde se guarda el resultado de Z con las variables agregadas
listaNueva = []
masHolgura = 0  # variable para llevar un contador de cuantas variables de holgura positivas se debe agregar
menosHolgura = 0  # variable para llevar un contador de cuantas variables de holgura negativas se debe agregar
artificial = 0  # variable para llevar un contador de cuantas variables de artificial se debe agregar
Result = ""  # Variable que amacenara el resultado


def getResult():
    return Result


# funcion que crea la matriz transpuesta vacia a partir del numero de variables y restricciones
def crearMatrizTrans(variables, restricciones):
    #Creacion de una matriz vacia
    for i in range(variables):
        matrizTrans.append([])
        for j in range(restricciones+2):
            matrizTrans[i].append(None)   

#Agarra la funcion objetivo y cada una de las restricciones y le agrega las de holgura que llevan cada una 
def agregarHA(variables,restricciones):
    global menosHolgura
    global masHolgura
    global artificial
    #agrega la fila de Z mas las variables de holgura y artificiales 
    for i in range(restricciones):
        listaZ.append(listaNueva[i])
    for j in range(masHolgura):
        listaZ.append(0)#agrega 0 porque las de holgura llevan 0 
    for i in range(menosHolgura):
        listaZ.append(0)#agrega 0 porque las de holgura llevan 0 

    listaZ.append(0)
    matrizNueva.append(listaZ)#Anade esa lista a la matriz que se va imprimir 

    #agrega cada restriccion en una lista con las variables de holgut=ra y artificial en 0 y las mete a la matriz
    for i in range(variables):
        listaRestriccion = []
        for j in range(restricciones):
            listaRestriccion.append(float(matrizTrans[i][j]))
        for x in range(menosHolgura):
            listaRestriccion.append(0)
        for x in range(masHolgura):
            listaRestriccion.append(0)

        listaRestriccion.append(float(matrizTrans[i][restricciones]))
        listaRestriccion.append(matrizTrans[i][restricciones+1])
        matrizNueva.append(listaRestriccion)

    #agregar los 1 de holgura y artificial
    for i in range(menosHolgura):
        matrizNueva[i+1][restricciones+i]=-1
    for i in range(masHolgura):
        matrizNueva[i+1][restricciones+menosHolgura+i]=1

    for i in matrizNueva:
        print(i," matrizNueva")

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


def dualMax(variables, restricciones, matrizX, listaVariables):
    global Result
    for i in range(restricciones):
        if matrizX[i][variables+1] == ">=":

            matrizX[i][variables+1] = "<="
            for j in range(variables+1):
                try:
                    aux = float(matrizX[i][j])
                    aux = -aux
                    matrizX[i][j] = str(aux)
                except:
                    pass

    # listaNueva contiene la nueva Min W
    for x in range(0, restricciones):
        # Le asigno a listaNueva los nuevos valores de Z
        listaNueva.append(matrizX[x][variables])

    # Con este for se tranpone la matriz con los datos de Z que estaban en listaVariables
    for x in range(variables):
        matrizTrans[x][restricciones] = listaVariables[x]
        matrizTrans[x][restricciones+1] = ">="

    # Con este for transpone la matrizX en la matrizTrans que sera la que vamos a utilizar
    for w in range(variables):
        for y in range(restricciones):
            matrizTrans[w][y] = matrizX[y][w]

    # Funcion para evaluar las restricciones y sumas las variables
    evaluarRestricciones(restricciones, variables)
    # Funcion que agrega las variables a cada fila
    agregarHA(variables, restricciones)

    for y in range(variables+1):
        if(y == 0):
            Result += "Z: "
            for coef in range(variables):
                if coef != 0 and int(matrizNueva[y][coef]) >= 0:
                    Result += " + "
                else:
                    Result += " "
                Result += str(matrizNueva[y][coef])+"x"+str(coef+1)
            Result += "\n"
        else:
            Result += "R"+str(y)+": "
            for coef in range(variables):
                if coef != 0 and int(matrizNueva[y][coef]) >= 0:
                    Result += " + "
                else:
                    Result += " "
                Result += str(matrizNueva[y][coef])+"x"+str(coef+1)
            Result += str(matrizNueva[y][-1])+" "+str(matrizNueva[y][-2])+"\n"

    for i in range(variables):
        for j in range(restricciones+1):
            try:
                matrizTrans[i][j] = float(matrizTrans[i][j])
            except:
                pass

    for i in range(len(listaNueva)):
        try:
            listaNueva[i] = float(listaNueva[i])
        except:
            pass
    Result += "\n * R = Var Artificial\n * S = Var Holgura\n * X = Var Decision\n\n"
    controlador = Controlador(True, listaNueva, matrizTrans, restricciones)
    controlador.inicioControlador()
    Result += controlador.solControlador()
    print('termino DualMax')

# Funcion de min que recibe las variables, restricciones, listaVariables que es la que contiene la fila de Z
# y tambien matrizX que es la que nos manda la interfaz


def dualMin(variables, restricciones, matrizX, listaVariables):
    global Result
    for i in range(restricciones):
        if matrizX[i][variables+1] == "<=":

            matrizX[i][variables+1] = ">="
            for j in range(variables+1):
                try:
                    aux = float(matrizX[i][j])
                    aux = -aux
                    matrizX[i][j] = str(aux)
                except:
                    pass

    # listaNueva contiene la nueva Min W
    for x in range(restricciones):
        # Le asigno a listaNueva los nuevos valores de Z
        listaNueva.append(matrizX[x][variables])

    # Con este for transpone la matrizX en la matrizTrans que sera la que vamos a utilizar
    for w in range(variables):
        for y in range(restricciones):
            matrizTrans[w][y] = matrizX[y][w]

    # Con este for se tranpone la matriz con los datos de Z que estaban en listaVariables y depende de signo lo cambia ya que es la funcion de MIN
    for x in range(variables):
        matrizTrans[x][restricciones] = listaVariables[x]
        matrizTrans[x][restricciones+1] = "<="

    evaluarRestricciones(restricciones, variables)
    agregarHA(variables, restricciones)

    # imprimir matriz en forma ordenada
    Result += "Minimo\n"
    for y in range(variables+1):
        if(y == 0):
            Result += "\tZ: "
            for coef in range(variables):
                if coef != 0 and int(matrizNueva[y][coef]) >= 0:
                    Result += " + "
                else:
                    Result += " "
                Result += str(matrizNueva[y][coef])+"x"+str(coef+1)
            Result += "\nSujeto a:\n"
        else:
            Result += "\tR"+str(y)+": "
            for coef in range(variables):
                if coef != 0 and int(matrizNueva[y][coef]) >= 0:
                    Result += " + "
                else:
                    Result += " "
                Result += str(matrizNueva[y][coef])+"x"+str(coef+1)
            Result += str(matrizNueva[y][-1])+" "+str(matrizNueva[y][-2])+"\n"

    for i in range(variables):
        for j in range(restricciones+1):
            try:
                matrizTrans[i][j] = float(matrizTrans[i][j])
            except:
                pass

    for i in range(len(listaNueva)):
        try:
            listaNueva[i] = float(listaNueva[i])
        except:
            pass
    Result += "\n * R = Var Artificial\n * S = Var Holgura\n * X = Var Decision\n\n"
    controlador = Controlador(False, listaNueva, matrizTrans, restricciones)
    controlador.inicioControlador()
    Result += controlador.solControlador()
    print('termino DualMin')
