from database.DB_connect import DBConnect
from model.invoice import Invoice
from model.Playlist import Playlist

class DAO():
    @staticmethod
    def get_generi():
        "mi servono tutti i clienti"
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """select c.*
                from Customer c"""
        cursor.execute(query)

        res = []
        for row in cursor:
            res.append(Customers(**row))

        cursor.close()
        cnx.close()
        return res

    @staticmethod
    def get_nodi(c):
        """Nodi----> fatture del cliente"""
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = f"""
                SELECT i.*
                from Invoice i
                where i.CustomerId =%s"""

        cursor.execute(query,(c,))
        res = []
        for row in cursor:
            res.append(Invoice(**row))

        cursor.close()
        cnx.close()
        return res


    @staticmethod
    def get_archi(c,b):
        """ Archi---> se la distanza temporale tra i due acquisti è >0 e minore o uguale a k"""
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = f"""select i.InvoiceId id1, i1.InvoiceId as id2, (i.Total +i1.Total )/datediff(i.InvoiceDate,i1.InvoiceDate) as peso
                    from Invoice i, Invoice i1 
                    where i.CustomerId =i1.CustomerId and i.InvoiceId != i1.InvoiceId and  i.CustomerId =%s and 
                    datediff(i.InvoiceDate,i1.InvoiceDate)>0 and  datediff(i.InvoiceDate,i1.InvoiceDate)<=%s"""
        cursor.execute(query,(c,b))
        res = []
        for row in cursor:
            res.append((row["id1"],row["id2"], row["peso"]))
        cursor.close()
        cnx.close()
        return res
