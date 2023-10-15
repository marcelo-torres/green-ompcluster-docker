#!/bin/bash

OUTBOUND_NETWORK_DELAY_DEFAULT="30ms"

# Get container names
container_names_str=$(docker ps --format "{{.Names}}" --filter "ancestor=ompc-mpi-base")
container_names=($container_names_str)


for i in "${!container_names[@]}"
do
    container_name=${container_names[$i]}
    echo "Adding $OUTBOUND_NETWORK_DELAY_DEFAULT delay to $container_name"
    docker exec $container_name tc qdisc add dev eth0 root netem delay $OUTBOUND_NETWORK_DELAY_DEFAULT
done
