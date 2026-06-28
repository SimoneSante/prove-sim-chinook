from database.DB_connect import DBConnect
from model.dipendente import Dipendente
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
        """Nodi---> dipendenti che supportano almeno un cliente del
paese selezionato"""
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = f"""with customer_ridotta as (SELECT distinct c.CustomerId as cid,  c.SupportRepId idDipendente
                    from Customer c
                    where c.Country ="{c}")
                    Select distinct e.*
                    from customer_ridotta cr, Employee e
                    where e.EmployeeId=cr.idDipendente"""

        cursor.execute(query)
        res = []
        for row in cursor:
            res.append(Dipendente(**row))

        cursor.close()
        cnx.close()
        return res

    @staticmethod
    def get_archi(c):
        """Archi---> due dipendenti sono collegati se almeno due clienti diversi
che sono legati a due dipendenti hanno acquistato tracce dello stesso genere"""
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = f"""with customer_ridotta as (SELECT distinct c.CustomerId as cid,  c.SupportRepId idDipendente
                    from Customer c
                    where c.Country ="{c}"),
                    Invoice_ridotto as(
                    select i.InvoiceId as Iid, i.CustomerId as cid
                    FROM Invoice i),
                    track_ridotto as (
                    select t.TrackId as tid, t.GenreId gid
                    from Track t)
                    SELECT distinct least(cr.idDipendente, cr1.idDipendente) as id1, greatest(cr.idDipendente, cr1.idDipendente) as id2
                    from customer_ridotta cr, customer_ridotta cr1, Invoice_ridotto ir, Invoice_ridotto ir1, InvoiceLine il, InvoiceLine il1, track_ridotto tr, track_ridotto tr1
                    where cr.cid!=cr1.cid and  cr.idDipendente!=cr1.idDipendente and ir.cid=cr.cid and ir1.cid=cr1.cid
                    and ir.Iid=il.InvoiceId and ir1.Iid=il1.InvoiceId and il1.TrackId=tr.tid and il.TrackId=tr.tid
                    and tr.gid=tr1.gid
                    group by least(cr.idDipendente, cr1.idDipendente) , greatest(cr.idDipendente, cr1.idDipendente)

                                """

        cursor.execute(query)
        res = []
        for row in cursor:
            res.append((row["id1"], row["id2"]))

        cursor.close()
        cnx.close()
        return res

    @staticmethod
    def get_pesi(c):
        """Priority----> PER OGNI DIPENDENTE SI CALCOLA IL FATTURATO SUPPORTATO COME SOMMA DELLE INVOICE DEI
CLIENTI SUPPORTATOALTER
"""
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = f"""with customer_ridotta as (SELECT distinct c.CustomerId as cid,  c.SupportRepId idDipendente
                    from Customer c
                    where c.Country ="{c}")
                    
                    SELECT cr.idDipendente as idD, sum(i.Total) as peso
                    FROM customer_ridotta cr, Invoice i
                    where cr.cid =i.CustomerId 
                    group by cr.idDipendente"""

        cursor.execute(query)
        res = {}
        for row in cursor:
            res[row["idD"]] = row["peso"]

        cursor.close()
        cnx.close()
        return res

