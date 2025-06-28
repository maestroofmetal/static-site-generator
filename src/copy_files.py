import os
import shutil

#copies files from src directory to dest dir
def copy_static_to_public():
    #gets the absolut path of working this file's directory
    current_dir = os.path.dirname(__file__)
    print(current_dir)
    #gets the parent directory
    parent_dir = os.path.abspath(os.path.join(current_dir, ".."))
    
    #creates variables of source and destination directories
    src = os.path.join(parent_dir, "static")
    dest = os.path.join(parent_dir, "public")
    
    #deletes destination folder if it exists then creates it
    if os.path.exists(dest):
        print(f"Deleting {dest}/ ...\n...\n...\n...")
        shutil.rmtree(dest)
    print(f"Copying {src}/ to new directory {dest}/")
    shutil.copytree(src, dest) #recursively copies an entire directory rooted at src to dest
    print("Files succesfully copied!")