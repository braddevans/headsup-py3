#!/usr/bin/env python

# landscape-sysinfo-mini.py -- a trivial re-implementation of the
# sysinfo printout shown on debian at boot time. No twisted, no reactor, just /proc.
#
# Loosly based on https://github.com/jnweiger/landscape-sysinfo-mini which in turn was
# inspired by ubuntu 14.10 /etc/update-motd.d/50-landscape-sysinfo

from __future__ import division

import sys

from tabulate import tabulate
import multiprocessing

import os
import re
import platform
import subprocess
import time


def main():
    # update-motd.d scripts must start with printing a single blank line
    print()
    args = sys.argv[1:]
    # For percentages, direct percentage formatting with '{:.2%}'.format(val)
    # could also have been used, but was found to be significantly slower than the
    # equivalent %-style formatting.
    switch(args)


def get_memory_stats():
    memory_info = get_meminfo()
    memory_usage = 1 - memory_info['MemFree:'] / (memory_info['MemTotal:'] or 1)
    swap_total = memory_info['SwapTotal:']
    if swap_total == 0:
        swap_usage = None
    else:
        swap_usage = 1 - memory_info['SwapFree:'] / swap_total
    return memory_usage, swap_usage


def get_system_load_average():
    with open('/proc/loadavg') as fh:
        one_min_avg, five_min_avg, fifteen_min_avg, _ = fh.read().split(None, 3)
        return float(five_min_avg)


def get_number_of_running_processes():
    processes_list = [e for e in os.listdir('/proc') if e.isnumeric()]
    return len(processes_list)


def get_root_fs_stats():
    statfs = os.statvfs('/')
    root_usage = 1 - statfs.f_bavail / statfs.f_blocks
    root_size_in_gb = statfs.f_bsize * statfs.f_blocks / 2 ** 30
    return root_usage, root_size_in_gb


def get_device_address(device):
    """ find the local ip address on the given device """
    if device is None:
        return None
    command = ['ip', 'route', 'list', 'dev', device]
    ip_routes = subprocess.check_output(command).strip()
    for line in decode_bytes(ip_routes).split('\n'):
        seen = ''
        for a in line.split():
            if seen == 'src':
                return a
            seen = a
    return None


def get_default_net_device():
    """ Find the device where the default route is. """
    with open('/proc/net/route') as fh:
        for line in fh:
            iface, dest, _ = line.split(None, 2)
            if dest == '00000000':
                return iface
    return None


def get_number_of_logged_in_users():
    logged_in_users = subprocess.check_output(['who']).strip()
    return len(decode_bytes(logged_in_users).split('\n'))


def get_meminfo():
    items = {}
    with open('/proc/meminfo') as fh:
        for line in fh:
            line_items = line.split()
            if len(line_items) == 3:
                key, value, unit = line_items
            else:
                key, value = line_items
            items[key] = int(value)
    return items


def decode_bytes(bytes):
    return bytes.decode("utf-8")


def get_swap_usage():
    memory_usage, swap_usage = get_memory_stats()
    return ".1f%" * 100 if swap_usage else '---'


def get_memory_usage():
    memory_usage, swap_usage = get_memory_stats()
    return memory_usage * 100

def print_extra():
    print("Arch: %s" % platform.machine())
    print("Version: %s" % platform.version())
    print("OS Type: %s" % platform.uname().system)
    print("Kernel: %s" % platform.uname().release)
    print(f"Hostname: {platform.uname().node}")
    print(f"Uname: {platform.uname()}")
    print(f"libc_ver: {platform.libc_ver()}")

def print_table():
    load_average = get_system_load_average()
    processes = get_number_of_running_processes()
    defaultdev = get_default_net_device()
    root_usage, root_size_in_gb = get_root_fs_stats()
    ipaddr = get_device_address(defaultdev)
    num_users = get_number_of_logged_in_users()
    memory_info = get_meminfo()
    mem_free = (memory_info['MemFree:'] / 1000) / 1000
    mem_max = (memory_info['MemTotal:'] / 1000) / 1000
    table = [
        [f"System load:", f"%.1f%%" % (load_average * 100)
         + f" ({(load_average*100) / (multiprocessing.cpu_count()):.2f}% per-core)"
           f"({multiprocessing.cpu_count()} cores)"],
        ["Processes:", "%d" % processes],
        [f"Usage of /:", "%.1f%% of %.2fGB" % (root_usage * 100, root_size_in_gb)],
        ["Users logged in:", "%d" % num_users],
        [f"Memory Usage:", f"{get_memory_usage():.2f}% (MemFree: {mem_free:.2f} GB, MemMax: {mem_max:.2f} GB)"],
        ["IP address for", "%s: %s" % (defaultdev, ipaddr)],
        [f"Swap Usage:", get_swap_usage()]
    ]
    print(tabulate(table))


def switch(args):
    """
    switch loop through entered arguments
    Args:
        args (list):
    """
    arg: str
    for arg in args:
        if arg == "--extra":
            print("System information as of %s\n" % time.asctime())
            print_extra()
            print_table()
        elif arg == "--extra-only":
            print("System information as of %s\n" % time.asctime())
            print_extra()
            sys.exit(0)
        elif arg == "--help" or arg == "-h":
            print(f"Usage: [--help, --extra, --extra-only]")
            sys.exit(0)
        else:
            print_table()
    if len(args) == 0:
        print_table()



if __name__ == '__main__':
    main()
