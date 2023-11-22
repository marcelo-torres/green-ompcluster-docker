#!/bin/bash

#docker run -it ompc-mpi-base

cd task-bench

step=1000
width=7

basic_types=(
    trivial
    stencil_1d
    stencil_1d_periodic
    dom
    tree
    fft
    nearest
    no_comm
    "spread -period 2"
    random_nearest
)

compute_bound="-kernel compute_bound -iter 1024"
for t in "${basic_types[@]}"; do
    echo $t
    mpirun -np 4 ./ompcluster/main -steps $step -width $width -type $t $compute_bound | grep Tasks
    echo
done

