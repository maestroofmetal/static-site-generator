import unittest
from html_converter import text_node_to_html_node
from textnode import TextType, TextNode

class test_html_converter(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    
    def test_bold(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold node")
        
    def test_italics(self):
        node = TextNode("This is an italics node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italics node")
        
    def test_code(self):
        node = TextNode("This is a code node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code node")
        
    def test_link(self):
        node = TextNode(None, TextType.LINK, "www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.props,{"href": "www.boot.dev"})
        
    def test_image(self):
        node = (TextNode("Shrek", TextType.IMAGE,
            "https://as2.ftcdn.net/jpg/05/59/91/77/1000_F_559917754_dPi14NuRWEofju2XA0Jz07kSITgjYYJm.jpg"))
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.props, {"src": "https://as2.ftcdn.net/jpg/05/59/91/77/1000_F_559917754_dPi14NuRWEofju2XA0Jz07kSITgjYYJm.jpg", "alt": "Shrek"})
        
    def test_none(self):
        node = TextNode("Nonetype exception",None)
        with self.assertRaises(Exception) as none_text:
           text_node_to_html_node(node)
        self.assertEqual(str(none_text.exception), "None text_type!")
    
    def test_catch_all(self):
        node = TextNode("This is for the catchall", "asdf")
        with self.assertRaises(Exception) as catch_all:
            text_node_to_html_node(node)
        self.assertEqual(str(catch_all.exception), "Unrecognized text_type!")