import bs4
import json
import uuid
import psycopg2
import pandas as pd
import yfinance as yf
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
from influxdb import InfluxDBClient
from dbconnector import get_DBConnection

def update_symbols_db():
    myurl = "http://markets.cboe.com/us/equities/market_statistics/listed_symbols/"

    # opening up connection & grabbing the page
    uClient = uReq(myurl)
    page_html = uClient.read()
    # close connection
    uClient.close()

    page_soup = soup(page_html, "html.parser")
    lines = page_soup.findAll("td", {"class":"text--left"})

    try:
        connection = get_DBConnection()
        cursor = connection.cursor()

        # Provide a valid SQL statement. In this case a DELETE statement
        deleteStatement     = "DELETE FROM core_symbol"
        # Delete obsolete rows
        cursor.execute(deleteStatement)
        connection.commit()
        cursor.close()
        connection.close()

        connection2 = get_DBConnection()
        cursor2 = connection2.cursor()
        run_once = 0
        keyexample = {}

        for line in lines:
            dictator = {}
            symbol_text = line.a.text
            symbol = yf.Ticker(symbol_text)
            dictator = symbol.info
            if(run_once == 0):
                keyexample = dictator

            if(bool(dictator)):
                for key in sorted(dictator.keys()):
                    if key not in keyexample.keys():
                        del dictator[key]

                if "52WeekChange" in dictator:
                    dictator["weekchange"] = dictator.pop("52WeekChange")
                if "state" in dictator:
                    dictator["state_"] = dictator.pop("state")
                if "open" in dictator:
                    dictator["open_"] = dictator.pop("open")
                if "underlyingsymbol" in dictator:
                    del dictator["underlyingsymbol"]
                
                
                dictator["id"] = str(uuid.uuid4())
                dictator["symbol_name"] = symbol_text

                keys = dictator.keys()
                columns = ','.join(keys)
                values = ','.join(['%({})s'.format(k) for k in keys])
                insert = 'insert into core_symbol ({0}) values ({1})'.format(columns, values)
                #print(cursor.mogrify(insert, dictator))
                cursor2.execute(cursor2.mogrify(insert, dictator))

                connection2.commit()
                count = cursor2.rowcount
                print (count, "Record inserted successfully into core_symbol table")

            
            else:
                print("Empty dict")
            

    except (Exception, psycopg2.Error) as error :
        if(connection2):
            print(dictator)
            print("Failed to insert record into core_symbol table", error)

    finally:
        #closing database connection.
        if(connection2):
            cursor2.close()
            connection2.close()
            print("PostgreSQL connection is closed")

    try:

        connection3 = get_DBConnection()
        cursor3 = connection3.cursor()
        postgreSQL_select_Query = "select symbol_name from core_symbol"
        cursor3.execute(postgreSQL_select_Query)
        symbol_records = cursor3.fetchall() 
        cursor3.close()
        connection3.close()

        connection4 = get_DBConnection()
        cursor4 = connection4.cursor()

        for line in lines:
            symbol_text = line.a.text
            if symbol_text not in symbol_records:
                postgres_insert_query = """ INSERT INTO core_symbol (ID, symbol_name) VALUES (%s,%s)"""
                record_to_insert = (str(uuid.uuid4()), symbol_text)
                cursor4.execute(postgres_insert_query, record_to_insert)

                connection4.commit()
            else:
                print(symbol_text, "in list")
    
    except (Exception, psycopg2.Error) as error :
        if(connection4):
            print("Failed to insert record into core_symbol table", error)

    finally:
        #closing database connection.
        if(connection4):
            cursor4.close()
            connection4.close()
            print("PostgreSQL connection is closed")
    