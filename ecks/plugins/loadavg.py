"""
   Ecks plugin to collect system load average

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

from decimal import Decimal

def get_loadavg(parent, host, community):
    """ This is a plugin to be loaded by Ecks

    return an array of tuples containing (name, value) for each measured interval (normally 1, 5 and 15 minutes)

    name is the description of the interval returned by the host
    
    value is a python Decimal (see decimal module) containing the floating point representation of the load average
    """
    load = (1,3,6,1,4,1,2021,10,1) # UCD-SNMP-MIB
    data = parent.get_snmp_data(host, community, load, 1)
    return map(parent._build_answer,
        parent._extract(data, str, 2),
        map(Decimal, parent._extract(data, str, 3)),
    )
