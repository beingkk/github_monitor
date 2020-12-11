import pandas
import numpy
import requests
import json
import datetime
import time
import os, sys
import yaml


def jprint(obj):
    ''' Create a formatted string of the Python JSON object '''
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

def get_params(args):
    ''' Get the params for fetching traffic data '''
    with open(get_param_file(args), 'r') as f:
        config_params = yaml.load(f, Loader=yaml.FullLoader)
    return config_params

def get_param_file(args):
    ''' Specify the parameter config file '''
    if len(args) < 2:
        return 'configs_def.yaml'
    else:
        return args[1]

def get_datetime_string():
    ''' Get strings representing today's date and time '''
    time_now = str(datetime.datetime.now())
    date_now = time_now.split(' ')[0]
    return time_now, date_now

def logfile_exists(log_filename, log_folder):
    ''' Check if a traffic log file exists for the particular repo '''
    list_of_logs = os.listdir(log_folder)
    if len(set(list_of_logs).intersection(set([log_filename])))!=0:
        return True
    else:
        return False

def date_checked(log_dataframe, date_now):
    ''' Check if today's data has already been fetched '''

    if len(log_dataframe) == 0:
        return False

    most_recent_date = log_dataframe.sort_values('date_when_checked', ascending=False).iloc[0].date_when_checked

    if date_now == most_recent_date:
        return True
    else:
        return False

def check_github_traffic_api(params, headers, collect_data={}):
    ''' Check Github's API '''
    for endpoint in params['endpoints_to_check']:
        response = requests.get(
            f"https://api.github.com/repos/{params['owner_name']}/{params['repo_name']}/traffic/{endpoint}",
            headers=headers)
        print(f'Checked {endpoint}: status code {response.status_code}')
        collect_data[endpoint] = response.json()
        time.sleep(1)
    return collect_data
