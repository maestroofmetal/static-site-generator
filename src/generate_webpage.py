import os
from markdown_to_html_node import markdown_to_html_node
from htmlnode import HTMLNode

def extract_title(markdown):
    lines = markdown.splitlines()
    header_line = ""
    for line in lines:
        if line.strip().startswith("# "):
            header_line = line.strip().lstrip("#").strip()
    if header_line== "":
        raise(Exception("No title found!"))
    return header_line

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    #opens the markdown and template files and saves the contents
    with open(from_path) as markdown_file:
        markdown_file_text = markdown_file.read()
    with open(template_path) as template_file:
        template_file_text = template_file.read()
    
    #finally converts the markdown to HTML    
    converted_text = markdown_to_html_node(markdown_file_text).to_html()
    
    #extracts the title from the markdown file
    title = extract_title(markdown_file_text)
    
    #replaces the title and content in the template
    html_page = template_file_text.replace("{{ Title }}", title).replace("{{ Content }}",converted_text)
    
    #creates the destination path if it doesn't exist
    if not os.path.exists(os.path.dirname(dest_path)):
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    
    #writes the HTML page to dest_path
    with open(dest_path, "w") as html_file:
        html_file.write(html_page)
        
        
extract_title("\n # Hello")