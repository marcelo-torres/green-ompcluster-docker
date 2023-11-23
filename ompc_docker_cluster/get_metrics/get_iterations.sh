#!/bin/bash

ROOT=/volume
HOST_FILE=$ROOT/ompc-host-file
TRACES_DIR=$ROOT/traces
prefix="get_metrics"


#
# CONFIGURATION
#

separator="_"

head_container='head'$separator'1'
containers=('worker_c1'$separator'1' 'worker_c2'$separator'1' 'worker_c4'$separator'1')
execution_iterations=(
    1024
    1048576 # 1024 * 1024
    1073741824 # 1024 * 1024 * 1024
)
executions_per_container=10

#
# EXECUTION
#

# Prepare ompcbench and OMPC scheduler
cd /ompcbench/
source venv/bin/activate
export OMPCLUSTER_SCHEDULER=nheft


for i in "${!containers[@]}"
do
    container_name="${containers[$i]}"
    worker_container="$prefix""$separator""$container_name"

    for j in "${!execution_iterations[@]}"
    do
        iterations="${execution_iterations[$j]}"

        iteration_trace_dir=$TRACES_DIR/$container_name/iter_$iterations

        tasks_durations_files=()
        for exec in $(seq 1 $executions_per_container)
        do
            echo
            echo "$exec of $executions_per_container - $iterations iter. ($container_name)"
            
            # Prepare trace file prefix
            current_trace_dir="$iteration_trace_dir/$exec"
            trace_file_prefix="$container_name-iter_$iterations-$exec"

            # Prepare context
            cd $ROOT
            if [ -d "$current_trace_dir" ]; then
                echo "$current_trace_dir will be deleted."
                rm -r $current_trace_dir
            fi
            mkdir -p $current_trace_dir

            # Update host file
            rm $HOST_FILE
            head_container_full_name="$prefix""$separator""$head_container"
            echo -e "$head_container_full_name\n$worker_container:1" >> $HOST_FILE

            # Set trace env variables
            full_trace_prefix="$current_trace_dir/$trace_file_prefix"
            export OMPCLUSTER_PROFILE=$full_trace_prefix
            export OMPCLUSTER_TASK_GRAPH_DUMP_PATH=$full_trace_prefix

            # Execute application
            echo "Executing application..."            
            mpirun -np 2 --hostfile $HOST_FILE /task-bench/ompcluster/main -steps 1 -width 1 -type trivial -kernel compute_bound -iter $execution_iterations

            # Merge trace files
            echo "Merging trace files..."
            cd $current_trace_dir
            merged_trace_file_name="$container_name-iter_$iterations-merged.json"
            merged_trace_file="$current_trace_dir/$merged_trace_file_name"
            ompcbench merge --ompc-prefix $trace_file_prefix --output $merged_trace_file_name

            # Extract tasks durations
            cd $ROOT
            tasks_durations_file="$current_trace_dir/$container_name-iter_$iterations-durations_""$exec"".csv"
            python3 extract_tasks_durations.py $merged_trace_file $tasks_durations_file
            tasks_durations_files+=($tasks_durations_file)
        done

        tasks_durations_files_arg=$(printf " %s" "${tasks_durations_files[@]}")
        tasks_durations_files_arg=${tasks_durations_files_arg:1}
        echo $tasks_durations_files
        
        tasks_mean_duration_file="$iteration_trace_dir/$container_name-iter_$iterations""_mean_durations.csv"
        python3 mean_tasks_durations.py $tasks_mean_duration_file $tasks_durations_files
    done
done
