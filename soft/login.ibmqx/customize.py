#
# Collective Knowledge (individual environment - setup)
#
# See CK LICENSE.txt for licensing details
# See CK COPYRIGHT.txt for copyright details
#

import os

##############################################################################

def version_cmd(i):

    # The concept of version is not generally applicable to credentials

    return {'return':0, 'cmd':'', 'version':'N/A'}

##############################################################################

def dirs(i):
    dirs    = i.get('dirs', [])

    # The concept of directories is not applicable to credentials

    return {'return':0, 'dirs':[]}

##############################################################################

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

    ck              = i['ck_kernel']

    ibmqx_api_key   = os.environ.get('IBMQX_API_KEY','')

    interactive     = i.get('interactive','')

    env             = i['env']                      # target structure to deposit the future environment variables

    if interactive and not ibmqx_api_key:
        kernel_ret = ck.inp({'text': 'Please enter your IBM QuantumExperience API key: '})
        if kernel_ret['return']:
            return kernel_ret
        else:
            ibmqx_api_key = kernel_ret['string']

    if ibmqx_api_key:
        env['CK_IBM_API_TOKEN'] = ibmqx_api_key
    else:
        return {'return':1, 'error':'Environment variable IBMQX_API_KEY should be set!'}

    return {'return':0, 'bat':''}

