# headsup

A trivial alternative to Ubuntu's landscape-info with no external dependencies, that runs in 10% of the time of `/etc/update-motd.d/50-landscape-sysinfo`. Because perf matters.

Originally forked from https://github.com/jnweiger/landscape-sysinfo-mini/. Changes include removing utmp dependency and generally speeding things up.


Install
-------

If you want the `headsup` command available:

    $ pip install headsup

If you just want to replace the Ubuntu default, copy the `headsup.py` file into `/etc/updated-motd.d/50-headsup` (and remove the standard Ubuntu one if present) and make the script executable. `pam_motd` runs these scripts in order to create the motd.


Usage
```shell
$ headsup

----------------  --------------------------------------------
System load:      100.0% (6.25% per-core)(16 cores)
Processes:        599
Usage of /:       4.8% of 188.76GB
Users logged in:  2
Memory Usage:     29.78% (MemFree: 23.02 GB, MemMax: 32.78 GB)
IP address for    enp4s0: 192.168.2.5
Swap Usage:       ---
----------------  --------------------------------------------


$ headsup --extra
Arch: x86_64
Version: #97-Ubuntu SMP Mon Oct 2 21:09:21 UTC 2023
OS Type: Linux
Kernel: 5.15.0-87-generic
Hostname: dev-vm
Uname: uname_result(system='Linux', node='dev-vm', release='5.15.0-87-generic', version='#97-Ubuntu SMP Mon Oct 2 21:09:21 UTC 2023', machine='x86_64')
libc_ver: ('glibc', '2.35')
System information as of Fri Oct 27 21:08:53 2023    

----------------  --------------------------------------------
System load:      100.0% (6.25% per-core)(16 cores)
Processes:        599
Usage of /:       4.8% of 188.76GB
Users logged in:  2
Memory Usage:     29.78% (MemFree: 23.02 GB, MemMax: 32.78 GB)
IP address for    enp4s0: 192.168.2.5
Swap Usage:       ---
----------------  --------------------------------------------


$ headsup --extra-only
Arch: x86_64
Version: #97-Ubuntu SMP Mon Oct 2 21:09:21 UTC 2023
OS Type: Linux
Kernel: 5.15.0-87-generic
Hostname: dev-vm
Uname: uname_result(system='Linux', node='dev-vm', release='5.15.0-87-generic', version='#97-Ubuntu SMP Mon Oct 2 21:09:21 UTC 2023', machine='x86_64')
libc_ver: ('glibc', '2.35')
System information as of Fri Oct 27 21:08:53 2023
```
