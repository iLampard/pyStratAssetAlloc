# -*- coding: utf-8 -*-

import os
import sys
import unittest

import pyStratAssetAlloc.test.strat.alloc as alloc
import pyStratAssetAlloc.test.strat.timing as timing

thisFilePath = os.path.abspath(__file__)

sys.path.append(os.path.sep.join(thisFilePath.split(os.path.sep)[:-2]))


def test():
    print('Python ' + sys.version)
    suite = unittest.TestSuite()

    tests = unittest.TestLoader().loadTestsFromTestCase(alloc.Test_Risk_Parity)
    suite.addTests(tests)
    tests = unittest.TestLoader().loadTestsFromTestCase(timing.Test_GF_MA)
    suite.addTests(tests)
    tests = unittest.TestLoader().loadTestsFromTestCase(timing.Test_GF_LLT)
    suite.addTests(tests)
    tests = unittest.TestLoader().loadTestsFromTestCase(timing.Test_GX_RPS)
    suite.addTests(tests)


    res = unittest.TextTestRunner(verbosity=3).run(suite)
    if len(res.errors) >= 1 or len(res.failures) >= 1:
        sys.exit(-1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    test()
