import csv
import os

keys = {}

with open('data/HANDEL_rename1.csv', 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for rowDict in reader:
        keys[rowDict[0]] = rowDict[1]

path = 'C:\\Users\\ryanmerritt28\\Desktop\\HANDEL-I'

for curr_name, dst_name in keys.items():
    try:
        os.rename(f'{os.path.join(path, curr_name)}.svs', f'{os.path.join(path, dst_name)}.svs')
        print('Changed', curr_name, 'to', dst_name)
    except:
        print(f'{curr_name} not found. Moving on...')
        continue
