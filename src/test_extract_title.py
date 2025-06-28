import unittest
from generate_webpage import extract_title

class test_webpage_generation(unittest.TestCase):
   
    def test_proper_formatting(self):
        markdown = "# Hello"
        result = "Hello"
        self.assertEqual(extract_title(markdown),result)

    def test_improper_formatting(self):
        markdown = " \n # Hello"
        result = "Hello"
        self.assertEqual(extract_title(markdown), result)
    
    def test_really_fucked_up_formatting(self):
        markdown = " ** fi * \n afsdhiouafseopij \n\n # Hello"
        result = "Hello"
        self.assertEqual(extract_title(markdown), result)
        
    def test_no_header(self):
        markdown = "this isn't the header you're looking for"
        with self.assertRaises(Exception):
            extract_title(markdown)
if __name__ == '__main__':
    unittest.main()