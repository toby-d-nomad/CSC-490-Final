from connection.controller import connection


def getView(stored_procs):
    try:
        con=connection()
        cur=con.cursor()
        stored_proc=stored_procs
        cur.execute(stored_proc)
        result=cur.fetchall()
        cur.close()
        con.commit()
        con.close()
        return result
    except Exception as e:
        error=e
        return error
    
def CRUDFunction(stored_procs, param):
    try:
        con=connection()
        cur=con.cursor()
        stored_proc=stored_procs
        para=param
        cur.execute(stored_proc, para)
        cur.close()
        con.commit()
    except Exception as e:
        error=e
        return error