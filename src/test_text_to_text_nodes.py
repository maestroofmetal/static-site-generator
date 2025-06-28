import unittest
from textnode import TextNode, TextType
from split_delimiter import *


class TestTextToTextNodes(unittest.TestCase):

    def test_plain_text(self):
        result = text_to_text_nodes("Just a sentence.")
        expected = [TextNode("Just a sentence.", TextType.TEXT)]
        self.assertEqual(result, expected)

    def test_bold_and_italic(self):
        result = text_to_text_nodes("This is **bold** and _italic_.")
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(".", TextType.TEXT)
        ]
        self.assertEqual(result, expected)

    def test_code_inline(self):
        result = text_to_text_nodes("Some `code` here.")
        expected = [
            TextNode("Some ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" here.", TextType.TEXT)
        ]
        self.assertEqual(result, expected)

    def test_link_and_image(self):
        result = text_to_text_nodes("Visit [OpenAI](https://openai.com) and see ![logo](logo.png)")
        expected = [
            TextNode("Visit ", TextType.TEXT),
            TextNode("OpenAI", TextType.LINK, "https://openai.com"),
            TextNode(" and see ", TextType.TEXT),
            TextNode("logo", TextType.IMAGE, "logo.png")
        ]
        self.assertEqual(result, expected)

    def test_nested_styles_sequential(self):
        result = text_to_text_nodes("**bold** _italic_ `code`")
        expected = [
            TextNode("bold", TextType.BOLD),
            TextNode(" ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" ", TextType.TEXT),
            TextNode("code", TextType.CODE)
        ]
        self.assertEqual(result, expected)

    def test_mixed_markdown(self):
        result = text_to_text_nodes("A _mix_ of [things](url.com) and ![img](pic.jpg).")
        expected = [
            TextNode("A ", TextType.TEXT),
            TextNode("mix", TextType.ITALIC),
            TextNode(" of ", TextType.TEXT),
            TextNode("things", TextType.LINK, "url.com"),
            TextNode(" and ", TextType.TEXT),
            TextNode("img", TextType.IMAGE, "pic.jpg"),
            TextNode(".", TextType.TEXT)
        ]
        self.assertEqual(result, expected)

    def test_invalid_syntax_ignored(self):
        # Unmatched bold markers will raise ValueError
        with self.assertRaises(ValueError):
            text_to_text_nodes("This is **not closed properly.")

if __name__ == "__main__":
    unittest.main()