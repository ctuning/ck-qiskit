#!/usr/bin/env python3

import qiskit.tools.apps.optimization


num_of_qubits   = 2
circuit_depth   = 4
num_params      = 2 * num_of_qubits * circuit_depth     # make sure you set this correctly to the number of parameters used by the ansatz


## Previously used for Hydrogen VQE in QISKit implementation
#
def universal_ansatz(current_params, entangler_map=None):
    if entangler_map==None:
        # Which qubits to use (0 to 1 best to avoid qiskit bugs)
        entangler_map = {1: [0]}

    return qiskit.tools.apps.optimization.trial_circuit_ryrz(num_of_qubits, circuit_depth, current_params, entangler_map, None, False)

