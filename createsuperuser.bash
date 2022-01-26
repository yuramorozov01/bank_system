#!/bin/bash

docker-compose exec bank python3 ./src/manage.py createsuperuser
