import psycopg2

def get_DBConnection():
    
    conn = psycopg2.connect(
        host="192.168.23.141",
        database="stockdashboard",
        user="stockdashboard",
        password="stockdashboard")
    
    return conn
