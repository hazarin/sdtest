#!/bin/bash

# turn on bash's job control
set -m

# Start cluster
python manage.py qcluster &

# Start server
python manage.py runserver 0.0.0.0:8000
