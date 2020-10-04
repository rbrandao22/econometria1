## Lista empírica 1

import numpy as np


class Exercicio_1:
    '''
    Gera 100 amostras, c/ 100 realizações N(0,1) cada, depois calcula quantos
    intervalos de confiança estimados contém o parâmetro verdadeiro.
    '''
    
    def __init__(self, sample_size, samples_nbr, mean, std, z):
        self.sample_size = sample_size
        self.samples_nbr = samples_nbr
        self.mean = mean
        self.std = std
        self.z = z
        self.X = np.random.normal(mean, std, size=(samples_nbr, sample_size))
        self.count = 0

    def countTrueCIs(self):

        for x in self.X:
            avg = np.average(x)
            CI = [avg - self.z * self.std / np.sqrt(self.sample_size),
                  avg + self.z * self.std / np.sqrt(self.sample_size)]
            if self.mean > CI[0] and self.mean < CI[1]:
                self.count += 1
        return

    def printResults(self):
        trueProportion = self.count / samples_nbr
        print("This draw yielded ", trueProportion * 100,
              "% CIs enclosing true average")
        return
            

if __name__ == '__main__':
    sample_size = 100
    samples_nbr = 100
    mean = 0
    std = 1
    z = 1.96
    instance = Exercicio_1(sample_size, samples_nbr, mean, std, z)
    instance.countTrueCIs()
    instance.printResults()
