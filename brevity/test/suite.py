"""This file aggregates and runs all test scripts."""

import unittest
import unittestscript
import samples_docs.samples_docs_test

suite = unittest.TestLoader()
suite = suite.loadTestsFromNames(unittestscript,
                                 samples_docs.samples_docs_test)
unittest.TextTestRunner().run(suite)
