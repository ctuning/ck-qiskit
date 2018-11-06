#!/usr/bin/env python3

"""
Example used in the readme. In this example a Bell state is made and then measured.

## Running this script using the "lightweight" CK infrastructure to import QISKit library...

# 1) on local simulator:
    ck virtual env --tags=lib,qiskit,v0.6 --shell_cmd=quantum_coin_flip.py

# 2) on remote simulator (need the API Token from IBM QuantumExperience) :
    CK_IBM_BACKEND=ibmq_qasm_simulator ck virtual env --tag_groups="lib,qiskit,v0.6 login,qiskit"  --shell_cmd=quantum_coin_flip.py

# 3) on remote quantum hardware (need the API Token from IBM QuantumExperience) :
    CK_IBM_BACKEND=ibmq_16_melbourne ck virtual env --tag_groups="lib,qiskit,v0.6 login,qiskit"  --shell_cmd=quantum_coin_flip.py

"""
import sys
import os

# We don't know from where the user is running the example,
# so we need a relative position from this file path.
# TODO: Relative imports for intra-package imports are highly discouraged.
# http://stackoverflow.com/a/7506006
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
from qiskit import QISKitError, execute
from qiskit import Aer, IBMQ

local_backends_names    = [b.name() for b in Aer.backends()]
remote_backends_names   = []
backend_name    = os.environ.get('CK_IBM_BACKEND', 'qasm_simulator')

try:
    print('Trying to connect to the LOCAL backend "{}"...'.format(backend_name))
    backend = Aer.get_backend( backend_name )
except KeyError:
    print('Could not find the LOCAL backend "{}" - available LOCAL backends:\n\t{}'.format(backend_name, local_backends_names))
    try:
        api_token   = os.environ.get('CK_IBM_API_TOKEN')
        if not api_token:
            print('CK_IBM_API_TOKEN is not defined, so cannot connect to REMOTE backends - bailing out.'.format(backend_name))
            exit(1)
        print('\nCK_IBM_API_TOKEN found.\nTrying to connect to the REMOTE backend "{}"...'.format(backend_name))
        IBMQ.enable_account( api_token )
        backend = IBMQ.get_backend( backend_name )
        remote_backends_names = [b.name() for b in IBMQ.backends(operational=True)]
    except KeyError as ex:
        print('Could not find the REMOTE backend "{}" - available remote backends:\n\t{}'.format(backend_name, remote_backends_names))
        exit(1)
print('Using "{}" backend...\n'.format(backend.name()))

email   = os.environ.get('CK_IBM_API_EMAIL', 'N/A')
print("User email: {}\n".format(email))

timeout = int( os.environ.get('CK_IBM_TIMEOUT', 120) )
shots   = int( os.environ.get('CK_IBM_REPETITION', 10) )

try:
    # Create a Quantum Register with 2 qubits.
    qr = QuantumRegister(2)
    # Create a Classical Register with 2 bits.
    cr = ClassicalRegister(2)
    # Create a Quantum Circuit with the Quantum Register and Classical Register
    circuit = QuantumCircuit(qr, cr)

    # Add an H gate to qubit 0, putting this qubit in superposition.
    circuit.h(qr[0])
    # Add a CX gate to control qubit 0 and target qubit 1, putting
    # the qubits in a Bell state.
    circuit.cx(qr[0], qr[1])

    # Add a Measure gate to observe the state.
    circuit.measure(qr, cr)

    # Compile and execute the Quantum Program using the given backend.
    job = execute(circuit, backend=backend, shots=shots, seed=1)

    result = job.result()

    # Show the results.
    print(result)       # 'COMPLETED'

    q_execution_time = result.get_data().get('time')
    if q_execution_time:
        print("Quantum execution time: {} sec".format(q_execution_time) )

    print(result.get_data())

except QISKitError as ex:
    print('Error in the circuit! {}'.format(ex))


########################### Save output to CK format. ##############################

import json
import numpy as np

# See https://stackoverflow.com/questions/26646362/numpy-array-is-not-json-serializable
#
class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, np.bool_):
            return bool(obj)
        elif isinstance(obj, np.complex):
            return obj.real         # if you care about the imaginary part, try (obj.real, obj.imag)
        return json.JSONEncoder.default(self, obj)

output_dict = {
    'backend_name':     backend_name,
    'local_backends':   local_backends_names,
    'remote_backends':  remote_backends_names,
    'email':            email,
    'result':           result.get_data(),
}

formatted_json  = json.dumps(output_dict, cls=NumpyEncoder, sort_keys = True, indent = 4)
#print(formatted_json)

with open('tmp-ck-timer.json', 'w') as json_file:
    json_file.write( formatted_json )
