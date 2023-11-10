import sys
import csv

def get_mean_durations_from_files(files):

    durations_list=[]

    for file in files:
        with open(file, newline='') as csvfile:
            csv_reader = csv.reader(csvfile)
            tasks_durations=[]
            for count, row in enumerate(csv_reader):
                if count == 0: # Ignore header
                    continue
                tasks_duration=float(row[1])
                tasks_durations.append(
                    tasks_duration
                )
            durations_list.append(
                tasks_durations
            )
    
    assert len(durations_list) > 0
    for i in range(len(durations_list)-1):
        assert len(durations_list[i]) == len(durations_list[i+1])

    size = len(durations_list[0])
    sum = [0] * size
    for list in durations_list:
        for i in range(size):
            sum[i] += list[i]

    mean_durations = [0] * size
    count = len(durations_list)
    for i in range(size):
        mean_durations[i] = sum[i] / count

    return[ (i+1, mean_durations[i]) for i in range(size)]

def save_tasks_durations_to_csv(file_path, durations):
    headers = ['Task Id', 'Mean duration (seconds)']

    with open(file_path, 'w', encoding='UTF8') as file:
        writer = csv.writer(file)
        writer.writerow(headers)

        for task_id, task_duration in durations:
            writer.writerow([str(task_id), str(task_duration)])

def get_args():
    args = sys.argv[1:]
    if len(args) < 2:
        sys.exit('Invalid arguments')
    merge_file = args[0:1][0]
    input_files = args[1:]

    return merge_file, input_files

if __name__ == '__main__':
    merge_file, input_files = get_args()

    mean_durations = get_mean_durations_from_files(input_files)

    save_tasks_durations_to_csv(merge_file, mean_durations)


