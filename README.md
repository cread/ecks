# Ecks

A simple way to get data out of a remote machine using SNMP without having to deal with a single MIB or OID.

The goal of Ecks is simple - make it really easy to get get any data from an SNMP service.

Ecks is made up of a core class that will collect data via SNMP,
and a set of plugins that contain the OID and the code needed to
transform the results from nested OID's to usable data.

## Installation

The easiest way to install Ecks is:

```
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
