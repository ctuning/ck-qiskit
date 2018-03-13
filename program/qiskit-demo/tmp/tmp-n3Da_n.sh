#! /bin/bash


export PATH=/home/flavio/CK_REPOS/ck-env/platform.init/generic-linux:$PATH


. /home/flavio/CK_REPOS/local/env/984773850e8364e6/env.sh
. /home/flavio/CK_REPOS/local/env/45e24744419974be/env.sh

export CK_IBM_BACKEND=ibmqx_qasm_simulator
export CK_IBM_REPETITION=1
export CK_IBM_TIMEOUT=1200
export CK_IBM_VERBOSE=1


echo    executing code ...
 ${CK_ENV_COMPILER_PYTHON_FILE} ../teleport.py > tmp-stdout.tmp 2> tmp-stderr.tmp
