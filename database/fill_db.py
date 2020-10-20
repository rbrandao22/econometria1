import os
import psycopg2

conn = psycopg2.connect("dbname=monitoria user=postgres password=passwd"\
                        " hostaddr=127.0.0.1 port=5432")
cur = conn.cursor()

sql_code = r'''
DROP TABLE IF EXISTS ajr4;

CREATE TABLE ajr4 (
    id              integer,
    shortnam        text,
    africa          real,
    lat_abst        real,
    rich4           real,
    avexpr          real,
    logpgp95        real,
    logem4          real,
    asia            real,
    loghjypl        real,
    baseco          real
);
'''
sql_code += "\nCOPY ajr4 FROM '/var/lib/postgresql/data/pgdata/csv/"\
    "maketable4.csv' DELIMITER ',' CSV HEADER;"
cur.execute(sql_code)
print('Tabela carregada com sucesso')

conn.commit()
cur.close()
conn.close()
