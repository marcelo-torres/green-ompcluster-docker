import csv
import random
import os

def get_mean_durations_from_files(files):

    tasks_durations=[]

    for file in files:
        with open(file, newline='') as csv_file:
            csv_reader = csv.reader(csv_file)
            for count, row in enumerate(csv_reader):
                if count == 0: # Ignore header
                    continue
                task_duration=float(row[1])
                tasks_durations.append(
                    task_duration
                )
    return tasks_durations

def get_mean_durations_from_worker(iterations, worker_name):
    mean_durations_file=[]

    for it in iterations:
        for i in range(10):
            id=i+1
            file_name = f'selected_traces/{worker_name}/iter_{it}/{id}/{worker_name}-iter_{it}-durations_{id}.csv'
            mean_durations_file.append(
                file_name
            )
    
    return get_mean_durations_from_files(mean_durations_file)

def get_mean_durations_from_workers_list(iterations, workers):
    workers_tasks_durations_list = []
    for worker in workers:
        tasks_durations = get_mean_durations_from_worker(iterations, worker)
        workers_tasks_durations_list.append(
            (worker, tasks_durations)
        )
    return workers_tasks_durations_list

def get_graph_sizes(graph_sizes_file):

    graph_sizes = []

    with open(graph_sizes_file, newline='') as csv_file:
        csv_reader = csv.reader(csv_file)
        for count, row in enumerate(csv_reader):
             if count == 0: # Ignore header
                 continue
             graph_type=row[0]
             tasks_count=int(row[1])

             graph_sizes.append(
                 (graph_type, tasks_count)
             )

        return graph_sizes

def generate_tasks_durations(tasks_durations, count, seed):
    random.seed(seed)

    generated_tasks_durations = []
    for i in range(count):
        task_duration = random.choice(tasks_durations)
        generated_tasks_durations.append(
            (i+1, task_duration)
        )
    return generated_tasks_durations


def save_to_file(generate_tasks_durations, file_name):
    headers = ['Task Id', 'Mean duration (seconds)']
    
    with open(file_name, 'w', encoding='UTF8') as file:
        writer = csv.writer(file)
        writer.writerow(headers)

        for task_id, task_duration in generate_tasks_durations:
            writer.writerow([str(task_id), str(task_duration)])


def generate_tasks_durations_and_save(graph_sizes, workers_tasks_durations_list, seed):
    for graph_type, tasks_count in graph_sizes:
        for worker, tasks_durations in workers_tasks_durations_list:
            generated_tasks_durations = generate_tasks_durations(tasks_durations, tasks_count, seed)
            
            file_location=f'tasks_durations/{graph_type}'
            file_name=f'{worker}.csv'

            if not os.path.exists(file_location):
                os.makedirs(file_location) 

            save_to_file(generated_tasks_durations, file_location+'/'+file_name)

if __name__ == '__main__':

    seed = 1700704603
    graph_type_sizes_file='./graph_type_sizes_64x32.csv'

    iterations = [68719476736]
    workers=['amd_epyc_7453', 'intel_i5h', 'intel_i3']
   
    graph_sizes = get_graph_sizes(graph_type_sizes_file)
    workers_tasks_durations_list = get_mean_durations_from_workers_list(iterations, workers)
    generate_tasks_durations_and_save(graph_sizes, workers_tasks_durations_list, seed)
