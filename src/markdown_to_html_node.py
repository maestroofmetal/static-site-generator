from split_delimiter import markdown_to_blocks, text_to_text_nodes
from block_types import BlockType, block_to_block_type
from html_converter import text_node_to_html_node
from htmlnode import ParentNode
from textnode import *

def text_to_children(text):
    children_nodes = []
    text_nodes = text_to_text_nodes(text)
    for node in text_nodes:
        children_nodes.append(text_node_to_html_node(node))
    return children_nodes
    
def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    html_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)

        match block_type:
            # most basic conversion
            case BlockType.PARAGRAPH:
                block_text = " ".join(line.strip() for line in block.strip().splitlines())
                if block_text:
                    html_nodes.append(
                    ParentNode("p",text_to_children(block_text))
                )
            
            #creates heading nodes
            case BlockType.HEADING: html_nodes.append(
                ParentNode(f"h{len(block.split(' ', 1)[0])}",
                           text_to_children(block.split(" ",1)[1]))
            )
            
            #creates code nodes
            case BlockType.CODE: 
                code_text = block[3:-3].lstrip("\n")
                html_nodes.append(ParentNode("pre",[
                    ParentNode("code",[text_node_to_html_node(TextNode(
                    code_text,TextType.TEXT))])])
                )
                
            #creates quote nodes
            case BlockType.QUOTE: html_nodes.append(ParentNode(
                "blockquote",text_to_children(block.replace("> ", ""))))
            
            #creates unordered list nodes
          
            case BlockType.UNORDERED_LIST: 
                html_nodes.append(
                ParentNode("ul",
                           [ParentNode("li", 
                                       text_to_children(
                                           line.removeprefix("- ").removeprefix("* ")))
                            for line in block.splitlines()])
            )
                
            #creates ordered list nodes
            case BlockType.ORDERED_LIST:
                html_nodes.append(
                ParentNode("ol",
                           [ParentNode("li",
                                       text_to_children(line.split(". ",1)[1]))
                            for line in block.splitlines()])
            )
            
    return ParentNode("div", html_nodes)