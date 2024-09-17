#!/bin/bash

gunicorn -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8040 main:app
