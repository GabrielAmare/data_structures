from .Graph import Graph
from graphviz import Digraph


class Node(Graph.Node):
    @property
    def originLayer(self):
        """Return the layer (starting from origins) of the node"""
        return self.origins.map(lambda origin: origin.originLayer).max(default=-1)+1

    @property
    def targetLayer(self):
        """Return the layer (starting from targets) of the node"""
        return self.targets.map(lambda target: target.targetLayer).max(default=-1)+1


class Link(Graph.Link):
    def __init__(self, graph, origin, target, **data):
        # TODO: Make an OR operator between those two and check if it's right !
        try:
            assert origin.originLayer <= target.originLayer or target.originLayer == 0, f"Link origin and target should be ordonned {origin.originLayer} {target.originLayer}"
        except:
            assert target.targetLayer <= origin.targetLayer or origin.targetLayer == 0, f"Link origin and target should be ordonned {target.targetLayer} {origin.targetLayer}"
        super().__init__(graph, origin, target, **data)


class DirectedAcyclicGraph(Graph):
    """
        Directed Acyclic Graph represent a structure where nodes
        are ordonned by layers.
        Layers can be calculated from the root origin(s) or the root target(s)
    """
    Node = Node
    Link = Link

    def render(self, filepath, node_text, node_config, link_config,
               node_uid=lambda node: str(hex(id(node))),
               link_ignore=lambda link: False,
               node_ignore=lambda link: False,
               graph_config=None,
               engine='dot'):
        if graph_config is None:
            graph_config = {}
        dot = Digraph(engine=engine)

        dot.attr(overlap='false', **graph_config)

        for node in self.nodes:
            if not node_ignore(node):
                dot.node(node_uid(node), node_text(node), **node_config(node), ordering="out")

        for link in self.links:
            if not link_ignore(link) and not node_ignore(link.origin) and not node_ignore(link.target):
                dot.edge(node_uid(link.origin), node_uid(link.target), **link_config(link))

        dot.render(filepath, view=True)










