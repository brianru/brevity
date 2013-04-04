import unittest
import application as br
import glob
import tempfile


class RoundTripXMLTestCase(unittest.TestCase):
    """Try round-tripping every document in a test suite folder.
    Include XML -> TXT/MD/LaTeX -> XML
    and TXT/MD/LaTeX -> XML -> TXT/MD/LaTeX

    """
    def setUp(self):
        self.xml_files = glob.glob('samples/*.xml')
        self.im = br.Importer()
        self.ex = br.ExporterDirector()
        for doc in self.xml_files:
            self.runTest(doc)

    def runTest(self, doc):
        self.assertEqual(doc,
                         self.ex.export_to_xml(self.im.import_from_xml(doc),
                                               tempfile.TemporaryFile()))


if __name__ == "__main__":
    unittest.main()
