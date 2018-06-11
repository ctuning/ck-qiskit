#!/usr/bin/env python3

"""
This script runs Variational-Quantum-Eigensolver on H2 (Hydrogen molecule)

Example running it partially using CK infrastructure:
    time ck virtual `ck search env:* --tags=lib,qiskit` `ck search env:* --tags=ibmqx,login` `ck search env:* --tags=hackathon` --shell_cmd='ibm_vqe_hydrogen.py'
"""

import os
import json

import numpy as np
from scipy import linalg as la

from qiskit import QuantumProgram, register
from qiskit.tools.apps.optimization import trial_circuit_ryrz, Hamiltonian_from_file, make_Hamiltonian, eval_hamiltonian, group_paulis

from hackathon.utils import cmdline_parse_and_report


if __name__ == '__main__':
    n = 2   # Number of qubits
    m = 6   # Depth of circuit
    num_params  = 2 * n * m

    start_params, sample_number, q_device_name, minimizer_method, minimizer_options, minimizer_function = cmdline_parse_and_report(
        num_params                  = num_params,
        q_device_name_default       = 'local_qasm_simulator',
        q_device_name_help          = "Real devices: 'ibmqx4' or 'ibmqx5'. Use 'ibmq_qasm_simulator' for remote simulator or 'local_qasm_simulator' for local",
        minimizer_options_default   = '{"maxfev":200, "xatol": 0.001, "fatol": 0.001}'
        )
    # q_device_name = os.environ.get('CK_IBM_BACKEND', 'local_qasm_simulator') # try 'local_qasm_simulator', 'ibmq_qasm_simulator', 'ibmqx4', 'ibmqx5'

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

    # Ignore warnings due to chopping of small imaginary part of the energy
    #import warnings
    #warnings.filterwarnings('ignore')

    # Import hamiltonian for H2 from file
    ham_name = 'H2Equilibrium.txt'
    pauli_list = Hamiltonian_from_file(ham_name)
    pauli_list_grouped = group_paulis(pauli_list) # Groups a list of (coeff,Pauli) tuples into tensor product basis (tpb) sets

    # Calculate Exact Energy classically, to compare with quantum solution
    H = make_Hamiltonian(pauli_list)
    exact = np.amin(la.eigh(H)[0])
    print('The exact ground state energy is: {:.4f}'.format(exact))

    entangler_map = {1: [0]}    # Which qubits to use (0 to 1 best to avoid qiskit bugs)

    # Initialise quantum program
    Q_program = QuantumProgram()

    def objective_function(current_params, sample_number):
        return eval_hamiltonian(Q_program, pauli_list_grouped, trial_circuit_ryrz(n, m, current_params, entangler_map, None, False), sample_number, q_device_name).real

    initial_out = objective_function(start_params,sample_number)   # Initial objective function value
    print('Initial guess at solution is: {:.4f}'.format(initial_out))

    optimizer_output = minimizer_function(objective_function, start_params, my_args=(sample_number), my_options = minimizer_options)

    out = optimizer_output.fun   # Final optimised value
    print('Final optimised solution is: {:.4f}'.format(out))
