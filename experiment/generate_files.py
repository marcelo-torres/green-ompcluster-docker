from csv import reader  
import os
import shutil

from datetime import datetime, timedelta

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


def get_cluster_green_energy_files(
        dc01_file, dc01_init_timedelta,
        dc02_file, dc02_init_timedelta,
        dc03_file, dc03_init_timedelta,
        dc04_file, dc04_init_timedelta
        ):
    cluster_files = []

    def append_machines_to_cluster(count, model, pv_area, init_timedelta):
        for i in range(count):
            cluster_files.append(
                (model, pv_area, init_timedelta)
            )

    # Head
    append_machines_to_cluster(1, dc01_file, 1, dc01_init_timedelta)

    # DC-01
    append_machines_to_cluster(8, dc01_file, 1, dc01_init_timedelta)

    # DC-02
    append_machines_to_cluster(6, dc02_file, 1, dc02_init_timedelta)

    # DC-03
    append_machines_to_cluster(3, dc03_file, 1, dc03_init_timedelta)

    # DC-04
    append_machines_to_cluster(6, dc04_file, 1, dc04_init_timedelta)

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


def to_datetime_from_string(dt_str):
    dt_str = dt_str.split(' ')
    date = dt_str[0]
    date = list(map(int, date.split('-')))
    time = dt_str[1]
    time = list(map(int, time.split(':')))

    return datetime(date[0], date[1], date[2], time[0], time[1], time[2])


def get_green_energy_available(source_file, pv_area, init_timedelta):
    
    with open(source_file, 'r') as file:
        csv_reader = reader(file)
        
        init_dt_time = None

        solar_irradiance_list= []
        for line, row in enumerate(csv_reader):
            if line == 0:
                continue # skip header

            dt = to_datetime_from_string(row[0])

            if line == 1 and init_timedelta is not None:
                init_dt_time = dt + init_timedelta
                print(init_dt_time)

            if dt < init_dt_time:
                continue

            if dt < init_dt_time + timedelta(hours=24):
                continue

            solar_irradiance_in_W_m2 = float(row[2])
            solar_irradiance = pv_area * solar_irradiance_in_W_m2

            # Energy (J) = Potency (W) * Time (s)
            total_green_power_during_one_minute = solar_irradiance * 60

            solar_irradiance = round(solar_irradiance, DEFAULT_ROUND)
            for i in range (5):
                # The source file logs solar irradiance in interval of 5 minutes, but the target file expects
                # 1 minute intervals
                solar_irradiance_list.append(
                    str(total_green_power_during_one_minute)
                 )
        
        return solar_irradiance_list
    

def generate_task_graph_file(cluster_files, file_location, graph='1'):

    graph_name = f'OMPCLUSTER_HEFT_TASKS_GRAPH_{graph}'

    with open(file_location + graph_name, 'w') as f:
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
            energy_usage_communication = ['0' for i in enumerate(power_usages)]
            row =','.join(energy_usage_communication) # TODO
            f.write(row + '\n')


def generate_green_energy_available_file(cluster_green_energy_files):
    file_name = 'OMPCLUSTER_MOHEFT_GREEN_ENER'
    with open(file_name, 'w') as f:
        f.write(file_name + '\n')
        f.write('OMPCLUSTER_MOHEFT_GREEN_P_x_I_y' + '\n')

        for source_file, pv_area, init_timedelta in cluster_green_energy_files:
            green_energy_available = get_green_energy_available(source_file, pv_area, init_timedelta)
            row =','.join(green_energy_available)
            f.write(row + '\n')


def generate_no_green_energy_available_file(lines, columns):
    file_name = 'OMPCLUSTER_MOHEFT_GREEN_ENER'
    with open(file_name, 'w') as f:
        f.write(file_name + '\n')
        f.write('OMPCLUSTER_MOHEFT_GREEN_P_x_I_y' + '\n')

        for i in range(lines): 
            row =','.join('0' * columns)
            f.write(row + '\n')


if __name__ == '__main__':

    c1_power = 15 * 60 # Intel Core i3-6006U -> 100% *  15W
    c2_power = 45 * 60  # Intel Core i5-10300H -> 100% * 45W
    c4_power = 184.5 * 60  # AMD EPYC 7453 -> 41% * 2 * 225W = 184.5W

    power_usages = get_cluster_energy_usage(c1_power, c2_power, c4_power)
    generate_task_energy_consumption_file(power_usages)

    generate_no_green_energy_available_file(24, 100)

    experiment_1 = ['experiment_1']
    experiment_2 = ['experiment_2_1', 'experiment_2_2', 'experiment_2_3', 'experiment_2_4']
    
    for experiment in experiment_1 + experiment_2:
        if not os.path.exists(experiment):
            os.mkdir(experiment)

    topologies = [
        'trivial',
        'stencil_1d',
        'stencil_1d_periodic',
        'dom',
        'tree',
        'fft',
        'nearest',
        'no_comm',
        'spread -period 2',
        'random_nearest',
    ]

    base_path = './../ompc_docker_cluster/get_metrics/tasks_durations/'

    for topology in topologies:
        worker_c1_file = f'{base_path}/{topology}/intel_i3.csv'
        worker_c2_file = f'{base_path}/{topology}/intel_i5h.csv'
        worker_c4_file = f'{base_path}/{topology}/amd_epyc_7453.csv'

        location = f'experiment_1/{topology}/'
        if os.path.exists(location):
            shutil.rmtree(location)
        os.mkdir(location)

        shutil.copyfile('OMPCLUSTER_HEFT_RANKS', f'{location}OMPCLUSTER_HEFT_RANKS')
        shutil.copyfile('OMPCLUSTER_MOHEFT_ENER_CONS', f'{location}OMPCLUSTER_MOHEFT_ENER_CONS')
        shutil.copyfile('OMPCLUSTER_MOHEFT_SEL_CRIT', f'{location}OMPCLUSTER_MOHEFT_SEL_CRIT')
        shutil.copyfile('OMPCLUSTER_MOHEFT_GREEN_ENER', f'{location}OMPCLUSTER_MOHEFT_GREEN_ENER')
  
        cluster_files = get_cluster_files(worker_c1_file, worker_c2_file, worker_c4_file)
        generate_task_graph_file(cluster_files, location, graph=1)
        generate_task_graph_file(cluster_files, location, graph=2)

    dc01_file = './../photovolta/data/splitted/selected/m282-29_photovolta_2016_part_1_17.csv'
    dc02_file = './../photovolta/data/splitted/selected/m166-13_photovolta_2016_part_1_7.csv'
    dc03_file = './../photovolta/data/splitted/selected/m280-19_photovolta_2016_part_1_13.csv'
    dc04_file = './../photovolta/data/splitted/selected/m33-86_photovolta_2016_part_2_4.csv'

    dc01_time = 0
    dc02_time = 6
    dc03_time = 12
    dc04_time = 18

    for i in range(4):
        # It simulates the cycle day
        dc01_time += 6 * i
        dc02_time += 6 * i
        dc03_time += 6 * i
        dc04_time += 6 * i

        cluster_green_energy_files = get_cluster_green_energy_files(
            dc01_file, timedelta(hours=dc01_time),
            dc02_file, timedelta(hours=dc02_time),
            dc03_file, timedelta(hours=dc03_time),
            dc04_file, timedelta(hours=dc04_time)
        )

        generate_green_energy_available_file(cluster_green_energy_files)

        experiment = experiment_2[i]

        for topology in topologies:
            location = f'{experiment}/{topology}/'
            if os.path.exists(location):
                shutil.rmtree(location)
            os.mkdir(location)

            shutil.copyfile('OMPCLUSTER_HEFT_RANKS', f'{location}OMPCLUSTER_HEFT_RANKS')
            shutil.copyfile('OMPCLUSTER_MOHEFT_ENER_CONS', f'{location}OMPCLUSTER_MOHEFT_ENER_CONS')
            shutil.copyfile('OMPCLUSTER_MOHEFT_SEL_CRIT', f'{location}OMPCLUSTER_MOHEFT_SEL_CRIT')
            shutil.copyfile('OMPCLUSTER_MOHEFT_GREEN_ENER', f'{location}OMPCLUSTER_MOHEFT_GREEN_ENER')

            exp1_location = f'experiment_1/{topology}/'
            shutil.copyfile(f'{exp1_location}OMPCLUSTER_HEFT_TASKS_GRAPH_1', f'{location}OMPCLUSTER_HEFT_TASKS_GRAPH_1')

        
        
    
