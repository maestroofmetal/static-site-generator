import unittest
from textnode import TextNode, TextType
from split_delimiter import split_nodes_delimiter, extract_markdown_images, extract_markdown_links

class TestSplitNodesDelimiter(unittest.TestCase):

    def test_no_delimiter_text_node(self):
        nodes = [TextNode("This is plain text", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        expected = [TextNode("This is plain text", TextType.TEXT)]
        self.assertEqual(result, expected)

    def test_even_delimiters_raises_exception(self):
        nodes = [TextNode("This **text** has **bad** markdown **", TextType.TEXT)]
        with self.assertRaises(Exception) as context:
            split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertIn("Invalid Markdown syntax", str(context.exception))

    def test_single_bold_split(self):
        nodes = [TextNode("This is **bold** text", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT)
        ]
        self.assertEqual(result, expected)

    def test_multiple_bold_splits(self):
        nodes = [TextNode("**Bold1** and **Bold2**", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        expected = [
            TextNode("", TextType.TEXT),
            TextNode("Bold1", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("Bold2", TextType.BOLD),
            TextNode("", TextType.TEXT)
        ]
        self.assertEqual(result, expected)

    def test_mixed_text_types_are_unchanged(self):
        nodes = [
            TextNode("Normal", TextType.TEXT),
            TextNode("Bold", TextType.BOLD),
            TextNode("Italic", TextType.ITALIC)
        ]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        expected = nodes  # Only TEXT type is split; others are untouched
        self.assertEqual(result, expected)

    def test_italic_split(self):
        nodes = [TextNode("This *is* italic", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
        expected = [
            TextNode("This ", TextType.TEXT),
            TextNode("is", TextType.ITALIC),
            TextNode(" italic", TextType.TEXT)
        ]
        self.assertEqual(result, expected)
    
    def test_code_split(self):
        nodes = [TextNode("This `is` code", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "`", TextType.CODE)
        expected = [
            TextNode("This ", TextType.TEXT),
            TextNode("is", TextType.CODE),
            TextNode(" code", TextType.TEXT)
        ]
        self.assertEqual(result, expected)
        
    def test_text_type_not_text(self):
        nodes = [TextNode("This should add directly", TextType.CODE)]
        result = split_nodes_delimiter(nodes, "`", TextType.CODE)
        expected = [TextNode("This should add directly", TextType.CODE)]
        self.assertEqual(result, expected)
        
    def test_empty_text(self):
        nodes = [TextNode("", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        expected = [TextNode("",TextType.TEXT)]
        self.assertEqual(result, expected)
    
    def test_no_whitespace(self):
        nodes = [TextNode("**bold text**", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        expected  = [TextNode("", TextType.TEXT),
                     TextNode("bold text", TextType.BOLD),
                     TextNode("",TextType.TEXT)]
        self.assertEqual(result, expected)
    
    def test_adjacent_delimiters(self):
        nodes = [TextNode("****unbolded****", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        expected = [TextNode("", TextType.TEXT),
                    TextNode("", TextType.BOLD),
                    TextNode("unbolded", TextType.TEXT),
                    TextNode("",TextType.BOLD),
                    TextNode("", TextType.TEXT)]
        self.assertEqual(result, expected)
        
    def test_just_one_delimiter(self):
        nodes = [TextNode("**", TextType.TEXT)]
        with self.assertRaises(Exception):
            TextNode.split_nodes_delimiter(nodes, "**", TextType.BOLD)
    
    def test_extract_single_image(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    
    def test_extract_single_link(self):
        matches = extract_markdown_links(
            "Check [Google](https://google.com)"
        )
        self.assertListEqual([("Google", "https://google.com")], matches)
        
    def test_no_images(self):
        matches = extract_markdown_images("No memes for you.")
        self.assertListEqual([], matches)
    
    def test_no_links(self):
        matches = extract_markdown_links("No links here.")
        self.assertListEqual([], matches)
        
    def test_multiple_images(self):
        matches = extract_markdown_images(
            "![image 1](https://i.imgur.com/zjjcJKZ.png) and ![image 2](https://i.imgur.com/zjjcJKZ.png)"
            )
        self.assertListEqual([
            ("image 1", "https://i.imgur.com/zjjcJKZ.png"),
                              ("image 2", "https://i.imgur.com/zjjcJKZ.png")]
                             , matches)
    
    def test_extract_multiple_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)")
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)
        
if __name__ == "__main__":
    unittest.main()