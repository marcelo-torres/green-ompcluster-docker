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

echo
bash network_setup.sh

head_container="$prefix""$separator""head-1"

echo
echo "[i] Use '. stop_cluster.sh' to stop all containers"
echo "[i] Use 'docker attach $head_container' to attach to the head node"




