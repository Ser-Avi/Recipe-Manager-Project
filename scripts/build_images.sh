#!/bin/sh

docker build -t recipe_page_api:latest -f ../Dockerfile ../
docker build -t recipe_page_app:latest -f ../frontend/Dockerfile ../frontend
