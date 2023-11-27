#!/bin/bash

base_path='selected_traces'

processors=(
    amd_epyc_7453
    intel_i3
    intel_i5h
)

iterations=(
    '34359738368'
    '68719476736'
)

for p in "${!processors[@]}"
do
    processor=${processors[$p]}

    base_path_processor="$base_path/$processor"

    for it in "${!iterations[@]}"
    do
        iteration=${iterations[$it]}
        echo $iteration

        base_path_it="$base_path_processor/iter_$iteration"

        mean_duration_file=$processor'-iter_'$iteration'_mean_durations.csv'
        printf "python3 mean_tasks_durations.py $base_path_it/$mean_duration_file "
        for i in $(seq 1 10)
        do
            file=$processor'-iter_'$iteration'-durations_'$i'.csv'
            full_path="$base_path_it/$i/$file"
            printf "$full_path "
        done
        echo -e "\n"
    done
done