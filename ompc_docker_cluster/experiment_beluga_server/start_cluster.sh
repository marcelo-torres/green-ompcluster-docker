#!/bin/bash

prefix="experiment_beluga_server"
separator="-"

# Build base image
image_exists=$(docker images | grep ompc-mpi-base)
if [ ! "$image_exists" ]; then
    current_dir=$pwd
    cd ./../image_base
    /bin/bash generate_mpi_images.sh
    cd $current_dir
fi

bash stop_cluster.sh
docker compose up -d || exit 1

echo "\n"
bash network_setup.sh.sh

head_container="$prefix""$separator""head-1"

echo "\n[i] Use 'docker compose stop' to stop all containers"
echo "\n[i] Use 'docker attach $head_container' to attach to the head node"




