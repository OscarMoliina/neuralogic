import networkx as nx
from graphviz import Digraph
import matplotlib.pyplot as plt

from neuralogic.nn import *
from neuralogic.logicgate import LogicGate
from neuralogic.lgutils import *

def create_graph(lg:LogicGate) -> nx.DiGraph:
    G = nx.DiGraph()
    for n in lg.neurons:
        for inp, w in zip(n.inputs, n.weights):
            G.add_edge(inp, n, weight = w)
    return G

def draw_graph(G):
    pos = nx.spring_layout(G)
    nx.draw_networkx_nodes(G, pos)
    nx.draw_networkx_labels(G, pos)
    nx.draw_networkx_edges(G, pos, edge_color='r', arrows=True)
    plt.show()

def create_dot_graph(lg):
    dot = Digraph(format='png')
    dot.attr(dpi='300')
    for node in lg.inputs:
        dot.node(str(node.key), 
                 #str(node), 
                 shape='diamond', 
                 fillcolor='gray', 
                 style='filled', 
                 fontname="Poppins bold")

    for n in lg.neurons:
        dot.node(str(id(n)),str(n.key), 
                 #str(n), 
                 shape='ellipse', 
                 fillcolor='turquoise', 
                 style='filled', 
                 fontname="Poppins bold")
    
    for n in lg.neurons:
        for inp, w in zip(n.inputs, n.weights):
            name = str(inp.key) if inp.key != None else str(id(inp))
            dot.edge(name, 
                     str(n.key), 
                     label='  '+str(w),
                     color='black', 
                     fontcolor='crimson', 
                     penwidth='3.0', 
                     fontname="Poppins bold",
                     splines="ortho")
    
    return dot

def draw_dot_graph(dot):
    dot.render('./dots/neural_network', view=True)
