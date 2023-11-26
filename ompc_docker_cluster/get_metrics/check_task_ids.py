import sys
import csv

def get_ids_from_csv_file(file):
    with open(file, newline='') as csvfile:
        csv_reader = csv.reader(csvfile)
        tasks_ids=[]
        for count, row in enumerate(csv_reader):
            if count == 0: # Ignore header
                continue
            task_id=int(row[0])
            tasks_ids.append(
                task_id
            )
    return tasks_ids

def are_task_ids_valid(tasks_ids):
    last_id = 0
    for actual_id in tasks_ids:
        valid = actual_id == last_id +1
        if not valid:
            return False
        last_id = actual_id

    return True

if __name__ == '__main__':

    file_to_check = sys.argv[1:][0]
    try:
        tasks_ids = get_ids_from_csv_file(file_to_check)
        valid = are_task_ids_valid(tasks_ids)
    except:
        valid = False
    
    if valid:
        print('0')
    else:
        print('1')