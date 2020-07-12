import unittest

from .DirectedAcyclicGraph import DirectedAcyclicGraph
from .Graph import Graph


class TestGraph(unittest.TestCase):
    def test_0001(self):
        """Test Graph.__init__ method"""
        graph = Graph()

    def test_0002(self):
        """Test Graph.setNode method"""
        graph = Graph()
        node1 = graph.setNode()
        node2 = graph.setNode()

        self.assertIsNot(node1, node2)
        self.assertIs(node1.graph, graph)
        self.assertIs(node2.graph, graph)

    def test_0003(self):
        """Test Graph.setLink method"""
        graph = Graph()
        node1 = graph.setNode()
        node2 = graph.setNode()

        self.assertIsNot(node1, node2)
        self.assertIs(node1.graph, graph)
        self.assertIs(node2.graph, graph)

    def test_0004(self):
        """Test Graph.hasNode method"""
        g1 = Graph()
        n1 = g1.setNode()

        g2 = Graph()
        n2 = g2.setNode()

        self.assertTrue(g1.hasNode(n1))
        self.assertTrue(g2.hasNode(n2))

        self.assertFalse(g1.hasNode(n2))
        self.assertFalse(g2.hasNode(n1))

    def test_0005(self):
        """Test Graph.hasLink method"""
        g1 = Graph()
        n11 = g1.setNode()
        n12 = g1.setNode()
        l1 = g1.setLink(n11, n12)

        g2 = Graph()
        n21 = g2.setNode()
        n22 = g2.setNode()
        l2 = g2.setLink(n21, n22)

        self.assertTrue(g1.hasLink(l1))
        self.assertTrue(g2.hasLink(l2))

        self.assertFalse(g1.hasLink(l2))
        self.assertFalse(g2.hasLink(l1))

    def test_0006(self):
        """Test Graph.delLink method """
        graph = Graph()
        node1 = graph.setNode()
        node2 = graph.setNode()
        link = graph.setLink(node1, node2)

        graph.delLink(link)

        self.assertFalse(graph.hasLink(link))

    def test_0007(self):
        """Test Graph.delNode method """
        graph = Graph()
        node1 = graph.setNode()
        node2 = graph.setNode()
        link = graph.setLink(node1, node2)

        graph.delNode(node1)

        self.assertFalse(graph.hasNode(node1))
        self.assertFalse(graph.hasLink(link))
        self.assertTrue(graph.hasNode(node2))

class TestDirectedAcyclicGraph(unittest.TestCase):
    def test_0001(self):
        """Test DirectedAcyclicGraph.Node.originLayer & .targetLayer"""
        graph = DirectedAcyclicGraph()
        node1 = graph.setNode()
        node2 = graph.setNode()
        node3 = graph.setNode()
        node4 = graph.setNode()

        l1 = graph.setLink(node1, node2)
        l2 = graph.setLink(node1, node3)
        l3 = graph.setLink(node3, node4)

        self.assertEqual(node1.originLayer, 0)
        self.assertEqual(node1.targetLayer, 2)
        self.assertEqual(node2.originLayer, 1)
        self.assertEqual(node2.targetLayer, 0)
        self.assertEqual(node3.originLayer, 1)
        self.assertEqual(node3.targetLayer, 1)
        self.assertEqual(node4.originLayer, 2)
        self.assertEqual(node4.targetLayer, 0)


