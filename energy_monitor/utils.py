'''
utility helper functions
'''
# Author: Matt Clifford <matt.clifford@bristol.ac.uk>

import numpy as np
from tqdm import tqdm
import re
from csv import reader, writer
import os
from datetime import timedelta
import pandas as pd

'''
dummy function for testing with
'''
def dummy_compute(iters=20):
    for i in tqdm(range(iters)):
        a = np.arange(3*40*5*600).reshape((3,40,5,600))
        b = np.arange(3*40*5*600)[::-1].reshape((5,40,600,3))
        np.dot(a, b)[2,3,2,1,2,2]
    return

'''
PwrData.csv utils
'''
def get_PwrData_csv(datetime_obj):
    '''
    get start time +-1 second incase of discrepancies
    '''
    csv_list = []
    for sec in [-1, 0, 1]:
        adjusted_datetime = datetime_obj + timedelta(seconds=sec)
        csv_list.append(_construct_PwrData_csv_name(adjusted_datetime))
    return csv_list

def _construct_PwrData_csv_name(datetime_obj):
    '''
    get PwdData file name from datetime object
    '''
    name = 'PwrData_'
    name += str(datetime_obj.year) + '-'
    name += str(datetime_obj.month) + '-'
    name += str(datetime_obj.day) + '-'
    name += str(datetime_obj.hour) + '-'
    name += str(datetime_obj.minute) + '-'
    name += str(datetime_obj.second) + '.csv'
    return os.path.join(os.path.expanduser("~"), 'Documents', name)
'''
datetime string constuction
'''
def get_date_string(datetime_obj):
    '''
    convert datetime object into string format
    '''
    date = str(datetime_obj.year) + '-'
    date += str(datetime_obj.month) + '-'
    date += str(datetime_obj.day) + '-'
    date += str(datetime_obj.hour) + '-'
    date += str(datetime_obj.minute) + '-'
    date += str(datetime_obj.second)
    return date

'''
read joules from csv file
'''
def read_csv(csv_file):
    dict_results = dict()
    with open(csv_file, 'r') as file:
        line = reader(file)
        for row in line:
            if len(row) > 0 and bool(re.match(r"Average IA Power", row[0])):
                dict_results['average_ia'] = float(re.findall(r"\d+\.\d+", row[0])[0])
            elif len(row) > 0 and bool(re.match(r"Total Elapsed Time", row[0])):
                dict_results['time'] = float(re.findall(r"\d+\.\d+", row[0])[0])
            elif len(row) > 0 and bool(re.match(r"Cumulative IA Energy_\d+ \(Joules\)", row[0])):
                dict_results['cumulative_ia'] = float(re.findall(r"\d+\.\d+", row[0])[0])
    return dict_results
    
'''
read time series data from csv file
'''
def read_timeseries(column_name, csv_file):
    df = pd.read_csv(csv_file)
    df_dropna = df.dropna(axis='rows')
    data = df_dropna[column_name].values.tolist()
    return data

'''
read the files that we generate and return a dictionary
'''
def read_results(result_file):
    dict_results = dict()
    with open(result_file, 'r') as file:
        lines = file.readlines()
        lines = [word.replace('\n', '') for word in lines]
        keys = lines[0].split(',')
        lines_splitted = [_.split(',') for _ in lines[1:]]
        for idx, key in enumerate(keys):
            dict_results[key] = [float(line[idx]) for line in lines_splitted]
        return dict_results

def check_written(file):
    '''
    check if a file has done being written todo
    '''
    try:
        f = open(file, 'r')
        f.close()
        return True
    except PermissionError:
        return False

def log_data(csv_filepath, dictionary):
    '''
    store the dictionary into a .csv file
    '''
    # if doesn't exist: 'w' else 'a'
    if not os.path.isfile(csv_filepath):
        # make sure directories exist before writing
        os.makedirs(os.path.split(csv_filepath)[0], exist_ok=True)
        with open(csv_filepath, 'w', newline='') as csvfile:
            spamwriter = writer(csvfile, delimiter=',')
            fields = list(dictionary.keys())
            spamwriter.writerow(fields)
            values = list(dictionary.values())
            spamwriter.writerow(values)
    else:
        with open(csv_filepath, 'a', newline='') as csvfile:
            spamwriter = writer(csvfile, delimiter=',')
            values = list(dictionary.values())
            spamwriter.writerow(values)
