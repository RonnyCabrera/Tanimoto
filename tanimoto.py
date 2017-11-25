from multiprocessing import Process
import math
import time

#Leer archivo "ZIN_chemicals.tsv" y Guardar en lista "listComplete"
def leerArchivo(list):
    f = open('ZINC_chemicals.tsv', 'r')

    for linea in f.readlines():
        list.append(linea.split("\t"))

    f.close()

#Contar letras Comunes
def contar(caracter, letra):
    cont = 0
    if(caracter == letra):
        cont = 1
    return cont

#Crear lista con ID y cantidad de letras comunes
def letrasComunes(list1, list2):

    #Recorrer la lista "listComplete"
    for i in range (len(list1)):
        cont1 = 0
        cont2 = 0
        cont3 = 0
        cont4 = 0
        cont5 = 0
        cont6 = 0
        cont7 = 0
        cont8 = 0
        cont9 = 0
        cont10 = 0
        cont11 = 0
        cont12 = 0
        cont13 = 0
        #Recorrer la formula del quimico
        for caracter in list1[i][3]:
            cont1 += contar(caracter, "Br")
            cont2 += contar(caracter, "C")
            cont3 += contar(caracter, "c")
            cont4 += contar(caracter, "F")
            cont5 += contar(caracter, "H")
            cont6 += contar(caracter, "l")
            cont7 += contar(caracter, "N")
            cont8 += contar(caracter, "n")
            cont9 += contar(caracter, "O")
            cont10 += contar(caracter, "P")
            cont11 += contar(caracter, "S")
            cont12 += contar(caracter, "s")
            cont13 = contar(caracter, "@")
        #Crear lista "listChemicals"
        list2.append([list1[i][1], cont1, cont2, cont3, cont4, cont5, cont6, cont7, cont8, cont9, cont10, cont11, cont12, cont13])

#Elegir el menor entre dos elementos comunes
def elegirMenor(chemicalA, chemicalB, i):
    if(chemicalA[i] < chemicalB[i]):
        return chemicalA[i]
    else :
        return chemicalB[i]

#Caclular los tres valores Na, Nb, Nc entre dos quimicos
def elementosComunes(chemicalA, chemicalB):
    Nt = []
    Nc = []

    #Recorro lista
    for i in range (1, len(chemicalA)):
        Nc.append(elegirMenor(chemicalA, chemicalB, i))

    #Sumo los elementos de Na
    Na = sum(chemicalA[1:])
    #Sumo los elementos de Nb
    Nb = sum(chemicalB[1:])
    #Sumo los elementos de Nc
    Nc = sum(Nc)

    Nt.append([Na, Nb, Nc])

    return Nt

#Calculo el valor de la formula Tanimoto
def calcularTanimoto(chemicalA, chemicalB):
    #Guardo en Nt los valores de Na, Nb, Nc respectivamente
    Nt = elementosComunes(chemicalA, chemicalB)
    #Calculo el denominador de la formula Tanimoto
    deno = Nt[0][0] + Nt[0][1] - Nt[0][2]
    #Si el denminador es 0 me retorne un NO
    #Por ejemplo : al comparar el Quimico "N" con otro Quimico "N"
    T = Nt[0][2] / (float)(deno)
    #Redondeo el valor Tanimoto a dos decimales
    return round(T, 2)

#Creo un archivo para los resultados
def crearArchivo():
    f = open('archivo.tsv', 'w')
    f.close()

#Recorro el array de todos los elementos para calcular la formula Tanimoto
def tanimotoTotal(t, n, p, list):
    #Abro archivo para escribir Quimico 1, Quimico 2, Tanimoto
    f = open('archivo.tsv', 'a')
    #Verifico que numero de thread
    if (t % 2 == 0):
        #Calculo los limites de cada thread con una formula progresiva
        #Para cualquier tamano de archivo, cualquier cantidad de core
        #Formula inicial : n * (raiz(t/2, 2) / raiz(p/2, 2))
        fi = int(n*(math.sqrt(t/2)/math.sqrt(p/2)))
        #Formula final : n * (raiz(t, 2) / raiz(p, 2))
        ff = int(n*(math.sqrt(t+1)/math.sqrt(p)))
        for i in range (fi, ff):
            for j in range (i):
                #Escribo en archivo
                f.write(str(list[i][0]) + "\t" + str(list[j][0]) + "\t" + str(calcularTanimoto(list[i], list[j])) + "\n")
        #Cierro archivo
        f.close()
    else:
        #Formula inicial : n * (raiz(t, 2) / raiz(p, 2))
        fi = int(n*(math.sqrt(t)/math.sqrt(p)))
        #Formula final : n * (raiz(t/2, 2) / raiz(p/2, 2))
        ff = int(n*(math.sqrt((t+1)/2)/math.sqrt(p/2)))
        for i in range (fi, ff):
            for j in range (i):
                #Escribo en archivo
                f.write(str(list[i][0]) + "\t" + str(list[j][0]) + "\t" + str(calcularTanimoto(list[i], list[j])) + "\n")
        #Cierro archivo
        f.close()


if __name__ == '__main__':
    start = time.time()

    #Lista para guardar datos de Archivo ZINC_chemicals.tsv
    listComplete = []

    leerArchivo(listComplete)

    #Lista para guardar el ID_Quimico, C, c, @
    listChemicals = []

    letrasComunes(listComplete, listChemicals)

    #Libero memoria eliminando array
    del(listComplete)

    #Tamano total de Qumicos
    l = len(listChemicals)
    #Numero de core
    nproc = 4

#t0 = threading.Thread(target=tanimotoTotal, args=(0, l, nproc, listChemicals, ))
    p0 = Process(target=tanimotoTotal, args=(0, l, nproc, listChemicals, ))
#t1 = threading.Thread(target=tanimotoTotal, args=(1, l, nproc, listChemicals, ))
    p1 = Process(target=tanimotoTotal, args=(1, l, nproc, listChemicals, ))
#t2 = threading.Thread(target=tanimotoTotal, args=(2, l, nproc, listChemicals, ))
    p2 = Process(target=tanimotoTotal, args=(2, l, nproc, listChemicals, ))
#t3 = threading.Thread(target=tanimotoTotal, args=(3, l, nproc, listChemicals, ))
    p3 = Process(target=tanimotoTotal, args=(3, l, nproc, listChemicals, ))

#t0.start()
    p0.start()
#t1.start()
    p1.start()
#t2.start()
    p2.start()
#t3.start()
    p3.start()

#t0.join()
    p0.join()
#t1.join()
    p1.join()
#t2.join()
    p2.join()
#t3.join()
    p3.join()

    del(listChemicals)

    end = time.time()

    print (end - start)
