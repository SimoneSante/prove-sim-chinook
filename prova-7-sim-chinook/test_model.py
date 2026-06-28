from model.model import Model


def main():
    model = Model()

    c=1
    b=180

    print(f"Costruisco il grafo con c = {c}...")
    model.build_graph(c,b)
    n_nodi, n_archi = model.get_stats()
    print(f" il grafo creato contiene {n_nodi} nodes e {n_archi} edges")

    s=model.topprod()
    print(f"nodo più influente {s}")

    poiu = model.getArchiPesoMaggiore()
    for n in poiu[:5]:
        print(f" {n}")
if __name__ == "__main__":
    main()