# -*- coding: utf-8 -*-

# Copyright 2017, IBM.
#
# This source code is licensed under the Apache License, Version 2.0 found in
# the LICENSE.txt file in the root directory of this source tree.

"""
The eval_hamiltonian function has been borrowed from QISKit's tools/apps/optimization.py
and slightly modified by dividiti to fit our benchmarking needs.
"""

import uuid
import copy
import numpy as np

from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
from qiskit.extensions.standard import h, x, y, z
from qiskit.tools.apps.optimization import make_Hamiltonian, group_paulis, measure_pauli_z


def eval_hamiltonian(Q_program, hamiltonian, input_circuit, shots, device, timeout=60):
    """Calculates the average value of a Hamiltonian on a state created by the
     input circuit

    Args:
        Q_program (QuantumProgram): QuantumProgram object used to run the
            input circuit.
        hamiltonian (array or matrix or list): a representation of the
            Hamiltonian or observables to be measured. If it is a list, it is
            a list of Pauli operators grouped into tpb sets.
        input_circuit (QuantumCircuit): input circuit.
        shots (int): number of shots considered in the averaging. If 1 the
            averaging is exact.
        device (str): the backend used to run the simulation.
    Returns:
        float: Average value of the Hamiltonian or observable.
    """
    energy = 0

    if 'statevector' in device:
        # Hamiltonian is not a pauli_list grouped into tpb sets
        if not isinstance(hamiltonian, list):
            circuit = ['c' + str(uuid.uuid4())]    # unique random circuit for no collision
            Q_program.add_circuit(circuit[0], input_circuit)
            result = Q_program.execute(circuit, device, shots=shots, timeout=timeout,
                                       config={"data": ["statevector"]})
            statevector = result.get_data(circuit[0]).get('statevector')
            if statevector is None:
                statevector = result.get_data(
                    circuit[0]).get('statevector')
                if statevector:
                    statevector = statevector[0]
            # Diagonal Hamiltonian represented by 1D array
            if (hamiltonian.shape[0] == 1 or
                    np.shape(np.shape(np.array(hamiltonian))) == (1,)):
                energy = np.sum(hamiltonian * np.absolute(statevector) ** 2)
            # Hamiltonian represented by square matrix
            elif hamiltonian.shape[0] == hamiltonian.shape[1]:
                energy = np.inner(np.conjugate(statevector),
                                  np.dot(hamiltonian, statevector))
        # Hamiltonian represented by a Pauli list
        else:
            circuits = []
            circuits_labels = []
            circuits.append(input_circuit)
            # Trial circuit w/o the final rotations
            circuits_labels.append('circuit_label0' + str(uuid.uuid4()))
            Q_program.add_circuit(circuits_labels[0], circuits[0])
            # Execute trial circuit with final rotations for each Pauli in
            # hamiltonian and store from circuits[1] on
            n_qubits = input_circuit.regs['q'].size
            q = QuantumRegister(n_qubits, "q")
            i = 1
            for p in hamiltonian:
                circuits.append(copy.deepcopy(input_circuit))
                for j in range(n_qubits):
                    if p[1].v[j] == 0 and p[1].w[j] == 1:
                        circuits[i].x(q[j])
                    elif p[1].v[j] == 1 and p[1].w[j] == 0:
                        circuits[i].z(q[j])
                    elif p[1].v[j] == 1 and p[1].w[j] == 1:
                        circuits[i].y(q[j])

                circuits_labels.append('circuit_label' + str(i) + str(uuid.uuid4()))
                Q_program.add_circuit(circuits_labels[i], circuits[i])
                i += 1
            result = Q_program.execute(circuits_labels, device, shots=shots, timeout=timeout)
            # no Pauli final rotations
            statevector_0 = result.get_data(
                circuits_labels[0])['statevector']
            i = 1
            for p in hamiltonian:
                statevector_i = result.get_data(
                    circuits_labels[i])['statevector']
                # inner product with final rotations of (i-1)-th Pauli
                energy += p[0] * np.inner(np.conjugate(statevector_0),
                                          statevector_i)
                i += 1
    # finite number of shots and hamiltonian grouped in tpb sets
    else:
        circuits = []
        circuits_labels = []
        n = int(len(hamiltonian[0][0][1].v))
        q = QuantumRegister(n, "q")
        c = ClassicalRegister(n, "c")
        i = 0
        for tpb_set in hamiltonian:
            circuits.append(copy.deepcopy(input_circuit))
            circuits_labels.append('tpb_circuit_' + str(i) + str(uuid.uuid4()))
            for j in range(n):
                # Measure X
                if tpb_set[0][1].v[j] == 0 and tpb_set[0][1].w[j] == 1:
                    circuits[i].h(q[j])
                # Measure Y
                elif tpb_set[0][1].v[j] == 1 and tpb_set[0][1].w[j] == 1:
                    circuits[i].s(q[j]).inverse()
                    circuits[i].h(q[j])
                circuits[i].measure(q[j], c[j])
            Q_program.add_circuit(circuits_labels[i], circuits[i])
            i += 1
        result = Q_program.execute(circuits_labels, device, shots=shots, timeout=timeout)
        for j, _ in enumerate(hamiltonian):
            for k, _ in enumerate(hamiltonian[j]):
                energy += hamiltonian[j][k][0] *\
                    measure_pauli_z(result.get_counts(
                        circuits_labels[j]), hamiltonian[j][k][1])

    return energy

