from Imprimir import *
tabla = [[]]
arregloFilas = []
arregloCol = []


class MetodoSimplex:

    sol_simplex = ''

    '''
    Clase en la cual se implementa el metodo simplex
    esto quiere decir que se lleva a cabo un gauss jordan
    verificacion si se encuentra en la solucion optima
    '''

    def __init__(self, tablaAux, arregloFilasAux, arregloColumnasAux, esMin):
        global tabla, arregloFilas, arregloCol
        tabla = tablaAux  # tabla donde se almacena la forma estandar
        arregloFilas = arregloFilasAux  # nombre de filas o variable basicas
        arregloCol = arregloColumnasAux  # nombre de columnas
        self.esMin = esMin  # booleano para saber si es minimizar o maximizar
        self.flagDg = False  # bandera de funcion degenerada

    def textSol(self):
        return self.sol_simplex

# verificar si el ciclo ya acabo
    '''
    Funcion que verifica si ya los valores de la fila U
    son negativos o 0 en caso de que se trate de maximizar
    para saber si ya se llego a la condicion de parada
    '''

    def optimoMax(self):
        global tabla
        for x in range(0, len(tabla[0])-2):
            valor = tabla[0][x].NUM
            if(valor > 0):
                return False
        return True

    '''
    Funcion que verifica si ya los valores de la fila U
    son positivos o 0 en caso de que se trate de minimizar
    para saber si ya se llego a la condicion de parada
    '''

    def optimoMin(self):
        global tabla
        for x in range(len(tabla[0])-2):
            # print(tabla[0][x].NUM)
            valor = tabla[0][x].NUM
            if(valor < 0):
                return False
        return True
    '''
    Funcion encargada de encontrar el mayor positivo
    para saber cual sera la columna Pivot
    '''

    def encontrarColPivotMax(self):
        global tabla
        indica = (tabla[0][0].NUM)
        col = 0
        for x in range(len(tabla[0])-2):
            if indica < (tabla[0][x].NUM):
                indica = (tabla[0][x].NUM)
                col = x
        return col
    '''
    Funcion encargada de encontrar el mas negativo
    para asi saber cual es la columna pivot
    '''

    def encontrarColPivotMin(self):
        global tabla
        indica = tabla[0][0].NUM
        col = 0

        for x in range(len(tabla[0])-2):
            if indica > tabla[0][x].NUM:
                indica = tabla[0][x].NUM
                col = x
        return col

    '''
    Funcion encargad de convertir el elemento[fila Pivot]
    [columna Pivot] en uno para ello se debe verificar que
    la division no sea entre 0
    '''

    def realizarDivision(self, columna):
        global tabla
        for x in range(1, len(tabla)):
            if tabla[x][columna] != 0:
                i = round(tabla[x][len(tabla[x])-2]/tabla[x][columna], 2)
                tabla[x][len(tabla[x])-1] = i
            else:
                tabla[x][len(tabla[x])-1] = 0

    '''
    Funcion encargada de encontrar cual es el menor positivo
    y asi poder encontrar el pivote en la iteraccion
    '''

    # OJO VERIFICAR QUE HAYAN POSITIVOS Y QUE NO HAYAN IGUALES MENORES POSITIVOS
    def hallarFilaPivot(self):
        global tabla  # indica siempre debera ser positivo
        indica = 1000
        fila = -1
        for x in range(1, len(tabla)):
            if(tabla[x][len(tabla[x])-1] > 0 and tabla[x][len(tabla[x])-1] < indica):
                indica = tabla[x][len(tabla[x])-1]
                fila = x
        return fila

    '''
    Funcion encargada de validar si corresponde a 
    minimizar o maximizar para luego poder encontrar la columna Pivot
    '''

    def elegirCol(self):
        if(self.esMin is True):
            return self.encontrarColPivotMax()  # self.encontrarColPivotMin()
        else:
            return self.encontrarColPivotMax()

    '''
    Funcion encargada de verificar si existen dos o mas coeficientes
    minimos con el mismo valor
    De esta forma verificamos si se trata de una funcion degenerada o no
    '''

    def degeneradaSolucion(self, fila):
        cont = 0

        for i in range(1, len(tabla)):
            if tabla[i][len(tabla[i])-1] == tabla[fila][len(tabla[i])-1]:
                cont += 1
                fila = i
        lista = [cont, fila]
        return lista

    '''
    Funcion que verifica si la bandera de degenerada
    esta activada en caso de que si, se realiza un print
    indicando al usuario 
    '''

    def verificarDegenerada(self, degenerada):
        if self.flagDg is True:
            self.sol_simplex += "\n\n-> Solucion Degenerada hubo empate en coef minimo en coef minimo en el estado:" + \
                str(degenerada)+"\n"
    '''
    Funcion invocada cuando existe una variable no basica con valor de 0 en la fila U
    , en dicha funcion se encuentra la fila pivot para realizar el gauss jordan correspondiente
    ademas de cambiar los valores en las variables basicas y finalmente imprimir la matriz
    indicando la solucion extra
    lo que recibe es la columna donde esta el 0 en U
    '''

    def solucionExtra(self, col):
        global tabla, arregloFilas, arregloCol
        impresion = Imprime()

        columnaPivot = col
        self.realizarDivision(columnaPivot)
        filaPivot = self.hallarFilaPivot()
        self.sol_simplex += "\n- Numero Pivot: " + \
            str(round(tabla[filaPivot][columnaPivot], 2))+",VB entrante: " + \
            arregloCol[columnaPivot] + \
            ",VB saliente: " + arregloFilas[filaPivot]
        self.convertir_Fila_Pivot(filaPivot, columnaPivot)
        self.modificar_Filas(filaPivot, columnaPivot)
        self.modificar_FilaZ(filaPivot, columnaPivot)
        auxFila = arregloFilas[filaPivot]
        arregloFilas[filaPivot] = arregloCol[columnaPivot]
        impresion.imprime_Matriz()
        self.sol_simplex += impresion.result_imprime()
        self.sol_simplex += "\n\n** Solucion EXTRA debido a que la variable no basica: " + \
            auxFila+" tenia un valor de 0 en el estado Final**"
    # ------------------------------------------------

    '''
    Funcion la cual se controla el metodo simplex
    en esta funcion se verifica la condicion de parada dependiendo
    si se trata de minimizar(positivos) y maximizar (negativos)
    Se encuentra la columna Pivot
    Se encuentra fila pivot para luego hacer el gauss jordan y llegar
     a la solucion optima
    '''

    def start_MetodoSimplex_Max(self):

        impresion = Imprime()
        estados = 0
        global tabla, arregloFilas, arregloCol
        print_Aux = Print()
        multiplesSol = Multiples_Solucion()
        s = Solucion()
        degenerada = 0
        s_Extra = Solucion()
        cont = 0
        # imprime matriz iteracion 0
        print_Aux.imprime_Matriz(tabla, arregloFilas, arregloCol)
        self.sol_simplex += print_Aux.print_result()
        while True:

            # Condicion de parada
            if self.optimoMax() is True and self.esMin is False or self.optimoMax() is True and self.esMin is True:
                self.verificarDegenerada(degenerada)  # DEGENERADA
                self.sol_simplex += print_Aux.print_result()
                self.sol_simplex += "\n- Estado Final\n"

                s.mostrarSolucion(tabla, arregloFilas, arregloCol, self.esMin)
                self.sol_simplex += s.solucionResult()

                # se verifican si existe una solucion multiple
                if multiplesSol.localizar_VB(tabla, arregloFilas, arregloCol) != -1:
                    # existen multiples soluciones
                    self.sol_simplex += "\n->Existen multiples soluciones\n"
                    self.solucionExtra(multiplesSol.localizar_VB(
                        tabla, arregloFilas, arregloCol))

                    # muestra solucin extra
                    s_Extra.mostrarSolucion(
                        tabla, arregloFilas, arregloCol, self.esMin)
                    self.sol_simplex += s_Extra.solucionResult()

                return tabla

            # Elige cual es el valor en U mas negativo o mas positivo
            columnaPivot = self.elegirCol()

            self.realizarDivision(columnaPivot)  # Convierte la columna Pivot

            filaPivot = self.hallarFilaPivot()

            if(filaPivot == -1):  # VERIFICA SOLUCION ACOTADA  # verificacion solucion acotada
                self.sol_simplex += "\n- Estado: " + str(estados)+"\n"
                self.sol_simplex += "** Solucion NO acotada  debido a que en la columnaPivot:" + \
                    str(columnaPivot) + \
                    " cada uno de los valores es negativo o 0 **"
                s.mostrarSolucion(tabla, arregloFilas, arregloCol, self.esMin)
                self.sol_simplex += s.solucionResult()
                return tabla  # break

            # verifica si se cumple con una funcin degenerada
            if self.degeneradaSolucion(filaPivot)[0] >= 2:
                self.flagDg = True
                filaPivot = self.degeneradaSolucion(filaPivot)[1]

                degenerada = estados+1

            self.sol_simplex += "\n- Estado: " + str(estados)
            estados += 1
            self.sol_simplex += "\n- Numero Pivot: " + \
                str(round(tabla[filaPivot][columnaPivot], 2)) + ",VB entrante: " + \
                arregloCol[columnaPivot] + \
                ",VB saliente: " + arregloFilas[filaPivot]
            arregloFilas[filaPivot] = arregloCol[columnaPivot]

            self.convertir_Fila_Pivot(
                filaPivot, columnaPivot)  # Metodo gauss jordan
            self.modificar_Filas(filaPivot, columnaPivot)
            self.modificar_FilaZ(filaPivot, columnaPivot)

            impresion.imprime_Matriz()
            self.sol_simplex += impresion.result_imprime()
    '''
    FUncion utilizada para el metodo gauss jordan 
    lo que se encarga es hacer el valor de la columna
    donde se encuentra el pivote en 0
    Multiplica el valor por la fila pivot y se lo resta
    '''

    def modificar_Filas(self, filaPivot, columnaPivot):
        global tabla
        for i in range(1, len(tabla)):
            if i != filaPivot:
                arg1 = tabla[i][columnaPivot]
                for j in range(0, len(tabla[i])-1):
                    x = tabla[i][j]-arg1*tabla[filaPivot][j]
                    tabla[i][j] = x

    '''
    FUncion utilizada para el metodo gauss jordan 
    lo que se encarga es hacer el valor de la columna
    donde se encuentra el pivote en 0
    Multiplica el valor por la fila pivot y se lo resta
    En este caso se realiza el procedimiento para la fila U
    '''

    def modificar_FilaZ(self, filaPivot, columnaPivot):
        global tabla
        lista = []
        lista2 = []
        for i in range(len(tabla[0])-2):

            arg2 = tabla[0][columnaPivot].NUM
            y = tabla[0][i].NUM-arg2*tabla[filaPivot][i]
            lista2.append(y)

        arg2 = tabla[0][columnaPivot].NUM

        if self.esMin is True:
            y = tabla[0][len(tabla[0])-2].NUM-arg2 * \
                tabla[filaPivot][len(tabla[0])-2]
        else:
            y = tabla[0][len(tabla[0])-2].NUM+arg2 * \
                tabla[filaPivot][len(tabla[0])-2]
        lista2.append(y)
        x = 0
        while x < len(lista2):
            tabla[0][x].NUM = lista2[x]
            x += 1

    '''
    Funcion encargada de hacer el valor pivote en uno
    para ello multiplica cada uno de los valores de
    la fila por 1/ ese valor arreglo[fila pivot][ columna Pivot]
    '''

    def convertir_Fila_Pivot(self, filaPivot, columnaPivot):

        if(tabla[filaPivot][columnaPivot] != 0):

            denominador = (1/tabla[filaPivot][columnaPivot])
        else:
            denominador = 1
        y = 0
        while y < len(tabla[filaPivot])-1:
            numerador = (tabla[filaPivot][y])
            x = numerador*denominador
            tabla[filaPivot][y] = x
            y += 1


# Impresion de la parte grafica
class Imprime:
    result = ''

    def __init__(self):
        pass
    # Constructor

    '''
    Funcion en la cual se imprimen el nombre
    correspondiente a cada una de las filas ya sea
    var de holgura artificial o basica
    '''

    def imprime_Columnas(self):
        global arregloCol
        aux = "\nputo\n\t"
        aux2 = "\t"
        for i in arregloCol:
            aux += i+"\t"
            aux2 += ""
        aux2 += ""
        self.result += aux+"\n"+aux2+"\n"

    def imprimeFilaU(self):
        global arregloFilas
        aux = arregloFilas[0]+"\t"
        for x in range(len(tabla[0])):
            var2 = round(tabla[0][x].NUM, 2)
            aux += str(var2)+"\t"
        self.result += aux+"\n"

    '''
    Funcion encargada de imprimir la primer matriz
    una vez se encuentre estandarizada
    '''

    def imprime_Matriz(self):
        global tabla, arregloFilas
        if(len(tabla) != 0):
            aux = ""
            self.imprime_Columnas()
            self.imprimeFilaU()
            for i in range(1, len(tabla)):
                aux = arregloFilas[i]+"\t"
                for j in range(len(tabla[i])):
                    var = round(tabla[i][j], 2)
                    aux += str(var)+"\t"
                self.result += aux+"\n"

    def result_imprime(self):
        return self.result
