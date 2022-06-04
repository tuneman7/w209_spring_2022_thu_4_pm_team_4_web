#!/bin/bash
IMAGE_NAME=w209_proj_don_irwin
APP_NAME=w209_proj_don_irwin
DOCKER_FILE=Dockerfile.209proj

docker rmi $(docker images --filter "dangling=true" -q --no-trunc)

echo "docker stop ${APP_NAME}"
docker stop ${APP_NAME}
echo "docker rm ${APP_NAME}"
docker rm ${APP_NAME}

#build docker from the docker file
echo "docker build -t ${IMAGE_NAME} -f ${DOCKER_FILE}" 
docker build -t ${IMAGE_NAME} -f ${DOCKER_FILE} .
echo "docker run --name ${APP_NAME} -p  8888:8888 -p 5001:5000  ${IMAGE_NAME} "
docker run --name ${APP_NAME} -p  8888:8888 -p 5001:5000  ${IMAGE_NAME} 
