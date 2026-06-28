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
            self._idMap[n.ArtistId] = n
        edges = list(DAO.get_archi(c))
        for e in edges:
            self._graph.add_edge(self._idMap[e[0]], self._idMap[e[1]], weight=e[2])

    def get_stats(self):
        return self._graph.number_of_nodes(), self._graph.number_of_edges()

    def get_genere(self):
        return DAO.get_generi()

    def topprod(self):
        nodi = self._graph.nodes()
        li = []
        for n in nodi:
            peso_in = 0.0
            peso_out = 0.0

            archi_out = list(self._graph.out_edges(n, data=True))

            for k in archi_out:
                peso_out = peso_out + float(k[2]["weight"])

            archi_in = list(self._graph.in_edges(n, data=True))
            for k in archi_in:
                peso_in = peso_in + float(k[2]["weight"])
            li.append((n, (peso_out - peso_in)))
        li = sorted(li, key=lambda x: x[1], reverse=True)

        return li[0]

    def connesse(self):
        lista=list(nx.connected_components(self._graph))
        largest=max(nx.connected_components(self._graph),key=len)
        k=len(lista)
        return k, largest

    def getArchiPesoMaggiore(self):
        edges=self._graph.edges(data=True)
        edgesMaggiori=sorted(edges, key=lambda x: x[2]["weight"], reverse=True)

        return edgesMaggiori