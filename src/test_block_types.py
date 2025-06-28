import unittest
from block_types import *

class TestBlockToBlockType(unittest.TestCase):

    def test_code_block(self):
        code = "```\ndef hello():\n    return 'hello'\n```"
        self.assertEqual(block_to_block_type(code), BlockType.CODE)

    def test_heading_blocks(self):
        for i in range(1, 7):
            heading = "#" * i + " Heading"
            with self.subTest(heading=heading):
                self.assertEqual(block_to_block_type(heading), BlockType.HEADING)

    def test_quote_block(self):
        quote = "> This is a quote\n> Spanning multiple lines"
        self.assertEqual(block_to_block_type(quote), BlockType.QUOTE)

    def test_unordered_list(self):
        ul = "- Item one\n- Item two\n- Item three"
        self.assertEqual(block_to_block_type(ul), BlockType.UNORDERED_LIST)

    def test_ordered_list(self):
        ol = "1. First\n2. Second\n3. Third"
        self.assertEqual(block_to_block_type(ol), BlockType.ORDERED_LIST)

    def test_ordered_list_with_wrong_numbers(self):
        bad_ol = "1. First\n3. Third"
        self.assertEqual(block_to_block_type(bad_ol), BlockType.PARAGRAPH)

    def test_paragraph_block(self):
        para = "This is just a normal paragraph.\nIt spans multiple lines."
        self.assertEqual(block_to_block_type(para), BlockType.PARAGRAPH)

    def test_empty_block(self):
        empty = ""
        self.assertEqual(block_to_block_type(empty), BlockType.PARAGRAPH)

    def test_mixed_list_starts(self):
        mixed = "- Item one\n2. Second"
        self.assertEqual(block_to_block_type(mixed), BlockType.PARAGRAPH)

    def test_code_block_inline_backticks(self):
        not_code = "`inline code`"
        self.assertEqual(block_to_block_type(not_code), BlockType.PARAGRAPH)