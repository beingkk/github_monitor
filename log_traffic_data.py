from github_monitoring_utils import *

# Fetch parameters from the specified config file
params = get_params(sys.argv)
path_to_token = params['path_to_token']
owner_name = params['owner_name']
repo_name = params['repo_name']
log_folder = params['log_folder']
endpoints_to_check = params['endpoints_to_check']
print(f"Fetching traffic data for repo {owner_name}/{repo_name} into {log_folder} folder")

# Request header, needed for authorisation
headers = {'Authorization': 'token %s' % open(path_to_token, "r").read()}
# Get today's date and time
time_now, date_now = get_datetime_string()
# Filename of the repo logs
log_filename = f'traffic_log_{repo_name}.csv'

# Check if a traffic log file of the repo exists
if logfile_exists(log_filename, log_folder):
    # Read in the log file
    log_dataframe = pandas.read_csv(f'{log_folder}{log_filename}')
    print(f"Read {log_filename}")
    # Save a backup, just in case
    log_dataframe.to_csv(f'{log_folder}{log_filename[:-4]}_BACKUP.csv', index=False)
else:
    # Create a new dataframe, with columns representing the fields to check
    log_dataframe = pandas.DataFrame(data={
        'date_when_checked':[],
        'time_when_checked':[],
        'popular/paths':[],
        'popular/referrers':[],
        'views':[],
        'clones':[]
    })
    print("Log file didn't exist; created a new table.")

# Check if today's data has been already registered
if date_checked(log_dataframe, date_now):
    print("Abort! We already have traffic data from today")
else:
    collect_data = {}
    collect_data['date_when_checked'] = date_now
    collect_data['time_when_checked'] = time_now
    collect_data = check_github_traffic_api(params, headers, collect_data)
    # Turn the responses to strings
    collect_data_str = {}
    for key in list(collect_data.keys()):
        collect_data_str[key] = str(collect_data[key])
    # Add the responses to the log dataframe
    log_dataframe = log_dataframe.append(collect_data_str, ignore_index=True)
    # Overwrite the log file
    log_dataframe.to_csv(f'{log_folder}{log_filename}', index=False)

    print(f"Collected and added traffic data for {date_now} in {log_filename}")
