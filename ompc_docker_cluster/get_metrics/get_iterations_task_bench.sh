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
execution_iterations=(
    #1024
    #536870912 # 2^29
    #8589934592 # 2^33
    #17179869184 # 2^34
    #34359738368 # 2^35
    
    68719476736 # 2^36
   
   
    # > 6 minutes
    #137438953472 # 2^37
    #274877906944 # 2^38
    #549755813888 # 2^39
)
executions_per_machine=10

#
# EXECUTION
#

# Prepare ompcbench and OMPC scheduler
cd /ompcbench/
source venv/bin/activate
export OMPCLUSTER_SCHEDULER=nheft

machine='intel_i5h'


for j in "${!execution_iterations[@]}"
do
    iterations="${execution_iterations[$j]}"

    iteration_trace_dir=$TRACES_DIR/$machine/iter_$iterations

    tasks_durations_files=()
    for exec in $(seq 1 $executions_per_machine)
    do
        echo
        echo "$exec of $executions_per_machine - $iterations iter. ($machine)"
        
        # Prepare trace file prefix
        current_trace_dir="$iteration_trace_dir/$exec"
        trace_file_prefix="$machine-iter_$iterations-$exec"

        # Prepare context
        cd $ROOT
        if [ -d "$current_trace_dir" ]; then
            echo "$current_trace_dir will be deleted."
            rm -r $current_trace_dir
        fi
        mkdir -p $current_trace_dir

        # Set trace env variables
        full_trace_prefix="$current_trace_dir/$trace_file_prefix"
        export OMPCLUSTER_PROFILE=$full_trace_prefix
        export OMPCLUSTER_TASK_GRAPH_DUMP_PATH=$full_trace_prefix

        # Execute application
        echo "Executing application..."            
        mpirun -np 2 /task-bench/ompcluster/main -steps 1 -width 1 -type trivial -kernel compute_bound -iter $execution_iterations

        # Merge trace files
        echo "Merging trace files..."
        cd $current_trace_dir
        merged_trace_file_name="$machine-iter_$iterations-merged.json"
        merged_trace_file="$current_trace_dir/$merged_trace_file_name"
        ompcbench merge --ompc-prefix $trace_file_prefix --output $merged_trace_file_name

        # Extract tasks durations
        cd $ROOT
        tasks_durations_file="$current_trace_dir/$machine-iter_$iterations-durations_""$exec"".csv"
        python3 extract_tasks_durations.py $merged_trace_file $tasks_durations_file
        tasks_durations_files+=($tasks_durations_file)
    done

    tasks_durations_files_arg=$(printf " %s" "${tasks_durations_files[@]}")
    tasks_durations_files_arg=${tasks_durations_files_arg:1}
    echo $tasks_durations_files
    
    tasks_mean_duration_file="$iteration_trace_dir/$machine-iter_$iterations""_mean_durations.csv"
    python3 mean_tasks_durations.py $tasks_mean_duration_file $tasks_durations_files
done
