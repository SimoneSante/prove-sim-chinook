from database.DB_connect import DBConnect
from model.genere import Genere
from model.Playlist import Playlist

class DAO():
    @staticmethod
    def get_generi():
        "prendo tutti i paesi"
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """select distinct c.Country 
                    from Customer c"""
        cursor.execute(query)

        res = []
        for row in cursor:
            res.append(Genere(**row))

        cursor.close()
        cnx.close()
        return res

    @staticmethod
    def get_nodi(c):
        """NODI-->  generi musicali acquistati da almeno un cliente del paese selezionato
(in base al paese vedere quali sono i generi ascoltati)"""
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = f"""with Track_ridottoas as ( 
                    select distinct t.TrackId as tid, t.GenreId as genere
                    from Track t
                    ),
                    customer_ridotto as (
                    select distinct c.customerId as id
                    from Customer c
                    where c.Country="{c}"
                    )
                    Select distinct g.*
                    from Track_ridottoas tr, customer_ridotto cr, Invoice i, InvoiceLine il, Genre g
                    where cr.id=i.CustomerId  and i.InvoiceId =il.InvoiceId and il.TrackId =tr.tid and g.GenreId =tr.genere"""

        cursor.execute(query)
        res = []
        for row in cursor:
            res.append(Genere(**row))

        cursor.close()
        cnx.close()
        return res


    @staticmethod
    def get_archi(c):
        """ Si crea un arco tra due generi se uno stesso cliente di un determinato paese ha comprato
            tracce di entrambi i generi"""
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = f""" with Track_ridottoas as ( 
                    select distinct t.TrackId as tid, t.GenreId as genere
                    from Track t
                    ),
                    customer_ridotto as (
                    select distinct c.customerId as id
                    from Customer c
                    where c.Country="{c}"
                    )
                    select least(tr.genere ,tr1.genere) as id1, greatest(tr.genere, tr1.genere) as id2, count(distinct cr.id ) as peso 
                    FROM customer_ridotto cr, Invoice i, InvoiceLine il,Invoice i1,InvoiceLine il1 , Track_ridottoas tr, Track_ridottoas tr1 
                    where i.CustomerId =cr.id and cr.id =i1.CustomerId and i.InvoiceId =il.InvoiceId and i1.InvoiceId =il1.InvoiceId and 
                    il.TrackId =tr.tid and il1.TrackId=tr1.tid and tr.genere !=tr1.genere 
                    group by least(tr.genere ,tr1.genere) , greatest(tr.genere, tr1.genere)
                    order by peso desc"""

        cursor.execute(query)
        res = []
        for row in cursor:
            res.append((row["id1"],row["id2"], row["peso"]))
        cursor.close()
        cnx.close()
        return res
