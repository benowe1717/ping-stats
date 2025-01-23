#!/usr/bin/env python3
"""
Gather statistics about all IPs in your route to a destination
"""

import sys

from src.classes.parseargs import ParseArgs
from src.classes.mtr import MTR


def combine_traces(traces: list) -> dict:
    """
    Take all traces and combine them into a single dictionary.
    """
    combined_traces = {}
    for trace in traces:
        ip = trace['ip_addr']

        if ip in combined_traces:
            for key, value in trace.items():
                if key != 'ip_addr':
                    combined_traces[ip][key].append(value)

        else:
            combined_traces.update({ip: {}})
            for key, value in trace.items():
                if key != 'ip_addr':
                    combined_traces[ip][key] = [value]

    return combined_traces


def calculate_averages(traces: dict) -> dict:
    """
    Loop through the dictionary and find all instances of IPs with multiple
    values. Make the multiple values a single value through averages.
    """
    for ip, trace in traces.items():
        for key, value in trace.items():
            if len(value) > 1:
                count = len(value)
                total = sum(value)
                average = round((total / count), 2)
                trace[key] = average

            elif len(value) == 1:
                trace[key] = value[0]

    return traces


def main():
    """Main program loop"""
    args = sys.argv
    parseargs = ParseArgs(args)

    if len(parseargs.ips) == 0:
        print('ERROR: No IPs found!')
        sys.exit(1)

    traces = []
    mtr = MTR(parseargs.ips)
    for ip in mtr.ips:
        mtr.run_mtr(ip)
        results = mtr.parse_output()
        if len(results) == 0:
            continue

        for result in results:
            traces.append(result)

    combined_traces = combine_traces(traces)
    averaged_traces = calculate_averages(combined_traces)


if __name__ == '__main__':
    main()
