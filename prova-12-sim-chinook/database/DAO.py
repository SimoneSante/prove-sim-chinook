from database.DB_connect import DBConnect
from model.meditype import Mediatype

class DAO():
    @staticmethod
    def get_generi():
        "Paese"
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
        """Nodi --> Mediatype comprati da clienti del paese selezionato"""
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = f"""
                with Customer_ridotto as (
                SELECT c.CustomerId as cid
                from Customer c
                where c.Country ="{c}")
                select distinct mt.*
                from MediaType mt, Track t, InvoiceLine il, Invoice i,  Customer_ridotto cr
                where mt.MediaTypeId =t.MediaTypeId  and t.TrackId =il.TrackId  and il.InvoiceId = I.InvoiceId and cr.cid 
                and cr.cid =i.CustomerId  """

        cursor.execute(query)
        res = []
        for row in cursor:
            res.append(Mediatype(**row))

        cursor.close()
        cnx.close()
        return res


    @staticmethod
    def get_archi(c):
        """ Archi---> se almeno un cluente ha acquistato brani di entrambi"""
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = f"""with Customer_ridotto as (
                    SELECT c.CustomerId as cid
                    from Customer c
                    where c.Country ="{c}")
                    select distinct least(mt.MediaTypeId, mt1.MediaTypeId) as id1, greatest(mt.MediaTypeId, mt1.MediaTypeId) as id2, count(distinct cr.cid ) as peso
                    from MediaType mt, Track t, InvoiceLine il, Invoice i,  Customer_ridotto cr, MediaType mt1, Track t1, InvoiceLine il1, Invoice i1,  Customer_ridotto cr1
                    where mt.MediaTypeId =t.MediaTypeId  and t.TrackId =il.TrackId  and il.InvoiceId = I.InvoiceId and cr.cid 
                    and cr.cid =i.CustomerId  and mt1.MediaTypeId =t1.MediaTypeId  and t1.TrackId =il1.TrackId  and il1.InvoiceId = I1.InvoiceId and cr1.cid 
                    and cr1.cid =i1.CustomerId and mt.MediaTypeId !=mt1.MediaTypeId and cr.cid =cr1.cid 
                    group by least(mt.MediaTypeId, mt1.MediaTypeId), greatest(mt.MediaTypeId, mt1.MediaTypeId)"""
        cursor.execute(query)
        res = []
        for row in cursor:
            res.append((row["id1"],row["id2"], row["peso"]))
        cursor.close()
        cnx.close()
        return res
