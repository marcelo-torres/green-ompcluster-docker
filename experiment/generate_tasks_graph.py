from csv import reader  

def get_cluster_files(worker_c1_file, worker_c2_file, worker_c4_file):
    cluster_files = []

    def append_machines_to_cluster(count, model):
        for i in range(count):
            cluster_files.append(worker_c1_file)

    # Head
    append_machines_to_cluster(1, worker_c1_file)

    # DC-01
    append_machines_to_cluster(8, worker_c1_file)

    # DC-02
    append_machines_to_cluster(2, worker_c1_file)
    append_machines_to_cluster(4, worker_c2_file)

    # DC-03
    append_machines_to_cluster(1, worker_c1_file)
    append_machines_to_cluster(1, worker_c2_file)
    append_machines_to_cluster(1, worker_c4_file)

    # DC-04
    append_machines_to_cluster(2, worker_c2_file)
    append_machines_to_cluster(4, worker_c4_file)

    return cluster_files

def get_tasks_durations(source_file):
    
    with open(source_file, 'r') as file:
        csv_reader = reader(file)
        
        tasks_durations = []
        for line, row in enumerate(csv_reader):
            if line == 0:
                continue # skip header
            task_duration = row[1]
            tasks_durations.append(task_duration)
        
        return tasks_durations


def generate_task_graph(cluster_files):

    graph = '1'
    graph_name = f'OMPCLUSTER_HEFT_TASKS_GRAPH_{graph}'

    with open(graph_name, 'w') as f:
        f.write(graph_name + '\n')
        f.write('OMPCLUSTER_HEFT_COMP_G_x_P_y_T_z' + '\n')

        for source_file in cluster_files:
            tasks_durations = get_tasks_durations(source_file)
            row =','.join(tasks_durations)
            f.write(row + '\n')

    pass

if __name__ == '__main__':
    worker_c1_file = './../ompc_docker_cluster/get_metrics/application/traces/worker_c1_1/worker_c1_1_mean_durations_and_energy.csv'
    worker_c2_file = './../ompc_docker_cluster/get_metrics/application/traces/worker_c2_1/worker_c2_1_mean_durations_and_energy.csv'
    worker_c4_file = './../ompc_docker_cluster/get_metrics/application/traces/worker_c4_1/worker_c4_1_mean_durations_and_energy.csv'

    cluster_files = get_cluster_files(worker_c1_file, worker_c2_file, worker_c4_file)
    generate_task_graph(cluster_files)
    

    pass