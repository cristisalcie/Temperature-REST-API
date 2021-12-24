#!/bin/bash

# Copy changes to docker container
docker cp rest_api/src/main.py rest_api_sprc_hw2:/app/

# Restart container to apply changes
docker container restart rest_api_sprc_hw2
