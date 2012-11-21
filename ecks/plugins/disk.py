"""
    Ecks plugin to collect disk usage information

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

from pprint import pprint

def _calc_size(block_size, block_count):
    if block_size and block_count:
        return block_size * block_count
    else:
        return -1


def get_disk(parent, host, community):
    """ This is a plugin to be loaded by Ecks

    return an array of tuples containing (type, path, size in bytes, used bytes) for each block device

    type is an integer which is one of the following:
        hrStorageOther	        = 1
        hrStorageRam	        = 2
        hrStorageVirtualMemory	= 3
        hrStorageFixedDisk	    = 4
        hrStorageRemovableDisk	= 5
        hrStorageFloppyDisk	    = 6
        hrStorageCompactDisc	= 7
        hrStorageRamDisk	    = 8
        hrStorageFlashMemory	= 9
        hrStorageNetworkDisk	= 10
    """
    disks = (1,3,6,1,2,1,25,2,3,1) # HOST-RESOURCES-MIB
    data = parent.get_snmp_data(host, community, disks, 1)

    # We need to work this out the long was as there are cases where size or used is not supplied
    details = []
    formatted = []

    for i in [t for t in parent._extract(data, int, 1)]:
      details.append([ value for (oid, (data_type, index), value) in data if index == i  and data_type != 1])

    for dev in details:
      if len(dev) != 5:
        continue
      formatted.append((
        tuple(dev[0])[-1],
        str(dev[1]),
        int(dev[2]) * int(dev[3]),
        int(dev[2]) * int(dev[4])
        ))

    return formatted

