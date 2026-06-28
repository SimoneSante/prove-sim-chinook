from database.DB_connect import DBConnect
from model.cantanti import Cantante

class DAO():
    @staticmethod
    def get_generi():
        "Playlist"
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """SELECT distinct c.Country 
                    from Customer c
                    """
        cursor.execute(query)

        res = []
        for row in cursor:
            res.append(str(row))

        cursor.close()
        cnx.close()
        return res

    @staticmethod
    def get_nodi(c):
        """Nodi---> artisti della playlist selezionata"""
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = f"""with Track_ridotto as(
                select t.TrackId as tid, t.AlbumId as aid
                from Track t
                )
                select distinct art.*
                FROM Artist art, Album a, Track_ridotto t, PlaylistTrack pt
                where pt.PlaylistId = %s and pt.TrackId =t.tid and a.AlbumId =t.aid and a.ArtistId =art.ArtistId """

        cursor.execute(query,(c,))
        res = []
        for row in cursor:
            res.append(Cantante(**row))

        cursor.close()
        cnx.close()
        return res


    @staticmethod
    def get_archi(c):
        """Archi--> due artisti sono collegati se almeno 2 playlist li contengono"""
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = f"""with playlist_selezionata as (with Track_ridotto as(
                    select t.TrackId as tid, t.AlbumId as aid
                    from Track t
                    )
                    select distinct a.ArtistId as artid
                    FROM Album a, Track_ridotto t, PlaylistTrack pt
                    where pt.PlaylistId = %s and pt.TrackId =t.tid and a.AlbumId =t.aid )
                    
                    select least(a.ArtistId,a1.ArtistId) as id1, greatest(a.ArtistId,a1.ArtistId) as id2, count(distinct pt.PlaylistId) as peso
                    from Album a, Track t, PlaylistTrack pt, playlist_selezionata ps, playlist_selezionata ps1, Album a1, Track t1, PlaylistTrack pt1
                    where pt.PlaylistId!=%s and pt.PlaylistId=pt1.PlaylistId and pt.TrackId!= pt1.TrackId and pt.TrackId=t.TrackId and pt1.TrackId=t1.TrackId and
                    t.AlbumId=a.AlbumId and t1.AlbumId=a1.AlbumId and a.ArtistId=ps.artid and a1.ArtistId=ps1.artid and a.ArtistId!=a1.ArtistId
                    group by least(a.ArtistId,a1.ArtistId), greatest(a.ArtistId,a1.ArtistId)"""
        cursor.execute(query,(c,c))
        res = []
        for row in cursor:
            res.append((row["id1"],row["id2"], row["peso"]))
        cursor.close()
        cnx.close()
        return res
