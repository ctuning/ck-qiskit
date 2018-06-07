import numpy as np
from scipy.optimize import minimize


from hackathon import optimizers as optimizers
from hackathon import utils as utils
import json
import os
import re



# Fake quantum computer output function. Just a noisy 2D parabola with global minimum of zero at zero.
def quantum_expectation(params,samples):
    a0 = params[0]
    a1 = params[1]
    f = a0**2 + a1**2 + np.random.normal(0,1./samples**0.5)
    return f

def vqe_entry():
    ##### THIS IS THE CUSTOM CODE TO BE WRITTEN BY THE PARTICIPANT ########

    samples = 10000 # The participant decides to use this many samples for all iterations of the minimiser
    # I've used numpy 'minimize' here but this can be completely custom! TODO: add simulated annealing example
    res =  optimizers.my_nelder_mead(quantum_expectation, x0=np.array([1.3,2.7]), my_args=(samples), my_options={'maxfev':200, 'xatol': 0.001, 'fatol': 0.001})
    out = res.fun
    n_samples = res.nfev * samples # We may need a more systematic method of calculating this

    ####### CUSTOM CODE BY PARTICIPANT ENDS HERE #######################
    return out, n_samples

# This function outputs the time to solution Tave, given the vqe_entry participant code, the known solution 'solution'
# of the problem (e.g. ground state), the required precision 'delta', and the desired probability of success 'p'

if __name__ == '__main__':
    #print(hackathon.hello())
    Tave, Terr, t_ave, t_err, s, s_err, out_list, n_samples_list = utils.benchmark_code(vqe_entry)
    #print('Time to solution: {:.0f} +/- {:.0f}'.format(Tave, Terr))


    # Wrting output ... Move on hackahton.write_output? 
    output = {"program": utils.get_min_func_src_code(), "Tave":Tave, "Terr":Terr}
    with open('tmp-ck-output.json', 'w') as f:
             json.dump(output, f, ensure_ascii=False)
    # Uncomment this line to see what fraction were succesful
    # print('{:.3f} +/- {:.3f} \% of runs successful'.format(s*100,s_err*100))

    # Uncomment here to see what solutions were given
    # print('Solutions given were:')
    # print(out_list)
