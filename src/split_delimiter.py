from textnode import TextType, TextNode
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        new_delimited_list = []
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        delim_ls = node.text.split(delimiter)
        if len(delim_ls) % 2 == 0:
            raise ValueError("Invalid Markdown syntax!")
        for i in range(0,len(delim_ls)):
            if i % 2 == 0:
                new_delimited_list.append(TextNode(delim_ls[i],TextType.TEXT))
            else:
                new_delimited_list.append(TextNode(delim_ls[i],text_type))
        new_nodes.extend(new_delimited_list)
    return new_nodes

def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

