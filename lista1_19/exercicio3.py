## Lista empírica 1 2019

import numpy as np
import psycopg2


class GMM:
    '''
    Calcula estimativa a partir de dados de Acemoglu, Johnson e Robinson
    '''

    def __init__(self, data):
        self.data = data


        
if __name__ == "__main__":
    sql_code = "SELECT * FROM ajr4;"
    conn = psycopg2.connect("dbname=monitoria user=postgres password=passwd"\
                            " hostaddr=127.0.0.1 port=5432")
    cur = conn.cursor()
    cur.execute(sql_code)
    data = cur.fetchall()
    conn.commit()
    cur.close()
    conn.close()
    instance = GMM(data)
