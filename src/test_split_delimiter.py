import unittest
from textnode import TextNode, TextType
from split_delimiter import *

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
    
    def test_single_image_middle(self):
        nodes = [TextNode("This is an ![alt](url.png) example", TextType.TEXT)]
        result = split_nodes_image(nodes)
        expected = [
            TextNode("This is an ", TextType.TEXT),
            TextNode("alt", TextType.IMAGE, "url.png"),
            TextNode(" example", TextType.TEXT)
        ]
        self.assertEqual(result, expected)
        
    def test_single_image_only(self):
        nodes = [TextNode("![pic](img.jpg)", TextType.TEXT)]
        result = split_nodes_image(nodes)
        expected = [
            TextNode("pic", TextType.IMAGE, "img.jpg")
        ]
        self.assertEqual(result, expected)

    def test_multiple_images(self):
        nodes = [TextNode("Here ![one](1.png) and ![two](2.jpg)", TextType.TEXT)]
        result = split_nodes_image(nodes)
        expected = [
            TextNode("Here ", TextType.TEXT),
            TextNode("one", TextType.IMAGE, "1.png"),
            TextNode(" and ", TextType.TEXT),
            TextNode("two", TextType.IMAGE, "2.jpg")
        ]
        self.assertEqual(result, expected)

    def test_image_at_start(self):
        nodes = [TextNode("![start](start.jpg) then more text", TextType.TEXT)]
        result = split_nodes_image(nodes)
        expected = [
            TextNode("start", TextType.IMAGE, "start.jpg"),
            TextNode(" then more text", TextType.TEXT)
        ]
        self.assertEqual(result, expected)

    def test_image_at_end(self):
        nodes = [TextNode("Text before ![end](end.jpg)", TextType.TEXT)]
        result = split_nodes_image(nodes)
        expected = [
            TextNode("Text before ", TextType.TEXT),
            TextNode("end", TextType.IMAGE, "end.jpg")
        ]
        self.assertEqual(result, expected)

    def test_non_text_node_is_untouched(self):
        node = TextNode("![img](x.png)", TextType.LINK, "https://example.com")
        result = split_nodes_image([node])
        self.assertEqual(result, [node])  # Should not split non-TEXT nodes

    def test_malformed_markdown_ignored(self):
        text = "Broken image ![no close paren](url.jpg"
        result = split_nodes_image([TextNode(text, TextType.TEXT)])
        expected = [TextNode(text, TextType.TEXT)]
        self.assertEqual(result, expected)

    def test_no_image_markdown(self):
        text = "No images here"
        result = split_nodes_image([TextNode(text, TextType.TEXT)])
        expected = [TextNode(text, TextType.TEXT)]
        self.assertEqual(result, expected)
        
    def test_single_link_middle(self):
        nodes = [TextNode("Click [here](https://example.com) now", TextType.TEXT)]
        result = split_nodes_link(nodes)
        expected = [
            TextNode("Click ", TextType.TEXT),
            TextNode("here", TextType.LINK, "https://example.com"),
            TextNode(" now", TextType.TEXT)
        ]
        self.assertEqual(result, expected)

    def test_single_link_only(self):
        nodes = [TextNode("[link](https://a.com)", TextType.TEXT)]
        result = split_nodes_link(nodes)
        expected = [TextNode("link", TextType.LINK, "https://a.com")]
        self.assertEqual(result, expected)

    def test_multiple_links(self):
        nodes = [TextNode("Go to [Google](https://google.com) or [OpenAI](https://openai.com)", TextType.TEXT)]
        result = split_nodes_link(nodes)
        expected = [
            TextNode("Go to ", TextType.TEXT),
            TextNode("Google", TextType.LINK, "https://google.com"),
            TextNode(" or ", TextType.TEXT),
            TextNode("OpenAI", TextType.LINK, "https://openai.com")
        ]
        self.assertEqual(result, expected)

    def test_link_at_start(self):
        nodes = [TextNode("[Start](start.com) of sentence", TextType.TEXT)]
        result = split_nodes_link(nodes)
        expected = [
            TextNode("Start", TextType.LINK, "start.com"),
            TextNode(" of sentence", TextType.TEXT)
        ]
        self.assertEqual(result, expected)

    def test_link_at_end(self):
        nodes = [TextNode("Go here [end](end.com)", TextType.TEXT)]
        result = split_nodes_link(nodes)
        expected = [
            TextNode("Go here ", TextType.TEXT),
            TextNode("end", TextType.LINK, "end.com")
        ]
        self.assertEqual(result, expected)

    def test_non_text_node_untouched(self):
        node = TextNode("[link](x.com)", TextType.ITALIC)
        result = split_nodes_link([node])
        self.assertEqual(result, [node])  # Non-TEXT nodes should be returned unchanged

    def test_malformed_link_not_matched(self):
        nodes = [TextNode("Broken [link](missing", TextType.TEXT)]
        result = split_nodes_link(nodes)
        expected = [TextNode("Broken [link](missing", TextType.TEXT)]
        self.assertEqual(result, expected)

    def test_no_links(self):
        nodes = [TextNode("Just plain text.", TextType.TEXT)]
        result = split_nodes_link(nodes)
        expected = [TextNode("Just plain text.", TextType.TEXT)]
        self.assertEqual(result, expected)

    def test_link_with_text_before_and_after(self):
        nodes = [TextNode("Intro [link](link.com) outro", TextType.TEXT)]
        result = split_nodes_link(nodes)
        expected = [
            TextNode("Intro ", TextType.TEXT),
            TextNode("link", TextType.LINK, "link.com"),
            TextNode(" outro", TextType.TEXT)
        ]
        self.assertEqual(result, expected)

    # test block conversion
    
    class TestMarkdownToBlocks(unittest.TestCase):

        def test_single_block(self):
            self.assertEqual(markdown_to_blocks("Just one block."), ["Just one block."])

        def test_two_blocks(self):
            md = "First block.\n\nSecond block."
            expected = ["First block.", "Second block."]
            self.assertEqual(markdown_to_blocks(md), expected)

        def test_three_blocks_triple_newlines(self):
            md = "Block one.\n\n\nBlock two.\n\n\nBlock three."
            expected = ["Block one.", "Block two.", "Block three."]
            self.assertEqual(markdown_to_blocks(md), expected)

        def test_blank_lines_with_spaces(self):
            md = "Block A.\n \n\t\nBlock B."
            expected = ["Block A.", "Block B."]
            self.assertEqual(markdown_to_blocks(md), expected)

        def test_internal_line_breaks(self):
            md = "Line 1\nLine 2\n\nNext block"
            expected = ["Line 1\nLine 2", "Next block"]
            self.assertEqual(markdown_to_blocks(md), expected)

        def test_leading_and_trailing_whitespace(self):
            md = "   Trim me   \n\n  Me too  "
            expected = ["Trim me", "Me too"]
            self.assertEqual(markdown_to_blocks(md), expected)

        def test_empty_input(self):
            self.assertEqual(markdown_to_blocks(""), [])

        def test_only_blank_lines(self):
            md = "\n\n   \n\n"
            self.assertEqual(markdown_to_blocks(md), [])

        def test_one_real_block_between_blanks(self):
            md = "  \n\n  Real content  \n\n   "
            expected = ["Real content"]
            self.assertEqual(markdown_to_blocks(md), expected)

        def test_markdown_style_content(self):
            md = "# Heading\n\n- Bullet 1\n- Bullet 2\n\nFinal paragraph."
            expected = ["# Heading", "- Bullet 1\n- Bullet 2", "Final paragraph."]
            self.assertEqual(markdown_to_blocks(md), expected)
        
if __name__ == "__main__":
    unittest.main()