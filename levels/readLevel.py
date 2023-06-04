import os
from io import open
#leer niveles por bloc de notas
def ReadLineForLine(file):
    #we will create contener list 
    lista_str=[]
    lista_buffer=[]
    lista_int=[]

    #open the file and go through each of its rows
    with open(file) as f:
        for line in f:
            #read line for line the array
            lista_str=([line.strip() for line in line.split(',')])
            lista_buffer=[]
            for num in lista_str: #convert them to integers
                lista_buffer.append(int(num))
            lista_int.append(lista_buffer)

    return lista_int

def scanMap(archivo):
    #if the map not exits we will create 
    if not os.path.exists(archivo):
        return []
    else:
        l=ReadLineForLine(archivo)
        return l


#leer niveles para modificarlos
def EditarNivel(archivo):
    scanMap(archivo)