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
echo ""

    # This is where pip will install the modules.
    # It has its own funny structure we don't control :
    #
EXTRA_PYTHON_SITE=${INSTALL_DIR}/python_deps_site

SHORT_PYTHON_VERSION=`${CK_ENV_COMPILER_PYTHON_FILE} -c 'import sys;print(sys.version[:3])'`
export PACKAGE_LIB_DIR="${EXTRA_PYTHON_SITE}/lib/python${SHORT_PYTHON_VERSION}/site-packages"
export PYTHONPATH=$PACKAGE_LIB_DIR:$PYTHONPATH

######################################################################################
echo "Removing '${EXTRA_PYTHON_SITE}' and the symbolic link ..."

rm -rf ${EXTRA_PYTHON_SITE} ${INSTALL_DIR}/build

######################################################################################
echo "Compiling QISKit Simulator ..."

cd ${INSTALL_DIR}/src/src/qasm-simulator-cpp
make CC="${CK_CXX}" LIBS="${CK_COMPILER_OWN_LIB_LOC} -lpthread -llapack -lblas"

if [ "${?}" != "0" ] ; then
  echo "Error: installation failed!"
  exit 1
fi

######################################################################################
echo "Installing QISKit to '${EXTRA_PYTHON_SITE}' ..."

cd ${INSTALL_DIR}/src

${CK_ENV_COMPILER_PYTHON_FILE} -m pip install -r requirements.txt qiskit --prefix=${EXTRA_PYTHON_SITE} --ignore-installed

if [ "${?}" != "0" ] ; then
  echo "Error: installation failed!"
  exit 1
fi

    # Because we have to provide a fixed name via meta.json ,
    # and $PACKAGE_LIB_DIR depends on the Python version,
    # we solve it by creating a symbolic link with a fixed name.
    #
ln -s $PACKAGE_LIB_DIR ${INSTALL_DIR}/build
