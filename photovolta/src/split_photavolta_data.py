import csv
import statistics

from datetime import datetime

def to_date_time(date_time_str):
    date_format = '%Y-%m-%d %H:%M:%S'
    return datetime.strptime(date_time_str, date_format)
    
def split_photovolta(source_file, new_files_prefix, report_file_name):
    with open(source_file, 'r', encoding='UTF-8') as photovolta_file:
        
        WINDOW_SIZE = 604800 # 7 days = 7 * 86400s; 1 Day = 86400s
        
        
        writer = None
        i = 0
        interval_values = []
        
        files_count = 0
        
        sep = ','
        report_file = open(report_file_name, 'w')
        report_file.write(f'Count{sep}Standard Deviation{sep}Mean{sep}File name\n')        
        
        def report_values(interval_values, file_name):
            std = statistics.stdev(interval_values)
            mean = statistics.mean(interval_values)
            
            print(f'\tCount: {len(interval_values)}')
            print('\tStandard Deviation: %.2f' % std)
            print('\tMean: %.2f\n' % mean)

            report_file.write(f'{len(interval_values)}{sep}{std}{sep}{mean}{sep}{file_name}\n')

        for line_number, line in enumerate(photovolta_file):
            if(line_number == 0):
                continue # skip header
               
            row = line.strip().split(',')
            date_time = to_date_time(row[0])
            interval_in_seconds = int(row[1])
            solar_irradiance = float(row[2])
            
            # Create a new file for each new subset
            if i == 0:         
                file_name = f'{new_files_prefix}_{files_count}.csv'
                msg = f'[{files_count}] Writing file {file_name}'
                print(msg)
                f = open(file_name, 'w')                
                writer = csv.writer(f)       
                writer.writerow(['timestamp', 'interval_in_seconds', 'solar_irradiance_in_W_m2'])
                
            writer.writerow([date_time, interval_in_seconds, solar_irradiance])
            interval_values.append(solar_irradiance)
            i += 300 # 300s = 5min

            if i >= WINDOW_SIZE:
                report_values(interval_values, file_name)
                
                f.close()
                writer = None
                i = 0
                interval_values = []
                files_count += 1
        if i < WINDOW_SIZE:
            report_values(interval_values, file_name)
            f.close()

        report_file.close()
        
    
if __name__ == '__main__':
    split_photovolta('../data/photovolta_2016_part_1.csv', '../data/splitted/photovolta_2016_part_1', '../data/splitted/report_part_1.csv')
    split_photovolta('../data/photovolta_2016_part_2.csv', '../data/splitted/photovolta_2016_part_2', '../data/splitted/report_part_2.csv')
                          
        
        
        
