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

    # This is where pip will install the modules.
    # It has its own funny structure we don't control :
    #
EXTRA_PYTHON_SITE=${INSTALL_DIR}/python_deps_site

    # This is the link that *will* be pointing at the directory with modules.
    # However, because we want to use asterisk expansion, we will create
    # the link itself *after* EXTRA_PYTHON_SITE has been already populated.
    #
export PACKAGE_LIB_DIR=${INSTALL_DIR}/build

######################################################################################
echo ""
echo "Removing '${EXTRA_PYTHON_SITE}' ..."
rm -rf ${EXTRA_PYTHON_SITE} ${PACKAGE_LIB_DIR}

######################################################################################
# Print info about possible issues
echo ""
echo "Note that you sometimes need to upgrade your pip to the latest version"
echo "to avoid well-known issues with user/system space installation:"

######################################################################################
echo "Compiling QISKit Simulator ..."

cd ${INSTALL_DIR}/src/src/qiskit-simulator/
make CC="${CK_CXX}" LIBS="${CK_COMPILER_OWN_LIB_LOC} -lpthread -llapack -lblas"

if [ "${?}" != "0" ] ; then
  echo "Error: installation failed!"
  exit 1
fi

######################################################################################
echo "Installing QISKit to '${PACKAGE_LIB_DIR}' ..."

cd ${INSTALL_DIR}/src

${CK_ENV_COMPILER_PYTHON_FILE} -m pip install -r requirements.txt qiskit --prefix=${EXTRA_PYTHON_SITE} --no-cache-dir # --ignore-installed

if [ "${?}" != "0" ] ; then
  echo "Error: installation failed!"
  exit 1
fi

    # In order for the asterisk to expand properly,
    # we have to do it AFTER the directory tree has been populated:
    #
ln -s $EXTRA_PYTHON_SITE/lib/python*/site-packages ${PACKAGE_LIB_DIR}
