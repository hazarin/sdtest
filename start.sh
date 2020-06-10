#!/bin/bash

# Start cluster
python manage.py qcluster &

# Start server
python manage.py runserver 0.0.0.0:$PORT
