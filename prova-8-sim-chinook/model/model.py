import networkx as nx
from database.DAO import DAO
from websockets.cli import print_over_input


class Model:
    def __init__(self):
        self._graph = nx.DiGraph()
        self._idMap = {}

    def build_graph(self, c):
        self._graph.clear()
        self._idMap.clear()

        nodi = DAO.get_nodi(c)
        self._graph.add_nodes_from(nodi)
        for n in nodi:
            self._idMap[n.TrackId] = n

        edges = list(DAO.get_archi(int(c)))
        mappa_pesi = DAO.get_pesi(c)
        for a in edges:
            p = self._idMap[a[0]]
            s = self._idMap[a[1]]
            peso1 = float(mappa_pesi[a[0]])
            peso2 = float(mappa_pesi[a[1]])

            somma = peso1 + peso2
            if peso1 == peso2:
                self._graph.add_edge(p, s, weight=somma)
                self._graph.add_edge(s, p, weight=somma)
            elif peso1 > peso2:
                self._graph.add_edge(p, s, weight=somma)
            elif peso1 < peso2:
                self._graph.add_edge(s, p, weight=somma)






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


    def getArchiPesoMaggiore(self):
        edges=self._graph.edges(data=True)
        edgesMaggiori=sorted(edges, key=lambda x: x[2]["weight"], reverse=True)

        return edgesMaggiori