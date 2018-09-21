#!/usr/bin/env python3

"""
This example runs a battery of unittests against the remote ibmq_qasm_simulator

## Running this script using the "lightweight" CK infrastructure to import Qiskit library:
    ck virtual `ck search env:* --tags=qiskit,lib`  `ck search env:* --tags=ibmqx,login` --shell_cmd=unittests.py

"""

# pylint: disable=C0103
'''
Unit Test
'''

import sys
import unittest
# pylint: disable=W0403
from Qconfig import API_TOKEN
sys.path.append('IBMQuantumExperience')
sys.path.append('../IBMQuantumExperience')

from IBMQuantumExperience import IBMQuantumExperience  # noqa
from IBMQuantumExperience import ApiError  # noqa
from IBMQuantumExperience import BadBackendError  # noqa


class TestQX(unittest.TestCase):
    '''
    Class with the unit tests
    '''

    def setUp(self):
        self.api = IBMQuantumExperience(API_TOKEN)
        self.qasm = """IBMQASM 2.0;

include "qelib1.inc";
qreg q[5];
creg c[5];
u2(-4*pi/3,2*pi) q[0];
u2(-3*pi/2,2*pi) q[0];
u3(-pi,0,-pi) q[0];
u3(-pi,0,-pi/2) q[0];
u2(pi,-pi/2) q[0];
u3(-pi,0,-pi/2) q[0];
measure q -> c;
"""

        self.qasms = [{"qasm": self.qasm},
                      {"qasm": """IBMQASM 2.0;

include "qelib1.inc";
qreg q[5];
creg c[3];
creg f[2];
x q[0];
measure q[0] -> c[0];
measure q[2] -> f[0];
"""}]

    def tearDown(self):
        pass

    # ---------------------------------
    #        TESTS
    # ----------------------------------

    def test_api_auth_token(self):
        '''
        Authentication with Quantum Experience Platform
        '''
        credential = self.api.check_credentials()
        self.assertTrue(credential)

    def test_api_get_my_credits(self):
        '''
        Check the credits of the user
        '''
        my_credits = self.api.get_my_credits()
        check_credits = None
        if 'remaining' in my_credits:
            check_credits = my_credits['remaining']
        self.assertIsNotNone(check_credits)

    def test_api_auth_token_fail(self):
        '''
        Authentication with Quantum Experience Platform
        '''
        self.assertRaises(ApiError,
                          IBMQuantumExperience, 'fail')

    def test_api_last_codes(self):
        '''
        Check last code by user authenticated
        '''
        self.assertIsNotNone(self.api.get_last_codes())

    def test_api_run_experiment(self):
        '''
        Check run an experiment by user authenticated
        '''
        backend = self.api.available_backend_simulators()[0]['name']
        backend = "ibmq_qasm_simulator" 
        shots = 1
        experiment = self.api.run_experiment(self.qasm, backend, shots)
        check_status = None
        if 'status' in experiment:
            check_status = experiment['status']
        self.assertIsNotNone(check_status)



    def test_api_run_experiment_fail_backend(self):
        '''
        Check run an experiment by user authenticated is not run because the
        backend does not exist
        '''
        backend = '5qreal'
        shots = 1
        self.assertRaises(BadBackendError,
                          self.api.run_experiment, self.qasm, backend, shots)

    def test_api_run_job(self):
        '''
        Check run an job by user authenticated
        '''
        backend = 'ibmq_qasm_simulator'
        shots = 1
        job = self.api.run_job(self.qasms, backend, shots)
        check_status = None
        if 'status' in job:
            check_status = job['status']
        self.assertIsNotNone(check_status)

    def test_api_run_job_fail_backend(self):
        '''
        Check run an job by user authenticated is not run because the backend
        does not exist
        '''
        backend = 'real5'
        shots = 1
        self.assertRaises(BadBackendError, self.api.run_job, self.qasms,
                          backend, shots)

    def test_api_get_jobs(self):
        '''
        Check get jobs by user authenticated
        '''
        jobs = self.api.get_jobs(2)
        self.assertEqual(len(jobs), 2)

    def test_api_backend_status(self):
        '''
        Check the status of a real chip
        '''
        is_available = self.api.backend_status()
        self.assertIsNotNone(is_available['available'])

    def test_api_backend_calibration(self):
        '''
        Check the calibration of a real chip
        '''
        calibration = self.api.backend_calibration()
        self.assertIsNotNone(calibration)

    def test_api_backend_parameters(self):
        '''
        Check the parameters of calibration of a real chip
        '''
        parameters = self.api.backend_parameters()
        self.assertIsNotNone(parameters)

    def test_api_backends_availables(self):
        '''
        Check the backends availables
        '''
        backends = self.api.available_backends()
        self.assertGreaterEqual(len(backends), 2)

    def test_api_backend_simulators_available(self):
        '''
        Check the backend simulators available
        '''
        backends = self.api.available_backend_simulators()
        self.assertGreaterEqual(len(backends), 1)

    def test_qx_api_version(self):
        '''
        Check the version of the QX API
        '''
        version = self.api.api_version()
        self.assertGreaterEqual(int(version.split(".")[0]), 4)


class TestAuthentication(unittest.TestCase):
    """
    Tests for the authentication features. These tests are in a separate
    TestCase as they need to control the instantiation of
    `IBMQuantumExperience` directly.
    """
    def test_url_404(self):
        with self.assertRaises(ApiError):
            api = IBMQuantumExperience(
                API_TOKEN,
                config={'url': 'https://qcwi-lsf.mybluemix.net/api/API_TEST'})

    def test_invalid_token(self):
        with self.assertRaises(ApiError):
            api = IBMQuantumExperience('INVALID_TOKEN')

    def test_url_unreachable(self):
        with self.assertRaises(ApiError):
            api = IBMQuantumExperience(
                API_TOKEN, config={'url': 'INVALID_URL'})



if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestQX)
    unittest.TextTestRunner(verbosity=2).run(suite)
