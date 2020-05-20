#!/usr/bin/python3

import os
import signal
import re
import argparse
from sys import exit
from time import sleep
from prometheus_client import start_http_server, Info


def exit_gracefully(signum, frame):
    print("\nExiting", flush=True)
    exit(0)


def get_bios_info():
    """Parse dmidecode output and return a dictionary of BIOS related values"""

    criteria = {"Vendor": "vendor",
                "Version": "version",
                "Release Date": "release_date",
                "BIOS Revision": "bios_revision",
                "Firmware Revision": "firmware_revision"}

    result = os.popen("dmidecode -t 0")
    output = result.read()

    metrics = {"node": os.getenv('MY_NODE_NAME') or "UNSET"}

    for key, value in criteria.items():
        p = re.compile(r'.*' + key + r':\s*(.*\n)')
        metric_value = p.search(output)
        if metric_value:
            metrics[value] = metric_value.group(1).strip()

    return metrics


def main():
    """Start exporter web server and refresh bios information"""

    # Parse Arguments
    parser = argparse.ArgumentParser(description='BIOS Prometheus Exporter')
    parser.add_argument('--port', dest='port', default=8000,
                        type=int, action='store', help='Set listening port')
    args = parser.parse_args()

    # Catch signals
    signal.signal(signal.SIGINT, exit_gracefully)
    signal.signal(signal.SIGTERM, exit_gracefully)

    # Create metric
    bios = Info('bios', 'Node BIOS Information')

    # Start Listener
    start_http_server(args.port)
    print("Listening on port", args.port, end='', flush=True)

    # Update BIOS Information
    while True:
        bios.info(get_bios_info())
        print('.', end='', flush=True)
        sleep(30)


if __name__ == '__main__':
    main()
