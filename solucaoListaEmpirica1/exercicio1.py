## Lista empírica 1 2020

import numpy as np
import psycopg2


class Estimativas:
    '''
    Calcula estimativas a partir de dados de Acemoglu, Johnson e Robinson (2001)
    '''

    def __init__(self):
        ## connects to database and loads data
        conn = psycopg2.connect("dbname=monitoria user=postgres password=passwd"\
                                " hostaddr=127.0.0.1 port=5432")
        cur = conn.cursor()
        sql_code = "SELECT * FROM ajr01;"
        cur.execute(sql_code)
        self.data = cur.fetchall()
        conn.commit()
        cur.close()
        conn.close()

        
    ### Itens a) e b) do exercício 12.32 do livro texto
    def item_a_ols(self):
        ## OLS 12.88: loggdp = beta0 * intercept + beta1 * risk + erro
        X = np.empty(shape=(len(self.data), 2))
        Y = np.empty(shape=(len(self.data), 1))
        for i in range(len(self.data)):
            X[i, 0] = 1
            X[i, 1] = self.data[i][3]
            Y[i, 0] = self.data[i][4]
        beta_ols = np.linalg.inv(X.transpose() @ X) @ X.transpose() @ Y
        print("12.88 beta OLS estimate is: ", beta_ols[1])
        erro = Y - X @ beta_ols
        sigma2 = (erro ** 2).sum() / len(Y)
        std_dev = ((sigma2 * np.linalg.inv(X.transpose() @ X))[1][1]) ** .5
        print("12.88 beta OLS standard deviation is: ", std_dev)

    def item_a_reduced(self):
        ## OLS 12.89: risk = beta0 * intercept + beta1 * logmortality + u
        X = np.empty(shape=(len(self.data), 2))
        Y = np.empty(shape=(len(self.data), 1))
        for i in range(len(self.data)):
            X[i, 0] = 1
            X[i, 1] = self.data[i][2]
            Y[i, 0] = self.data[i][3]
        beta_ols = np.linalg.inv(X.transpose() @ X) @ X.transpose() @ Y
        print("12.89 beta OLS estimate is: ", beta_ols[1])
        erro = Y - X @ beta_ols
        sigma2 = (erro ** 2).sum() / len(Y)
        std_dev = ((sigma2 * np.linalg.inv(X.transpose() @ X))[1][1]) ** .5
        print("12.89 beta OLS standard deviation is: ", std_dev)
        
    def item_a_2sls(self):        
        ## 2SLS 12.90: loggdp = beta0 * intercept + beta1 * risk + erro
        #              w/ logmortality as instrument for risk 
        X = np.empty(shape=(len(self.data), 2))
        Z = np.empty(shape=(len(self.data), 2))
        Y1 = np.empty(shape=(len(self.data), 1))
        for i in range(len(self.data)):
            X[i, 0] = 1
            X[i, 1] = self.data[i][3]
            Z[i, 0] = 1
            Z[i, 1] = self.data[i][2]
            Y1[i, 0] = self.data[i][4]
        # beta_2sls = (X'Z(Z'Z)^(-1)Z'X)^(-1)X'Z(Z'Z)^(-1)Z'Y1
        beta_2sls = np.linalg.inv(X.transpose() @ Z @\
                                  np.linalg.inv(Z.transpose() @ Z) @\
                                  Z.transpose() @ X) @\
                    X.transpose() @ Z @ np.linalg.inv(Z.transpose() @ Z) @\
                    Z.transpose() @ Y1
        
        print("12.90 beta 2SLS estimate is: ", beta_2sls[1])
        # variance estimation
        erro = Y1 - X @ beta_2sls
        n = len(Y1)
        sigma2 = (erro ** 2).sum() / n
        Q_xz = 1/n * X.transpose() @ Z
        Q_zz = 1/n * Z.transpose() @ Z
        Q_zx = 1/n * Z.transpose() @ X
        # homoskedastic case:
        # var beta_2sls = (1/n X'Z (1/n Z'Z)^(-1) 1/n Z'X)^(-1) * sigma^2
        std_dev_hom = ((np.linalg.inv(Q_xz @ np.linalg.inv(Q_zz) @ Q_zx) *\
                    sigma2)[1][1]) ** .5
        print("12.90 beta 2SLS (homoscedastic) standard deviation is: ", std_dev_hom)
        # general case:
        omega = np.zeros(shape=(2, 2))
        for i in range(n):
            Z_i = Z[i].transpose()[:, np.newaxis] # makes Z_i a l x 1 column vec
            omega += Z_i @ Z_i.transpose() * erro[i] ** 2
        omega /= n
        var_beta = (np.linalg.inv(Q_xz @ np.linalg.inv(Q_zz) @ Q_zx) @\
                    (Q_xz @ np.linalg.inv(Q_zz) @ omega @\
                     np.linalg.inv(Q_zz) @ Q_zx) @\
                    np.linalg.inv(Q_xz @ np.linalg.inv(Q_zz) @ Q_zx))[1][1]
        std_dev_gen = var_beta ** .5
        print("12.90 beta 2SLS (general) standard deviation is: ", std_dev_gen)
        std_dev_ols = ((sigma2 * np.linalg.inv(X.transpose() @ X))[1][1]) ** .5
        print("12.90 beta 2SLS (ols) standard deviation is: ", std_dev_ols)

        
    ### Item i) do exercício 12.32 do livro texto
    def item_i_reduced(self):
        ## risk = beta0 * intercept + beta1 * logmortality + beta2 *\
        ##        logmortality^2 + u
        X = np.empty(shape=(len(self.data), 3))
        Y = np.empty(shape=(len(self.data), 1))
        for i in range(len(self.data)):
            X[i, 0] = 1
            X[i, 1] = self.data[i][2]
            X[i, 2] = X[i, 1] ** 2
            Y[i, 0] = self.data[i][3]
        beta_ols = np.linalg.inv(X.transpose() @ X) @ X.transpose() @ Y
        print("Item (i) reduced form beta OLS estimate is: ", beta_ols)
        erro = Y - X @ beta_ols
        sigma2 = (erro ** 2).sum() / len(Y)
        var_beta = sigma2 * np.linalg.inv(X.transpose() @ X)
        std_dev = np.diagonal(var_beta) ** .5
        print("Item (i) reduced form beta OLS standard deviation is: ", std_dev)
        
    def item_i_2sls(self):        
        ## 2SLS 12.90: loggdp = beta0 * intercept + beta1 * risk + erro
        #              w/ logmortality & logmortality^2 as instruments for risk
        X = np.empty(shape=(len(self.data), 2))
        Z = np.empty(shape=(len(self.data), 3))
        Y1 = np.empty(shape=(len(self.data), 1))
        for i in range(len(self.data)):
            X[i, 0] = 1
            X[i, 1] = self.data[i][3]
            Z[i, 0] = 1
            Z[i, 1] = self.data[i][2]
            Z[i, 2] = Z[i, 1] ** 2
            Y1[i, 0] = self.data[i][4]
        # beta_2sls = (X'Z(Z'Z)^(-1)Z'X)^(-1)X'Z(Z'Z)^(-1)Z'Y1
        beta_2sls = np.linalg.inv(X.transpose() @ Z @\
                                  np.linalg.inv(Z.transpose() @ Z) @\
                                  Z.transpose() @ X) @\
                    X.transpose() @ Z @ np.linalg.inv(Z.transpose() @ Z) @\
                    Z.transpose() @ Y1
        
        print("Item (i) beta 2SLS estimate is: ", beta_2sls)
        # variance estimation
        erro = Y1 - X @ beta_2sls
        n = len(Y1)
        sigma2 = (erro ** 2).sum() / n
        Q_xz = 1/n * X.transpose() @ Z
        Q_zz = 1/n * Z.transpose() @ Z
        Q_zx = 1/n * Z.transpose() @ X
        # homoskedastic case:
        # var beta_2sls = (1/n X'Z (1/n Z'Z)^(-1) 1/n Z'X)^(-1) * sigma^2
        var_beta_hom = np.linalg.inv(Q_xz @ np.linalg.inv(Q_zz) @ Q_zx) * sigma2
        std_dev_hom = np.diagonal(var_beta_hom) ** .5
        print("Item (i) beta 2SLS (homoscedastic) standard deviation is: ", std_dev_hom)
        # general case:
        omega = np.zeros(shape=(3, 3))
        for i in range(n):
            Z_i = Z[i].transpose()[:, np.newaxis] # makes Z_i a l x 1 column vec
            omega += Z_i @ Z_i.transpose() * erro[i] ** 2
        omega /= n
        var_beta_gen = np.linalg.inv(Q_xz @ np.linalg.inv(Q_zz) @ Q_zx) @\
                       (Q_xz @ np.linalg.inv(Q_zz) @ omega @\
                        np.linalg.inv(Q_zz) @ Q_zx) @\
                       np.linalg.inv(Q_xz @ np.linalg.inv(Q_zz) @ Q_zx)
        std_dev_gen = np.diagonal(var_beta_gen) ** .5
        print("Item (i) beta 2SLS (general) standard deviation is: ", std_dev_gen)
        # save results for use in other methods (gmm below)
        self.X = X
        self.Z = Z
        self.Y = Y1
        self.beta_2sls = beta_2sls
        self.e_tilde = erro

        
    ### GMM c/ matriz eficiente
    def gmm(self):
        ## Regressão 12.90: loggdp = beta0 * intercept + beta1 * risk + erro
        #                   logmortality & logmortality^2 as instruments
        ## load previous data:
        X = self.X
        Z = self.Z
        Y = self.Y
        beta_2sls = self.beta_2sls
        e_tilde = self.e_tilde
        n = len(self.data)
        ## initialize omega matrices (uncentered and centered, see textbook\
        #   equations 13.8 and 13.9)
        omega_hat = np.zeros(shape=(3, 3))
        omega_hat_star = np.zeros(shape=(3, 3))
        g = np.empty(shape=(n, 3))
        g_bar = np.zeros(shape=(3, 1))
        ## fill w/ data:
        for i in range(n):
            g[i] = Z[i] * e_tilde[i]
            g_i = g[i].transpose()[:, np.newaxis] # makes g_i a l x 1 column vec
            g_bar += g_i
            omega_hat += g_i @ g_i.transpose()
        omega_hat /= n
        g_bar /= n
        for i in range(n):
            g_i = g[i].transpose()[:, np.newaxis]
            omega_hat_star += (g_i - g_bar) @ (g_i - g_bar).transpose()
        omega_hat_star /= n
        # from 13.6, beta_gmm (2-stage) = (X'ZWZ'X)^(-1)(X'ZWZ'Y) w/ W as omega
        inv_omega_hat = np.linalg.inv(omega_hat)
        beta_gmm_unc = np.linalg.inv(X.transpose() @ Z @ inv_omega_hat @\
                                     Z.transpose() @ X) @ (X.transpose() @ Z @\
                                                           inv_omega_hat @\
                                                           Z.transpose() @ Y)
        print("12.90 beta GMM two-stage estimate is: ", beta_gmm_unc)
        inv_omega_hat_star = np.linalg.inv(omega_hat_star)
        beta_gmm_cen = np.linalg.inv(X.transpose() @ Z @ inv_omega_hat_star @\
                                     Z.transpose() @ X) @ (X.transpose() @ Z @\
                                                           inv_omega_hat_star @\
                                                           Z.transpose() @ Y)
        print("12.90 beta GMM two-stage estimate is: ", beta_gmm_cen)


        
if __name__ == "__main__":
    instance = Estimativas()
    instance.item_a_ols()
    instance.item_a_reduced()
    instance.item_a_2sls()
    instance.item_i_reduced()
    instance.item_i_2sls()
    instance.gmm()
