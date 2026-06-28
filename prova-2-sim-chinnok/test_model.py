from model.model import Model


def main():
    model = Model()

    c=1

    print(f"Costruisco il grafo con c = {c}...")
    model.build_graph(c)
    n_nodi, n_archi = model.get_stats()
    print(f" il grafo creato contiene {n_nodi} nodes e {n_archi} edges")

    s = model.stampatop5()
    for k in s:
        print(f"{k[0].__str__()} -> {k[1].__str__()}: {k[2]["weight"]}")

    print(f" il miglior cantante è: {model.topprod()[0].__str__()} con {model.topprod()[1]}")
if __name__ == "__main__":
    main()