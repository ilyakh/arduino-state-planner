# -*- coding: utf-8 -*-

import networkx as nx


class Program:
    def __init__( self, states ):
        # creates an empty graph
        self.graph = nx.DiGraph()

        # adds setup node to the states
        self.graph.add_node( State( "Start" ) )

        # give self reference to each node
        for s in states:
            s.graph = self.graph

        # add states to the machine
        self.graph.add_nodes_from( states )

    def __getitem__( self, description ):
        candidates = \
            [ n for n in self.graph.nodes() if n.description == description ]

        # warns if there are multiple states with the same description
        if len(candidates) > 1:
            raise Exception( "Duplicate states are found. Combine?" )
        elif not len(candidates):
            raise Exception( "Node not found" )

        # candidate selection strategy
        return candidates.pop()

    def __iter__( self ):
        return self.graph.__iter__()


    def __str__( self ):
        return str( self.graph.nodes() )

class State:
    def __init__( self, description ):
        self.graph = None

        self.description = description
        self.code = id(self)
        self.delay = 1
        self.body = ""

    def __str__( self ):
        template = '<state description="{self.description}" code="{self.code}>'
        return template.format( self=self )

    def __repr__( self ):
        return self.__str__()

    def __lt__( self, other ):
        self.graph.add_edge( self, other )
        return other




if __name__ == "__main__":

    states = [
        State( "Wait for event" ),
        State( "React to button" ), State( "Timeout" ),
        State( "Turn off" ) ]

    p = Program( states )


    for s in p:
        print s

    p["Start"] > p["Wait for event"]
    p["Wait for event"] > p["Timeout"]
    p["Wait for event"] > p["React to button"] > p["Wait for event"]
    p["Timeout"] > p["Turn off"]
    # p["React to button"] > p["Wait for event"]

    def draw(g):
        import matplotlib.pyplot as pp

        pos=nx.layout.spectral_layout(g)

        node_labels = {}
        for n in g.nodes():
            node_labels[n] = n.description

        nx.draw_networkx_labels(g, pos, node_labels, label_pos=-1, font_size=16)

        nx.draw_networkx_nodes(g, pos, node_shape="o", node_color="b", linewidths=2.0)
        nx.draw_networkx_edges(g, pos, width=2)

        pp.draw()
        pp.show()


    draw( p.graph )