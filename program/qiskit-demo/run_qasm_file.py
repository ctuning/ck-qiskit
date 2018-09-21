#!/usr/bin/env python3

"""
This example parses a given QASM file and runs it remotely, the local simulator is not supported.

## Running this script using the "lightweight" CK infrastructure to import Qiskit library...

# 1) on remote simulator (need the API Token from IBM QuantumExperience) :
    CK_IBM_BACKEND=ibmq_qasm_simulator ck virtual `ck search env:* --tags=qiskit,lib`  `ck search env:* --tags=ibmqx,login` --shell_cmd=run_qasm_file.py

# 2) on remote quantum hardware (need the API Token from IBM QuantumExperience) :
    CK_IBM_BACKEND=ibmqx4 ck virtual `ck search env:* --tags=qiskit,lib`  `ck search env:* --tags=ibmqx,login` --shell_cmd=run_qasm_file.py
"""

from IBMQuantumExperience import IBMQuantumExperience
from IBMQuantumExperience import ApiError  # noqa
import helper
import sys
import os
import Qconfig

qasm_example_rel_path = 'examples/teleport.qasm'
qasm_example_abs_path = os.path.join(os.path.dirname(__file__), qasm_example_rel_path)

backend = os.environ.get('CK_IBM_BACKEND', 'ibmq_qasm_simulator')
timeout = int( os.environ.get('CK_IBM_TIMEOUT', 120) )
shots   = int( os.environ.get('CK_IBM_REPETITION', 10) )
verbose = int( os.environ.get('CK_IBM_VERBOSE', 0) ) != 0

api = IBMQuantumExperience(Qconfig.API_TOKEN, Qconfig.config, verify=True)

if verbose: print(api.backend_status(backend))

if verbose: print(api.get_my_credits())

# get qasm code to manage via ck too

#api.run_experiment(qasm, backend, shots, name=None, timeout)
valid = helper.parse( qasm_example_abs_path )
if not valid:
   print("Qsam Error")
   exit(1)

qasm_file = open(qasm_example_abs_path, 'r') 
quantum_program = qasm_file.read()
qasm_file.close()
q = [{'qasm': quantum_program} ]
## select q1 if you use api.run_experiment(qasm, backend, shots, name=None, timeout=60) . QSAM object for job
q1 = quantum_program 
max_credits = 3
status = api.run_job(q, backend, shots, max_credits)

lc = api.get_last_codes()
#if verbose: lc qasms
print (status)
idx =(status['qasms'][0]['executionId'])
#idx = status['executionId']
print(api.get_execution(idx))
print(api.get_result_from_execution(idx))

#api.run_experiment(q1, backend, shots, name="CK_IBM_EXP_NAME", timeout=timeout)

