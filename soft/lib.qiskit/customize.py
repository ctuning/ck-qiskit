#
# Collective Knowledge (individual environment - setup)
#
# See CK LICENSE.txt for licensing details
# See CK COPYRIGHT.txt for copyright details
#
# Author: Grigori Fursin, cTuning foundation/dividiti
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
    s=''

    iv=i.get('interactive','')

    cus=i.get('customize',{})
    fp=cus.get('full_path','')

    hosd=i['host_os_dict']
    tosd=i['target_os_dict']

    winh=hosd.get('windows_base','')

    ienv=cus.get('install_env',{})

    env=i['env']
    ep=cus['env_prefix']

    p1=os.path.dirname(fp)
    pl=os.path.dirname(p1)
    pi=os.path.dirname(pl)
    env[ep]=pi
    env[ep+'_LIB']=pi+'/'+ienv['PACKAGE_SUB_DIR1']
    ppath = pi+'/'+ienv['PACKAGE_SUB_DIR1']+"/"

   # spath = env['CK_ENV_LIB_QISKIT'] + '/src/src/qiskit-simulator/'
    spath = ppath+'out/'
    ## TO FIX for WIN 
    if winh=='yes':
        s+='\nset PYTHONPATH='+pl+';%PYTHONPATH%\n'
    else:
        s+='\nexport PYTHONPATH='+ppath+':${PYTHONPATH}\n'
        s+='\nexport CK_ENV_LIB_QISKIT_SIM='+spath+'\n'
    for k in ienv:
        if k.startswith('QISKIT_') or k=='CK_PYTHON_IPYTHON_BIN_FULL' or k=='CK_ENV_COMPILER_PYTHON_FILE':
           env[k]=ienv[k]
   
    return {'return':0, 'bat':s}
