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

    # This is where pip2/pip3 will install the modules.
    # It has its own funny structure we don't control :
    #
PY_DEPS_TREE=${INSTALL_DIR}/py_deps

    # This is the link that *will* be pointing at the directory with modules.
    # However, because we want to use asterisk expansion, we will create
    # the link itself *after* PY_DEPS_TREE has been already populated.
    #
export PACKAGE_LIB_DIR=${INSTALL_DIR}/build

######################################################################################
echo ""
echo "Removing '${PY_DEPS_TREE}' ..."
rm -rf ${PY_DEPS_TREE} ${PACKAGE_LIB_DIR}

######################################################################################
# Print info about possible issues
echo ""
echo "Note that you sometimes need to upgrade your pip to the latest version"
echo "to avoid well-known issues with user/system space installation:"

######################################################################################
echo "Compiling QISKit Simulator ..."

cd ${INSTALL_DIR}/src/src/qiskit-simulator/
make CC=${CK_CXX} # CC=${CK_CXX_PATH_FOR_CMAKE}

if [ "${?}" != "0" ] ; then
  echo "Error: installation failed!"
  exit 1
fi

######################################################################################
echo "Installing QISKit to '${PACKAGE_LIB_DIR}' ..."

cd ${INSTALL_DIR}/src

#${CK_PYTHON_PIP_BIN_FULL} install --upgrade -r requirements.txt qiskit --prefix=${PY_DEPS_TREE}
${CK_PYTHON_BIN} -m pip install -r requirements.txt qiskit --prefix=${PY_DEPS_TREE} --no-cache-dir --ignore-installed

if [ "${?}" != "0" ] ; then
  echo "Error: installation failed!"
  exit 1
fi

    # In order for the asterisk to expand properly,
    # we have to do it AFTER the directory tree has been populated:
    #
ln -s $PY_DEPS_TREE/lib/python*/site-packages ${PACKAGE_LIB_DIR}
