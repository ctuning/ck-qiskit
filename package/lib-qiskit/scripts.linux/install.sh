#! /bin/bash

#
# Installation script for Caffe.
#
# See CK LICENSE for licensing details.
# See CK COPYRIGHT for copyright details.
#
# Developer(s):
# - Flavio Vella, 2018;
#

# PACKAGE_DIR
# INSTALL_DIR

echo "**************************************************************"
echo "Installing Quantum Software Development Kit ..."



# Check extra stuff
export PACKAGE_LIB_DIR=${INSTALL_DIR}/build

######################################################################################
echo ""
echo "Removing '${PACKAGE_LIB_DIR}' ..."
rm -rf ${PACKAGE_LIB_DIR}

######################################################################################
# Print info about possible issues
echo ""
echo "Note that you sometimes need to upgrade your pip to the latest version"
echo "to avoid well-known issues with user/system space installation:"

SUDO="sudo "
if [[ ${CK_PYTHON_PIP_BIN_FULL} == /home/* ]] ; then
  SUDO=""
fi

# Check if has --system option
${CK_PYTHON_PIP_BIN_FULL} install --help > tmp-pip-help.tmp
if grep -q "\-\-system" tmp-pip-help.tmp ; then
 SYS=" --system"
fi
rm -f tmp-pip-help.tmp

######################################################################################
echo "Compiling QISKIT SIMULATOR"
cd ${INSTALL_DIR}/src/src/qiskit-simulator/
make;

if [ "${?}" != "0" ] ; then
  echo "Error: installation failed!"
  exit 1
fi

cd ${INSTALL_DIR}/src

echo "Installing in" ${PACKAGE_LIB_DIR}
#sudo -H env CC=${CK_CXX} ${CK_PYTHON_BIN} -m pip install -r requirements.txt --prefix=${PROJECTQ_LIB_DIR}  -U --no-cache-dir
#-r requirements.txt
${CK_PYTHON_PIP_BIN_FULL} install --upgrade -r requirements.txt qiskit -t ${PACKAGE_LIB_DIR}
#${CK_PYTHON_PIP_BIN_FULL} install qiskit -t ${PACKAGE_LIB_DIR} 


if [ "${?}" != "0" ] ; then
  echo "Error: installation failed!"
  exit 1
fi
