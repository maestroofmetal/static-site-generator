import os
from textnode import *
from copy_files import copy_static_to_public
from generate_webpage import generate_pages_recursive

def main():

   copy_static_to_public()

   #generates parent dir to be used for input and output paths
   main_dir = os.path.dirname(__file__)
   parent_dir = os.path.abspath(os.path.join(main_dir, ".."))

   input_file_path = os.path.join(parent_dir, "content")
   template_file_path = os.path.join(parent_dir, "template.html")
   output_file_path = os.path.join(parent_dir, "public")

   generate_pages_recursive(input_file_path, template_file_path, output_file_path)
   
if __name__ == "__main__":
    main()