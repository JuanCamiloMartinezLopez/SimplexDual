# Impresion de la parte grafica

class Print:
    result = ''
    # Constructor

    def __init__(self):
        pass

    '''
    Funcion en la cual se imprimen el nombre
    correspondiente a cada una de las filas ya sea
    var de holgura artificial o basica
    '''

    def imprime_Columnas(self, arregloCol):

        aux = "\t"
        #aux2 = "\t"
        for i in arregloCol:
            aux += i+"\t"
        self.result += aux+"\n"

    '''
    Imprime la fila de U 
    '''

    def imprimeFilaU(self, tabla, arregloFilas):

        aux = arregloFilas[0]+"\t"
        for x in range(len(tabla[0])):
            result = round(tabla[0][x].NUM, 2)
            aux += str(result)+"\t"
        self.result += aux+"\n"

    '''
    Funcion encargada de imprimir la primer matriz
    una vez se encuentre estandarizada
    '''

    def imprime_Matriz(self, tabla, arregloFilas, arregloCol):

        if(len(tabla) != 0):
            aux = "\n"
            self.imprime_Columnas(arregloCol)
            self.imprimeFilaU(tabla, arregloFilas)
            for i in range(1, len(tabla)):
                aux = arregloFilas[i]+"\t"
                for j in range(len(tabla[i])):
                    result = round(tabla[i][j], 2)
                    aux += str(result)+"\t"
                self.result += aux + "\n"

    def print_result(self):
        return self.result


class Solucion:
    '''Impresion del resultado final'''
    result = ''

    def __init__(self):

        self.lista = []
        self.lista2 = []

    '''
    Funcion utilizada para verificar cuales variables
    son las basicas para luego mostrar la solucion
    de la forma U (x1 =0,...)
    '''

    def mostrarSolucion(self, tabla, arregloFilas, arregloCol, esMin):
        self.lista.append("U")
        self.lista2.append(str(round(tabla[0][len(tabla[0])-2].NUM, 2)))
        for i in range(1, len(arregloFilas)):
            self.lista.append(arregloFilas[i])

            self.lista2.append(tabla[i][len(tabla[i])-2])

        self.colocar_Variables(arregloCol)
        self.imprimirVar()

    # coloca las variables que no son las basicas en la lista para luego imprimirlas
    def colocar_Variables(self, arregloCol):
        for i in range(0, len(arregloCol)-2):

            if arregloCol[i] in self.lista:
                continue
            else:
                self.lista.append(arregloCol[i])
                self.lista2.append(0)

    '''
    Funcion encargada de mostrar la respuesta final de
    la forma U = 332(x1:0,..)

    '''

    def imprimirVar(self):
        aux = "\n->Respuesta Final: U = " + \
            str(self.lista2[0])+"(" + str(self.lista[1]) + \
            ": " + str(round(self.lista2[1], 2))
        for i in range(2, len(self.lista)):
            aux += ","+str(self.lista[i]) + ": " + \
                str(round(self.lista2[i], 2))
        self.result += aux+" )"

    def solucionResult(self):
        return self.result


class Multiples_Solucion:
    '''
    Clase en la cual se verifica si el resultado final cuenta con 
    una solucion extra o no 
    '''

    def __init__(self):
        self.listaPosiciones = []

    def localizar_VB(self, tabla, arregloFilas, arregloCol):
        for i in range(1, len(arregloFilas)):
            self.listaPosiciones.append(arregloCol.index(arregloFilas[i]))

        return self.verificar_Multiples_Soluciones(tabla)

    '''
    Funcion en la cual se verifica si en la fila U
    existe alguna variable no basica con valor de 0 
    ya que debido a esto se considera que tiene soluciones
    extra
    '''

    def verificar_Multiples_Soluciones(self, tabla):
        for i in range(len(tabla[0])-2):
            if not i in self.listaPosiciones:
                if tabla[0][i].NUM == 0:
                    return i
        return -1
