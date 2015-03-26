#!/bin/bash
service postgresql start
service nginx start
service redis-server start
uwsgi --ini ordergogo/uwsgi.ini
