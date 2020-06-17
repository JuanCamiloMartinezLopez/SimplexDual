from tkinter import *
from Dual import *
from Imprimir import*
from tkinter.scrolledtext import ScrolledText

listaCambiada = []
matrizX = []
listaVariables = []


def modificar(variables, restricciones, opcion):
    print('listaCambiada:', listaCambiada)
    crearMatrizTrans(variables, restricciones)
    listaVariables = listaCambiada[:variables]
    print('ListaVariables:', listaVariables)
    listaRestriccionese = listaCambiada[variables:]
    filas = variables+2
    print('ListaRestricciones:', listaRestriccionese)
    matrizX = [listaRestriccionese[filas*i: filas *
                                   (i+1)] for i in range(restricciones)]
    print('matrizX', matrizX)
    if(opcion == "Máximo"):
        dualMax(variables, restricciones, matrizX, listaVariables)
    else:
        dualMin(variables, restricciones, matrizX, listaVariables)


class datos:

    frame = None
    tipo = None
    numX = None
    numR = None
    elements = []
    funcEspacios = []

    def __init__(self, root):
        # Se Inicia el frame del titulo
        frameTitle = Frame(root)
        frameTitle.pack(side=TOP)
        l1 = Label(frameTitle, text="Simplex Dual")
        l1.grid(row=0)
        l1.config(fg="red", font=1000)
        # Se instancia el frame principal
        self.frame = Frame(root)
        self.frame.pack()

        self.TipoDeProblema()

    def TipoDeProblema(self):
        self.clearFrame()
        tipo = ["Maximo", "Minimo"]
        self.opcion = StringVar()
        self.opcion.set(tipo[0])

        espacio = Label(self.frame, text="")
        espacio.grid(row=1)
        self.elements.append(espacio)

        l1 = Label(self.frame, text="Escoja el tipo del problema: ")
        l1.grid(row=2)
        self.elements.append(l1)
        opciones = OptionMenu(self.frame, self.opcion, *tipo)
        opciones.grid(row=3, column=0)
        self.elements.append(opciones)

        l1 = Label(self.frame, text="Variables")
        l1.grid(row=4)
        self.elements.append(l1)
        self.variables = Spinbox(self.frame, from_=2, to=5,
                                 state="readonly", width=10)
        self.variables.grid(row=5)
        self.elements.append(self.variables)

        l1 = Label(self.frame, text="Restricciones")
        l1.grid(row=6)
        self.elements.append(l1)
        self.restricciones = Spinbox(
            self.frame, from_=2, to=5, state="readonly", width=10)
        self.restricciones.grid(row=7)
        self.elements.append(self.restricciones)

        boton = Button(self.frame, text="Enviar", relief=RAISED, command=lambda: self.DatosDelProblema(
            self.opcion.get(), self.variables.get(), self.restricciones.get()))
        boton.grid(row=8)
        self.elements.append(boton)

        espacio = Label(self.frame, text="")
        espacio.grid(row=9)
        self.elements.append(espacio)

    def clearFrame(self):
        if len(self.elements) != 0:
            for element in self.elements:
                element.destroy()
            self.elements.clear()

    def DatosDelProblema(self, opcion, variables, restricciones):
        self.tipo = opcion
        self.numX = int(variables)
        self.numR = int(restricciones)
        self.clearFrame()
        columna = 0
        func = Label(self.frame, text=self.tipo+" = ")
        func.grid(row=0, column=columna)
        self.elements.append(func)
        columna += 1

        self.funcEspacios.append([])
        for i in range(self.numX):

            coe = Entry(self.frame, width=5, relief=RAISED)
            self.funcEspacios[0].append(coe)  # necesito control de cuadritos
            coe.grid(row=0, column=columna)
            self.elements.append(coe)
            columna += 1

            x = "x"+str(i+1)
            xpos = Label(self.frame, text=x)
            xpos.grid(row=0, column=columna)
            self.elements.append(xpos)
            columna += 1

            if i+1 != self.numX:
                suma = Label(self.frame, text=" + ")
                suma.grid(row=0, column=columna)
                self.elements.append(suma)
                columna += 1

        for i in range(1, self.numR+1):
            columCount = 0
            self.funcEspacios.append([])
            for y in range(0, self.numX):
                cuadrito = Entry(self.frame, width=5, relief=RAISED)
                # necesito control de cuadritos
                self.funcEspacios[i].append(cuadrito)
                cuadrito.grid(row=i, column=columCount)
                self.elements.append(cuadrito)
                columCount += 1

                x = "x"+str(y+1)
                xpos = Label(self.frame, text=x)
                xpos.grid(row=i, column=columCount)
                self.elements.append(xpos)
                columCount += 1

                if y+1 != variables:
                    suma = Label(self.frame, text=" + ")
                    suma.grid(row=i, column=columCount)
                    self.elements.append(suma)
                    columCount += 1
            simbolo = [">=", "<=", "="]
            simb = StringVar()
            simb.set(simbolo[0])
            menuOpciones = OptionMenu(self.frame, simb, *simbolo)
            menuOpciones.grid(row=i, column=columCount)
            self.elements.append(menuOpciones)
            columCount += 1

            cuadrito = Entry(self.frame, width=5, relief=RAISED)
            # necesito control de cuadritos
            self.funcEspacios[i].append(cuadrito)
            cuadrito.grid(row=i, column=columCount)
            self.elements.append(cuadrito)
            columCount += 1

            self.funcEspacios[i].append(simb)

        boton = Button(self.frame, text="Aceptar", relief=RAISED,
                       command=lambda: self.printear())
        boton.grid(row=self.numR+2, column=0, sticky=W)
        self.elements.append(boton)

        back = Button(self.frame, text="Atras", relief=RAISED,
                      command=lambda: self.TipoDeProblema())
        back.grid(row=self.numR+2, column=1, sticky=W)
        self.elements.append(back)

    def printear(self):
        simbolos = []
        for s in range(1, len(self.funcEspacios)):  # simbolos de restricciones
            simbolos.append(self.funcEspacios[s][-1].get())

        resultado = []
        resultado.append(self.tipo)  # pega la opcion max o min
        # pega num variablesy restricciones
        resultado.append(str(self.numX)+","+str(self.numR))

        linea = []
        for x in self.funcEspacios[0]:
            linea.append(x.get())
        resultado.append(linea)  # pega la funcion max o min

        for x in range(1, self.numR+1):
            linea = []
            for y in range(0, len(self.funcEspacios[x])-1):
                linea.append(self.funcEspacios[x][y].get())
            linea.append(simbolos[x-1])
            resultado.append(linea)  # pega lineas de la matriz
        for lis in range(2, len(resultado)):
            for lisItem in resultado[lis]:
                print(lisItem)
                listaCambiada.append(lisItem)
        self.clearFrame()
        ResultText = ScrolledText(self.frame, width=70, height=20)
        ResultText.grid(row=0)

        boton = Button(self.frame, text="Reiniciar", relief=RAISED,
                       command=lambda: self.TipoDeProblema())
        boton.grid(sticky=W)
        self.elements.append(boton)

        back = Button(self.frame, text="Atras", relief=RAISED,
                      command=lambda: self.DatosDelProblema())
        back.grid(sticky=W)
        self.elements.append(back)

        print('Variables:', self.numX)
        print('Restricciones:', self.numR)
        modificar(self.numX, self.numR, self.tipo)
        print('Resultado:', resultado)


root = Tk()
root.title("Simplex Dual")
root.iconphoto(False, PhotoImage(file='ecuacion.png'))
root.geometry("600x400")
root.resizable(True, True)
matriz = datos(root)
root.mainloop()
