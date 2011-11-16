"""
   Ecks plugin to collect system uptime

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

def get_uptime(parent, host, community):
    """ This is a plugin to be loaded by Ecks

    return the number of milliseconds since the system was booted
    """
    uptime = (1,3,6,1,2,1,25,1,1) # HOST-RESOURCE-MIB
    data = parent.get_snmp_data(host, community, uptime, 1)

    if data:
        return int(data[0][2])
    else:
        return None
