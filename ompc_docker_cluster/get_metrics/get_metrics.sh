#!/bin/bash

prefix="get_metrics"
separator="_"

head_container='head'$separator'1'
containers=('worker_c1'$separator'1' 'worker_c2'$separator'1' 'worker_c4'$separator'1')


EXECUTIONS_PER_CONTAINER=10
APPLICATION_DIR=/volume/application
HOST_FILE=/volume/ompc-host-file

cd /ompcbench/
source venv/bin/activate
export OMPCLUSTER_SCHEDULER=nheft

for i in "${!containers[@]}"
do
    worker_container="$prefix""$separator""${containers[$i]}"
    
    tasks_durations_files=()
    for exec in $(seq 1 $EXECUTIONS_PER_CONTAINER)
    do
        trace_file_prefix=${containers[$i]}
        must_execute=1
        while [ $must_execute -ne 0 ]
        do
            echo
            echo "$exec of $EXECUTIONS_PER_CONTAINER - $trace_file_prefix"
          
            # Prepare context
            cd $APPLICATION_DIR
            trace_dir="$APPLICATION_DIR/traces/$trace_file_prefix/$exec"
            if [ -d "$trace_dir" ]; then
                echo "$trace_dir will be deleted."
                rm -r $trace_dir
            fi
            mkdir -p $trace_dir
            
            # Set OMPC trace variables
            export full_trace_file_prefix="$trace_dir/$trace_file_prefix"
            export OMPCLUSTER_PROFILE=$full_trace_file_prefix
            export OMPCLUSTER_TASK_GRAPH_DUMP_PATH=$full_trace_file_prefix

            # Update host file
            rm $HOST_FILE
            head_container_full_name="$prefix""$separator""$head_container"
            echo -e "$head_container_full_name\n$worker_container:1" >> $HOST_FILE
            
            # Run application
            mpirun -np 2 --hostfile $HOST_FILE ./matmul 40 20

            # Merge output
            merged_trace_file="$trace_file_prefix"".json"
            cd $trace_dir
            ompcbench merge --ompc-prefix $trace_file_prefix --output $merged_trace_file

            # Extract tasks durations
            cd /volume
            relative_path_to_trace="./application/traces/$trace_file_prefix/"
            relative_path_to_trace_exec="$relative_path_to_trace""$exec/"
            tasks_durations_file="$relative_path_to_trace_exec""$trace_file_prefix""_durations_""$exec"".csv"
            
            tasks_durations_files+=($tasks_durations_file)
            python3 extract_tasks_durations.py "$relative_path_to_trace_exec""$merged_trace_file" $tasks_durations_file
            
            must_execute=$(python3 check_task_ids.py $tasks_durations_file)
            if [ $must_execute -ne 0 ]
            then
              echo "File $tasks_durations_file contains a erro and it will be reprocessed"
            fi
        done
        
    done

    tasks_durations_files_arg=$(printf " %s" "${tasks_durations_files[@]}")
    tasks_durations_files_arg=${tasks_durations_files_arg:1}
    echo $tasks_durations_files
    
    tasks_mean_duration_file="$relative_path_to_trace""$trace_file_prefix""_mean_durations.csv"
    python3 mean_tasks_durations.py $tasks_mean_duration_file $tasks_durations_files
    
    #cat tracing.json | jq . > tracing_formatted.json
    #dot -Tpdf worker_c4_1_graph_0.dot > graph_0.pdf
done





