from database.DB_connect import DBConnect
from model.genere import Genere
from model.track import Track

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
        query = """select t.*
                    from Track t
                    where t.GenreId =%s"""

        cursor.execute(query,(c,))
        res = []
        for row in cursor:
            res.append(Track(**row))

        cursor.close()
        cnx.close()
        return res

    @staticmethod
    def get_archi(c):
        """Arco= se una stessa fattura contiene brani contenenti ad entrambi gli album
peso numero di fatture distinte che contengono i due album"""
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """with validi as(select t.TrackId as id 
                    from Track t
                    where t.GenreId =%s)
                    
                    select distinct least(pl.TrackId, pl1.TrackId) as id1, greatest(pl.TrackId, pl1.TrackId) as id2, count(pl.PlaylistId) as peso
                    from PlaylistTrack pl, PlaylistTrack pl1, validi v, validi v1
                    where pl.PlaylistId =pl1.PlaylistId  and pl.TrackId < pl1.TrackId and pl.TrackId=v.id and pl1.TrackId=v1.id
                    group by  least(pl.TrackId, pl1.TrackId), greatest(pl.TrackId, pl1.TrackId)"""

        cursor.execute(query, (c,))
        res = []
        for row in cursor:
            res.append((row["id1"],row["id2"], row["peso"]))

        cursor.close()
        cnx.close()
        return res

