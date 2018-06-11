#!/usr/bin/env python3

"""
This script runs Variational-Quantum-Eigensolver on H2 (Hydrogen molecule)

Example running it partially using CK infrastructure:
    time CK_IBM_BACKEND=ibmq_qasm_simulator ck virtual `ck search env:* --tags=lib,qiskit` `ck search env:* --tags=ibmqx,login` `ck search env:* --tags=hackathon` --shell_cmd='python3 ibm_vqe.py'
"""

import os
import numpy as np
from scipy import linalg as la
from scipy.optimize import minimize
from qiskit import QuantumProgram, register

from qiskit.tools.apps.optimization import trial_circuit_ryrz, Hamiltonian_from_file, make_Hamiltonian, eval_hamiltonian, group_paulis

from hackathon import optimizers as optimizers

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

q_device = os.environ.get('CK_IBM_BACKEND', 'local_qasm_simulator') # try 'local_qasm_simulator', 'ibmq_qasm_simulator', 'ibmqx4', 'ibmqx5'
print("Using '%s' backend" % q_device)

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

n = 2   # Number of qubits
m = 6   # Depth of circuit

entangler_map = {1: [0]}    # Which qubits to use (0 to 1 best to avoid qiskit bugs)

start_params = np.random.randn(2 * n * m)  # Initial guess of ansatz
shots = 1000 # Number of shots to use for quantum computer expectation estimation

# Initialise quantum program
Q_program = QuantumProgram()

def objective_function(current_params, shots):
    return eval_hamiltonian(Q_program, pauli_list_grouped, trial_circuit_ryrz(n, m, current_params, entangler_map, None, False), shots, q_device).real

initial_out = objective_function(start_params,shots)   # Initial objective function value
print('Initial guess at solution is: {:.4f}'.format(initial_out))

minimizer_method    = 'my_nelder_mead' # FIXME: to be passed as a parameter
minimizer_options   = {'maxfev':200, 'xatol': 0.001, 'fatol': 0.001}

minimizer_function  = getattr(optimizers, minimizer_method)   # minimizer_method is a string/name, minimizer_function is an imported callable

# Optimization
optimizer_output = minimizer_function(objective_function, start_params, my_args=(shots), my_options = minimizer_options)

out = optimizer_output.fun   # Final optimised value
print('Final optimised solution is: {:.4f}'.format(out))
