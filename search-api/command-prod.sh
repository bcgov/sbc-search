#!/bin/bash

gunicorn -b 0.0.0.0:5000 wsgi --worker-class=gevent --worker-connections=1000 --timeout 90
