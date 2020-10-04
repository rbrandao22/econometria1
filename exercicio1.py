## Lista empírica 1

# importação dos módulos necessários
import numpy as np


class Exercicio_1:
    '''
    Gera 100 amostras, c/ 100 realizações N(0,1) cada, depois calcula quantos
    ICs estimados contém o parâmetro verdadeiro
    '''
    
    def __init__(self, sample_size, samples_nbr, mean, std, z):
        self.sample_size = sample_size
        self.samples_nbr = samples_nbr
        self.mean = mean
        self.std = std
        self.z = z
        self.X = np.random.normal(mean, std, size=(samples_nbr, sample_size))
        self.count = 0

    def countTrueICs(self):

        for x in self.X:
            avg = np.average(x)
            IC = [avg - self.z * self.std / np.sqrt(self.sample_size),
                  avg + self.z * self.std / np.sqrt(self.sample_size)]
            if self.mean > IC[0] and self.mean < IC[1]:
                self.count += 1
        return

    def printResults(self):
        trueProportion = self.count / samples_nbr
        print("This draw yielded ", trueProportion,
              "% ICs enclosing true average")
        return
            

if __name__ == '__main__':
    sample_size = 100
    samples_nbr = 100
    mean = 0
    std = 1
    z = 1.96
    instance = Exercicio_1(sample_size, samples_nbr, mean, std, z)
    instance.countTrueICs()
    instance.printResults()
