#!/usr/bin/env python3

"""
Visualize a QISKit ansatz function

Example running it partially using CK infrastructure:
    time ck virtual `ck search env:* --tags=qiskit,lib` `ck search env:* --tags=deployed,ansatz` --shell_cmd="$HOME/CK/ck-qiskit/program/visualize-ansatz/visualize_ansatz.py"
"""

from qiskit.tools.visualization._circuit_visualization import matplotlib_circuit_drawer

import custom_ansatz    # the file will be different depending on the plugin choice


def get_first_callable( namespace ):
    "return the first callable function in the given namespace"

    callable_names = [ attrib_name for attrib_name in dir(namespace) if callable(getattr(namespace, attrib_name)) ]

    top_level_methods = len(callable_names)

    if top_level_methods==1:
        return callable_names[0]
    else:
        raise Exception("Expecting exactly one top level function in 'custom_optimizer.py', but found {} ({}). Please refactor your code".format(top_level_methods, callable_names))


ansatz_method   = get_first_callable( custom_ansatz )
ansatz_function = getattr(custom_ansatz, ansatz_method)     # ansatz_method is a string/name, ansatz_function is an imported callable
ansatz_circuit  = ansatz_function( [0.0]*100 )              # give it a huge vector of fake arguments

matplotlib_circuit_drawer(ansatz_circuit, filename='ansatz_circuit.png')

