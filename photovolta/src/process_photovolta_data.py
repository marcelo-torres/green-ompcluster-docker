import csv

from datetime import datetime

def to_date_time(date_time_str):
    date_format = '%Y-%m-%d %H:%M:%S'
    return datetime.strptime(date_time_str, date_format)


def process_photovolta_data(source_file, new_file, date_time_limit):

    INTERVAL_SIZE = 300 # 300s = 5min
    ERROR_TOLERANCE_IN_SECONDS = 2

    def must_remove_data(date_time):
        return date_time_limit is not None and date_time < date_time_limit

    with open(source_file, 'r', encoding='UTF-8') as photovolta_file:
        with open(new_file, 'w', encoding='UTF8') as photovolta_new_file:
            writer = csv.writer(photovolta_new_file)
    
            previous_time_stamp = None
            offset = 0
            
            for line_number, line in enumerate(photovolta_file):
                if(line_number == 0): 
                    writer.writerow(['timestamp', 'interval_in_seconds', 'solar_irradiance_in_W_m2'])
                    continue # skip header
                
                row = line.strip().split(',')
                date_time = to_date_time(row[0])

                solar_irradiance = row[1]
                
                time_stamp = date_time.timestamp()
                if previous_time_stamp is None:
                    previous_time_stamp = time_stamp
                    time_stamp_diff = 0
                    diff = 0
                else:
                    time_stamp_diff = time_stamp - previous_time_stamp
                    diff = time_stamp_diff - INTERVAL_SIZE
                
                # Adjust intervals with a small error
                m = time_stamp_diff % INTERVAL_SIZE
                if m <= ERROR_TOLERANCE_IN_SECONDS:
                    time_stamp_diff -= m
                elif m >= (INTERVAL_SIZE - ERROR_TOLERANCE_IN_SECONDS):
                    time_stamp_diff += (INTERVAL_SIZE-m)
                
                
                if diff == 0:
                    # The time stamp diff is equal to INTERVAL_SIZE
                    offset+=INTERVAL_SIZE
                    
                elif diff >= -ERROR_TOLERANCE_IN_SECONDS and diff <= ERROR_TOLERANCE_IN_SECONDS:
                    # Some intervals have size equal between INTERVAL_SIZE-2 and INTERVAL_SIZE+2
                    offset+=INTERVAL_SIZE
                
                elif(time_stamp_diff > INTERVAL_SIZE and time_stamp_diff % INTERVAL_SIZE == 0):
                    # Include omitted intervalds due no solar irradiation
                
                    omitted_intervals = int(time_stamp_diff / INTERVAL_SIZE) - 1
                    
                    for i in range(omitted_intervals):
                        omitted_time_stamp = previous_time_stamp + (i+1)*INTERVAL_SIZE
                        omitted_date_time = datetime.fromtimestamp(omitted_time_stamp)
                        omitted_solar_irradiance = 0
                        offset+=INTERVAL_SIZE
                        #print(f'{omitted_date_time} {INTERVAL_SIZE} {omitted_solar_irradiance} ({i}) {offset}')
                        
                        if not must_remove_data(omitted_date_time):
                            writer.writerow([omitted_date_time, offset, omitted_solar_irradiance])
                        else:
                            print(f'ignoring {date_time}')
                        
                    offset+=INTERVAL_SIZE
                else:
                    print(date_time)
                    print(f'Error: Diff={diff} cannot be handled')
               
                #print(f'{date_time} {time_stamp_diff} {solar_irradiance} {offset}')
                if not must_remove_data(date_time):
                    writer.writerow([date_time, offset, solar_irradiance])
                else:
                    print(f'ignoring {date_time}')

                previous_time_stamp = time_stamp  

if __name__ == '__main__':
    process_photovolta_data('../data/photovolta_2016_raw_data_part_1.csv', '../data/photovolta_2016_part_1.csv', None)
    
    # The second interval begins at 2016-11-16 11:10:01, but it is not known if it was omitted because the solar 
    # irradiation was zero or if the data collection started at this time. So, this data will be removed until 
    # the next day.
    date_time_limit = datetime(2016, 11, 17, 0, 0, 0)
    process_photovolta_data('../data/photovolta_2016_raw_data_part_2.csv', '../data/photovolta_2016_part_2.csv', date_time_limit)


