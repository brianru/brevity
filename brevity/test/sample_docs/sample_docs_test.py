import sys
sys.path.insert(0, '.')
import unittest
import brevity.application as br
import glob
import tempfile
import datetime


class ParametrizedTestCase(unittest.TestCase):
    """Try round-tripping every document in a test suite folder.
    Include XML -> TXT/MD/LaTeX -> XML
    and TXT/MD/LaTeX -> XML -> TXT/MD/LaTeX

    """
    def __init__(self, methodName='runTest', param=None):
        super(ParametrizedTestCase, self).__init__(methodName)
        print 'param: %s' % (param)
        self.param = param

    @staticmethod
    def parametrize(testcase_class, param=None):
        """Create a suite containing all tests taken from the given subclass, passing them the parameter 'param'.

        """
        testloader = unittest.TestLoader()
        print testloader.getTestCaseNames(testcase_class)
        testnames = testloader.getTestCaseNames(testcase_class)
        suite = unittest.TestSuite()
        for name in testnames:
            suite.addTest(testcase_class(name, param=param))
        return suite


class RoundTripXMLTest(ParametrizedTestCase):
    def setUp(self):
        self.im = br.Importer()
        self.ex = br.ExporterDirector()

    def testRoundTripXML(self):
        a = self.im.import_from_xml(self.param)
        b = self.ex.export_to_xml(a, tempfile.NamedTemporaryFile(delete=False))
        log = []
        counter = 0
        with open(self.param, 'r') as x:
            with b as y:
                # Logging to fix these errors. Assert does not use this code.
                y.seek(0)
                for (a, b) in zip(x.readlines(), y.readlines()):
                    counter += 1
                    if a != b:
                        log.append((counter, a, b))
                else:
                    with open('brevity/test/logs/%s.txt' % (datetime.datetime.now()), 'w') as f:
                        for (i, j, k) in log:
                            f.write('%s:\n%s\n%s\n' % (i, j[:-1], k[:-1]))
                y.seek(0)
                self.assertEqual(x.read(), y.read())


def suite():
    suite = unittest.TestSuite()
    xml_files = glob.glob('brevity/test/sample_docs/*.xml')
    for doc in xml_files:
        a = ParametrizedTestCase.parametrize(RoundTripXMLTest, param=doc)
        suite.addTest(a)
    return suite

if __name__ == "__main__":
    unittest.main()
