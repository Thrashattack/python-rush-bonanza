import unittest
from src.spec.core.slots.MonteCarloTest import MonteCarloTest


def suite():
    suite = unittest.TestSuite()
    suite.addTest(MonteCarloTest('test_rtp'))
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite())