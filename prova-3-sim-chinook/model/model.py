import networkx as nx
from database.DAO import DAO
from websockets.cli import print_over_input


class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._idMap = {}

    def build_graph(self, c):
        self._graph.clear()
        self._idMap.clear()

        nodi = DAO.get_nodi(c)
        self._graph.add_nodes_from(nodi)
        for n in nodi:
            self._idMap[n.AlbumId] = n
        edges = list(DAO.get_archi(int(c)))
        for e in edges:
            self._graph.add_edge(self._idMap[e[0]], self._idMap[e[1]], weight=e[2])




    def get_stats(self):
        return self._graph.number_of_nodes(), self._graph.number_of_edges()

    def get_genere(self):
        return DAO.get_generi()

    def connesse(self):
        lista=list(nx.connected_components(self._graph))
        largest=max(nx.connected_components(self._graph),key=len)
        k=len(lista)
        return k, len(largest)

    def getArchiPesoMaggiore(self):
        edges=self._graph.edges(data=True)
        edgesMaggiori=sorted(edges, key=lambda x: x[2]["weight"], reverse=True)

        return edgesMaggiori