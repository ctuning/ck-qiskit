import numpy as np
from scipy import linalg as la
from scipy.optimize import minimize
# importing the QISKit
from qiskit import QuantumProgram
import Qconfig

# import optimization tools
from qiskit.tools.apps.optimization import trial_circuit_ryrz
from qiskit.tools.apps.optimization import Hamiltonian_from_file, make_Hamiltonian
from qiskit.tools.apps.optimization import eval_hamiltonian, group_paulis


from hackathon import optimizers as optimizers
from hackathon import utils as utils
import json
import os,sys
import warnings



# Optimization
def objective_function(theta, shots):
    return eval_hamiltonian(Q_program, pauli_list_grouped, trial_circuit_ryrz(n, m, theta, entangler_map, None, False), shots,
                            device).real


def vqe_entry(vqe_opt):
    ##### THIS IS THE CUSTOM CODE TO BE WRITTEN BY THE PARTICIPANT ########
    samples = vqe_opt['shot'] # The participant decides to use this many samples for all iterations of the minimiser
    # I've used numpy 'minimize' here but this can be completely custom! TODO: add simulated annealing example
    res =  optimizers.my_nelder_mead(objective_function, x0=vqe_opt['x0'], my_args=(samples), my_options=vqe_opt['options'])
#    print(res)    
    out = res['fun']
    n_samples = res['nfev'] * samples # We may need a more systematic method of calculating this

    ####### CUSTOM CODE BY PARTICIPANT ENDS HERE #######################
    return out, n_samples

# This function outputs the time to solution Tave, given the vqe_entry participant code, the known solution 'solution'
# of the problem (e.g. ground state), the required precision 'delta', and the desired probability of success 'p'

if __name__ == '__main__':
    # Ignore warnings due to chopping of small imaginary part of the energy
    warnings.filterwarnings('ignore')

    Q_program = QuantumProgram()
    try:
        Q_program.set_api(Qconfig.APItoken, Qconfig.config["url"], verify=True, hub=Qconfig.config["hub"], group=Qconfig.config["group"], project=Qconfig.config["project"])

    except:
        offline = True
        print("""WARNING: There's no connection with IBMQuantumExperience servers.
             cannot test I/O intesive tasks, will only test CPU intensive tasks
             running the jobs in the local simulator""")
                                                            
    # Initialise quantum program
    Q_program = QuantumProgram()
    Q_program.set_api(Qconfig.APItoken, Qconfig.config["url"])

    # Device selection Similuator or IBMQ. The code gets the available backends and check if your choice is in. 
    device = 'local_qasm_simulator'
    if 'CK_IBM_BACKEND' in os.environ: 
        device = os.environ['CK_IBM_BACKEND']
    
    # Specify if you want to use or your own minimizer either an existing method
    available_backends = Q_program.available_backends()
    print(device)
    print(available_backends)
    if device not in available_backends:
        print("The backends available for use are: {}\n".format(",".join(available_backends)))

        sys.exit() 
    else: 
        print(device) 

    # Application specific part

    # Import hamiltonian for H2 from file
    ham_name = '../H2Equilibrium.txt'
    pauli_list = Hamiltonian_from_file(ham_name)

    # Calculate Exact Energy classically, to compare with quantum solution
    H = make_Hamiltonian(pauli_list)
    exact = np.amin(la.eigh(H)[0])
    print('The exact ground state energy is: {:.4f}'.format(exact))

    # Parameters. To set via CK
    shots = 10 # Number of shots
    if 'CK_IBM_SHOT' in os.environ:
         shots = int(os.environ['CK_IBM_SHOTS'])
    tout = 1200
    if 'CK_IBM_TIMEOUT' in os.environ:
         tout = int(os.environ['CK_IBM_TIMEOUT'])

    N = 10
    if 'CK_SAMPLES' in os.environ:
         N = int(os.environ['CK_SAMPLES'])
    n = 2   # Number of qubits
    m = 6   # Depth of circuit
   
    entangler_map = {1: [0]}  # Which qubits to use (0 to 1 best to avoid qiskit bug
    pauli_list_grouped = group_paulis(pauli_list)
     
    initial_theta = np.random.randn(2 * n * m)    

    #  Initial objective function value
    initial_out = objective_function(initial_theta,shots)



    # N is the number of solutions 
    # solution is exact computed before 
    # delta is the tollerance 
    # probability 

    solution = exact 
    delta = 1e-1
    if 'CK_DELTA' in os.environ:
         delta = int(os.environ['CK_DELTA'])
    p = 10 # Prob
    if 'CK_PROBABILITY' in os.environ:
         p = int(os.environ['CK_PROBABILITY'])
    vqe_opt = {'shot': shots, 'x0':initial_theta, 'method':'Neder-Mead', 'options':{'maxfev':2, 'xatol': 0.001, 'fatol': 0.001} }
    Tave, Terr, t_ave, t_err, s, s_err, out_list, n_samples_list = utils.benchmark_code(vqe_entry, N, solution, delta, p, vqe_opt)
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
