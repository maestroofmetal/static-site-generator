import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("h1","Header Text",None,None)
        node2 = HTMLNode("h1","Header Text",None,None)
        self.assertEqual(node, node2)
        
    def test_ne(self):
        node = HTMLNode("h1","Header Text",None,None)
        node2 = HTMLNode("a","link", None, {"href": "https://bootdev.com"})
        self.assertNotEqual(node, node2)
        
    def test_repr_eq(self):
        node = HTMLNode("a","Link",None,{"href": "https://bootdev.com"})
        node2 = HTMLNode("a","Link",None,{"href": "https://bootdev.com"})
        self.assertEqual(node.__repr__(),node2.__repr__())
    
    def test_repr_ne(self):
        node = HTMLNode("h1","Header Text",None,None)
        node2 = HTMLNode("a","link", None, {"href": "https://bootdev.com"})
        self.assertNotEqual(node.__repr__(),node2.__repr__())
    
    def test_props_to_html_output(self):
        node = HTMLNode("a","link",None,{
        "href": "https://www.google.com",
        "target": "_blank",
        })
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')
        
    def test_to_html_props(self):
        node = HTMLNode(
            "div",
            "Hello, world!",
            None,
            {"class": "greeting", "href": "https://boot.dev"},
        )
        self.assertEqual(
            node.props_to_html(),
            ' class="greeting" href="https://boot.dev"',
        )

    def test_values(self):
        node = HTMLNode(
            "div",
            "I wish I could read",
        )
        self.assertEqual(
            node.tag,
            "div",
        )
        self.assertEqual(
            node.value,
            "I wish I could read",
        )
        self.assertEqual(
            node.children,
            None,
        )
        self.assertEqual(
            node.props,
            None,
        )

if __name__ == "__main__":
    unittest.main()