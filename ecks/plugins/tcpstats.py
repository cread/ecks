"""
   Ecks plugin to collect TCP stack statistics

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

def ip_addr(data):
    return ".".join([ str(a) for a in data ])

def get_tcpstats(parent, host, community):
    """ This is a plugin to be loaded by Ecks

    return a list containing [
        tcpAttemptFails,    - http://www.oid-info.com/get/1.3.6.1.2.1.6.7
        tcpEstabResets,     - http://www.oid-info.com/get/1.3.6.1.2.1.6.8
        tcpCurrEstab        - http://www.oid-info.com/get/1.3.6.1.2.1.6.9
        tcpInSegs,          - http://www.oid-info.com/get/1.3.6.1.2.1.6.10
        tcpOutSegs,         - http://www.oid-info.com/get/1.3.6.1.2.1.6.11
        tcpRetransSegs,     - http://www.oid-info.com/get/1.3.6.1.2.1.6.12
        tcpInErrs,          - http://www.oid-info.com/get/1.3.6.1.2.1.6.14
        tcpOutRsts,         - http://www.oid-info.com/get/1.3.6.1.2.1.6.15
    ]

    """
    ids = [7, 8, 9, 10, 11, 12, 14, 15]

    stats = []
    for id in ids:
        try:
            stats = stats + [long(parent.get_snmp_data(host, community, (1,3,6,1,2,1,6,id), 1)[0][2])]
        except:
            return

    return stats
