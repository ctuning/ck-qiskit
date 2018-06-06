import numpy as np
from scipy.optimize import minimize

import hackathon
# Total time to solution, with each run taking time t, with success probability s and desired success probability p
def ttot(t,s,p):
    R = np.ceil(np.log(1-p)/np.log(1-s))
    return t*R

# Total time to solution (as defined in ttot(t,s,p)), calculated from data and returning errors
def total_time(ts, n_succ, n_tot, p):
    if n_succ == 0:
        return tuple([*[np.nan]*4,0,0])
    t_ave = np.mean(ts)
    t_err = np.std(ts)/len(ts)**0.5       # Standard error for t
    if n_succ == n_tot:
        return t_ave,t_err,t_ave,t_err,1,0     # Always works so return time per run. Also prevents np.log(0) in code that follows.
    s = float(n_succ)/n_tot
    s_err = (s*(1-s)/float(n_tot))**0.5   # Standard error for s (using binomial dist)
    Tave = ttot(t_ave,s,p)
    T_serr = ttot(t_ave,s+s_err,p)
    Terr = (( T_serr - Tave)**2 + (t_err*Tave/float(t_ave)) ** 2 ) ** 0.5  # Error in total error assuming t and s independent
    return Tave, Terr, t_ave, t_err, s, s_err

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
    res = minimize(quantum_expectation, x0=np.array([1.3,2.7]), args=(samples), method='Nelder-Mead', options={'maxfev':200, 'xatol': 0.001, 'fatol': 0.001})
    out = res.fun
    n_samples = res.nfev * samples # We may need a more systematic method of calculating this

    ####### CUSTOM CODE BY PARTICIPANT ENDS HERE #######################
    return out, n_samples

# This function outputs the time to solution Tave, given the vqe_entry participant code, the known solution 'solution'
# of the problem (e.g. ground state), the required precision 'delta', and the desired probability of success 'p'
def benchmark_code(vqe_entry, N = 100, solution = 0., delta = 1e-1, p=0.95):
    n_succ = 0
    out_list = []
    n_samples_list = []
    for i in range(N):
        out, n_samples = vqe_entry()  # 'out' is the global minimum 'found' by the participant's code, 'n_samples' is the number of samples they used in total throughout the optimisation procedure
        if abs(out-solution) <= delta:
            n_succ += 1
        out_list.append(out)
        n_samples_list.append(n_samples)
    Tave, Terr, t_ave, t_err, s, s_err = total_time(n_samples_list, n_succ, N, p)
    # The key metric is is Tave (which has error +/- Terr to 1 stdev), but we'll return everything to be stored anyway
    return Tave, Terr, t_ave, t_err, s, s_err, out_list, n_samples_list

if __name__ == '__main__':
    print(hackathon.hello())
    print(hackathon.get_min_func_src_code())
    Tave, Terr, t_ave, t_err, s, s_err, out_list, n_samples_list = benchmark_code(vqe_entry)
    print('Time to solution: {:.0f} +/- {:.0f}'.format(Tave, Terr))

    # Uncomment this line to see what fraction were succesful
    # print('{:.3f} +/- {:.3f} \% of runs successful'.format(s*100,s_err*100))

    # Uncomment here to see what solutions were given
    # print('Solutions given were:')
    # print(out_list)
