#!/bin/bash

#
# Build base image
#
ssh-keygen -t rsa -f ./id_rsa -q -N ""
docker build -t ompc-mpi-base .
rm id_rsa
rm id_rsa.pub
