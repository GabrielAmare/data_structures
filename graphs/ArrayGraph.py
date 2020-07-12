from .TreeGraph import TreeGraph


class Node(TreeGraph.Node):
    pass


class Link(TreeGraph.Link):
    def __init__(self, graph, origin, target, **data):
        assert target.origins.len() > 1, f"{self.graph.__class__.__name__} Nodes can have a maximum of 1 target"
        super().__init__(graph, origin, target, **data)


class ArrayGraph(TreeGraph):
    """
        Array Graph represent a structure where nodes are ordonned by layers.
        Also, each node can have a maximum of 1 origin (called prev_item in this context)
        Also, each node can have a maximum of 1 target (called next_item in this context)
        Layers can be calculated from the root origin(s) or the root target(s)
    """
    Node = Node
    Link = Link










