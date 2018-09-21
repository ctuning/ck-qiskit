#!/usr/bin/env python3

"""
Example used in the readme. In this example a Bell state is made and then measured.

## Running this script using the "lightweight" CK infrastructure to import QISKit library...

# 1) on local simulator:
    ck virtual env --tags=lib,qiskit --shell_cmd=quantum_coin_flip.py

# 2) on remote simulator (need the API Token from IBM QuantumExperience) :
    CK_IBM_BACKEND=ibmq_qasm_simulator ck virtual `ck search env:* --tags=qiskit,lib`  `ck search env:* --tags=ibmqx,login` --shell_cmd=quantum_coin_flip.py

# 3) on remote quantum hardware (need the API Token from IBM QuantumExperience) :
    CK_IBM_BACKEND=ibmqx4 ck virtual `ck search env:* --tags=qiskit,lib`  `ck search env:* --tags=ibmqx,login` --shell_cmd=quantum_coin_flip.py

"""
import sys
import os

# We don't know from where the user is running the example,
# so we need a relative position from this file path.
# TODO: Relative imports for intra-package imports are highly discouraged.
# http://stackoverflow.com/a/7506006
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from qiskit import QuantumProgram, QISKitError, available_backends, register

try:
    import Qconfig
    register(Qconfig.APItoken, Qconfig.config["url"], verify=False,
                      hub=Qconfig.config["hub"],
                      group=Qconfig.config["group"],
                      project=Qconfig.config["project"])
except:
    print("""
            WARNING: There's no connection with IBMQuantumExperience servers.
            cannot test I/O intesive tasks, will only test CPU intensive tasks
            running the jobs in the local simulator
            """)

print("The backends available for use are: {}\n".format(available_backends()))
#backend = os.environ.get('CK_IBM_BACKEND', 'ibmq_qasm_simulator')
backend = os.environ.get('CK_IBM_BACKEND', 'local_qasm_simulator')

timeout = int( os.environ.get('CK_IBM_TIMEOUT', 120) )
shots   = int( os.environ.get('CK_IBM_REPETITION', 10) )

# Create a QuantumProgram object instance.
Q_program = QuantumProgram()

try:
    # Create a Quantum Register called "qr" with 2 qubits.
    qr = Q_program.create_quantum_register("qr", 2)
    # Create a Classical Register called "cr" with 2 bits.
    cr = Q_program.create_classical_register("cr", 2)
    # Create a Quantum Circuit called "qc" with the Quantum Register "qr"
    # and the Classical Register "cr".
    qc = Q_program.create_circuit("bell", [qr], [cr])

    # Add an H gate to qubit 0, putting this qubit in superposition.
    qc.h(qr[0])
    # Add a CX gate to control qubit 0 and target qubit 1, putting
    # the qubits in a Bell state.
    qc.cx(qr[0], qr[1])

    # Add a Measure gate to observe the state.
    qc.measure(qr, cr)

    # Compile and execute the Quantum Program using the given backend.
    result = Q_program.execute(["bell"], backend=backend, shots=shots, seed=1, timeout=timeout)

    # Show the results.
    print(result)
    print(result.get_data("bell"))

except QISKitError as ex:
    print('Error in the circuit! {}'.format(ex))
