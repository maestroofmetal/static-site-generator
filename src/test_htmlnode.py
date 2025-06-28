import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

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
        
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    
    def test_leaf_to_html_a(self):
        node = LeafNode("a", "www.google.com")
        self.assertEqual(node.to_html(), "<a>www.google.com</a>")
    
    def test_leaf_no_value(self):
        node = LeafNode("a",None)
        self.assertRaises(ValueError, node.to_html)
    
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
        
    def test_simple_parent_node(self):
        child = LeafNode("p", "Hello")
        parent = ParentNode("div", [child])
        expected_html = "<div><p>Hello</p></div>"
        self.assertEqual(parent.to_html(), expected_html)

    def test_parent_node_with_multiple_children(self):
        child1 = LeafNode("p", "Paragraph 1")
        child2 = LeafNode("p", "Paragraph 2")
        parent = ParentNode("section", [child1, child2])
        expected_html = "<section><p>Paragraph 1</p><p>Paragraph 2</p></section>"
        self.assertEqual(parent.to_html(), expected_html)

    def test_parent_node_with_props(self):
        child = LeafNode("span", "Text")
        parent = ParentNode("div", [child], props={"class": "container", "id": "main"})
        expected_html = '<div class="container" id="main"><span>Text</span></div>'
        self.assertEqual(parent.to_html(), expected_html)

    def test_nested_parent_nodes(self):
        inner_child = LeafNode("em", "italic")
        inner_parent = ParentNode("p", [inner_child])
        outer_parent = ParentNode("div", [inner_parent])
        expected_html = "<div><p><em>italic</em></p></div>"
        self.assertEqual(outer_parent.to_html(), expected_html)

    def test_parent_node_without_tag_raises_error(self):
        child = LeafNode("p", "Hello")
        with self.assertRaises(ValueError):
            ParentNode(None, [child]).to_html()

    def test_parent_node_with_none_children_raises_error(self):
        with self.assertRaises(ValueError):
            ParentNode("div", None).to_html()

if __name__ == "__main__":
    unittest.main()