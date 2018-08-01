#!/usr/bin/python
# -*- coding: utf8 -*-

from game.grandalf.graphs import Vertex,Edge,Graph
from game.grandalf.layouts import SugiyamaLayout

class defaultview(object):
    w,h = 50,40

class Node:
    def __init__(self, taskNo, x, y):
        self.taskNo = int(taskNo)
        self.x      = int(x)
        self.y      = int(y)

def initNodes(env):
    taskCount = env.workflow.taskCount
    nodes = []
    V = [Vertex(data) for data in range(taskCount)]
    X = []
    for i in range(taskCount):
        for j in range(taskCount):
            if env.workflow.DAG[i, j] != 0:
                X.append(tuple((i, j)))
    E = [Edge(V[v], V[w]) for (v, w) in X]
    g = Graph(V, E)
    for v in V:
        v.view = defaultview()
    sug = SugiyamaLayout(g.C[0])
    sug.init_all(roots=[V[0]])
    sug.draw()
    index = 0
    for v in g.C[0].sV:
        x = v.view.xy[0] + 1000
        y = v.view.xy[1] + 150
        taskNo = v.data
        node = Node(v.data, x, y)
        nodes.append(node)
        index += 1
    nodes.sort(key=lambda x: x.taskNo, reverse=False)
    return nodes, X