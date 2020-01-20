#!/usr/bin/env bash

docker build -t congress_postgres .
docker run -itd -p 32768:5432 --name postgres congress_postgres