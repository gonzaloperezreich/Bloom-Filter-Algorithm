import csv
import sys
import numpy as np
import random as rd
import pandas as pd
import math
import time
from complement import genera_arreglo_b, genera_matriz_a, sacar_porcentaje_de_datos, hash
import bitarray

# create a dataframe after reading .csv file
dataframe = pd.read_csv('data/Popular-Baby-Names-Final.csv') 
t = 10 #tamaño de los test
n = dataframe.shape[0] #tamaño del csv
maxlen = 50 #solo dejamos los strings hasta con 50 caracteres
primo = 100000019
for m in range(450000, 900001, 90000): #tamaño de m
    for k in range(2, 8): #cantidad de funcions de hash
        e = math.pow(1 - math.exp(-k*n/m), k)
        print("\n" + "m: " + str(m) + " k: " + str(k) + " e: " + str(e) + "\n")
        print()    

        M = bitarray.bitarray(m)
        M.setall(0)
        a = genera_matriz_a(k, maxlen)
        b = genera_arreglo_b(k)

        # read csv, and split on "," the line
        csv_file = csv.reader(open('data/Popular-Baby-Names-Final.csv', "r"), delimiter=",")
        # ingresar valores del csv al filtro
        for row in csv_file:
            nombre = row[0]
            for i in range(k):
                r = hash(nombre, a[i], b[i], m)
                M[r] = 1

        for p in [80, 60, 40, 20]:
            buscar = sacar_porcentaje_de_datos('data/Popular-Baby-Names-Final.csv', 'data/Films-Actualizado.csv', p, t)
            c=0 #Número de negativos según el filtro.
            inicio1 = time.time()
            for s in buscar:
                #revisar filtro si tiene que entrar entrar = true
                entrar = True
                for i in range(k):
                    r = hash(s, a[i], b[i], m)
                    if(M[r] == 0):
                        entrar = False
                        c+= 1
                        break                
                if entrar:    
                    csv_file = csv.reader(open('data/Popular-Baby-Names-Final.csv', "r"), delimiter=",")   
                    for row in csv_file:
                        if s == row[0]:
                            break
                #Si nunca hizo break, el algoritmo dice que lo encontró (podría ser FP)
            fin1 = time.time()
            inicio2 = time.time()
            for s in buscar:
                csv_file = csv.reader(open('data/Popular-Baby-Names-Final.csv', "r"), delimiter=",")
                for row in csv_file:
                    if s == row[0]:
                        break #Si hace break, lo encontró
            fin2 = time.time()
            print(str(p) + ": Sin filtro demoro " + str(fin2-inicio2) + "s. Con filtro demoro " + str(fin1-inicio1) + \
                ".\nNúmero de negativos real: " + str(round((1-(p/100))*t)) + ". Número de negativos según el filtro: " + str(c))
