from database.DB_connect import DBConnect
from model.customers import Customers
from model.album import Album


class DAO():
    @staticmethod
    def get_generi():
        "PAESI"
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """SELECT distinct c.Country 
                    from Customer c"""
        cursor.execute(query)

        res = []
        for row in cursor:
            res.append(Cantante(**row))

        cursor.close()
        cnx.close()
        return res

    @staticmethod
    def get_nodi(c):
        """Nodi---> clienti che hanno acquistato almeno un brano del genere selezionato"""
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = f"""SELECT distinct c.*
                    FROM Invoice I, InvoiceLine il,  Track t, Customer c
                    where i.InvoiceId =il.InvoiceId and il.TrackId =t.TrackId and t.GenreId =%s and c.CustomerId =i.CustomerId 
                    """

        cursor.execute(query,(c,))
        res = []
        for row in cursor:
            res.append(Customers(**row))

        cursor.close()
        cnx.close()
        return res

    @staticmethod
    def get_archi(c):
        """archi---> due clienti sono collegati se hanno comprato brani che appartengono alla stessa playlist"""
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = f"""with track_ridotto as(
                        select t.TrackId as tid
                        from Track t
                        where t.GenreId=%s
                        )
                        
                        SELECT distinct least(i.CustomerId,i1.CustomerId) as id1, greatest(i.CustomerId,i1.CustomerId) as id2
                        from Invoice i, InvoiceLine il,  track_ridotto t, PlaylistTrack pt, Invoice i1, InvoiceLine il1,  track_ridotto t1, PlaylistTrack pt1
                        where i.CustomerId !=i1.CustomerId and i.InvoiceId =il.InvoiceId and il.TrackId =t.tid  and pt.TrackId =t.tid and
                        i1.InvoiceId =il1.InvoiceId and il1.TrackId =t1.tid and pt1.TrackId =t1.tid and pt.PlaylistId =pt1.PlaylistId 
                        group by least(i.CustomerId,i1.CustomerId), greatest(i.CustomerId,i1.CustomerId)
                                """

        cursor.execute(query,(c,))
        res = []
        for row in cursor:
            res.append((row["id1"], row["id2"]))

        cursor.close()
        cnx.close()
        return res

    @staticmethod
    def get_pesi(c):
        """priority numero di acquisti del cliente per quel genere
"""
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = f"""select i.CustomerId as id, count(t.TrackId ) as peso
                    from Invoice i, InvoiceLine il,  Track t
                    where i.InvoiceId =il.InvoiceId and il.TrackId =t.TrackId and t.GenreId =%s
                    group by i.CustomerId 
                    """

        cursor.execute(query,(c,))
        res = {}
        for row in cursor:
            res[row["id"]] = row["peso"]

        cursor.close()
        cnx.close()
        return res

