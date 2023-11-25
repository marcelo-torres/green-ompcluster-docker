#!/bin/bash

algorithms=(
    #heft
    #moheft_energy
    moheft_green_energy
)

base_path='experiment_1'

topologies=(
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

for i in "${!algorithms[@]}"
do
    algoritm="${algorithms[$i]}"
    export OMPCLUSTER_SCHEDULER=$algoritm

    for j in "${!topologies[@]}"
    do
        topology="${topologies[$j]}"
        experiment_path=$base_path/$topology
        export OMPCLUSTER_SCHEDULER_INPUT_DIRECTORY=$experiment_path

        echo $OMPCLUSTER_SCHEDULER
        echo $OMPCLUSTER_SCHEDULER_INPUT_DIRECTORY

        mpirun -np 24 /task-bench/ompcluster/main -steps 20 -width 10 -type $topology -kernel compute_bound -iter 1
    done

done

