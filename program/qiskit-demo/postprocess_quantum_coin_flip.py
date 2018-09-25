#
# Convert raw output to the CK format.
#
# Developer(s):
#   - Anton Lokhmotov, dividiti, 2018
#

import json
import os
import re
import sys

def ck_postprocess(i):
    ck=i['ck_kernel']
    rt=i['run_time']
    deps=i['deps']
    env=i.get('env',{})

    d={}
    d['env'] = env

    # Load stdout.
    lst=[]
    stdout=rt['run_cmd_out1']
    if os.path.isfile(stdout):
       r=ck.load_text_file({'text_file':stdout,'split_to_list':'yes'})
       if r['return']>0: return r
       lst=r['lst']

    backends_prefix = 'The backends available for use are: '
    save_next_line_to_json = False
    for line in lst:
        if save_next_line_to_json:
            d['output'] = json.loads(line.replace('\'','"'))
            d['post_processed']='yes'
            break
        if line.startswith(backends_prefix):
            d['available_backends'] = json.loads(line[len(backends_prefix):].replace('\'','"'))
        if line.startswith('COMPLETED'):
            save_next_line_to_json = True

    #TODO: get email.
    #d['CK_IBM_API_EMAIL']=env.get('CK_IBM_API_EMAIL','')

    rr={}
    rr['return']=0
    if d.get('post_processed','')=='yes':
        # Save to file.
        r=ck.save_json_to_file({'json_file':'tmp-ck-timer.json', 'dict':d})
        if r['return']>0: return r
    else:
        rr['return']=1
        rr['error']='failed to parse output'

    return rr

# Do not add anything here!
