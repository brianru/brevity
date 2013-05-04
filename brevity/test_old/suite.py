"""This file aggregates and runs all test scripts."""

import unittest
import unittestscript
import sample_docs.sample_docs_test as doc_suite

testloader = unittest.TestLoader()
suite = unittest.TestSuite()
suite.addTests((testloader.loadTestsFromModule(unittestscript),
               doc_suite.suite()))
unittest.TextTestRunner().run(suite)
