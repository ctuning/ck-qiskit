#
# Collective Knowledge (individual environment - setup)
#
# See CK LICENSE.txt for licensing details
# See CK COPYRIGHT.txt for copyright details
#
# Author(s):
# - Grigori Fursin, cTuning foundation/dividiti
# - Flavio Vella, dividiti
# - Anton Lokhmotov, dividiti
#

import os

##############################################################################
# setup environment setup

def setup(i):
    """
    Input:  {
              cfg              - meta of this soft entry
              self_cfg         - meta of module soft
              ck_kernel        - import CK kernel module (to reuse functions)

              host_os_uoa      - host OS UOA
              host_os_uid      - host OS UID
              host_os_dict     - host OS meta

              target_os_uoa    - target OS UOA
              target_os_uid    - target OS UID
              target_os_dict   - target OS meta

              target_device_id - target device ID (if via ADB)

              tags             - list of tags used to search this entry

              env              - updated environment vars from meta
              customize        - updated customize vars from meta

              deps             - resolved dependencies for this soft

              interactive      - if 'yes', can ask questions, otherwise quiet
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0

              bat          - prepared string for bat file
            }

    """

    import os

    # Get variables
    ck=i['ck_kernel']

    iv=i.get('interactive','')

    cus=i.get('customize',{})
    fp=cus.get('full_path','')

    hosd=i['host_os_dict']
    tosd=i['target_os_dict']

    winh    = hosd.get('windows_base','')
    macos   = hosd.get('macos','')

    ienv=cus.get('install_env',{})

    env=i['env']
    ep=cus['env_prefix']

    p1=os.path.dirname(fp)
    pl=os.path.dirname(p1)
    pi=os.path.dirname(pl)
    env[ep]=pi
    ppath=os.path.join(pi, ienv['PACKAGE_SUB_DIR1'])
    env[ep+'_LIB']=ppath

    pil_dlibs_path = os.path.join(ppath, 'PIL', '.dylibs')

    # Using a generic script to prepend the library search path
    # with the value expected to be set in $CK_ENV_COMPILER_GCC_LIB .
    #
    # GCC's dynamic library is an implicit dependency of Python's scipy package.
    # If this library is not found, dlopen() call buried deep in scipy library
    # fails to import ___addtf3 symbol.
    #
    # See this discussion:
    #   https://github.com/citwild/laugh-finder/issues/11#issuecomment-377997186
    #
    lib_path_adict = { 'action': 'lib_path_export_script',
                       'module_uoa': 'os',
                       'host_os_dict': hosd,
                       'lib_path': [ '$CK_ENV_COMPILER_GCC_LIB' ],
    }

    if not winh:
        pil_extra_dynamic_path = os.path.join(ppath, 'PIL', '.dylibs' if macos else '.libs')
        lib_path_adict['lib_path'].insert(0, pil_extra_dynamic_path)

    r = ck.access( lib_path_adict )
    if r['return']>0: return r
    shell_setup_script_contents = r['script']

    # FIXME: Fix for Windows.
    # FIXME: Should have no explicit exports.
    if winh=='yes':
        shell_setup_script_contents += '\nset PYTHONPATH='+pl+';%PYTHONPATH%\n'
    else:
        shell_setup_script_contents += '\nexport PYTHONPATH='+ppath+':${PYTHONPATH}\n'
        spath=os.path.join(ppath, 'out', 'qiskit_simulator')
        shell_setup_script_contents += '\nexport CK_ENV_LIB_QISKIT_SIM='+spath+'\n'

    for k in ienv:
        if k.startswith('QISKIT_') or k=='CK_PYTHON_IPYTHON_BIN_FULL' or k=='CK_ENV_COMPILER_PYTHON_FILE':
           env[k]=ienv[k]
   
    return {'return':0, 'bat':shell_setup_script_contents}
