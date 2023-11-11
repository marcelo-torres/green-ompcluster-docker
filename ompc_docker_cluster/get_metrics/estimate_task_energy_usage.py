import sys
from csv import writer
from csv import reader

def add_column_in_csv(input_file, output_file, transform_row):
    """ Append a column in existing csv using csv.reader / csv.writer classes"""
    # https://thispointer.com/python-add-a-column-to-an-existing-csv-file/

    with open(input_file, 'r') as read_obj, \
            open(output_file, 'w', newline='') as write_obj:
        
        csv_reader = reader(read_obj)
        csv_writer = writer(write_obj)

        for row in csv_reader:
            transform_row(row, csv_reader.line_num)
            csv_writer.writerow(row)

def get_args():
    args = sys.argv[1:]
    if len(args) < 3:
        sys.exit('Invalid arguments')
    mean_tasks_duration_file = args[0]
    output_file = args[1]
    power = float(args[2])

    return mean_tasks_duration_file, output_file, power


def estimate_task_energy(mean_tasks_duration_file, output_file, power):

    def calculate(row, line_num):
        if line_num == 1: # Header
            row.append('Energy')
            return

        task_duration = float(row[1])
        task_energy = power * task_duration
        row.append(task_energy)

    add_column_in_csv(mean_tasks_duration_file, output_file, calculate)

if __name__ == '__main__':
    mean_tasks_duration_file, output_file, power = get_args()
    estimate_task_energy(mean_tasks_duration_file, output_file, power)
