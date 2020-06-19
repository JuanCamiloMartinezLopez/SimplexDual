from MetodoSimplex import*
tabla = [[]]
variablesDecision = 0
arregloCol = []
arregloFilas = ["Z"]
arregloZ = []
arregloZ2 = []


class Z_Aux:
    '''
    Clase en la cual se cuenta con un constructor encargado de 
    crear un objeto el cual tiene como atributo numero y letra valor 
    la cual hace referencia a la columna en que se ubique
    '''

    def __init__(self, NUM, letra):

        self.NUM = NUM
        self.letra = letra

# crear Z


class Z:
    '''
    Clase la cual recibe como parametro si se trata de minimizar o 
    maximizar, ademas de una lista de lista en la cual se encuentran
    las restricciones en formato de [[3,2,1,"<="]] en donde los numeros
    corresponden a float y el simbolo es un string

    '''

    def __init__(self, arreglo, esMin, u):
        self.esMin = esMin
        self.restricciones = arreglo
        self.u = u


    '''
    Funcion en la cual se crean los objetos
    correspondientes a las variables basicas
    con sus respectivos atributos del numero y
    letra ya sea x1 x2 etc
    Ademas se agrega la solucion identificada mediante SOL
    '''

    def crearZ(self):

        global tabla
        self.convertirNulo_ObjetosU()
        for i in range(len(self.u)):
            global arregloZ
            if self.esMin == True:
                z = Z_Aux(self.u[i]*-1, "x"+str(i+1))
            else:
                z = Z_Aux(self.u[i], "x"+str(i+1))
            arregloZ.append(z)
        sol = Z_Aux(0, "SOL")
        arregloZ.append(sol)
        

    '''
    Funcion la cual va agregando va recorriendo restriccion por restriccion
    para realizar la suma correspondiente de acuerdo al despeje
    de las variables artificiales con los valores de la funcion objetivo
    '''

    def agregarRestricciones(self):
        global arregloZ
        for i in range(len(self.restricciones)):

            if self.restricciones[i][len(self.restricciones[i])-1] != "<=":
                # por que los dos ultimos son solucion y simbolo
                for j in range(len(self.restricciones[i])-2):
                    # si lo encontro devuelve la pos donde esta si no -1
                    if self.buscarArreglo("x"+str(j+1)) != -1:
                        # si es minimizar lo deja igual
                        numero = self.verificarMinX(self.restricciones[i][j])

                # si es minimizar lo multiplica*-1
                numero = self.verificarMinX(
                    self.restricciones[i][len(self.restricciones[i])-2])
                x = self.buscarArreglo("SOL")

            self.cambiarSignos()

    '''
    Funcion que cambia el signo del numero en la fila Z
    '''

    def cambiarSignos(self):
        global arregloZ, tabla
        arregloZ[len(arregloZ)-1].NUM = arregloZ[len(arregloZ)-1].NUM*-1

        for x in range(len(arregloZ)):
            tabla[0][self.ubicar_En_Tabla(arregloZ[x])] = arregloZ[x]

    '''
    Funcion la cual se utiliza para ubicar en la tabla
    el elemento de la fila U
    '''

    def ubicar_En_Tabla(self, elemento):
        global arregloCol
        for x in range(len(arregloCol)):
            if elemento.letra == arregloCol[x]:
                return x
        return -1

    ''' 
    Funcion que se utliza para 
    la creacion de objetos pertenecientes a las 
    variables de holgura en donde el valor del numero 
    corresponde a 0 0
    '''

    def convertirNulo_ObjetosU(self):
        for x in range(len(arregloCol)):
            z = Z_Aux(0, arregloCol[x])
            tabla[0][x] = z


class Matriz:

    def __init__(self, arreglo):
        self.matriz = arreglo

    def cantidad_filas(self):
        if(len(self.matriz) != 0):
            global variablesDecision, tabla
            filas = variablesDecision+2  # col solucion y col division
            for i in range(len(self.matriz)):
                indica = self.matriz[i][len(self.matriz[i])-1]
                filas += self.cantidad_filasAux(indica)
        tabla = [[0 for i in range(filas)] for i in range(len(self.matriz)+1)]

    # verifica si va necesitar el espacio para R y -S
    def cantidad_filasAux(self, argument):
        switcher = {">=": 2}
        return switcher.get(argument, 1)

    def variablesX(self):
        global variablesDecision
        for i in range(0, variablesDecision):
            arregloCol.append("x"+str(i+1))


class Restricciones:

    def __init__(self, arreglo, esMin):
        self.matriz = arreglo
        self.varR = 1
        self.varS = 1
        self.esMin = esMin
    '''
    Funcion en la cual se colococan dentro de la tabla general a utilizar
    un 1 0 -1 a las variables correspondientes a las artificiales
    '''

    def colocar_Restricciones(self):
        global variablesDecision
        posicion = variablesDecision-1  # aumenta en R y S

        for i in range(len(self.matriz)):
            for j in range(len(self.matriz[i])-2):
                tabla[i+1][j] = self.matriz[i][j]
            m = Matriz(self.matriz)
            self.verificar_Signo(self.matriz[i][len(self.matriz[i])-1])
            x = m.cantidad_filasAux(self.matriz[i][len(self.matriz[i])-1])
            posicion += x
            tabla[i+1][len(tabla[i])-2] = self.matriz[i][len(self.matriz[i])-2]
            if x == 2:
                tabla[i+1][posicion-1] = 1
                tabla[i+1][posicion] = -1
            else:
                tabla[i+1][posicion] = 1
        arregloCol.append("SOL")
        arregloCol.append("DIV")


    def MayorIgual(self):
        arregloCol.append("R"+str(self.varR))
        arregloCol.append("S"+str(self.varS))
        arregloFilas.append("R"+str(self.varR))
        z = Z_Aux(0, "S"+str(self.varS))
        global arregloZ
        arregloZ.append(z)
        self.varR += 1
        self.varS += 1

    def verificar_Min(self, argument):  # verifica que se trate de minimizar o maximizar
        switcher = {True: 1}
        return switcher.get(argument, -1)


    def MenorIgual(self):
        arregloCol.append("S"+str(self.varS))
        arregloFilas.append("S"+str(self.varS))
        self.varS += 1


    def Igual(self):
        arregloCol.append("R"+str(self.varR))
        arregloFilas.append("R"+str(self.varR))
        self.varR += 1

    def verificar_Signo(self, signo):  # verifica cual signo corresponde a la restriccion
        switcher = {">=": self.MayorIgual,
                    "<=": self.MenorIgual, "=": self.Igual}
        switcher[signo]()


class Controlador:

    result = ''
    '''
    Metodo main en donde se llaman a las funciones para
    la implementacion del metodo simplex
    '''

    def __init__(self, minimo, U, restricciones, vars):
        global variablesDecision
        variablesDecision = vars
        self.esMinimizar = minimo  # se recibe
        self.arregloZ = U
        self.arregloEntrada = restricciones

    '''
    Funcion en la cual se controla la creacion del areglo con objetos
    pertenecientes a la fila U, ademas se crea la tabla de forma estandarizada
    '''

    def solControlador(self):
        return self.result

    def inicioControlador(self):
        matriz = Matriz(self.arregloEntrada)  # crea objeto para la impresion
        matriz.cantidad_filas()  # crea la tabla
        matriz.variablesX()
        restricciones = Restricciones(self.arregloEntrada, self.esMinimizar)
        restricciones.colocar_Restricciones()

        z = Z(self.arregloEntrada, self.esMinimizar, self.arregloZ)
        z.crearZ()
        z.agregarRestricciones()

        global arregloFilas, arregloCol, tabla

        MS = MetodoSimplex(tabla, arregloFilas, arregloCol, self.esMinimizar)
        matrizDual = MS.start_MetodoSimplex()
        self.result = MS.textSol()
        arregloDual = self.imprimirResultadoDual(matrizDual)
        self.result += "\nSoluciones del problema original\n"
        for i in range(len(arregloDual)):
            self.result += "X"+str(i+1)+" = "+str(arregloDual[i])+"\n"

    def imprimirResultadoDual(self, matrizDual):
        arregloDual = []
        for i in range(len(matrizDual[0])):

            if matrizDual[0][i].letra != "SOL":
                if "S" in matrizDual[0][i].letra:
                    arregloDual.append((round(matrizDual[0][i].NUM*-1, 2)))
        return arregloDual
