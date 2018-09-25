# CK repository for Quantum Information Software Kit (QISKit)

[![Travis Build Status](https://travis-ci.org/ctuning/ck-qiskit.svg?branch=master)](https://travis-ci.org/ctuning/ck-qiskit)


## Install global prerequisites (Python3, C++ compiler, libraries and CK)

### on Ubuntu/Debian:
```
$ sudo apt-get install python3 python3-pip python3-tk
$ sudo apt-get install libblas-dev liblapack-dev
$ sudo python3 -m pip install ck
```

### on MacOS
```
$ brew update                                                           # this swaps python versions and makes 3 the default one
$ brew install freetype                                                 # needed for matplotlib
$ brew reinstall python                                                 # install and link python3 and pip3 to /usr/local/bin
$ export PATH=/usr/local/opt/python/bin:$PATH
$ brew install gcc\@7 || brew link --overwrite gcc\@7                   # to avoid symlink conflict with oclint
$ python3 -m pip install --ignore-installed --verbose pip setuptools    # use own pip!
$ python3 -m pip install ck                                             # install CK
```


## Common part of the installation (Linux or MacOSX)

### Install this CK repository with all its dependencies (other CK repos to reuse artifacts)

```
$ ck pull repo:ck-qiskit
```

## Run a couple of tests which will also install some dependencies

### Run the following to install the software dependencies (accept most defaults by pressing `Enter`/`Return`) and run a simple QISKit test on a local simulator:
```
$ ck run program:qiskit-demo --cmd_key=hello
...
 (printing output files)

    * tmp-stdout.tmp

      -- Ignoring SSL errors.  This is not recommended --
      The backends available for use are: ['ibmq_qasm_simulator', 'ibmqx2', 'ibmqx4', 'ibmqx5', 'local_qasm_simulator', 'local_statevector_simulator', 'local_unitary_simulator']

      COMPLETED
      {'counts': {'00': 529, '11': 495}}


    * tmp-stderr.tmp



Execution time: 2.077 sec.
```

### Please register at [IBM Quantum Experience](https://quantumexperience.ng.bluemix.net/qx/signup) and copy your API token from the ["Advanced"](https://quantumexperience.ng.bluemix.net/qx/account/advanced) tab (you may need to click on the "Regenerate" button first).

### Now you can run the same test, but this time using IBM QX remote simulator. When prompted, please provide your API Token and the email address you used to register it.

These credentials will be stored on your computer in the form of a "CK env entry" that can be automatically substituted in your further experiments.

```
$ ck run program:qiskit-demo --cmd_key=hello --env.CK_IBM_BACKEND=ibmq_qasm_simulator
...
 (printing output files)

    * tmp-stdout.tmp

      -- Ignoring SSL errors.  This is not recommended --
      The backends available for use are: ['ibmq_qasm_simulator', 'ibmqx2', 'ibmqx4', 'ibmqx5', 'local_qasm_simulator', 'local_statevector_simulator', 'local_unitary_simulator']

      COMPLETED
      {'creg_labels': 'cr[2]', 'additionalData': {'seed': 1}, 'time': 0.00130243, 'counts': {'11': 495, '00': 529}, 'date': '2018-09-20T14:29:49.648Z'}


    * tmp-stderr.tmp



Execution time: 10.422 sec.
```

You should now be all set to use CK-QISKit, running your quantum code both on the local simulator and on IBM's remote sim and hardware.


## IBM Quantum Experience (QX) documentation

- [Main Repo](https://github.com/QISKit)
- [IBM Quantum Experience user guides](https://github.com/QISKit/ibmqx-user-guides)

- QISKit [SDK](https://github.com/QISKit/qiskit-sdk-py/blob/master/README.md)
- QISKit [Getting Started Guide](https://www.qiskit.org/documentation/quickstart.html)
- QISKit [Tutorial](https://github.com/QISKit/qiskit-tutorial)


At a lower level, you can use the native [QISKit Python API](https://github.com/QISKit/qiskit-api-py) to call [OpenQASM](https://github.com/QISKit/openqasm/blob/master/README.md).

### Real Backends

- [IBMQX2](https://github.com/QISKit/ibmqx-backend-information/blob/master/backends/ibmqx2/README.md)
- [IBMQX3](https://github.com/QISKit/ibmqx-backend-information/blob/master/backends/ibmqx3/README.md)
- [IBMQX4](https://github.com/QISKit/ibmqx-backend-information/blob/master/backends/ibmqx4/README.md)
- [IBMQX5](https://github.com/QISKit/ibmqx-backend-information/blob/master/backends/ibmqx5/README.md)

### Local Simulators

- `local_qasm_simulator`
- `local_clifford_simulator`
- `local_unitary_simulator`
- `local_projectq_simulator`
- `local_qiskit_simulator`
