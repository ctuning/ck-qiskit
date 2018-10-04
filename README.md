# CK repository for Quantum Information Software Kit (QISKit)

[![Travis Build Status](https://travis-ci.org/ctuning/ck-qiskit.svg?branch=master)](https://travis-ci.org/ctuning/ck-qiskit)
[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)
[![compatibility](https://github.com/ctuning/ck-guide-images/blob/master/ck-compatible.svg)](https://github.com/ctuning/ck)

## Install prerequisites (Python 3, C++ compiler, libraries and CK)

### Ubuntu/Debian Linux
```
$ sudo apt-get install python3 python3-pip python3-tk
$ sudo apt-get install libblas-dev liblapack-dev
$ sudo python3 -m pip install ck
```

### macOS
```
$ brew update                                                           # this swaps python versions and makes 3 the default one
$ brew install freetype                                                 # needed for matplotlib
$ brew reinstall python                                                 # install and link python3 and pip3 to /usr/local/bin
$ export PATH=/usr/local/opt/python/bin:$PATH
$ brew install gcc\@7 || brew link --overwrite gcc\@7                   # to avoid symlink conflict with oclint
$ python3 -m pip install --ignore-installed --verbose pip setuptools    # use own pip!
$ python3 -m pip install ck                                             # install CK
```

## Install QISKit
```
$ ck pull repo:ck-qiskit
$ ck install package:lib-python-qiskit-0.5.7
```

## Test QISKit

Run a couple of tests to install some dependencies and test basic workflows.

### Local execution

Run the following to install the software dependencies (accept most defaults by pressing `Enter`/`Return`) and run a simple QISKit test on a local simulator:
```
$ ck run program:qiskit-demo --cmd_key=quantum_coin_flip
...
 (printing output files)

    * tmp-stdout.tmp

      -- Ignoring SSL errors.  This is not recommended --

                  WARNING: There's no connection with IBMQuantumExperience servers.
                  cannot test I/O intesive tasks, will only test CPU intensive tasks
                  running the jobs in the local simulator

      The backends available for use are: ['local_qasm_simulator', 'local_statevector_simulator', 'local_unitary_simulator']

      User email: N/A

      COMPLETED
      {'counts': {'00': 4, '11': 6}}


    * tmp-stderr.tmp


Execution time: 0.000 sec.
```

### Remote execution

Please register at [IBM Quantum Experience](https://quantumexperience.ng.bluemix.net/qx/signup) ("IBM QX") and copy your API token from the ["Advanced"](https://quantumexperience.ng.bluemix.net/qx/account/advanced) tab (you may need to click on the "Regenerate" button first).

Now you can run the same test, but this time using the IBM QX remote simulator. When prompted, please provide your API token and the email address you used to register it.

These credentials will be stored on your computer in the form of a "CK environment entry" and automatically used for further experiments.

```
$ ck run program:qiskit-demo --cmd_key=quantum_coin_flip --env.CK_IBM_BACKEND=ibmq_qasm_simulator
...
 (printing output files)

    * tmp-stdout.tmp

      -- Ignoring SSL errors.  This is not recommended --
      The backends available for use are: ['ibmq_16_melbourne', 'ibmq_qasm_simulator', 'ibmqx2', 'ibmqx4', 'ibmqx5', 'local_qasm_simulator', 'local_statevector_simulator', 'local_unitary_simulator']

      User email: anton@dividiti.com

      COMPLETED
      {'creg_labels': 'cr[2]', 'additionalData': {'seed': 1}, 'time': 0.00023725, 'counts': {'11': 6, '00': 4}, 'date': '2018-09-26T11:40:38.802Z'}


Execution time: 0.000 sec.
```

You should now be all set to use CK-QISKit, running your quantum code both on the local simulator and on IBM's remote simulator and hardware!


## IBM QX documentation

- [IBM QX user guides](https://github.com/QISKit/ibmqx-user-guides)
- QISKit [main repo](https://github.com/QISKit)
- QISKit [SDK](https://github.com/QISKit/qiskit-sdk-py/blob/master/README.md)
- QISKit [Getting Started Guide](https://www.qiskit.org/documentation/quickstart.html)
- QISKit [Tutorial](https://github.com/QISKit/qiskit-tutorial)

At a lower level, you can use the native [QISKit Python API](https://github.com/QISKit/qiskit-api-py) to call [OpenQASM](https://github.com/QISKit/openqasm/blob/master/README.md).

### Real devices

- [`ibmqx2`](https://github.com/Qiskit/qiskit-backend-information/blob/master/backends/yorktown/V1/README.md) ("IBM Q 5 Yorktown")
- [`ibmqx4`](https://github.com/Qiskit/qiskit-backend-information/blob/master/backends/tenerife/V1/README.md) ("IBM Q 5 Tenerife")
- [`ibmqx5`](https://github.com/Qiskit/qiskit-backend-information/blob/master/backends/rueschlikon/V1/README.md) ("IBM Q 16 Rueschlikon")
- [`ibmq_16_melbourne`](https://github.com/Qiskit/qiskit-backend-information/blob/master/backends/melbourne/V1/README.md) ("IBM Q 16 Melbourne")

### Local simulators

- `local_qasm_simulator`
- `local_statevector_simulator`
- `local_unitary_simulator`
