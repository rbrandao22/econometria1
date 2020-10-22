#!/bin/bash
sudo docker run --rm --name postgresdb -e POSTGRES_PASSWORD=passwd -e PGDATA=/var/lib/postgresql/data/pgdata -d -p 5432:5432 -v /mnt/postgresdb:/var/lib/postgresql/data postgres
