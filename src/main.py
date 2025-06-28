import os
import sys
from textnode import *
from copy_files import copy_static_to_docs
from generate_webpage import generate_pages_recursive

def main():
   #sets the basepath
   basepath = sys.argv[1] if len(sys.argv)>1 else "/"
      
   #does what it sounds like
   copy_static_to_docs()

   #generates parent dir to be used for input and output paths
   main_dir = os.path.dirname(__file__)
   parent_dir = os.path.abspath(os.path.join(main_dir, ".."))
   
   input_file_path = os.path.join(parent_dir, "content")
   template_file_path = os.path.join(parent_dir, "template.html")
   output_file_path = os.path.join(parent_dir, "docs")

   generate_pages_recursive(input_file_path, template_file_path, output_file_path, basepath)
   
if __name__ == "__main__":
    main()