"""
    Ecks plugin to collect process tree from a machine

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

def get_processes(parent, host, community):
    """ This is a plugin to be loaded by Ecks

    return an array of tuples containing (pid, proc_name, proc_args, status) for each process

    status is an int which maps to:
        running(1),
        runnable(2), -- waiting for resource (i.e., CPU, memory, IO)
        notRunnable(3), -- loaded but waiting for event
        invalid(4) -- not loaded

    """
    procs = (1,3,6,1,2,1,25,4,2,1) # HOST-RESOURCES-MIB
    data = parent.get_snmp_data(host, community, procs, 1)
    return map(parent._build_answer,
        parent._extract(data, int, 1), # PID
        parent._extract(data, str, 2), # Process Name
        parent._extract(data, str, 5), # Arguments
        parent._extract(data, int, 7), # Status
    )

    

