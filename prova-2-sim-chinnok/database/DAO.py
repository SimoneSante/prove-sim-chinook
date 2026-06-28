from database.DB_connect import DBConnect
from model.genere import Genere
from model.clienti import Cliente

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
            res.append(Genere(**row))

        cursor.close()
        cnx.close()
        return res

    @staticmethod
    def get_nodi(c):
        "clienti che hanno acquistato almeno un brano appartenente ad un genere"
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """with trackdepurato as (
                    SELECT t.TrackId as tid
                    from Track t
                    where t.GenreId =%s
                    )
                    Select distinct c.*
                    FROM Customer c, Invoice i, InvoiceLine il, trackdepurato t
                    where c.CustomerId =i.CustomerId and i.InvoiceId =il.InvoiceId and il.TrackId = t.tid"""

        cursor.execute(query,(c,))
        res = []
        for row in cursor:
            res.append(Cliente(**row))

        cursor.close()
        cnx.close()
        return res

    @staticmethod
    def get_archi(c):
        """arco se due clienti hanno acquistato almeno una volta lo stesso artista del genere dato

	                with --> tutte le tracce comprate da un cliente di quel genere"""
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """with cliente_track as	(select distinct i.CustomerId as cid, t.TrackId as tid
                from Invoice i, InvoiceLine il, Track t
                where i.InvoiceId= il.InvoiceId and il.TrackId= t.TrackId and t.GenreId=%s
                group by i.CustomerId, t.TrackId)
                
                select distinct least(ct.cid , ct1.cid ) as id1, greatest(ct.cid , ct1.cid ) as id2 
                from cliente_track ct, cliente_track ct1, Track t, Track t1, Album a, Album a1
                where ct.cid!=ct1.cid and ct.tid=t.TrackId and t.AlbumId=a.AlbumId and
                ct1.tid=t1.TrackId and t1.AlbumId=a1.AlbumId and a1.ArtistId =a.ArtistId 
                group by least(ct.cid, ct1.cid), greatest(ct.cid , ct1.cid )
                                """

        cursor.execute(query, (c,))
        res = []
        for row in cursor:
            res.append((row["id1"],row["id2"]))

        cursor.close()
        cnx.close()
        return res

    @staticmethod
    def get_pesi(c):
        """Spesa del genere per cliente somma di price*quantity solo delle tracce del genere passate come input"""
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """with trackdepurato as (
                    SELECT t.TrackId as tid
                    from Track t
                    where t.GenreId =%s
                    )
                    select i.CustomerId as id , sum(il.Quantity * il.UnitPrice ) as peso
                    from Invoice i, InvoiceLine il, trackdepurato t
                    where  i.InvoiceId =il.InvoiceId and  t.tid =il.TrackId
                    group by i.CustomerId
                                        """

        cursor.execute(query,(c,))
        res = {}
        for row in cursor:
            res[row["id"]] = row["peso"]

        cursor.close()
        cnx.close()
        return res
