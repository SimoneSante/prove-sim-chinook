from model.model import Model


def main():
    model = Model()

    c="USA"


    print(f"Costruisco il grafo con c = {c}...")
    model.build_graph(c)
    n_nodi, n_archi = model.get_stats()
    print(f" il grafo creato contiene {n_nodi} nodes e {n_archi} edges")

    s,k=model.connesse()
    print(f"numero di componenti connesse: {s}, dimensione componente più lunga {len(k)}")

    poiu = model.getArchiPesoMaggiore()
    for n in poiu[:5]:
        print(f" {n}")

if __name__ == "__main__":
    main()