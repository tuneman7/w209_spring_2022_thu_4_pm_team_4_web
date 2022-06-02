#!/bin/bash
IMAGE_NAME=w209_proj_don_irwin
APP_NAME=w209_proj_don_irwin
DOCKER_FILE=Dockerfile.209proj

docker build -t w209_proj -f Dockerfile.209proj .
