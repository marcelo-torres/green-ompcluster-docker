#!/bin/bash

steps=20
with=10
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

compute_bound="-kernel compute_bound -iter 1"

file="graph_type_sizes_$steps"x"$with.csv"

echo -e "graph type,number of tasks" > $file

export OMPCLUSTER_SCHEDULER=heft
for t in "${basic_types[@]}"; do
    line=$(mpirun -np 1 /task-bench/ompcluster/main -steps $steps -width $with -type $t $compute_bound | grep "Total Tasks")
    tasks=$( echo $line | tr -d -c 0-9)
    echo "$t: $tasks"
    echo -e "$t, $tasks" >> $file
done