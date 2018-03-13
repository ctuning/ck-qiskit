#! /bin/bash

#
# Installation script for Caffe.
#
# See CK LICENSE for licensing details.
# See CK COPYRIGHT for copyright details.
#
# Developer(s):
# - Grigori Fursin, 2017
#
# PACKAGE_DIR
# INSTALL_DIR

echo "Post install script"

#DEST_SRC=`ck find program:demo-projectq`
cp -r ${INSTALL_DIR}/src/out ${INSTALL_DIR}/build/
cp ${INSTALL_DIR}/src/qiskit/backends/_qiskit_cpp_simulator.py ${INSTALL_DIR}/build/qiskit/backends/_qiskit_cpp_simulator.py
return $?
