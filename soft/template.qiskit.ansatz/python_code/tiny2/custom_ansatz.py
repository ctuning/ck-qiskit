#!/usr/bin/env python3

import numpy as np
import qiskit

num_params = 2      # make sure you set this correctly to the number of parameters used by the ansatz

## Previously used for Helium VQE in Rigetti implementation
#
def tiny_ansatz_2(current_params):
    q = qiskit.QuantumRegister(2, "q")
    qc = qiskit.QuantumCircuit(q, qiskit.ClassicalRegister(2, "c"))

    qc.x(q[0])
    qc.x(q[1])
    qc.rx( np.pi/2, q[0])
    qc.h(q[1])
    qc.cx(q[0], q[1])
    qc.rz(current_params[0], q[1])
    qc.cx(q[0], q[1])
    qc.rx(-np.pi/2, q[0])
    qc.h(q[1])
    qc.h(q[0])
    qc.rx( np.pi/2, q[1])
    qc.cx(q[0], q[1])
    qc.rz(current_params[1], q[1])
    qc.cx(q[0], q[1])
    qc.h(q[0])
    qc.rx(-np.pi/2, q[1])

    return qc
