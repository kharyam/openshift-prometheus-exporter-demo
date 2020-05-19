#!/usr/bin/python3

import os, io, signal, re, sys
from time import sleep
from prometheus_client import start_http_server, Info

def exit_gracefully(signum, frame):
    print("Exiting...")
    sys.exit(0)

signal.signal(signal.SIGINT, exit_gracefully)
signal.signal(signal.SIGTERM, exit_gracefully)

def get_bios_info():
    criteria = {"Vendor" : "vendor",
                "Version" : "version",
                "Release Date" : "release_date",
                "BIOS Revision" : "bios_revision"}

    result = os.popen("dmidecode -t 0")
    output = result.read()

    metrics = {"node":os.getenv('MY_NODE_NAME')}

    for key,value in criteria.items():
        p = re.compile(r'.*' + key  + r':\s*(.*\n)')
        metrics[value] = p.search(output).group(1).strip()

    print ('Retrieved bios info', flush=True)
    return metrics

# Create a metric for the bios version
bios_version = Info('bios_version', 'Server BIOS Version')

# Main
if __name__ == '__main__':
    start_http_server(8000)
    while True:
        bios_version.info(get_bios_info())
        sleep(30)
