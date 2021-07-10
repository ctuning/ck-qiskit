# CK repository for Quantum Information Software Kit (QISKit)

**All CK components can be found at [cKnowledge.io](https://cKnowledge.io) and in [one GitHub repository](https://github.com/ctuning/ck-mlops)!**

*This project is hosted by the [cTuning foundation](https://cTuning.org).*

[![compatibility](https://github.com/ctuning/ck-guide-images/blob/master/ck-compatible.svg)](https://github.com/ctuning/ck)
[![automation](https://github.com/ctuning/ck-guide-images/blob/master/ck-artifact-automated-and-reusable.svg)](http://cTuning.org/ae)
[![workflow](https://github.com/ctuning/ck-guide-images/blob/master/ck-workflow.svg)](http://cKnowledge.org)

[![DOI](https://zenodo.org/badge/124924875.svg)](https://zenodo.org/badge/latestdoi/124924875)
[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)
[![Travis Build Status](https://travis-ci.org/ctuning/ck-qiskit.svg?branch=master)](https://travis-ci.org/ctuning/ck-qiskit)

## Install prerequisites (Python, CK, C++ compiler, libraries)

- Python 3.5+ ([required by QISKit](https://github.com/Qiskit/qiskit-terra#dependencies); [CK supports 2.7 and 3.3+](https://github.com/ctuning/ck#minimal-installation)).
- [Collective Knowledge](http://cknowledge.org).
- [Tkinter](https://wiki.python.org/moin/TkInter) (required for `program:visualize-ansatz`).

### Ubuntu/Debian Linux
```
$ sudo apt-get install python3 python3-pip python3-tk
$ sudo python3 -m pip install ck
```

### macOS
```
$ brew update                                                           # makes python3 the default python
$ brew unlink python                                                    # make sure we install Python 3.6, and not 3.7
$ brew install https://raw.githubusercontent.com/Homebrew/homebrew-core/f2a764ef944b1080be64bd88dca9a1d80130c558/Formula/python.rb
$ export PATH=/usr/local/opt/python/bin:$PATH                           # also append this to $HOME/.bash_profile
$ brew install freetype                                                 # needed for matplotlib
$ python3 -m pip install --ignore-installed --verbose pip setuptools    # use its own pip!
$ python3 -m pip install ck                                             # install CK
```

### Windows

Please see [here](https://github.com/ctuning/ck#windows).


## Install QISKit
```
$ ck pull repo:ck-qiskit
$ ck install package:lib-python-qiskit --force_version=0.6.1
```

## Test QISKit

Run a couple of tests to install some dependencies and test basic workflows.

### Local execution

Run the following to install the software dependencies (accept most defaults by pressing `Enter`/`Return`) and run a simple QISKit test on a local simulator:
```
$ ck run program:qiskit-0.6-demo --cmd_key=quantum_coin_flip
...
Trying to connect to the LOCAL backend "qasm_simulator"...
Using "qasm_simulator" backend...

User email: N/A

COMPLETED
{'counts': {'00': 4, '11': 6}}
```

### Remote execution

Please register at [IBM Quantum Experience](https://quantumexperience.ng.bluemix.net/qx/signup) ("IBM QX") and copy your API token from the ["Advanced"](https://quantumexperience.ng.bluemix.net/qx/account/advanced) tab (you may need to click on the "Regenerate" button first).

Now you can run the same test, but this time using the IBM QX remote simulator. When prompted, please provide your API token and the email address you used to register it.

These credentials will be stored on your computer in the form of a "CK environment entry" and automatically used for further experiments.

```
$ ck run program:qiskit-0.6-demo --cmd_key=quantum_coin_flip --env.CK_IBM_BACKEND=ibmq_qasm_simulator
...
Trying to connect to the LOCAL backend "ibmq_qasm_simulator"...
Could not find the LOCAL backend "ibmq_qasm_simulator" - available LOCAL backends:
        ['qasm_simulator', 'qasm_simulator_py', 'statevector_simulator', 'statevector_simulator_py', 'unitary_simulator', 'clifford_simulator']

CK_IBM_API_TOKEN found.
Trying to connect to the REMOTE backend "ibmq_qasm_simulator"...
Using "ibmq_qasm_simulator" backend...

User email: anton@dividiti.com

COMPLETED
{'counts': {'0x3': 6, '0x0': 4}}
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

### Local simulators (supported by `program:qiskit-0.6-demo`)

- `qasm_simulator`
- `qasm_simulator_py`
- `unitary_simulator`
