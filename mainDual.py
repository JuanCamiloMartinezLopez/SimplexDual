from tkinter import *
from Dual import *
from Imprimir import*

listaCambiada = []
matrizX = []
listaVariables=[]


def modificar(variables,restricciones,decision):

    crearMatrizTrans(variables, restricciones)
    lista=[]
    for x in range(variables):
            listaVariables.append(listaCambiada[x])


    for y in range(variables, len(listaCambiada)):
            lista.append(listaCambiada[y])


    filas=variables+2
    matrizX = [lista[filas*i : filas*(i+1)] for i in range(restricciones)]



    if(decision.get() == "Máximo"):
            dualMax(variables,restricciones,matrizX, listaVariables)
    else:
            dualMin(variables,restricciones,matrizX, listaVariables)



class datos:

    def __init__(self, root):

        frame = Frame(root)
        frame.pack(side=TOP)
        tipo = ["Maximo","Minimo"]
        self.opcion = StringVar()
        self.opcion.set(tipo[0])

        l1 = Label(frame,text="Simplex Dual")
        l1.grid(row=0)
        l1.config(fg = "blue",font=1000)

        espacio = Label(frame,text="")
        espacio.grid(row=1)

        l1 = Label(frame,text="Escoja el tipo del problema: ")
        l1.grid(row=2)
        opciones = OptionMenu(frame,self.opcion,*tipo)
        opciones.grid(row=3,column=0)
        
        l1 = Label(frame,text="Variables")
        l1.grid(row=4)
        self.variables = Spinbox(frame,from_=2, to=5,state="readonly",width=10)
        self.variables.grid(row=5)

        l1 = Label(frame,text="Restricciones")
        l1.grid(row=6)
        self.restricciones = Spinbox(frame,from_=2, to=5,state="readonly",width=10)
        self.restricciones.grid(row=7)

        boton = Button(frame,text="Enviar", relief = RAISED,command = lambda:self.llenarMatriz(root,self.opcion,self.variables,self.restricciones,boton))
        boton.grid(row=8)

        espacio = Label(frame,text="")
        espacio.grid(row=9)


    def llenarMatriz(self,root,opcion,variables,restricciones,boton):
        boton.destroy()
        nvar = int(variables.get())
        nres = int(restricciones.get())
        frame = Frame(root)
        frame.pack(side=TOP)
        columna = 0
        func = Label(frame,text=opcion.get()+" = ")
        func.grid(row=0,column=columna)
        columna+=1

        funcEspacios = []
        funcEspacios.append([])
        for i in range(nvar):

            coe = Entry(frame,width=5,relief=RAISED)
            funcEspacios[0].append(coe)       #necesito control de cuadritos
            coe.grid(row=0,column=columna)
            columna+=1

            x = "x"+str(i+1)
            xpos = Label(frame,text=x)
            xpos.grid(row=0,column=columna)
            columna+=1

            if i+1!=nvar:
                suma = Label(frame,text=" + ")
                suma.grid(row=0,column=columna)
                columna+=1



        boton1 = Button(frame,text="Aceptar", relief = RAISED,command = lambda:self.restriccionesLlenar(root,self.opcion,nvar,nres,funcEspacios,boton1))
        boton1.grid(row=10,sticky=W)

    def restriccionesLlenar(self,master,opcion,variables,restricciones,funcEspacios,buttonx):
        buttonx.destroy()
        for p in funcEspacios:
            for q in p:
                q.config(state="readonly")
        frame4 = Frame(master)
        frame4.pack()


        for i in range(restricciones):
            columCount=0
            funcEspacios.append([])
            for y in range(0,variables):
                cuadrito = Entry(frame4,width=5,relief=RAISED)
                funcEspacios[i+1].append(cuadrito)       #necesito control de cuadritos
                cuadrito.grid(row=i,column=columCount)
                columCount+=1

                x = "x"+str(y+1)
                xpos = Label(frame4,text=x)
                xpos.grid(row=i,column=columCount)
                columCount+=1

                if y+1!=variables:
                    suma = Label(frame4,text=" + ")
                    suma.grid(row=i,column=columCount)
                    columCount+=1

            simbolo = [">=","<=","="]
            simb = StringVar()
            simb.set(simbolo[0])
            menuOpciones = OptionMenu(frame4,simb,*simbolo)
            menuOpciones.grid(row=i,column=columCount)
            columCount+=1

            cuadrito = Entry(frame4,width=5,relief=RAISED)
            funcEspacios[i+1].append(cuadrito)       #necesito control de cuadritos
            cuadrito.grid(row=i,column=columCount)
            columCount+=1


            funcEspacios[i+1].append(simb)


        self.button2 = Button(frame4,text="Aceptar", relief = RAISED,command = lambda:self.printear(self.opcion,variables,restricciones,funcEspacios,self.button2))
        self.button2.grid(row=10,sticky=W)


    def printear(self,opcion,variables,restricciones,funcEspacios,button2):

        button2.destroy()
        simbolos = []
        for s in range(1,len(funcEspacios)):            #simbolos de restricciones
            simbolos.append(funcEspacios[s][-1].get())

        resultado = []
        resultado.append(opcion.get())        #pega la opcion max o min
        resultado.append(str(variables)+","+str(restricciones)) #pega num variablesy restricciones

        linea = []
        for x in funcEspacios[0]:
            linea.append(x.get())
        resultado.append(linea)         #pega la funcion max o min

        for x in range(1,restricciones+1):
            linea = []
            for y in range(0,len(funcEspacios[x])-1):
                linea.append(funcEspacios[x][y].get())
            linea.append(simbolos[x-1])
            resultado.append(linea)     #pega lineas de la matriz


        for lis in range(2,len(resultado)):
            for lisItem in resultado[lis]:
                print(lisItem)
                listaCambiada.append(lisItem)



        modificar(variables,restricciones,opcion)
        print(resultado)


root = Tk()
root.title("Simplex Dual")
root.geometry("600x400")
root.resizable(True, True)
matriz = datos(root)
root.mainloop()
