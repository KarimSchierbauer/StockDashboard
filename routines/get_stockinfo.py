import os
import pandas as pd
import yfinance as yf
from dbconnector import get_DBConnection
import psycopg2
import psycopg2.extras as extras
from io import StringIO

def getstockprice():
    connection = get_DBConnection()
    cursor = connection.cursor()
    postgreSQL_select_Query = "select symbol_name from core_symbol"
    cursor.execute(postgreSQL_select_Query)
    symbol_records = cursor.fetchall() 

    for row in symbol_records:
        conn = get_DBConnection()
        symbol = yf.Ticker(row[0])
        multidf = symbol.history(period="max")
        multidf.insert(loc=0, column='symbol', value=row[0])
        multidf.reset_index(inplace=True)
        copy_from_stringio(conn, multidf, "core_stock")

def copy_from_stringio(conn, df, table):
    """
    Here we are going save the dataframe in memory 
    and use copy_from() to copy it to the table
    """
    # save dataframe to an in memory buffer
    buffer = StringIO()
    df.to_csv(buffer, index_label='id', header=False)
    buffer.seek(0)
    
    cursor = conn.cursor()
    try:
        cursor.copy_from(buffer, table, sep=",")
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        #os.remove(df)
        print("Error: %s" % error)
        conn.rollback()
        cursor.close()
        return 1
    print("copy_from_stringio() done")
    cursor.close()
