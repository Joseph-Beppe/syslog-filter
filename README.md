
# Syslog Filter

## Description
The script filters a given Linux syslog file based on a regular expression and time window + optionally outputs it into .csv and .html files.

## Usage
```
usage: syslog_filter.py [-h] [--log-file LOG_FILE] [--regexp REGEXP]
                        [--output-file OUTPUT_FILE]
                        [--time-window TIME_WINDOW]

options:
  -h, --help            show this help message and exit
  --log-file LOG_FILE, -l LOG_FILE
                        Path to the log file. (default: /var/log/syslog)
  --regexp REGEXP, -r REGEXP
                        Regular expression to filter from the logs. (default:
                        (.*:..:..) (\S*) (.*(ERROR|error).*))
  --output-file OUTPUT_FILE, -o OUTPUT_FILE
                        Path to the output file without extension. Will create
                        csv and html. (default: None)
  --time-window TIME_WINDOW, -t TIME_WINDOW
                        Time window in format Mon.D.Time-Mon.D.Time
                        (Jun.4.07:25:59-Jun.5.15:18:00). (default: None)
```

## Notes (Time Format)
The script uses the default Linux Mint 21 (Ubuntu based) syslog time format. It requires the format's use in specifying a time window.

## Example
```
v@HP-Elite:~$ ./syslog_filter.py -t Jun.16.12:34:22-Jun.16.12:34:30 -o logs/error-logs_Jun-16-12:34
Jun 16 12:34:22 HP-Elite ntpd[1270]: error resolving pool 0.ubuntu.pool.ntp.org: Name or service not known (-2)
Jun 16 12:34:23 HP-Elite ntpd[1270]: error resolving pool 1.ubuntu.pool.ntp.org: Name or service not known (-2)
Jun 16 12:34:24 HP-Elite ntpd[1270]: error resolving pool 2.ubuntu.pool.ntp.org: Name or service not known (-2)


Found 3 logs.
The filtered logs intersect at: ntpd[1270]: error resolving pool * Name or service not known (-2)
```
