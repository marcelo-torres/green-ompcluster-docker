#!/bin/bash

#
# How to execute:
#    chmod +x generate_hostfile.sh && ./generate_hostfile.sh 
# or: 
#    sudo bash generate_hostfile.sh 
#

FILE=./ompc-host-file
NETWORK_NAME="ompc_docker_cluster_default"


# Delete file if exists
if [ -f "$FILE" ]; then
    echo "$FILE will be deleted."
    rm $FILE
fi


# Get container names
container_names_str=$(docker ps --format "{{.Names}}" --filter "ancestor=ompc-mpi-base")
container_names=($container_names_str)


# Reorder array to set head cointainer first
head_index=-1
for i in "${!container_names[@]}"
do
    name=${container_names[$i]}
    if [[ "$name" == *"head"* ]]; then
      head_index=$i
      break
    fi
done
container_names=("${container_names[$head_index]}" "${container_names[@]:0:$((head_index))}" "${container_names[@]:$head_index+1}")


# Write ipv4 to host file
for i in "${!container_names[@]}"
do
    ipv4=$(docker inspect -f "{{ .NetworkSettings.Networks.$NETWORK_NAME.IPAddress }}" ${container_names[$i]})
    echo "${container_names[$i]}: $ipv4"
    echo $ipv4 >> $FILE
done

echo "Entries added to $FILE"

