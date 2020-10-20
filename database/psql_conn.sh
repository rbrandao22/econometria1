#!/bin/bash
docker run -it --rm --net host --name psql postgres psql -h localhost -U postgres
