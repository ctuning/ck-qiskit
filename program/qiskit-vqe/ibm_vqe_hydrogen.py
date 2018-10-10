#!/usr/bin/env python3

"""
This script runs Variational-Quantum-Eigensolver using Qiskit library

Example running it partially using CK infrastructure:
    time ck virtual `ck search env:* --tags=qiskit,lib` \
                    `ck search env:* --tags=vqe,lib` \
                    `ck search env:* --tags=ansatz` \
                    `ck search env:* --tags=optimizer` \
                    `ck search env:* --tags=hamiltonian` \
                    --shell_cmd="$HOME/CK/ck-qiskit/program/qiskit-vqe/ibm_vqe_hydrogen.py --max_func_evaluations=10"
"""

import os
import json
import time
import inspect

import numpy as np
from scipy import linalg as la

from qiskit import QuantumProgram, register
from qiskit.tools.apps.optimization import make_Hamiltonian, group_paulis
from qiskit.tools.qi.pauli import Pauli, label_to_pauli
from eval_hamiltonian import eval_hamiltonian

from vqe_utils import cmdline_parse_and_report, get_first_callable

from vqe_hamiltonian import label_to_hamiltonian_coeff      # the file contents will be different depending on the plugin choice
import custom_ansatz                                        # the file contents will be different depending on the plugin choice

fun_evaluation_counter = 0    # global

# See https://stackoverflow.com/questions/26646362/numpy-array-is-not-json-serializable
#
class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, np.bool_):
            return bool(obj)
        return json.JSONEncoder.default(self, obj)


def vqe_for_qiskit(sample_number, pauli_list, timeout_seconds, json_stream_file):

    def expectation_estimation(current_params, report):

        timestamp_before_ee = time.time()

        timestamp_before_q_run = timestamp_before_ee    # no point in taking consecutive timestamps

        ansatz_circuit  = ansatz_function(current_params)

        global fun_evaluation_counter

        complex_energy, q_run_seconds = eval_hamiltonian(Q_program, pauli_list_grouped, ansatz_circuit, sample_number, q_device_name, timeout=timeout_seconds)
        energy = complex_energy.real

        if len(q_run_seconds)>0:                            # got the real measured q time
            total_q_run_seconds = sum( q_run_seconds )
        else:                                               # have to assume
            total_q_run_seconds = time.time() - timestamp_before_q_run
            q_run_seconds       = [ total_q_run_seconds ]

        q_runs              = len(q_run_seconds)
        total_q_run_shots   = sample_number * q_runs
        q_run_shots         = [sample_number] * q_runs

        report_this_iteration = {
            'total_q_seconds_per_c_iteration' : total_q_run_seconds,
            'seconds_per_individual_q_run' :    q_run_seconds,
            'total_q_shots_per_c_iteration' :   total_q_run_shots,
            'shots_per_individual_q_run' :      q_run_shots,
            'energy' : energy,
        }

        if report != 'TestMode':
            report['iterations'].append( report_this_iteration )
            report['total_q_seconds'] += report_this_iteration['total_q_seconds_per_c_iteration']  # total_q_time += total
            report['total_q_shots'] += report_this_iteration['total_q_shots_per_c_iteration']

            fun_evaluation_counter += 1

        report_this_iteration['total_seconds_per_c_iteration'] = time.time() - timestamp_before_ee

        print(report_this_iteration, "\n")
        json_stream_file.write( json.dumps(report_this_iteration, cls=NumpyEncoder)+"\n" )
        json_stream_file.flush()

        return energy

    # Initialise quantum program
    Q_program = QuantumProgram()

    # Groups a list of (coeff,Pauli) tuples into tensor product basis (tpb) sets
    pauli_list_grouped = group_paulis(pauli_list)


    report = { 'total_q_seconds': 0, 'total_q_shots':0, 'iterations' : [] }

    # Initial objective function value
    fun_initial = expectation_estimation(start_params, 'TestMode')
    print('Initial guess at start_params is: {:.4f}'.format(fun_initial))

    timestamp_before_optimizer = time.time()
    optimizer_output = minimizer_function(expectation_estimation, start_params, my_args=(report), my_options = minimizer_options)
    report['total_seconds'] = time.time() - timestamp_before_optimizer

    # Also generate and provide a validated function value at the optimal point
    fun_validated = expectation_estimation(optimizer_output['x'], 'TestMode')
    print('Validated value at solution is: {:.4f}'.format(fun_validated))

    # Exact (noiseless) calculation of the energy at the given point:
    complex_energy, _ = eval_hamiltonian(Q_program, pauli_list, ansatz_function(optimizer_output['x']), 1, 'local_statevector_simulator')
    optimizer_output['fun_exact'] = complex_energy.real

    optimizer_output['fun_validated'] = fun_validated

    print('Total Q seconds = %f' % report['total_q_seconds'])
    print('Total Q shots = %d' % report['total_q_shots'])
    print('Total seconds = %f' % report['total_seconds'])

    return (optimizer_output, report)


if __name__ == '__main__':

    start_params, sample_number, q_device_name, minimizer_method, minimizer_options, minimizer_function = cmdline_parse_and_report(
        num_params                  = custom_ansatz.num_params,
        q_device_name_default       = 'local_qasm_simulator',
        q_device_name_help          = "Real devices: 'ibmqx4' or 'ibmqx5'. Use 'ibmq_qasm_simulator' for remote simulator or 'local_qasm_simulator' for local",
        minimizer_options_default   = '{"maxfev":200, "xatol": 0.001, "fatol": 0.001}',
        start_param_value_default   = 0.0
        )
    # q_device_name = os.environ.get('VQE_QUANTUM_BACKEND', 'local_qasm_simulator') # try 'local_qasm_simulator', 'ibmq_qasm_simulator', 'ibmqx4', 'ibmqx5'

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

    # Load the Hamiltonian into Qiskit-friendly format:
    pauli_list = [ [label_to_hamiltonian_coeff[label], label_to_pauli(label)] for label in label_to_hamiltonian_coeff ]

    # Calculate Exact Energy classically, to compare with quantum solution
    H = make_Hamiltonian(pauli_list)
    classical_energy = np.amin(la.eigh(H)[0])
    print('The exact ground state energy is: {:.4f}'.format(classical_energy))

    # Load the ansatz function from the plug-in
    ansatz_method   = get_first_callable( custom_ansatz )
    ansatz_function = getattr(custom_ansatz, ansatz_method)     # ansatz_method is a string/name, ansatz_function is an imported callable

    timeout_seconds = int( os.environ.get('VQE_QUANTUM_TIMEOUT', '120') )

    json_stream_file = open('vqe_stream.json', 'a')

    # ---------------------------------------- run VQE: --------------------------------------------------

    (vqe_output, report) = vqe_for_qiskit(sample_number, pauli_list, timeout_seconds, json_stream_file)

    # ---------------------------------------- store the results: ----------------------------------------

    json_stream_file.write( '# Experiment finished\n' )
    json_stream_file.close()

    minimizer_src   = inspect.getsource( minimizer_function )
    ansatz_src      = inspect.getsource( ansatz_function )

    vqe_input = {
        "q_device_name"     : q_device_name,
        "minimizer_method"  : minimizer_method,
        "minimizer_src"     : minimizer_src,
        "minimizer_options" : minimizer_options,
        "ansatz_method"     : ansatz_method,
        "ansatz_src"        : ansatz_src,
        "sample_number"     : sample_number,
        "classical_energy"  : classical_energy
        }

    output_dict     = { "vqe_input" : vqe_input, "vqe_output" : vqe_output, "report" : report }
    formatted_json  = json.dumps(output_dict, cls=NumpyEncoder, sort_keys = True, indent = 4)

#    print(formatted_json)

    with open('ibm_vqe_report.json', 'w') as json_file:
        json_file.write( formatted_json )
