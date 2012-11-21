"""
   Copyright 2011 Chris Read (chris.read@gmail.com)

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

import logging
import os
import types
import sys


class Ecks():
    """
    A simple way to get data out of a remote machine using SNMP without having to deal with a single MIB or OID
    
    Simple Usage:

    >>> import ecks
    >>> e = ecks.Ecks()
    >>> e.get_data('127.0.0.1', 'public', 'disk')
    [(2, 'Physical memory', 8589934592, 5169360896), (3, 'Swap space', 134213632, 45056), (4, '/', 290984034304, 243201781760)]
    >>> e.get_data('127.0.0.1', 'public', 'cpu')
    (21, 9, 68)
    >>> e.get_data('127.0.0.1', 'public', 'uptime')
    18879153


    """

    plugins = []

    def __init__(self, timeout = 1):
        self.timeout = timeout
        if logging._handlers == {}:
            logging.basicConfig()
        self.logger = logging.getLogger(__name__ + ".Ecks")
        self._load_plugins()


    def _load_plugins(self):
        """
        Walk through our plugins and wire their get_ methods 
        """
        plugin_dir = os.path.join(os.path.dirname(__file__), "plugins")
        for plugin in os.listdir(plugin_dir):
            if plugin.endswith(".py") and (plugin != "__init__.py"):
                self.logger.debug("Loading file: %s" % os.path.join(plugin_dir, plugin))
                plugin_name = plugin[:-3]
                try:
                    exec("import plugins.%s" % plugin_name)
                    exec("self.get_%(func)s = types.MethodType(plugins.%(func)s.get_%(func)s, self)" % {"func": plugin_name})
                    self.logger.debug("Registered plugin: %s" % plugin_name)
                    self.plugins += [plugin_name]
                except AttributeError as e:
                    self.logger.warn("Invalid plugin: %s" % plugin_name)


    def _extract(self, data, value_type, filter):
        """
        Return a filtered list of data that matches the given filter and is coerced to type value_type

        data
            A sequence in the form (oid, (data_type, index) value) as returned by get_snmp_data

        value_type
            A primitive python type to coerce the value into from the pysnmp type it is

        filter
            An integer defining what oid type to return
        """
        return [ value_type(value) for (oid, (data_type, index), value) in data if data_type == filter ]


    def _build_answer(self, *answers):
        return tuple([ a for a in answers ])

    def get_snmp_data(self, host, community, query_oid, query_oid_only = None):
        """
        Get data from server using a Bulk SNMP Get.

        host
            Hostname of the machine you want to pull the data from

        community
            SNMP community string to use

        query_oid
            If set to something that evaluates as True then it will only return
            results that match the query oid. By default it will return everything.
        """
        try:
            from pysnmp.entity.rfc3413.oneliner import cmdgen
        except ImportError:
            print "ERROR: Unable to load 'pysnmp' module."

        error_indication, error_status, error_index, var_binds_list = cmdgen.CommandGenerator().bulkCmd(
            cmdgen.CommunityData(host, community),
            cmdgen.UdpTransportTarget((host, 161), timeout = self.timeout),
            0, 25, query_oid)

        if error_indication:
            self.logger.error(error_indication)
        elif error_status:
            self.logger.error(
                '%s at %s\n' % (error_status.prettyPrint(), error_index and var_binds_list[int(error_index) - 1] or '?'))

        prefix = len(query_oid)
        data = [ (tuple(oid)[:prefix], tuple(oid)[prefix:], val) for [(oid, val)] in var_binds_list ]
        if query_oid_only:
            data = [ (oid, key, value) for (oid, key, value) in data if oid == query_oid ]

        return data


    def get_data(self, host, comm, plugin):
        """
        Utility method to interface with plugins by name

        host
            Hostname of the machine you want to pull the data from

        community
            SNMP community string to use

        plugin
            The plugin to call
        """
        return eval("self.get_%s(host, comm)" % plugin)
