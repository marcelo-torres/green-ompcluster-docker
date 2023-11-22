#!/bin/bash

prefix="get_metrics"
separator="_"

head_container='head'$separator'1'
containers=('worker_c1'$separator'1' 'worker_c2'$separator'1' 'worker_c4'$separator'1')


EXECUTIONS_PER_CONTAINER=10
APPLICATION_DIR=/volume/application
HOST_FILE=/volume/ompc-host-file

# Application Variables
execution_graph_height=7
execution_graph_width=7
execution_iterations=4000000
#execution_iterations=1073741824 # 1024 * 1024 * 1024

cd /ompcbench/
source venv/bin/activate
export OMPCLUSTER_SCHEDULER=nheft

graph_types=(
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

for i in "${!containers[@]}"
do
    worker_container="$prefix""$separator""${containers[$i]}"
    
    for g in "${!graph_types[@]}"
    do
        graph_type="${graph_types[$g]}"
        
        # Remove spaces
        oldstr=" "
        newstr="_"
        graph_type_without_space=$(echo $graph_type | sed "s/$oldstr/$newstr/g")
        echo $
    
        tasks_durations_files=()
        for exec in $(seq 1 $EXECUTIONS_PER_CONTAINER)
        do
            trace_file_prefix="$graph_type_without_space""_""${containers[$i]}"
            must_execute=1
            while [ $must_execute -ne 0 ]
            do
                echo
                echo "$exec of $EXECUTIONS_PER_CONTAINER - $trace_file_prefix"
              
                # Prepare context
                cd $APPLICATION_DIR
                relative_trace_dir="traces/${containers[$i]}/$graph_type_without_space/$exec"
                trace_dir="$APPLICATION_DIR/$relative_trace_dir"
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
                mpirun -np 2 --hostfile $HOST_FILE /task-bench/ompcluster/main -steps $execution_graph_height -width $execution_graph_width -type $graph_type -kernel compute_bound -iter $execution_iterations

                # Merge output
                merged_trace_file="$trace_file_prefix"".json"
                cd $trace_dir
                ompcbench merge --ompc-prefix $trace_file_prefix --output "$trace_dir/$merged_trace_file"
                #ompcbench filter --ompc-prefix $trace_file_prefix --output $merged_trace_file

                # Extract tasks durations
                cd /volume
                relative_path_to_trace="./application/$relative_trace_dir/"
                tasks_durations_file="$relative_path_to_trace""$trace_file_prefix""_durations_""$exec"".csv"
                
                tasks_durations_files+=($tasks_durations_file)
                python3 extract_tasks_durations.py "$relative_path_to_trace""$merged_trace_file" $tasks_durations_file
                
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
        
        tasks_mean_duration_file="$relative_path_to_trace""../""$trace_file_prefix""_mean_durations.csv"
        python3 mean_tasks_durations.py $tasks_mean_duration_file $tasks_durations_files
    done
    
    #cat tracing.json | jq . > tracing_formatted.json
    #dot -Tpdf worker_c4_1_graph_0.dot > graph_0.pdf
done





