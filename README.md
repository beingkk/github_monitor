# github_monitor
Simple Python project for logging traffic to your repo.

# Welcome!
Github's insights presently only show you repo traffic data about the last two weeks. The code in this repo allows you to easily fetch and log the data via Github's API, so that you don't lose your traffic history.

This does not include a ready-made scheduling solution for automating the fetching (e.g. for daily checking), but you can read below how I implemented a very simple scheduled checking on my local machine.

This also does not include any analysis or displaying of the data.

# Installation

To clone the repo and install the dependencies, navigate to a convenient directory and run the following commands from the terminal:

```shell
$ git clone https://github.com/beingkk/github_monitor
$ cd github_monitor
$ conda env create -f conda_environment.yaml
```

# Usage

You will need a github authorisation token to be able use github's API to check your repo's traffic. Store it someplace safe, and provide only the full path to the token file in the config yaml file.
- `template_config.yaml` provides a template for configuring your parameters
- `template_token.txt` provides a dummy token file, in the format that the script is expecting

## One-off checking
Once your config file setup, you can run the script `log_traffic_data.py` and provide your config filename, for example `configs_test.yaml`

```
$ python log_traffic_data.py configs_test.yaml
```

If this is the first time, it will create a new file in your logging folder. Otherwise, it will add another row to the existing file.
The logging files follow the pattern `traffic_log_{repo_name}.csv` (you may want to change this to include owner's name as well). For an example of the schema, see `logs/traffic_log_github_monitor.csv` or `traffic_log_occupation-classification.csv` 

## Automated logging
There are many solutions to run scripts autmomatically at regular intervals (e.g. cron). For my use case, I very simply created an executable app on my macOS, and set up my calendar to run the app every day (following these two tutorials: [one](https://martechwithme.com/convert-python-script-app-windows-mac/) and [two](https://martechwithme.com/schedule-python-scripts-windows-mac/)). For an example of an executable file, see `log_traffic_data_test` - note, it should contain full paths).

# References

- Github's traffic API: [useful older summary](https://developer.github.com/v3/repos/traffic/), and [latest docs](https://docs.github.com/en/free-pro-team@latest/rest/reference/repos#traffic)
- Tutorial on scheduling python scripts on your Mac: [one](https://martechwithme.com/convert-python-script-app-windows-mac/) and [two](https://martechwithme.com/schedule-python-scripts-windows-mac/).
