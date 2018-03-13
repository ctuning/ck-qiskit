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
echo "Compiling QISKit Simulator ..."
cd ${INSTALL_DIR}/src/src/qiskit-simulator/
make # CC=${CK_CC_PATH_FOR_CMAKE} CXX=${CK_CXX_PATH_FOR_CMAKE}

if [ "${?}" != "0" ] ; then
  echo "Error: installation failed!"
  exit 1
fi

######################################################################################
echo "Installing QISKit to '${PACKAGE_LIB_DIR}' ..."

cd ${INSTALL_DIR}/src
#sudo -H env CC=${CK_CXX} ${CK_PYTHON_BIN} -m pip install -r requirements.txt --prefix=${PROJECTQ_LIB_DIR}  -U --no-cache-dir
${CK_PYTHON_PIP_BIN_FULL} install --upgrade -r requirements.txt qiskit -t ${PACKAGE_LIB_DIR}
#${CK_PYTHON_PIP_BIN_FULL} install qiskit -t ${PACKAGE_LIB_DIR} 

if [ "${?}" != "0" ] ; then
  echo "Error: installation failed!"
  exit 1
fi
