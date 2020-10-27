## Exame 2019

import numpy as np
import psycopg2


class GMM:
    '''
    Obtém estimativa de parâmetros sigma e beta por GMM, segundo escolha
    de instrumentos
    '''

    def __init__(self, j):
        # connect to database and extract data
        conn = psycopg2.connect("dbname=monitoria user=postgres password=passwd"\
                                " hostaddr=127.0.0.1 port=5432")
        cur = conn.cursor()
        sql_code = "SELECT consumo, tx_juros, retorno_sp FROM dados_eu;"
        cur.execute(sql_code)
        data = cur.fetchall()
        
        # initialize np arrays and vars
        self.j = j # (j is number of lags used w/ instruments)
        self.n = len(data) - 1 - j
        self.cons_ratio = np.empty(len(data)-1)
        self.ret_juros = np.empty(len(data)-1)
        self.ret_sp = np.empty(len(data)-1)
        
        # fill np arrays w/ data
        for t in range(len(data)-2):
            self.cons_ratio[t] = data[t+1][0] / data[t][0] # Ct+1/Ct
            self.ret_juros[t] = data[t+1][1] # Rt+1 juros
            self.ret_sp[t] = data[t+1][2] # Rt+1 S&P

        conn.commit()
        cur.close()
        conn.close()

    def gmm_calc(self):
        epsilon = 1e-8  # convergence param
        inc = 1e-4      # gradient increment
        step = 1e-3     # NR step
        self.beta = .5
        self.sigma = .5
        def J_calc_I(beta, sigma):  # J calc w/ W as identity matrix
            g_i = np.empty(8)
            g_i = g_i[:, np.newaxis] # makes g_i a column vector
            g_bar = np.zeros(8)
            g_bar = g_bar[:, np.newaxis]
            for t in range(self.n):
                j = self.j
                if t <= j:
                    continue
                z1 = self.ret_juros[t-j] * beta * self.cons_ratio[t-j] ** sigma
                z2 = self.ret_juros[t-j] * beta * self.cons_ratio[t-j] ** sigma\
                    * np.log(self.cons_ratio[t-j])
                z3 = self.ret_sp[t-j] * beta * self.cons_ratio[t-j] ** sigma
                z4 = self.ret_sp[t-j] * beta * self.cons_ratio[t-j] ** sigma *\
                    np.log(self.cons_ratio[t-j])
                f1 = self.ret_juros[t] * beta * self.cons_ratio[t] ** sigma - 1
                f2 = self.ret_sp[t] * beta * self.cons_ratio[t] ** sigma - 1
                g_i[0] = z1 * f1
                g_i[1] = z2 * f1
                g_i[2] = z3 * f1
                g_i[3] = z4 * f1
                g_i[4] = z1 * f2
                g_i[5] = z2 * f2
                g_i[6] = z3 * f2
                g_i[7] = z4 * f2
                g_bar += g_i
            g_bar /= self.n
            J = g_bar.transpose() @ np.identity(8) @ g_bar
            return J
        def NewtonRaphson_I():
            grad1 = (J_calc_I(self.beta+inc, self.sigma) - J_calc_I(self.beta, self.sigma)) / inc
            grad2 = (J_calc_I(self.beta, self.sigma+inc) - J_calc_I(self.beta, self.sigma)) / inc
            while (grad1**2 + grad2**2) > epsilon:
                self.beta -= step * grad1
                self.sigma -= step * grad2
                grad1 = (J_calc_I(self.beta+inc, self.sigma) - J_calc_I(self.beta, self.sigma)) / inc
                grad2 = (J_calc_I(self.beta, self.sigma+inc) - J_calc_I(self.beta, self.sigma)) / inc
        NewtonRaphson_I()
        print(self.beta)

        
if __name__ == "__main__":
    ## set in j number of lags for instruments
    j = 1
    instance = GMM(j)
    instance.gmm_calc()
