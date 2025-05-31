class HTMLNode:
    def __init__(self, tag= None, value= None, children= None, props= None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
        
    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        HTMLNode_print = ""
        for key, value in self.props.items():
            HTMLNode_print += f' {key}="{value}"'
        return HTMLNode_print
    #makes it so I can run equals tests
    def __eq__(self, other):
        return self.tag == other.tag and self.value == other.value and self.children == other.children and self.props == other.props
    #tells me what's in a node    
    def __repr__(self):
        return f"HTMLNode(tag= {self.tag}, value= {self.value}, children= {self.children}, props= {self.props})"