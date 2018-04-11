# CK repository for Quantum Information Software Kit (QISKit)

[![Travis Build Status](https://travis-ci.org/ctuning/ck-qiskit.svg?branch=master)](https://travis-ci.org/ctuning/ck-qiskit)


## Installation (on Ubuntu or Debian)

### Install global prerequisites, Python 3 and Pip 3 (Python 2 is **not** supported)
```
$ sudo apt install build-essential liblapack-dev libblas-dev libssl-dev libpng-dev libfreetype6-dev
$ sudo apt install python3 python3-pip python3-wheel pkg-config
$ sudo pip3 install setuptools
```

### Install Collective Knowledge
```
$ sudo pip3 install ck
```


## Installation (on MacOSX)

### Install global prerequisites, GCC compiler v.6+, Python3 and its Pip3 (Python 2 is **not** supported)
```
$ brew update
$ brew reinstall python                                                 # brew now installs python3 and pip3 by default
$ export PATH=/usr/local/opt/python/libexec/bin:$PATH
$ brew install gcc\@6 || brew link --overwrite gcc\@6                   # to avoid symlink conflict with oclint
$ python -m pip install --ignore-installed --verbose pip setuptools     # let python3 find its own pip and install its own setuptools
```

### Install Collective Knowledge
```
$ python -m pip install ck                                              # let python3 find its own pip and install CK
```


## Common part of the installation (Linux or MacOSX)

### Install this CK repository with all its dependencies (other CK repos to reuse artifacts)

```
$ ck pull repo:ck-qiskit
```

## Install Quantum Information Software Kit (QISKit)

```
$ ck list ck-qiskit:package:*
$ ck install package:lib-qiskit
```

## IBM Quantum Experience

### Documentation
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

- `local_clifford_simulator`
- `local_qasm_simulator`
- `local_unitary_simulator`
- `local_projectq_simulator`
- `local_qiskit_simulator`


## Run Programs

Get a valid [IBM_API_TOKEN](https://quantumexperience.ng.bluemix.net/qx/login) `->` myaccount `->` advanced

**NB:** An exception might be raised due to login failure (missing or invalid token).

#### Run an example using a local simulator

```
$ ck run program:qiskit-demo --cmd_key=hello \
  --env.CK_IBM_BACKEND=local_qasm_simulator
```


#### Run an example using a remote simulator

```
$ ck run program:qiskit-demo --cmd_key=hello \
  --env.CK_IBM_BACKEND=ibmqx_qasm_simulator --env.CK_IBM_API_TOKEN=<YOUR_TOKEN>
```

#### Run an example using IBMQX5 

```
$ ck run program:qiskit-demo --cmd_key=hello \
  --env.CK_IBM_BACKEND=ibmqx5 --env.CK_IBM_API_TOKEN=<YOUR_TOKEN>
```


## FAQ

### How to register my libraries and tools with CK?

CK will try to detect compilers and libraries automatically, but you can also
register them as follows:

```
$ ck detect soft:compiler.gcc
$ ck detect soft:compiler.python
$ ck detect soft:lib.blas
$ ck detect soft:lib.lapack
```

You can also register tools by providing a full path e.g.
```
$ ck detect soft:compiler.python --full_path=`which python3`
```

### Where does CK store my program and its output?

A program can be located on disk by its name as follows:
```
$ ck find program:projectq-shor
/home/flavio/CK-REPOS/ck-qiskit/program/qiskit-shor
$ ls `ck find program:qiskit-shor`
quantum_random_numbers.py  shor.py
```

Temporary files (including the executable, `stderr` and `stdout`) are in the `tmp` directory:
```
$ cd `ck find program:qiskit-shor`/tmp
```

## Troubleshooting

**TODO**
