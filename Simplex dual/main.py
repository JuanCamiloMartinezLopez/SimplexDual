import numpy as np
def main():
	print ("Ingrese el tipo de problema a realizar")
	print ("1.Maximizar")
	print ("2.Minimizar")
	s = input()
	while s != "1" and s != "2":
		print("Dato incorrecto ingreselo nuevamente")
		s = input()
	if s == "1" :
		print("Es un problema de Maximizar ")
	elif s == "2":
		print("Es un problema de Minimizar ")
	tipo = s
	variables = int(input("Ingrese la cantidad de variables "))
	nres = int(input("Ingrese el numero de restricciones "))
	fobjetivo = np.arange(variables)
	for j in range(variables):
		print("Ingrese el valor del coeficiente X{a} de la funcion objetivo ".format(a = j+1))
		np.append(fobjetivo,int(input()))

	restricciones = np.ones((variables,nres))
	vaux = np.arange(nres)


	for k in range(nres):
		for j in range(variables):
			restricciones[k][j] = int(input("Ingrese el valor del coeficiente X{coe} de la restriccion {res} ".format(coe=j+1,res = k+1)))

		print("Ingrese el tipo de relacion ")
		print("1.<=")
		print("2.>=")
		print("3.=")
		relacion = input()
		while relacion != "1" and relacion != "2" and relacion != "3":
			print("Dato incorrecto vuelva a ingresar")
			relacion = input()
		np.append(vaux,relacion)


	for j in restricciones:
		print (j)

	for j in vaux:
		print (j)

	


def simplex(self,tipo):
	pass
if __name__ == '__main__':
	main()