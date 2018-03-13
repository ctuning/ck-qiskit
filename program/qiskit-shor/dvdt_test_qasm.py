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
valid =helper.parse("../examples/teleport.qasm")
if valid == False: 
   print("Qsam Error")
   exit(1)

qasm_file = open("../examples/teleport.qasm", "r") 
quantum_program = qasm_file.read()
qasm_file.close()
q = [{'qasm': quantum_program} ]
## select q1 if you use api.run_experiment(qasm, device, shots, name=None, timeout=60) . QSAM object for job
q1 = quantum_program 
max_credits = 3
status = api.run_job(q, device, shots, max_credits)

lc = api.get_last_codes()
#if verbose: lc qasms
print (status)
idx =(status['qasms'][0]['executionId'])
#idx = status['executionId']
print(api.get_execution(idx))
print(api.get_result_from_execution(idx))

#api.run_experiment(q1, device, shots, name="CK_IBM_EXP_NAME", timeout=_tout)


