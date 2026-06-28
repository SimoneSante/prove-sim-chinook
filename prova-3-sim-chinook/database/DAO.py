from database.DB_connect import DBConnect
from model.genere import Genere
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
            res.append(Genere(**row))

        cursor.close()
        cnx.close()
        return res

    @staticmethod
    def get_nodi(c):
        "Nodi-> album che contendono almeno un brano del genere selezionato."
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """SELECT distinct a.*
                    from Track t, Album a
                    where t.GenreId =%s and t.AlbumId =a.AlbumId """

        cursor.execute(query,(c,))
        res = []
        for row in cursor:
            res.append(Album(**row))

        cursor.close()
        cnx.close()
        return res

    @staticmethod
    def get_archi(c):
        """Arco= se una stessa fattura contiene brani contenenti ad entrambi gli album
peso numero di fatture distinte che contengono i due album"""
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """SELECT distinct least(t.AlbumId , t1.AlbumId) as id1, greatest(t.AlbumId , t1.AlbumId) as id2, count(distinct il.InvoiceId) as peso
                    from InvoiceLine il, InvoiceLine il1, Track t, Track t1
                    where t.GenreId=%s and t1.GenreId =%s and il.InvoiceId=il1.InvoiceId and t.TrackId=il.TrackId and
                    t1.TrackId=il1.TrackId and t1.TrackId!=t.TrackId and t.AlbumId<t1.AlbumId and il.InvoiceLineId !=il1.InvoiceLineId 
                    group by  least(t.AlbumId , t1.AlbumId ), greatest(t.AlbumId , t1.AlbumId)

                                """

        cursor.execute(query, (c,c))
        res = []
        for row in cursor:
            res.append((row["id1"],row["id2"], row["peso"]))

        cursor.close()
        cnx.close()
        return res
