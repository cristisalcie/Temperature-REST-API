#!/bin/bash


# Stop rest api
cd rest_api
sudo docker-compose -f docker-compose.yml down
cd ..

# Remove rest api image
sudo docker image rm rest_api_image_sprc_hw2

# Build rest api image
cd rest_api
sudo docker build . -t rest_api_image_sprc_hw2
cd ..

# Start rest api
cd rest_api
sudo docker-compose -f docker-compose.yml up -d
cd ..
