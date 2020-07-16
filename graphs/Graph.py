from graphviz import Digraph

from ..data import DataConfig, MetaConfig
from ..arrays import Array


def indent(s: str, indent='  ') -> str:
    return "\n".join(indent + line for line in s.split('\n'))


def fancyJson(d: (dict, list, tuple, str, int, float, bool, None.__class__)) -> str:
    if isinstance(d, dict):
        if len(list(d.keys())):
            return "{\n" + indent(",\n".join(f"{repr(key)}: {fancyJson(val)}" for key, val in d.items())) + "\n}"
        else:
            return "{}"
    elif isinstance(d, (list, tuple)):
        if len(d):
            return "[\n" + indent(",\n".join(fancyJson(val) for val in d)) + "\n]"
        else:
            return "[]"
    else:
        return repr(d)


class GraphItem(DataConfig, MetaConfig):
    """
        GraphItem is a generic class for all Graph contained items,
        it implements both DataConfig and MetaConfig
        and as an item of a graph it stores it's owner graph.
    """

    def __init__(self, graph, **data):
        assert isinstance(graph, Graph)
        self.graph = graph
        DataConfig.__init__(self, **data)
        MetaConfig.__init__(self)

    @staticmethod
    def _match(cls, *configs, **config):
        """Abstract method to call match on a GraphItem"""
        return lambda item: item.match(*configs, **config)


class Node(GraphItem):
    def addOrigin(self, origin, **kwargs):
        """Create a link oriented from origin to self in self.graph"""
        assert self.graph.hasNode(origin), "can't link nodes between multiple graphs, try using Graph.copyNode"
        return self.graph.setLink(origin, self, **kwargs)

    def addTarget(self, target, **kwargs):
        """Create a link oriented from self to target in self.graph"""
        assert self.graph.hasNode(target), "can't link nodes between multiple graphs, try using Graph.copyNode"
        return self.graph.setLink(self, target, **kwargs)

    def forkOut(self, *targets, **kwargs):
        return [self.addTarget(target, **kwargs) for target in targets]

    def forkIn(self, *origins, **kwargs):
        return [self.addOrigin(origin, **kwargs) for origin in origins]

    def keepOrigins(self, *configs, **config):
        return self.originLinks.keep(Link._match(*configs, **config)).map(Link.getOrigin)

    def keepTargets(self, *configs, **config):
        return self.targetLinks.keep(Link._match(*configs, **config)).map(Link.getTarget)

    def isOriginOf(self, link):
        return self is link.origin

    def isTargetOf(self, link):
        return self is link.target

    def isVertexOf(self, link):
        return self.isOriginOf(link) or self.isTargetOf(link)

    @property
    def targetLinks(self):
        """Return all the links that connect self to its node targets"""
        return self.graph.links.keep(self.isOriginOf)

    @property
    def originLinks(self):
        """Return all the links that connect self to its node origins"""
        return self.graph.links.keep(self.isTargetOf)

    @property
    def links(self):
        """Return all the links of self"""
        return self.graph.links.keep(self.isVertexOf)

    @property
    def targets(self):
        """Return all the nodes connected as targets to self"""
        return self.targetLinks.map(Link.getTarget)

    @property
    def origins(self):
        """Return all the nodes connected as origins to self"""
        return self.originLinks.map(Link.getOrigin)

    def dict_id(self):
        """
            Method that return the id of a node in the graph, used for the $.toDict method
            can be redefined in subclasses.

            Constraints :
                (1) for two given nodes in a graph, their id should be different if the state of the graph is unchanged
                (2) if the graph changes, the id CAN change, but without any change in the graph state, it NEEDS to remain the same
                (3) preferable to make ids typed as str or int ..

            example of values :
            --> self.graph.nodes.index(self)
            --> id(self)
            --> hex(id(self))
        """
        return self.graph.nodes.index(self)

    def toDict(self):
        """Implementation of DictInterface.toDict"""
        return {
            '#': self.dict_id(),
            'meta': MetaConfig.toDict(self),
            'data': DataConfig.toDict(self)
        }

    def copy(self, newGraph=None, data=True, meta=True, original='copiedFrom'):
        """
            Make a copy of the node into a newGraph (can be the same as the current node graph)
            if data is True (by default), copy the data in the new node
            if meta is True (by default), copy the meta in the new node
            if original is not None, it will place the original node in the meta with the parameter <original> as key
            --> default value to save the original value is 'copiedFrom'
            --> be careful, the original node will be ignored when using $.toDict method
        """
        if newGraph is None:
            newGraph = self.graph
        assert isinstance(newGraph, Graph)
        if data:
            copy = newGraph.setNode(**self.data())
        else:
            copy = newGraph.setNode()

        if meta:
            copy.meta(**self.meta())

        if original is not None:
            copy.meta(original, self)

        return copy


class Link(GraphItem):
    def __init__(self, graph, origin, target, **data):
        assert isinstance(graph, Graph)
        assert origin in graph.nodes
        assert target in graph.nodes
        self.graph = graph
        self.origin = origin
        self.target = target
        DataConfig.__init__(self, **data)
        MetaConfig.__init__(self)

    def getOrigin(self):
        return self.origin

    def getTarget(self):
        return self.target

    def isOrigin(self, node):
        return self.origin is node

    def isTarget(self, node):
        return self.target is node

    def isVertex(self, node):
        return self.isOrigin(node) or self.isTarget(node)

    def copy(self, newOrigin, newTarget, data=True, meta=True, original='copiedFrom'):
        """
            Make a copy of the link with new origin and target (origin and target needs to be from the same graph)
            if data is True (by default), copy the data in the new link
            if meta is True (by default), copy the meta in the new link
            if original is not None, it will place the original link in the meta with the parameter <original> as key
            --> default value to save the original value is 'copiedFrom'
            --> be careful, the original link will be ignored when using $.toDict method
            --> the originals origin/target will not be set in new origin/target nodes as copy
        """

        if data:
            copy = newOrigin.addTarget(newTarget, **self.data())
        else:
            copy = newOrigin.addTarget(newTarget)

        if meta:
            copy.meta(**self.meta())

        if original is not None:
            copy.meta(original, self)

        return copy

    def toDict(self):
        """Implementation of DictInterface.toDict"""
        return {
            '#origin': self.origin.dict_id(),
            '#target': self.target.dict_id(),
            'meta': MetaConfig.toDict(self),
            'data': DataConfig.toDict(self)
        }


class Graph(MetaConfig):
    """
        Graph is a class that represent a structure of mathematic directed graphs,
        in the body of the class, two classes are defined : Node and Link
        those two class herits from the abstract class GraphItem
        you can build them by using $.setNode(**nodeData) and $.setLink(origin, target, **linkData)

        Graph inherit from MetaConfig, so you can store metadata in the graph itself
        such as 'name', 'author', 'description', ...

        PS :
            For more informations about this structure you can consult the wikipedia's article about it
            --> https://en.wikipedia.org/wiki/Directed_graph
    """
    Node = Node
    Link = Link

    def __init__(self, **meta):
        MetaConfig.__init__(self, **meta)
        self.nodes = Array()
        self.links = Array()

    def hasNode(self, node):
        """Return True is the node is in the graph"""
        return node in self.nodes

    def hasLink(self, link):
        """Return True is the link is in the graph"""
        return link in self.links

    def setNode(self, **nodeData):
        """Create a new Node in the graph, from it's data"""
        node = self.__class__.Node(self, **nodeData)
        self.nodes.append(node)
        return node

    def setLink(self, origin, target, **linkData):
        """Create a new Link in the graph, from it's origin node, target node, and data"""
        assert self.hasNode(origin), f"can't make a link in a graph if the node is not in this graph"
        assert self.hasNode(target), f"can't make a link in a graph if the node is not in this graph"
        link = self.__class__.Link(self, origin, target, **linkData)
        self.links.append(link)
        return link

    def delNode(self, node):
        assert self.hasNode(node)
        self.nodes.remove(node)
        node.links.apply(lambda link: self.delLink(link))
        del node

    def delLink(self, link):
        assert self.hasLink(link)
        self.links.remove(link)
        del link

    def toDict(self):
        """Implementation of DictInterface.toDict"""
        return {
            'meta': MetaConfig.toDict(self),
            'nodes': list(self.nodes.map(lambda node: node.toDict())),
            'links': list(self.links.map(lambda link: link.toDict()))
        }

    @classmethod
    def fromDict(cls, d):
        """Implementation of DictInterface.fromDict"""
        g = cls(**d.get('meta', {}))

        for nodeData in d.get('nodes', []):
            node = g.setNode(**nodeData.get('data', {}))
            node.meta(**nodeData.get('meta', {}))
            node.meta('#', nodeData.get('#'))

        for linkData in d.get('links', []):
            origin_id = linkData.get('#origin')
            target_id = linkData.get('#target')

            origin = g.nodes.first(lambda node: node.meta('#') == origin_id)
            target = g.nodes.first(lambda node: node.meta('#') == target_id)

            link = g.setLink(origin, target, **linkData.get('data'))
            link.meta(**linkData.get('meta', {}))

        return g

    def render(self, filepath, node_text, node_config, link_config,
               node_uid=lambda node: str(hex(id(node))),
               link_ignore=lambda link: False,
               node_ignore=lambda link: False,
               engine='dot'):
        dot = Digraph(engine=engine)

        for node in self.nodes:
            if not node_ignore(node):
                dot.node(node_uid(node), node_text(node), **node_config(node))

        for link in self.links:
            if not link_ignore(link) and not node_ignore(link.origin) and not node_ignore(link.target):
                dot.edge(node_uid(link.origin), node_uid(link.target), **link_config(link))
        dot.render(filepath, view=True)


if __name__ == '__main__':
    g = Graph(name='a tests graph')

    x = g.setNode(type='variable', name='x')
    y = g.setNode(type='variable', name='y')
    a = g.setNode(type='operator', name='add', symbol='+')

    x.addTarget(a, type='argument', index=0)
    y.addTarget(a, type='argument', index=1)

    print(fancyJson(g.toDict()))

    help(Graph)
