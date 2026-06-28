from database.DB_connect import DBConnect
from model.cantanti import Cantante
from model.album import Album


class DAO():
    @staticmethod
    def get_generi():
        "tutti i generi"
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """select distinct g.*
                    from genre g"""
        cursor.execute(query)

        res = []
        for row in cursor:
            res.append(Cantante(**row))

        cursor.close()
        cnx.close()
        return res

    @staticmethod
    def get_nodi(c):
        """Nodi -----> paesi dei clienti che hanno acquistato almeno
un brano del genere selezionato"""
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """with t_semplice as (select t.TrackId 
from Track t
where t.GenreId =%s
)

Select distinct c.Country as paese
from t_semplice t, InvoiceLine il, Invoice i, Customer c
where il.TrackId=t.TrackId and i.InvoiceId =il.InvoiceId
and i.CustomerId =c.CustomerId"""

        cursor.execute(query, (c,))
        res = []
        for row in cursor:
            res.append(row["paese"])

        cursor.close()
        cnx.close()
        return res

    @staticmethod
    def get_archi(c):
        """Arco---->> arco tra due paesi se clienti uno di
un paese ed uno di un altro hanno comprato tracce
di un stesso artista appartenente al genere scelto"""
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """with customer_semplice as (
                    select c.CustomerId as id, c.Country as paese
                    from Customer c
                    ),
                    t_semplice as (select t.TrackId as tid, t.AlbumId aid
                    from Track t
                    where t.GenreId =%s
                    )
                    Select distinct least(c.paese , c1.paese ) as id1, greatest(c.paese , c1.paese ) as id2, count(distinct a.ArtistId ) as peso
                    from customer_semplice c, customer_semplice c1, Invoice i, Invoice i1, InvoiceLine il, InvoiceLine il1, t_semplice t, t_semplice t1, Album a, Album a1
                    where c.id!=c1.id and c.paese!=c1.paese and c.id=i.CustomerId and 
                    i.InvoiceId=il.InvoiceId and il.TrackId=t.tid and a.AlbumId=t.aid and
                    c1.id=i1.CustomerId and 
                    i1.InvoiceId=il1.InvoiceId and il1.TrackId=t1.tid and a1.AlbumId=t1.aid
                    and a.ArtistId=a1.ArtistId
                    group by least(c.paese , c1.paese ) , greatest(c.paese , c1.paese )
                                """

        cursor.execute(query, (c,))
        res = []
        for row in cursor:
            res.append((row["id1"], row["id2"], row["peso"]))

        cursor.close()
        cnx.close()
        return res

