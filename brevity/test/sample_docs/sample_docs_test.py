import sys
sys.path.insert(0, '.')
import unittest
import brevity.application as br
import glob
import tempfile


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
        testnames = testloader.getTestCaseNames(testcase_class)
        suite = unittest.TestSuite()
        for name in testnames:
            suite.addTest(testcase_class(name, param=param))


class RoundTripXMLTest(ParametrizedTestCase):
    def setUp(self):
        self.im = br.Importer()
        self.ex = br.ExporterDirector()

    def runTest(self):  # separate into multiple lines
        print self.param
        a = self.im.import_from_xml(self.param)
        b = self.ex.export_to_xml(a, tempfile.TemporaryFile())
        with open(self.param, 'r') as x:
            with open(b, 'r') as y:
                self.assertEqual(x, y)

suite = unittest.TestSuite()
xml_files = glob.glob('*.xml')
for doc in xml_files:
    suite.addTest(ParametrizedTestCase.parametrize(RoundTripXMLTest, 'brevity/test/sample_docs/' + doc))

if __name__ == "__main__":
    unittest.main()
