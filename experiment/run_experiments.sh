#!/bin/bash

# docker run --name ompc-experiment -v $PWD:/volume -it ompc-mpi-base 

output_file='output.txt'

algorithms=(
    heft
    moheft_energy
    moheft_green_energy
)

experiments=(
    'experiment_1'
    'experiment_2_1'
    'experiment_2_2'
    'experiment_2_3'
    'experiment_2_4'
)



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

echo $(date) > $output_file

for e in "${!experiments[@]}"
do
    experiment="${experiments[$e]}"
    base_path=/ompc/volume/experiment/$experiment

    echo
    echo ==== $experiment ====
    echo

    echo >> $output_file
    echo ==== $experiment ==== >> $output_file
    echo >> $output_file

    for i in "${!algorithms[@]}"
    do
        algoritm="${algorithms[$i]}"
        export OMPCLUSTER_SCHEDULER=$algoritm

        echo $algoritm
        echo
        echo $algoritm >> $output_file
        echo >> $output_file

        for j in "${!topologies[@]}"
        do
            topology="${topologies[$j]}"

            echo $topology
            echo $topology >> $output_file

            experiment_path=$base_path/$topology
            export OMPCLUSTER_SCHEDULER_INPUT_DIRECTORY=$experiment_path


            output=$(mpirun -np 24 /task-bench/ompcluster/main -steps 20 -width 10 -type $topology -kernel compute_bound -iter 1 | grep -E 'Objectives|Makespan')
            echo $output
            echo $output >> $output_file
            echo
            echo >> $output_file
        done
    done

done
