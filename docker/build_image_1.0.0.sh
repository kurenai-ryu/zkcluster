#!/bin/bash
#!/usr/bin/env bash
SRC=$(cd $(dirname "$0"); cd ..; pwd)
cd $SRC
#docker ps -a | awk '{ print $1,$2 }' | grep zkcluster:1.0.0 | awk '{print $1 }' | xargs -I {} docker rm {}
docker ps -a | grep "zkcluster:1.0.0" | awk '{print $1}' | xargs docker rm
#docker rmi zkcluster
docker images -a | grep "zkcluster" | awk '{print $3}' | xargs docker rmi
docker build -t zkcluster:1.0.0 -f docker/Dockerfile .
