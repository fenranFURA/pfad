import requests
import string
import csv

import os
import datetime
import matplotlib.pyplot as plt

file_path = "../../week1/src/daily_KP_SUN_2024.csv"

data = []
dataDraw = []

# Read the CSV file
with open(file_path, 'r', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        data.append(row)

# Print the data (you can modify this part to process the data as needed)
for row in data:
    columns = row
    if len(columns) == 0:
        continue
    # columns[0] should be a str type
    year = columns[0]
    if year.isdigit():
        year_num = int(year)
        if year_num < 1961:
            continue
        if year_num > 2024:
            continue
    else:
        continue

    month = int(columns[1])
    day = int(columns[2])

    date = datetime.date(int(year),month,day)
    value = columns[3]

    print(f'{date} - {value}')
    dataDraw.append((date, value)) 

# plot
fig, ax = plt.subplots()
ax.plot([record[0] for record in dataDraw], [float(record[1]) for record in dataDraw])
plt.show()