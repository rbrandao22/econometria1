import os
import psycopg2

conn = psycopg2.connect("dbname=monitoria user=postgres password=passwd"\
                        " hostaddr=127.0.0.1 port=5432")
cur = conn.cursor()


## Table w/ consumption data and return rates
sql_code = r'''
DROP TABLE IF EXISTS dados_EU;

CREATE TABLE dados_EU (
    ano             integer,
    consumo         real,
    tx_juros        real,
    retorno_sp      real
);
'''
sql_code += "\nCOPY dados_EU FROM '/var/lib/postgresql/data/pgdata/csv/"\
    "dados_EU.csv' DELIMITER ';' CSV HEADER;"
cur.execute(sql_code)
print('Tabela dados_EU carregada com sucesso')


## Table - real gdp US
sql_code2 = r'''
DROP TABLE IF EXISTS gdp_EU;

CREATE TABLE gdp_EU (
    date            text,
    gdp             real
);
'''
sql_code2 += "\nCOPY gdp_EU FROM '/var/lib/postgresql/data/pgdata/csv/"\
    "GDPCA.csv' DELIMITER ',' CSV HEADER;"
cur.execute(sql_code2)
print('Tabela gdp_EU carregada com sucesso')


## Table - real gdp per capita US
sql_code3 = r'''
DROP TABLE IF EXISTS gdppc_EU;

CREATE TABLE gdppc_EU (
    date            text,
    gdp             real
);
'''
sql_code3 += "\nCOPY gdppc_EU FROM '/var/lib/postgresql/data/pgdata/csv/"\
    "A939RX0Q048SBEA.csv' DELIMITER ',' CSV HEADER;"
cur.execute(sql_code3)
print('Tabela gdppc_EU carregada com sucesso')


conn.commit()
cur.close()
conn.close()
