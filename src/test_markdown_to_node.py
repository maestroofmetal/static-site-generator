import unittest
from htmlnode import ParentNode
from textnode import TextNode, TextType
from markdown_to_html_node import markdown_to_html_node

class test_markdown_to_html_node(unittest.TestCase):

    def test_paragraph_block(self):
        markdown = "This is a paragraph."
        result = markdown_to_html_node(markdown)
        self.assertEqual(result.tag, "div")
        self.assertEqual(len(result.children), 1)
        self.assertEqual(result.children[0].tag, "p")
        self.assertEqual(result.children[0].children[0].value, "This is a paragraph.")

    def test_heading_block(self):
        markdown = "## A heading"
        result = markdown_to_html_node(markdown)
        heading_node = result.children[0]
        self.assertEqual(heading_node.tag, "h2")
        self.assertEqual(heading_node.children[0].value, "A heading")

    def test_code_block(self):
        markdown = "```\ndef hello():\n    return 'hello'\n```"
        result = markdown_to_html_node(markdown)
        pre = result.children[0]
        self.assertEqual(pre.tag, "pre")
        code = pre.children[0]
        self.assertEqual(code.tag, "code")
        self.assertEqual(code.children[0].value, "def hello():\n    return 'hello'\n")

    def test_quote_block(self):
        markdown = "> This is a quote\n> Still a quote"
        result = markdown_to_html_node(markdown)
        quote_node = result.children[0]
        self.assertEqual(quote_node.tag, "blockquote")
        self.assertEqual(quote_node.children[0].value, "This is a quote\nStill a quote")

    def test_unordered_list_block(self):
        markdown = "- Item one\n- Item two"
        result = markdown_to_html_node(markdown)
        ul = result.children[0]
        self.assertEqual(ul.tag, "ul")
        self.assertEqual(len(ul.children), 2)
        self.assertEqual(ul.children[0].tag, "li")
        self.assertEqual(ul.children[0].children[0].value, "Item one")
        self.assertEqual(ul.children[1].children[0].value, "Item two")

    def test_ordered_list_block(self):
        markdown = "1. First\n2. Second"
        result = markdown_to_html_node(markdown)
        ol = result.children[0]
        self.assertEqual(ol.tag, "ol")
        self.assertEqual(len(ol.children), 2)
        self.assertEqual(ol.children[0].tag, "li")
        self.assertEqual(ol.children[0].children[0].value, "First")
        self.assertEqual(ol.children[1].children[0].value, "Second")

    def test_mixed_blocks(self):
        markdown = "# Heading\n\nParagraph text.\n\n> Quote\n\n- List"
        result = markdown_to_html_node(markdown)
        tags = [child.tag for child in result.children]
        self.assertEqual(tags, ["h1", "p", "blockquote", "ul"])
        self.assertEqual(result.children[1].children[0].value, "Paragraph text.")
        self.assertEqual(result.children[2].children[0].value, "Quote")
        self.assertEqual(result.children[3].children[0].children[0].value, "List")
    
    def test_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here
    
    This is another paragraph with _italic_ text and `code` here
    
    """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )
        
    def test_lists(self):
        md = """
- This is a list
- with items
- and _more_ items

1. This is an `ordered` list
2. with items
3. and more items

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
        )

    def test_headings(self):
        md = """
# this is an h1

this is paragraph text

## this is an h2
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
        )
        
if __name__ == '__main__':
    unittest.main()