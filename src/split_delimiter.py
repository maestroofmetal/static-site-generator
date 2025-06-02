from textnode import TextType, TextNode

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        new_delimited_list = []
        if node.text_type == TextType.TEXT:
            delimited_list = node.text.split(delimiter)
            if len(delimited_list) % 2 != 0:
                for i in range(0,len(delimited_list)):
                    if i % 2 == 0:
                        new_delimited_list.append(TextNode(delimited_list[i],TextType.TEXT))
                    else:
                        new_delimited_list.append(TextNode(delimited_list[i],text_type))
            else:
                raise Exception("Invalid Markdown syntax!")
            new_nodes.extend(new_delimited_list)
        else:
            new_nodes.append(node)
    return new_nodes