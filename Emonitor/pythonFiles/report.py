import pandas as pd
import os
import subprocess

BASE_DIR = os.path.dirname(__file__)
csv_path = os.path.join(BASE_DIR, '..', 'data', 'main_statistics.csv')
df = pd.read_csv(csv_path)

lfist_size = [14, 9, 11, 8, 9, 11, 9, 1]

first_date = df.iloc[0]['date']

last_date = df.iloc[-1]['date']

date_difference = (pd.Timestamp(last_date) - pd.Timestamp(first_date)).days

numeric_columns = df.columns[1:len(df.columns)].to_list()

with open(os.path.join(BASE_DIR, '..', 'report.txt'), 'w') as file:
    file.write('The examination report\n')
    file.write('\n')
    file.write(f"First examination: {first_date}\n")
    file.write(f"Last examination: {last_date}\n")
    file.write(f"Length of the research period: {date_difference} days\n")
    file.write('\n')
    file.write('General statistics:\n')
    file.write('\n')
    file.write('angry    disgust    fear    happy    neutral    sad      surprisee\n')

    for emotion, index in zip(numeric_columns, range(1, 8)):
        file.write((str(round(df[emotion].to_numpy().sum()/len(df), 2)) + '%').ljust(lfist_size[index]))

    file.write('\n')
    file.write('\n')
    file.write('Statistics for days in percents:\n')
    file.write('\n')
    file.write('    date          angry    disgust    fear    happy    neutral    sad      surprisee\n')
    for index, row in df.iterrows():
        file.write(str(index).ljust(4))
        for col, col_number in zip(df.columns, range(8)):
            file.write(str(row[col]).ljust(lfist_size[col_number]))
        file.write('\n')

subprocess.Popen(['notepad.exe', 'report.txt'])