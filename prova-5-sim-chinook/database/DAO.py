from database.DB_connect import DBConnect
from model.genere import Genere
from model.Playlist import Playlist


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
        "Vertici-> playlist che contengono almeno un brano del genere selezionati"
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """SELECT distinct pt.PlaylistId as id
                    from PlaylistTrack pt, Track t
                    where pt.TrackId =t.TrackId and t.GenreId=%s"""

        cursor.execute(query, (c,))
        res = []
        for row in cursor:
            res.append(row["id"])

        cursor.close()
        cnx.close()
        return res

    @staticmethod
    def get_info_nodi():
        "informazioni dei nodi:"
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """select distinct p.*
                    from playlistTrack pt, Playlist p
                    where pt.PlaylistId=p.PlaylistId"""

        cursor.execute(query)
        mappa = {}
        for row in cursor:
            p = Playlist(**row)
            mappa[p.PlaylistId] = p

        cursor.close()
        cnx.close()
        return mappa

    @staticmethod
    def get_archi(c):
        """ Archi: se 2 playlist condividono almeno un brano(quindi uguale) che appartiene allo stesso genere richiesto
                Peso: numero di brani condivisi"""
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """with Track_ridotto as (Select t.TrackId as tid, t.GenreId as genere
                    from Track t)

                    SELECT least(pt.PlaylistId , pt1.PlaylistId ) as id1, greatest(pt.PlaylistId , pt1.PlaylistId ) as id2, count(distinct pt.TrackId) as peso
                    FROM PlaylistTrack pt, PlaylistTrack pt1,Track_ridotto tr, Track_ridotto tr1 
                    where pt.PlaylistId !=pt1.PlaylistId and pt.TrackId =tr.tid and tr.genere=%s and pt1.TrackId =tr1.tid and tr1.genere=%s and
                    pt.TrackId =pt1.TrackId 
                    group by  least(pt.PlaylistId , pt1.PlaylistId ), greatest(pt.PlaylistId , pt1.PlaylistId )"""

        cursor.execute(query, (c, c))
        res = []
        for row in cursor:
            res.append((row["id1"], row["id2"], row["peso"]))

        cursor.close()
        cnx.close()
        return res

    @staticmethod
    def get_priority(c):
        """Criterio di direzione degli archi:
            gli archi vanno dal nodo con più brani di quel genere a quello che ne ha meno"""
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """with Track_ridotto as (Select t.TrackId as tid, t.GenreId as genere
                from Track t)

                select  pt.PlaylistId as idpla, count(distinct tr.tid) as priority
                from Track_ridotto tr, PlaylistTrack pt
                where tr.tid=pt.TrackId and tr.genere=%s
                group by pt.PlaylistId 
                """

        cursor.execute(query, (c,))
        res = {}
        for row in cursor:
            res[row["idpla"]] = row["priority"]

        cursor.close()
        cnx.close()
        return res

