import pandas as pd
import os
import glob
from datetime import datetime
import csv

file_path = r'csv-files'
all_files = glob.glob(os.path.join(file_path, "*.csv"))

df_from_each_file = (pd.read_csv(f) for f in all_files)
concatenated_df = pd.concat(df_from_each_file, ignore_index=True)
concatenated_df['date'] = pd.to_datetime(concatenated_df['Date in meter'],format='%d-%m-%Y %H:%M')
concatenated_df.index = concatenated_df['date']
meter_status = []
group_by_meter = concatenated_df.groupby('Meter')
for name, group in group_by_meter:
    meter_details = {name: {'days_connected': [], 'days_disconnected': []}}
    group_by_date = group.groupby(pd.TimeGrouper(freq='1D'))
    for date_group, data in group_by_date:
        try:
            datetime_field = data['Date in meter'].values[-1]
            dt = datetime.strptime(datetime_field, "%d-%m-%Y %H:%M")
            only_date= dt.date()
            status = data['Connection Status'].values[-1]
            if status == 'Connected':
                meter_details[name]['days_connected'].append(only_date)
            else:
                meter_details[name]['days_disconnected'].append(only_date)
        except IndexError:
            only_date = date_group.date()
            meter_details[name]['days_disconnected'].append(only_date)
    meter_status.append(meter_details)

with open(os.path.join(file_path, "output_what.csv"), "wb") as csv_file:
    writer = csv.writer(csv_file, delimiter=',')
    writer.writerow(['Meter', 'Days Connected', 'Days Disconnected'])
    for meter in meter_status:
        for key, value in meter.items():
            max_rows = max([len(value['days_connected']), len(value['days_disconnected'])])
            for i in range(0, max_rows):
                day_connected = value['days_connected'][i] if i < len(value['days_connected']) else None
                day_disconnected = value['days_disconnected'][i] if i < len(value['days_disconnected']) else None
                writer.writerow([key, day_connected, day_disconnected])



