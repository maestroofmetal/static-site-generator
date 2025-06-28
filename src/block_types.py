from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"
    
def block_to_block_type(markdown_block):
    check_list = markdown_block.splitlines()
    
    #checks if markdown block is code
    if markdown_block.startswith("```") and markdown_block.endswith("```"):
        return BlockType.CODE
        
    #checks if markdown block is a header
    heading_count = ""
    for i in range(1,7):
        heading_count += "#"
        if markdown_block.startswith(f"{heading_count} "):
            return BlockType.HEADING
    
    #checks if markdown block is a quote block
    if check_list != [] and all(line.startswith(">") for line in check_list):
        return BlockType.QUOTE
    
    #checks if markdown block is an unordered list
    if check_list != [] and all(line.startswith("- ") for line in check_list) or check_list != [] and all(line.startswith("* ") for line in check_list):
        return BlockType.UNORDERED_LIST
    
    #checks if markdown block is an ordered list
    if check_list != [] and all(line.startswith(f"{i+1}. ") for i, line in enumerate(check_list)):
        return BlockType.ORDERED_LIST
    
    #returns paragraph if none of the above were flagged
    return BlockType.PARAGRAPH