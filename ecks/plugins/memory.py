"""
   Ecks plugin to collect system memory usage information

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

def get_memory(parent, host, community):
    """ This is a plugin to be loaded by Ecks

    return a tuple containing (total_swap, avail_swap, total_real, avail_real, mem_buffer, mem_cached). Values are in kiloBytes

    """
    memory = (1,3,6,1,4,1,2021,4) # UCD-SNMP-MIB
    data = parent.get_snmp_data(host, community, memory, 1)

    if data:
        return map(parent._build_answer,
            parent._extract(data, int, 3),
            parent._extract(data, int, 4),
            parent._extract(data, int, 5),
            parent._extract(data, int, 6),
            parent._extract(data, int, 14),
            parent._extract(data, int, 15),
        )[0]
