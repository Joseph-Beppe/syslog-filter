#!/usr/bin/env python3

'''
The script filters a given Linux syslog file based on a regular expression and time window
+ optionally outputs it into .csv and .html files.

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
'''

import argparse
import re
from os import makedirs, path
from pandas import read_csv

class SyslogFilter:
    ''' Filters a given log file based on a regular expression '''
    def __init__(self, args):
        self.log_file = args.log_file
        self.regexp = args.regexp
        self.output_file = args.output_file
        self.time_window = args.time_window
        self.filtered_logs = []
        self.intersection = ""

    def csv_to_html(self):
        ''' Converts .csv file to .html '''
        read_csv(self.output_file + ".csv").to_html(self.output_file + ".html", justify="left")

    def create_csv(self):
        ''' Saves self.filtered_logs as .csv '''
        if "/" in self.output_file:
            makedirs(path.dirname(self.output_file), exist_ok=True)
        with open(self.output_file + ".csv", "w", encoding="utf-8") as output_file:
            output_file.write("Timestamp, User, Log Message\n")
            for log in self.filtered_logs:
                output_file.write(f"{log[0]}, {log[1]}, {log[2].replace(',', '')}\n")

    def print_intersection(self):
        ''' Prints sentenced self.intersection '''
        if self.intersection:
            print(f"The filtered logs intersect at: {self.intersection}")
        else:
            print("Found no intersection in the filtered logs.")

    def find_intersection(self):
        ''' Finds matching elements in all filtered logs '''
        log_messages = []
        self.intersection = ""

        for log in self.filtered_logs:
            log_messages.append(log[2].split(" "))
        intersection = set.intersection(*map(set,log_messages))
        if intersection:
            for element in self.filtered_logs[0][2].split(" "):
                if element in intersection:
                    self.intersection += f"{element} "
                else:
                    self.intersection += "* "

    def print_summary(self):
        ''' Currently, prints number of found logs '''
        print(f"Found {len(self.filtered_logs)} logs.")

    def print_filtered_log(self):
        ''' Prints self.filtered_logs '''
        for log in self.filtered_logs:
            print(f"{log[0]} {log[1]} {log[2]}")

    def filter_time_window(self, time_stamp):
        ''' Returns True if time_stamp is inside self.time_window '''
        start_time = self.time_window.split("-")[0].split(".")
        end_time = self.time_window.split("-")[1].split(".")
        after_start = False
        before_end = False

        if time_stamp[0] == start_time[0]:
            if (time_stamp[1] > start_time[1]) or ((time_stamp[1] == start_time[1]) and (time_stamp[2] >= start_time[2])):
                after_start = True
        if time_stamp[0] == end_time[0]:
            if (time_stamp[1] < end_time[1]) or ((time_stamp[1] == end_time[1]) and (time_stamp[2] <= end_time[2])):
                before_end = True
        return after_start and before_end

    def filter_log(self):
        ''' Filters a log file to match regexp and time window '''
        with open(self.log_file, "r", encoding="utf-8") as log_file:
            for line in log_file:
                result = re.search(self.regexp, line)
                if result is not None:
                    if self.time_window:
                        if not self.filter_time_window(result.groups()[0].replace("  "," ").split(" ")):
                            continue
                    self.filtered_logs.append([result.groups()[0], result.groups()[1], result.groups()[2]])

    def filter(self):
        ''' Handles filtering based on given arguments '''
        self.filter_log()
        self.print_filtered_log()
        print("\n")
        self.print_summary()
        if self.filtered_logs:
            self.find_intersection()
            self.print_intersection()
            if self.output_file:
                self.create_csv()
                self.csv_to_html()

def parse_arguments():
    ''' Returns parsed command line arguments '''
    parser = argparse.ArgumentParser()

    parser.add_argument('--log-file', '-l', default="/var/log/syslog", type=str,
                        help='Path to the log file. (default: %(default)s)')
    parser.add_argument('--regexp', '-r', default=r"(.*:..:..) (\S*) (.*(ERROR|error).*)", type=str,
                        help='Regular expression to filter from the logs. (default: %(default)s)')
    parser.add_argument('--output-file', '-o', default=None, type=str,
                        help='Path to the output file without extension. Will create csv and html. (default: %(default)s)')
    parser.add_argument('--time-window', '-t', default=None, type=str,
                        help='Time window in format Mon.D.Time-Mon.D.Time (Jun.4.07:25:59-Jun.5.15:18:00). (default: %(default)s)')

    return parser.parse_args()

def main():
    ''' Main entry point '''
    args = parse_arguments()
    syslog_filter = SyslogFilter(args)
    syslog_filter.filter()

if __name__ == "__main__":
    main()
