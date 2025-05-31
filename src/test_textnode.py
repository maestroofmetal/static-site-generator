import unittest
from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a different text node", TextType.BOLD)
        self.assertNotEqual(node, node2)
        
    def test_type_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)
        
    def test_first_url_blank(self):
        node = TextNode("This is a link node without a url", TextType.LINK, None)
        node2 = TextNode("This node has a url", TextType.LINK,"www.google.com")
        self.assertNotEqual(node, node2)
        
    def test_urls_match(self):
        node = TextNode("This is a url", TextType.LINK,"www.bootdev.com")
        node2 = TextNode("This is a url", TextType.LINK,"www.bootdev.com")
        self.assertEqual(node,node2)
        
    def test_urls_dont_match(self):
        node = TextNode("This is a url", TextType.LINK,"www.bootdev.com")
        node2 = TextNode("This is a url", TextType.LINK,"www.google.com")
        self.assertNotEqual(node,node2)
        
if __name__ == "__main__":
    unittest.main()