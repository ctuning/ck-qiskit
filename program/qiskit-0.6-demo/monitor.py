from IBMQuantumExperience import IBMQuantumExperience
from IBMQuantumExperience import ApiError  # noqa
import helper
import sys
import os
import Qconfig
from pprint import pprint


verbose = False
if 'CK_IBM_VERBOSE' in os.environ:
    _verb = int(os.environ['CK_IBM_VERBOSE'])
    if (_verb > 0): verbose = True


# to fix via ck
mytoken= Qconfig.API_TOKEN 
cloud_frontend = 'https://quantumexperience.ng.bluemix.net/api'
api = IBMQuantumExperience(mytoken, config={'url': cloud_frontend}, verify=True)



# Exec 
_device_list = ['ibmqx5', 'ibmqx4', 'ibmqx_hpc_qasm_simulator', 'ibmqx2', 'ibmqx_qasm_simulator', 'local_unitary_simulator', 'local_qasm_simulator']

# number of repetition
shots = 1 
# in sec
_tout = 1200

#device
device = ""


available_backends = api.available_backends()
if 'CK_IBM_BACKEND' in os.environ:
    device = os.environ['CK_IBM_BACKEND']
if 'CK_IBM_REPETITION' in os.environ:
    shots = os.environ['CK_IBM_REPETITION']
if 'CK_IBM_TIMEOUT' in os.environ:
    _tout = os.environ['CK_IBM_TIMEOUT']

found = False
for n in available_backends:
    if verbose: print (n['name'])
    if n['name'] == device:
       found = True


if (found is False):
   device = _device_list[0]

if verbose: print(api.backend_status(device))

if verbose: print(api.get_my_credits())

# get qasm code to manage via ck too

#api.run_experiment(qasm, device, shots, name=None, timeout)
lc = api.get_last_codes()
#if verbose: print(lc)
limit = 5
my_jobs = api.get_jobs(limit)

#for j in my_jobs:
#    print(j)
#    print("\n")

njobs =len(my_jobs)
print(njobs)

exec_ids = []
for i in range(0,4):
    qasms = my_jobs[i]['qasms']
    for j in qasms:
        exec_ids.append(j['executionId'])

#if verbose: lc qasms
for i in exec_ids:
    print(api.get_result_from_execution(i))


