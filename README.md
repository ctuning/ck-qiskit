# ck-qiskit
CK repository for Quantum Information Software Kit (QISKit)


## Installation 

### Install global prerequisites (Ubuntu)

```
$ sudo apt-get install build-essential
$ sudo apt install libblas-dev liblapack-dev
```

### Install Python 3
(Python 2 is **not** supported)

```
$ sudo apt-get install python3 python3-pip
$ sudo pip3 install scipy
```

### Install Collective Knowledge

```
$ sudo pip3 install ck
```

### Install this CK repository with all its dependencies (other CK repos to reuse artifacts)
```
$ ck pull repo --url=git@github.com:dividiti/ck-qiskit
```


## Packages installation

List all the packages available 

```
$ ck list ck-qiskit:package:*
```

## IBM QuantumExperience

**Documentation**

[Main Repo](https://github.com/QISKit) and [IBMQX USER GUIDES](https://github.com/QISKit/ibmqx-user-guides)

[QISKit SDK](https://github.com/QISKit/qiskit-sdk-py/blob/master/README.md) and [Getting Started Guide](https://www.qiskit.org/documentation/quickstart.html)

[QISKit Tutorial](https://github.com/QISKit/qiskit-tutorial)


At a lower level, you can use the native Python API to call OpenQASM 

[QISKit API](https://github.com/QISKit/qiskit-api-py)

[OpenQASM](https://github.com/QISKit/openqasm/blob/master/README.md)



**Real Backends**

[IBMQX2](https://github.com/QISKit/ibmqx-backend-information/blob/master/backends/ibmqx2/README.md) 

[IBMQX3](https://github.com/QISKit/ibmqx-backend-information/blob/master/backends/ibmqx3/README.md)

[IBMQX4](https://github.com/QISKit/ibmqx-backend-information/blob/master/backends/ibmqx4/README.md)

[IBMQX5](https://github.com/QISKit/ibmqx-backend-information/blob/master/backends/ibmqx5/README.md)



### Quantum Information Software Kit (QISKit) package

```
$ ck install package:lib-qiskit
```

### Run Programs

Get a valid [IBM_API_TOKEN](https://quantumexperience.ng.bluemix.net/qx/login) -> myaccount -> advanced

1) Run an example using the local simulator. An exception might be  raised due to login failure (missing or invalid token)

```
$ ck run program:qiskit-demo --cmd_key=hello --env.CK_IBM_BACKEND=local_qasm_simulator
```


2) Run an example using the remote simulator

```
$ ck run program:qiskit-demo --cmd_key=hello --env.CK_IBM_API_TOKEN=<YOUR_TOKEN> --env.CK_IBM_BACKEND=ibmqx_qasm_simulator
```

3) Run an example using IBMQX5 

```
$ ck run program:qiskit-demo --cmd_key=hello --env.CK_IBM_API_TOKEN=<YOUR_TOKEN> --env.CK_IBM_BACKEND=ibmqx5
```


## FAQ

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
