import csv
import json
import sys

def microsecond_to_second(microsecond):
    return microsecond / 1000000

def is_task_execution_event(event):
    name = event['name']
    if name is None:
        return False
    return name.startswith('Task')

def get_task_id_from_event(event):
    name = event['name']
    if name is None:
        return None
    
    s = name.split(' ')
    return int(s[1])

def get_tasks_durations(trace_file):
    with open(trace_file) as f:
        data = json.load(f)
        tasks_duration = []

        for event in data['traceEvents']:
            if(is_task_execution_event(event)):
                task_id = get_task_id_from_event(event)
                task_duration = microsecond_to_second(float(event['dur']))

                tasks_duration.append(
                    (task_id, task_duration)
                )
        return tasks_duration

def save_tasks_durations_to_csv(file_path, durations):
    headers = ['Task Id', 'Duration (seconds)']

    with open(file_path, 'w', encoding='UTF8') as file:
        writer = csv.writer(file)
        writer.writerow(headers)

        for task_id, task_duration in durations:
            writer.writerow([str(task_id), str(task_duration)])

def sortByTaskId(task_id_duration):
  return task_id_duration[0]

def tune_tasks_duration(tasks_duration):
    #tasks_duration.sort(key=sortByTaskId)
    first_id = tasks_duration[0][0]
    first_id-=1

    return[ (task_id-first_id, task_duration) for task_id, task_duration in tasks_duration]

def get_args():
    args = sys.argv[1:]
    if len(args) != 2:
        sys.exit('Invalid arguments')
    trace_file = args[0]
    csv_file = args[1]

    return trace_file, csv_file



if __name__ == '__main__':
    
    trace_file, csv_file = get_args()

    tasks_duration = get_tasks_durations(trace_file)
    tasks_duration.sort(key=sortByTaskId)
    tasks_duration = tune_tasks_duration(tasks_duration)
    
    save_tasks_durations_to_csv(csv_file, tasks_duration)