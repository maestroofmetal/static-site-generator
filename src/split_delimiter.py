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
    
def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        working_text = node.text

        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        while True:
            images = extract_markdown_images(working_text)
            if not images:
                break
            alt, url = images[0]
            image_md = f"![{alt}]({url})"
            before, after = working_text.split(image_md, 1)
            if before != "":
                new_nodes.append(TextNode(before, TextType.TEXT))
            new_nodes.append(TextNode(alt, TextType.IMAGE, url))
            working_text = after
            
        if working_text != "": new_nodes.append(TextNode(working_text, TextType.TEXT))
    return new_nodes
        
def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        working_text = node.text

        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        while True:
            links = extract_markdown_links(working_text)
            if not links:
                break
            text, url = links[0]
            link_md = f"[{text}]({url})"
            before, after = working_text.split(link_md, 1)
            if before != "":
                new_nodes.append(TextNode(before, TextType.TEXT))
            new_nodes.append(TextNode(text, TextType.LINK, url))
            working_text = after
            
        if working_text != "": new_nodes.append(TextNode(working_text, TextType.TEXT))
    return new_nodes

def text_to_text_nodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def markdown_to_blocks(markdown):
    blocks = re.split(r'\n\s*\n', markdown)
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks