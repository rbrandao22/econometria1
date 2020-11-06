import os
import psycopg2

conn = psycopg2.connect("dbname=monitoria user=postgres password=passwd"\
                        " hostaddr=127.0.0.1 port=5432")
cur = conn.cursor()

sql_code = r'''
DROP TABLE IF EXISTS ajr01;

CREATE TABLE ajr01 (
    longname            text,
    shortnam            text,
    logmort0            real,
    risk                real,
    loggdp              real,
    campaign            integer,
    source0             integer,
    slave               integer,
    latitude            real,
    neoeuro             integer,
    asia                integer,
    africa              integer,
    other               integer,
    edes1975            real,
    campaignsj          integer,
    campaignsj2         integer,
    mortnaval1          real,
    logmortnaval1       real,
    mortnaval2          real,
    logmortnaval2       real,
    mortjam             real,
    logmortjam          real,
    logmortcap250       real,
    logmortjam250       real,
    wandcafrica         real,
    malfal94            real,
    wacacontested       real,
    mortnaval2250       real,
    logmortnaval2250    real,
    mortnaval1250       real,
    logmortnaval1250    real
);
'''
sql_code += "\nCOPY ajr01 FROM '/var/lib/postgresql/data/pgdata/csv/"\
    "AJR2001.csv' WITH DELIMITER ';' NULL AS 'NA' CSV HEADER;"
cur.execute(sql_code)
print('Tabela carregada com sucesso')

conn.commit()
cur.close()
conn.close()
