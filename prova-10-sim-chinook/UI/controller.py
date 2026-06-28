import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillDDGenre(self):
        self._view._ddGenre.options.clear()
        self._view._ddGenre.value = None

        listaS = self._model.get_genere()

        for l in listaS:
            self._view._ddGenre.options.append(
                ft.dropdown.Option(
                    key=l.GenreId,
                    text=l.Name,
                )
            )
        self._view.update_page()

    def handleCreaGrafo(self, e):
        self._view.txt_result.controls.clear()
        try:
            genere = str(self._view._ddGenre.value)
        except ValueError:
            self._view.txt_result.controls.append(ft.Text("selezionare entrambi gli anni"))
        if genere is None:
            self._view.txt_result.controls.append(
                ft.Text("selezionare campi valido", color="red")
            )
        self._model.build_graph(genere)
        stats = self._model.get_stats()
        self._view.txt_result.controls.append(
            ft.Text(f"il grafo ha:{stats[0]} nodi e {stats[1]} archi", color="green"))
        k = self._model.topprod()
        self._view.txt_result.controls.append(
            ft.Text(f"il più influente è {k[0].Name} con {k[1]}", color="blue"))
        r = self._model.stampatop5()
        for t in r:
            self._view.txt_result.controls.append(
                ft.Text(f"{t[0].Name} ----- {t[1].Name} :  {t[2]}", color="blue"))
        self._view.update_page()


    def handleCammino(self,e):
        pass