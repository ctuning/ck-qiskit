#!/usr/bin/env python3

"""
This script runs Variational-Quantum-Eigensolver on H2 (Hydrogen molecule)

Example running it partially using CK infrastructure:
    time ck virtual `ck search env:* --tags=qiskit,lib`  `ck search env:* --tags=hackathon`  --shell_cmd="$HOME/CK/ck-qiskit/program/qiskit-vqe/ibm_vqe_hydrogen.py --minimizer_method=my_minimizer"
"""

import os
import json
import time
import inspect

import numpy as np
from scipy import linalg as la

from qiskit import QuantumProgram, register
from qiskit.tools.apps.optimization import trial_circuit_ryrz, Hamiltonian_from_file, make_Hamiltonian, eval_hamiltonian, group_paulis
from qiskit.tools.qi.pauli import Pauli, label_to_pauli

from hackathon.utils import cmdline_parse_and_report


# See https://stackoverflow.com/questions/26646362/numpy-array-is-not-json-serializable
#
class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, np.bool_):
            return bool(obj)
        return json.JSONEncoder.default(self, obj)


def Hamiltonian_from_list(list_of_pairs):
    pauli_list = []
    for pair in list_of_pairs:
        label, weight = pair
        pauli_list.append([weight, label_to_pauli(label)])
    return pauli_list


def vqe_for_qiskit(sample_number):

    def expectation_estimation(current_params, report):

        timestamp_before_ee = time.time()

        timestamp_before_q_run = timestamp_before_ee    # no point in taking consecutive timestamps
        energy = eval_hamiltonian(Q_program, pauli_list_grouped, trial_circuit_ryrz(n, m, current_params, entangler_map, None, False), sample_number, q_device_name).real
        q_run_seconds   = time.time() - timestamp_before_q_run
        q_run_shots     = sample_number

        report_this_iteration = {
            'total_q_seconds_per_c_iteration' : q_run_seconds,
            'seconds_per_individual_q_run' : [ q_run_seconds ],
            'total_q_shots_per_c_iteration' : q_run_shots,
            'shots_per_individual_q_run' : [ q_run_shots ],
            'energy' : energy
            }

        if report != 'TestMode':
            report['iterations'].append( report_this_iteration )
            report['total_q_seconds'] += report_this_iteration['total_q_seconds_per_c_iteration']  # total_q_time += total
            report['total_q_shots'] += report_this_iteration['total_q_shots_per_c_iteration']

        report_this_iteration['total_seconds_per_c_iteration'] = time.time() - timestamp_before_ee

        print(report_this_iteration, "\n")

        return energy


    report = { 'total_q_seconds': 0, 'total_q_shots':0, 'iterations' : [] }

    # Initialise quantum program
    Q_program = QuantumProgram()

    initial_out = expectation_estimation(start_params, { 'total_q_seconds': 0, 'total_q_shots':0, 'iterations' : [] })   # Initial objective function value
    print('Initial guess at solution is: {:.4f}'.format(initial_out))

    timestamp_before_optimizer = time.time()
    optimizer_output = minimizer_function(expectation_estimation, start_params, my_args=(report), my_options = minimizer_options)

    # override the returned function value by one computed by us
    optimizer_output['fun_validated'] = expectation_estimation(optimizer_output['x'], 'TestMode')

    report['total_seconds'] = time.time() - timestamp_before_optimizer

    print('Total Q seconds = %f' % report['total_q_seconds'])
    print('Total Q shots = %d' % report['total_q_shots'])
    print('Total seconds = %f' % report['total_seconds'])

    return (optimizer_output, report)

#    out = optimizer_output.fun   # Final optimised value
#   print('Final optimised solution is: {:.4f}'.format(out))


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

    # Build hamiltonian for H2 from the list below:
    #ham_name = '../H2Equilibrium.txt'
    #pauli_list = Hamiltonian_from_file(ham_name)
    pauli_list = Hamiltonian_from_list([
        ('ZZ',  0.011279956224107712),
        ('II', -1.0523760606256514),
        ('ZI',  0.39793570529466216),
        ('IZ',  0.39793570529466227),
        ('XX',  0.18093133934472627)
        ])

    pauli_list_grouped = group_paulis(pauli_list) # Groups a list of (coeff,Pauli) tuples into tensor product basis (tpb) sets

    # Calculate Exact Energy classically, to compare with quantum solution
    H = make_Hamiltonian(pauli_list)
    classical_energy = np.amin(la.eigh(H)[0])
    print('The exact ground state energy is: {:.4f}'.format(classical_energy))

    entangler_map = {1: [0]}    # Which qubits to use (0 to 1 best to avoid qiskit bugs)

    # ---------------------------------------- run VQE: ----------------------------------------

    (vqe_output, report) = vqe_for_qiskit(sample_number)

    # ---------------------------------------- store the results: ----------------------------------------

    minimizer_src   = inspect.getsource( minimizer_function )

    vqe_input = {
        "q_device_name"     : q_device_name,
        "minimizer_method"  : minimizer_method,
        "minimizer_options" : minimizer_options,
        "sample_number"     : sample_number,
        "minimizer_src"     : minimizer_src,
        "classical_energy"  : classical_energy
        }

    output_dict     = { "vqe_input" : vqe_input, "vqe_output" : vqe_output, "report" : report }
    formatted_json  = json.dumps(output_dict, cls=NumpyEncoder, sort_keys = True, indent = 4)

#    print(formatted_json)

    with open('ibm_vqe_report.json', 'w') as json_file:
        json_file.write( formatted_json )
