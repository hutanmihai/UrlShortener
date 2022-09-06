#!/bin/sh

echo 'Waiting for postgres...'
sleep 10

python3 urlshortener/manage.py runserver 0.0.0.0:8000