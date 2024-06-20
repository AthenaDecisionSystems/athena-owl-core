#!/bin/bash
scriptDir=$(dirname $0)

IMAGE_NAME=jbcodeforce/athena-owl-backend

if [[ $# -eq 1 ]]
then
  TAG=$1
else
  TAG=latest
fi

cd $scriptDir/../src
docker build -f Dockerfile -t  ${IMAGE_NAME}:${TAG} .

docker tag  ${IMAGE_NAME}:${TAG}   ${IMAGE_NAME}:latest
