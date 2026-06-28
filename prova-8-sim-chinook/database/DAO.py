from database.DB_connect import DBConnect
from model.genere import Genere
from model.track import Track


class DAO():
    @staticmethod
    def get_generi():
        "Artisti"
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """
                select distinct a.*
                from artist a"""
        cursor.execute(query)

        res = []
        for row in cursor:
            res.append((**row))

        cursor.close()
        cnx.close()
        return res

    @staticmethod
    def get_nodi(c):
        "Nodi--> album dell artista selezionato"
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """select distinct a.*
                from Album a
                where a.ArtistId=%s"""

        cursor.execute(query, (c,))
        res = []
        for row in cursor:
            res.append(Track(**row))

        cursor.close()
        cnx.close()
        return res

    @staticmethod
    def get_archi(c):
        """Archi --> due album di quell artista sono collegati
se almeno un cliente ha comprato brani di entrambi """
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """with album_ridotto as (
                    select distinct a.AlbumId as id
                    from Album a
                    where a.ArtistId=%s 
                    )
                    
                    select distinct least(a.id , a1.id ) as id1, greatest(a.id , a1.id ) as id2
                    from Invoice i, Invoice i1, InvoiceLine il, InvoiceLine il1, Track t, Track t1, album_ridotto a, album_ridotto a1
                    where i.CustomerId =i1.CustomerId and il.InvoiceId =i.InvoiceId 
                    and i1.InvoiceId =il1.InvoiceId and t.TrackId =il.TrackId  and t1.TrackId =il1.TrackId 
                    and t.AlbumId =a.id and t1.AlbumId =a1.id and t.TrackId !=t1.TrackId  
                    group by  least(a.id , a1.id ) , greatest(a.id , a1.id )


                                """

        cursor.execute(query, (c,))
        res = []
        for row in cursor:
            res.append((row["id1"], row["id2"]))

        cursor.close()
        cnx.close()
        return res

    @staticmethod
    def get_pesi(c):
        """Pesi---->> numero totale di brani acquistati di quell album
"""
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """SELECT a.AlbumId as id, count(il.TrackId)
                    from InvoiceLine il, Track t, Album a
                    where il.TrackId=t.TrackId and a.ArtistId =%s and a.AlbumId =t.AlbumId 
                    Group by a.AlbumId  """

        cursor.execute(query, (c,))
        res = {}
        for row in cursor:
            res[row["id"]] = row["peso"]

        cursor.close()
        cnx.close()
        return res