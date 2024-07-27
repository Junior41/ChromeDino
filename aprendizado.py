import random
import math
from mpmath import *
import globais as gl

class aprendizado:
    def __init__(self):
        self.aleatoriedade = 1
        self.scoreAnterior = 1
        self.vitorias = 0;
        self. geracao = []
        self.score = []

    def camadaEntrada(self, dino, distanciaObjeto, alturaObjeto, velocidade, alturaDino, larguraObj):

        neuronios = []
        i = 0;
        while(i < 5):
            neuronios.append(max(0, dino.cromossomos[i] * distanciaObjeto + dino.cromossomos[i+1] * alturaObjeto + dino.cromossomos[i+2] * velocidade
            + alturaDino * dino.cromossomos[i+3] + larguraObj * dino.cromossomos[i+4] + dino.cromossomos[i+5]))
            i+=1

        return neuronios

    def primeiraCamada(self, dino, distanciaObjeto, alturaObjeto, velocidade, alturaDino, larguraObj):

        entradas = self.camadaEntrada(dino, distanciaObjeto, alturaObjeto, velocidade, alturaDino, larguraObj)
        neuronios = []
        i = 30
        j = 0

        while(j < 5):
            aux = 0

            for l in range(5):
                aux += dino.cromossomos[i] * entradas[l]
                i+=1

            aux += dino.cromossomos[i] #bias

            i+=1
            neuronios.append(max(0, aux))
            j+=1

        #return math.tanh(neuronio1), max(0, neuronio2)
        return neuronios

    def camadaSaida(self, dino, distanciaObjeto, alturaObjeto, velocidade, alturaDino, larguraObj):
        entradas = self.primeiraCamada(dino, distanciaObjeto, alturaObjeto, velocidade, alturaDino, larguraObj)
        neuronios = []
        i = 60
        j = 0

        while(j < 2):

            aux = 0

            for l in range(5):
                aux += dino.cromossomos[i] * entradas[l]
                i+=1

            neuronios.append(max(0, aux))
            j+=1

        #return max(0, neuronio1), max(0, neuronio2)
        return neuronios

    def saida(self, dino, distanciaObjeto, alturaObjeto, velocidade, alturaDino, larguraObj):
        entradas = self.camadaSaida(dino, distanciaObjeto, alturaObjeto, velocidade, alturaDino, larguraObj)

        if(entradas[0] > 0):
            return 1 #pula
        elif(entradas[1] > 0):
            return 0 #abaixa

        return 2 #não faz nada


    def mutacao(self, dino, melhorDino):

        for i in range(gl.quantcromossomos):
            operacao = random.randint(0,1)
            aplica = random.randint(0,1)
            pesoOperacao = random.randint(1,5)
            if(aplica):
                if(operacao == 1):
                    dino.cromossomos[i] = melhorDino.cromossomos[i] + (self.aleatoriedade / pesoOperacao)
                else:
                    dino.cromossomos[i] = melhorDino.cromossomos[i] - (self.aleatoriedade / pesoOperacao)

        return dino


    def crossover(self, dinos):
        melhores = dinos[-3 : -1]

        if(len(dinos) <= 1):
            print(dinos[0].score)
            print("FIM DO TREINAMENTO")
            exit(1)

        arquivo = open("resultados.txt", "a")

        string = "\n" + str(len(dinos)) + " - " + str(dinos[-1].score)

        arquivo.write(string)

        arquivo.close()

        # ajustando a aleatoriedade
        self.aleatoriedade = (2000 + self.scoreAnterior) / melhores[-1].score
        #self.aleatoriedade = self.scoreAnterior / melhores[1].score
        self.scoreAnterior = melhores[-1].score

        filho = dinos[0]
        if(len(dinos) % 10 == 0): # caso o número da seleção seja múltiplo de 10 gera um filho aleatório
            for i in range(gl.quantcromossomos):
                cromossomo = 0
                while(cromossomo == 0):
                    cromossomo = random.randint(-100,100)
                filho.cromossomos[i] = cromossomo

            self.aleatoriedade = 100

        else:
            for i in range(gl.quantcromossomos):
                media = (melhores[0].cromossomos[i] + melhores[1].cromossomos[i]) / 2
                filho.cromossomos[i] = media

        return filho, self.aleatoriedade

    def controlaDino(self, dino, distancia, altura, velocidade, alturaDino, larguraObj):
        return self.saida(dino, distancia, altura, velocidade, alturaDino, larguraObj)
