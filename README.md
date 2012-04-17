# Ecks

In the original Men in Black comics, an agent named Ecks went rogue and wanted to eliminate the MiB. This little 
Python library has a similar aim...

Ecks provides a simple way to get data out of a remote machine using SNMP without having to deal with a single MIB 
or OID.

Ecks is made up of a core class that will collect data via SNMP, 
and a set of plugins that contain the OID and the code needed to
transform the results from nested OID's to usable data.

For far too long people have been abusing their servers by connecting to them using SSH 
and then scraping the output of processes like `df`, `free`, `uptime` and `netstat` to find out what their
machines are up to. They do this because it's easier than using SNMP. Ecks now makes the right way the easy way...

## Installation

The easiest way to install Ecks is:

```shell
pip install ecks
```

You can also clone the repository and run `python setup.py install`

## Requirements

The python requirements to use the library are:

* Python 2.6 or higher
* [pysnmp](http://pysnmp.sourceforge.net/)

Some of the OID's used by the standard plugins shipped with Ecks are not enabled by default on some Linux distributions.

The following `snmpd.conf` file should get you enough access to test with:

    com2sec notConfigUser  default       my-secret-community
    group   notConfigGroup v2c           notConfigUser
    view    systemview     included      .1
    access  notConfigGroup ""            any       noauth    exact  systemview none none

If you are worried about other people being able to just read your data then I suggest you restrict the IP address(es)
that can access the host as well.


## Usage

```python
>>> import ecks
>>> e = ecks.Ecks()
>>> e.get_data('127.0.0.1', 'public', 'disk')
[(2, 'Physical memory', 8589934592, 5169360896), (3, 'Swap space', 134213632, 45056), (4, '/', 290984034304, 243201781760)]
>>> e.get_data('127.0.0.1', 'public', 'cpu')
(21, 9, 68)
>>> e.get_data('127.0.0.1', 'public', 'uptime')
18879153
>>> e.get_uptime('127.0.0.1', 'public')
18879153
```

Note that the last two method calls are interchangable.

This shows how easy it is to get the data out of the system. What you do with it then is up to you...

I currently use this library to feed our internal time series monitoring system and send email alerts 
when certain thresholds are crossed.

## Plugins

All the hard work is done by the plugins. Currently I have working plugins for:

* CPU Utilization 
* Disk Utilization (think `df -k`)
* Load average (think `uptime`)
* Memory Utilization (think `free`)
* Network Interface Counters (think `ifconfig`)
* Process Tree (think `ps -ef`)
* TCP Connections (think `netstat -an -p tcp`)
* Uptime (you guessed it - think `uptime`)
* TCP Stack Statistics
* OS Identification

More plugins coming soon (and more info on how to create your own)...

## Platforms

All base plugins have been tested to work with the default SNMP agent for:

* Solaris
* Ubuntu
* RedHat Enterprise Linux
* OSX
* Windows Server

Note: For the windows systems, the load average has no meaning and so does not work.
The way CPU and Memory are reported are different, so use `wincpu` and `winmemory` instead of `cpu` and `memory` 

## Copyright

Copyright (c) 2011-2012 Chris Read. See LICENSE for details.
