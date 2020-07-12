from .DirectedAcyclicGraph import DirectedAcyclicGraph


class Node(DirectedAcyclicGraph.Node):
    def addChild(self, node, **config):
        """Shortcut to add a child (target)"""
        self.graph.setLink(self, node, **config)

    def setParent(self, node, **config):
        """Shortcut to set the parent (origin)"""
        self.graph.setLink(node, self, **config)


class Link(DirectedAcyclicGraph.Link):
    def __init__(self, graph, origin, target, **data):
        assert target.origins.len() < 1, f"{graph.__class__.__name__} Nodes can have a maximum of 1 origin"
        super().__init__(graph, origin, target, **data)


class TreeGraph(DirectedAcyclicGraph):
    """
        Tree Graph represent a structure where nodes are ordonned by layers.
        Also, each node can have a maximum of 1 origin (called parent in this context)
        Layers can be calculated from the root origin(s) or the root target(s)
    """
    Node = Node
    Link = Link
