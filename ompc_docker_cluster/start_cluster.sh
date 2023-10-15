#!/bin/bash

# Build base image
image_exists=$(docker images | grep ompc-mpi-base)
if [ ! "$image_exists" ]; then
    cd image_base
    /bin/bash generate_mpi_images.sh
    cd ..
fi


docker-compose stop
docker-compose up -d && echo "\n[i] Use 'docker-compose stop' to stop all containers" && echo "\n[i] Use 'docker attach ompc_docker_cluster_head_1' to attach to the head node"

echo "\n"
bash generate_hostfile.sh

echo "\n"
bash set-network-delay.sh
