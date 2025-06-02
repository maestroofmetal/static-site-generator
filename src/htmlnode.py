from textnode import TextNode

class HTMLNode:
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
        
    def to_html(self):
        raise NotImplementedError("to_html not implemented")
    
    def props_to_html(self):
        if self.props is None:
            return ""
        HTMLNode_print = ""
        for key, value in self.props.items():
            HTMLNode_print += f' {key}="{value}"'
        return HTMLNode_print
    
    #makes it so I can run equals tests
    def __eq__(self, other):
        return (self.tag == other.tag and
                self.value == other.value and
                self.children == other.children and
                self.props == other.props)
        
    #tells me what's in a node
    def __repr__(self):
        return (f"HTMLNode(tag= {self.tag}, value= {self.value}, "
                f"children= {self.children}, props= {self.props})")

# Child class of HTMLNode    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props = None):
        super().__init__(tag, value, None, props)
        
    def to_html(self):
        if self.value is None:
            raise ValueError("invalid HTML: no value")
        if self.tag is None:
            return f"{self.value}"
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
        
#another child class of HTMLNode
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        child_string = ""
        if self.tag == None:
            raise ValueError("Parent nodes must have a tag")
        if self.children == None or self.children == []:
            raise ValueError("Not a Parent node")
        for child in self.children:
            child_string += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{child_string}</{self.tag}>"
    