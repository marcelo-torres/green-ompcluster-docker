#!/bin/bash

# Build base image
image_exists=$(docker images | grep ompc-mpi-base)
if [ ! "$image_exists" ]; then
    current_dir=$pwd
    cd ./../image_base
    /bin/bash generate_mpi_images.sh
    cd $current_dir
fi


docker-compose stop
docker-compose up -d || exit 1

echo "\n"
bash generate_hostfile.sh
bash set-network-delay.sh

echo "\n[i] Use 'docker-compose stop' to stop all containers"
echo "\n[i] Use 'docker attach cluster_test_head_1' to attach to the head node"




