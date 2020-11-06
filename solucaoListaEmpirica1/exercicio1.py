## Lista empírica 1 2020

import numpy as np
import psycopg2


class Estimativas:
    '''
    Calcula estimativas a partir de dados de Acemoglu, Johnson e Robinson (2001)
    '''

    def __init__(self):
        # connects to database and loads data
        conn = psycopg2.connect("dbname=monitoria user=postgres password=passwd"\
                                " hostaddr=127.0.0.1 port=5432")
        cur = conn.cursor()
        sql_code = "SELECT * FROM ajr01;"
        cur.execute(sql_code)
        self.data = cur.fetchall()
        conn.commit()
        cur.close()
        conn.close()

    def item_a(self):
        ## item a do exercício 12.32 do livro texto
        # regressão loggdp = beta0 * intercept + beta1 * risk + erro
        X = np.empty(shape=(len(self.data), 2))
        Y = np.empty(shape=(len(self.data), 1))
        for i in range(len(self.data)):
            X[i, 0] = 1
            X[i, 1] = self.data[i][3]
            Y[i, 0] = self.data[i][4]
        beta_ols = np.linalg.inv(X.transpose() @ X) @ X.transpose() @ Y
        print("Beta OLS estimate is: ", beta_ols[1])
        erro = Y - X @ beta_ols
        sigma2 = (erro ** 2).sum() / len(Y)
        std_dev = (sigma2 * np.linalg.inv(X.transpose() @ X))[1][1]
        print("Beta OLS standard deviation is: ", std_dev)

        
if __name__ == "__main__":
    instance = Estimativas()
    instance.item_a()
