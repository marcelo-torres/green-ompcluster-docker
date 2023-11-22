from csv import reader  

DEFAULT_ROUND = 2

def get_cluster_files(worker_c1_file, worker_c2_file, worker_c4_file):
    cluster_files = []

    def append_machines_to_cluster(count, model):
        for i in range(count):
            cluster_files.append(model)

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


def get_cluster_energy_usage(c1_power, c2_power, c4_power):
    power_usages = []

    def append_machines_to_cluster(count, model):
        for i in range(count):
            power_usages.append(model)

    # Head
    append_machines_to_cluster(1, c1_power)

    # DC-01
    append_machines_to_cluster(8, c1_power)

    # DC-02
    append_machines_to_cluster(2, c1_power)
    append_machines_to_cluster(4, c2_power)

    # DC-03
    append_machines_to_cluster(1, c1_power)
    append_machines_to_cluster(1, c2_power)
    append_machines_to_cluster(1, c4_power)

    # DC-04
    append_machines_to_cluster(2, c2_power)
    append_machines_to_cluster(4, c4_power)

    return power_usages


def get_cluster_green_energy_files(dc01_file, dc02_file, dc03_file, dc04_file):
    cluster_files = []

    def append_machines_to_cluster(count, model, pv_area):
        for i in range(count):
            cluster_files.append(
                (model, pv_area)
            )

    # Head
    append_machines_to_cluster(1, dc01_file, 1)

    # DC-01
    append_machines_to_cluster(8, dc01_file, 1)

    # DC-02
    append_machines_to_cluster(6, dc02_file, 1)

    # DC-03
    append_machines_to_cluster(3, dc03_file, 1)

    # DC-04
    append_machines_to_cluster(6, dc04_file, 1)

    return cluster_files


def get_tasks_durations(source_file):
    
    with open(source_file, 'r') as file:
        csv_reader = reader(file)
        
        tasks_durations = []
        for line, row in enumerate(csv_reader):
            if line == 0:
                continue # skip header
            task_duration = float(row[1])
            task_duration = round(task_duration, DEFAULT_ROUND)
            tasks_durations.append(
                str(task_duration)
            )
        
        return tasks_durations


def get_tasks_energy_usage(source_file):
    
    with open(source_file, 'r') as file:
        csv_reader = reader(file)
        
        energy_usages = []
        for line, row in enumerate(csv_reader):
            if line == 0:
                continue # skip header
            energy_usage = float(row[2])
            energy_usage = round(energy_usage, DEFAULT_ROUND)
            energy_usages.append(
                str(energy_usage)
            )
        
        return energy_usages


def get_green_energy_available(source_file, pv_area):
    
    with open(source_file, 'r') as file:
        csv_reader = reader(file)
        
        solar_irradiance_list= []
        for line, row in enumerate(csv_reader):
            if line == 0:
                continue # skip header
            solar_irradiance_in_W_m2 = float(row[2])
            solar_irradiance = pv_area * solar_irradiance_in_W_m2
            solar_irradiance = round(solar_irradiance, DEFAULT_ROUND)
            solar_irradiance_list.append(  # TODO Multiply by 5
                str(solar_irradiance)
            )
        
        return solar_irradiance_list
    

def generate_task_graph_file(cluster_files):

    graph = '1'
    graph_name = f'OMPCLUSTER_HEFT_TASKS_GRAPH_{graph}'

    with open(graph_name, 'w') as f:
        f.write(graph_name + '\n')
        f.write('OMPCLUSTER_HEFT_COMP_G_x_P_y_T_z' + '\n')

        for source_file in cluster_files:
            tasks_durations = get_tasks_durations(source_file)
            row =','.join(tasks_durations)
            f.write(row + '\n')


def generate_task_energy_consumption_file(power_usages):

    file_name = 'OMPCLUSTER_MOHEFT_ENER_CONS'
    with open(file_name, 'w') as f:
        f.write(file_name + '\n')

        f.write('OMPCLUSTER_MOHEFT_IDLE_CONS_P_x' + '\n')
        energy_usage_idle = [str(round(power * 0.01, DEFAULT_ROUND)) for power in power_usages]
        row =','.join(energy_usage_idle)
        f.write(row + '\n')

        f.write('OMPCLUSTER_MOHEFT_EXEC_CONS_P_x' + '\n')
        row =','.join(map(str, power_usages))
        f.write(row + '\n')
        
        f.write('OMPCLUSTER_MOHEFT_CONS_P_x_P_y' + '\n')
        for source_file in power_usages:
            energy_usage_communication = ['1' for i in enumerate(power_usages)]
            row =','.join(energy_usage_communication) # TODO
            f.write(row + '\n')


def generate_green_energy_available_file(cluster_green_energy_files):
    file_name = 'OMPCLUSTER_MOHEFT_GREEN_ENER'
    with open(file_name, 'w') as f:
        f.write(file_name + '\n')
        f.write('OMPCLUSTER_MOHEFT_GREEN_P_x_I_y' + '\n')

        for source_file, pv_area in cluster_green_energy_files:
            green_energy_available = get_green_energy_available(source_file, pv_area)
            row =','.join(green_energy_available)
            f.write(row + '\n')


if __name__ == '__main__':
    worker_c1_file = './../ompc_docker_cluster/get_metrics/application/traces/worker_c1_1/worker_c1_1_mean_durations.csv'
    worker_c2_file = './../ompc_docker_cluster/get_metrics/application/traces/worker_c2_1/worker_c2_1_mean_durations.csv'
    worker_c4_file = './../ompc_docker_cluster/get_metrics/application/traces/worker_c4_1/worker_c4_1_mean_durations.csv'

    dc01_file = './../photovolta/data/splitted/selected/m282-29_photovolta_2016_part_1_17.csv'
    dc02_file = './../photovolta/data/splitted/selected/m166-13_photovolta_2016_part_1_7.csv'
    dc03_file = './../photovolta/data/splitted/selected/m280-19_photovolta_2016_part_1_13.csv'
    dc04_file = './../photovolta/data/splitted/selected/m38-05_photovolta_2016_part_2_4.csv'

    # AMD EPYC 7453 
    #   TDP: 225W
    #   Cores: 28
    #
    # Pc = 225W / 28 = 8.03571428571W
    #
    #
    # 1 x Pc ~  8.03571W
    # 2 x Pc ~ 16.07143W
    # 4 x Pc ~ 32.14286W
    c1_power = 8.03571
    c2_power = 16.07143
    c4_power = 32.14286

    cluster_files = get_cluster_files(worker_c1_file, worker_c2_file, worker_c4_file)
    generate_task_graph_file(cluster_files)

    power_usages = get_cluster_energy_usage(c1_power, c2_power, c4_power)
    generate_task_energy_consumption_file(power_usages)

    cluster_green_energy_files = get_cluster_green_energy_files(dc01_file, dc02_file, dc03_file, dc04_file)
    generate_green_energy_available_file(cluster_green_energy_files)
    