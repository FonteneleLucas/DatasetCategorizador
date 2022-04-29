import numpy as np
from collections import defaultdict
import string
import csv
import pathlib


class TG(object):

    def __init__(self, _entrada, _quantClasses):
        self.entrada = _entrada
        self.matrizEntrada = self._matrizEntrada()
        self.quantClasses = _quantClasses
        self.maior = self._maior()
        self.menor = self._menor()
        self.amplitude = self._amplitude()
        
        self.intervalos = self._intervalos()
        self.classes = self._geradorClasses()
        self.listaCategorias = self._defineClasses()
        self.dadosCategorizados = self._categorizador()

    def _matrizEntrada(self):
        print("Lendo dataset de entrada...")
        f = open(self.entrada, 'r').read()
        dataList = [line.split(',') for line in f.split('\n') if line]
        return dataList

    def _menor(self):
        arrayMin = []
        for j in range(len(self.matrizEntrada)):
            menor = 0
            for i in range(len(self.matrizEntrada[j])):
                comparador = min(menor, int(self.matrizEntrada[j][i]))
                if comparador < menor:
                    menor = comparador
            arrayMin.append(menor)
        return arrayMin

    def _maior(self):
        arrayMax = []
        for j in range(len(self.matrizEntrada)):
            maior = 0
            for i in range(len(self.matrizEntrada[j])):
                comparador = max(maior, int(self.matrizEntrada[j][i]))
                if comparador > maior:
                    maior = comparador
            arrayMax.append(maior)
        return arrayMax

    def _amplitude(self):
        amplitudeArray = []
        for j in range(len(self.menor)):
            amplitudeArray.append(int(self.maior[j]) - int(self.menor[j]))
        return amplitudeArray

    def _geradorClasses(self):
        b = list(string.ascii_lowercase)
        a = []
        for i in range(ord('a'), ord(b[self.quantClasses])):
            a.append(chr(i))
        return a

    def _intervalos(self):
        print("Definindo intervalos...")
        intervaloArray = []
        for j in range(len(self.menor)):
            valorRef = round(int(self.amplitude[j]) / int(self.quantClasses))
            if valorRef < 1:
                intervaloArray.append(1)
            else:
                intervaloArray.append(valorRef)
        return intervaloArray

    def _defineClasses(self):
        print("Definindo classes...")
        classesArrayFinal = []
        for j in range(len(self.amplitude)):
            classesArray = []
            i = 0
            cont = 0
            while i < self.amplitude[j]:
                i += self.intervalos[j]
                if cont < self.quantClasses:
                    classesArray.append([i, self.classes[cont]]) 
                    cont+=1
            classesArrayFinal.append(classesArray)

        
        for i in range(len(classesArrayFinal)):
            if len(classesArrayFinal[i]) == 0:
                classesArrayFinal[i].append([0, self.classes[0]])
        #print("Classes geradas: ", classesArrayFinal)
        return classesArrayFinal 
                
    def _categorizador(self):
        arraySaida = []
        print("Iniciando categorizacao...")
        for j in range(len(self.matrizEntrada)):
            #print(self.matrizEntrada)
            arrayCategorizado = []
            for i in range(len(self.matrizEntrada[j])):
                #print(self.matrizEntrada[j])
                for k in range(self.quantClasses):
                    if int(self.matrizEntrada[j][i]) <= int(self.listaCategorias[j][k][0]):
                        arrayCategorizado.append(self.listaCategorias[j][k][1])
                        break
                    if k == self.quantClasses - 1:
                        arrayCategorizado.append(self.listaCategorias[j][k][1])
            arraySaida.append(arrayCategorizado)
        return arraySaida

    def exportaResultadoCsv(self, nomeArquivo):
        print("Exportando dados...")
        f = open(nomeArquivo,"w+", newline='')
        writer = csv.writer(f)
        for i in range(len(self.dadosCategorizados)):
            writer.writerow(self.dadosCategorizados[i])
        f.close()
        print("Dados exportados para: %s\\%s" %(pathlib.Path(__file__).parent.resolve(), nomeArquivo))

    
dataset = TG('Data_set - tranpostoNormal2020-2021 (1).csv', 3)
#dataset = TG('datasetTranpose2.csv', 5)

#print("1 - Matriz carregada: ", dataset._matrizEntrada()[0])
#print("2 - Menor", dataset._menor())
#print("3 - Maior", dataset._maior())
#print("4 - Amplitude", dataset._amplitude())
#print("5 - Classes:", dataset._geradorClasses())
#print("7 - Intervalos: ", dataset._intervalos())
#print("6 - Define Classes:", dataset._defineClasses())
#print("7 - Dados Categorizados:", dataset._categorizador())
dataset.exportaResultadoCsv("resultadoDatasetOk.txt")