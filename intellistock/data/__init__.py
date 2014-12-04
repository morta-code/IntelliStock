import os
import sqlite3
from urllib.request import urlopen
import csv
import io
from data import data

ARCHIVE_BASE_URL = "http://hunyadym.hu/stock"
ARCHIVE_LIST = "list.php"

def setup_database():
    if os.path.isfile(data.DB_PATH):
        data.conn = sqlite3.connect(data.DB_PATH)
        return
    
    global conn
    data.conn = sqlite3.connect(data.DB_PATH)
    data.conn.execute('''CREATE TABLE StockData (
                    id INTEGER PRIMARY KEY,
                    paper_name TEXT,
                    datetime INTEGER,
                    close REAL,
                    volume INTEGER);''')
                    
    data.conn.execute('''CREATE TABLE Stocks (
                    paper_name TEXT);''')
    data.conn.commit()
    initialize_database()
    
    persist_stocks()
    
    data.conn.commit()

def initialize_database():
    urlpath = urlopen(ARCHIVE_BASE_URL + "/" + ARCHIVE_LIST)
    
    files = urlpath.read().decode('utf-8').split()

    for f in files:
        load_from_csv(f)
        return
        
def load_from_csv(csv_path):
    global stocks    
    
    urlpath = urlopen(ARCHIVE_BASE_URL + "/" + csv_path)
    
    file = urlpath.read().decode('utf-8')
    
    csv_reader = csv.reader(io.StringIO(file))
    next(csv_reader) #skip header
    
    for row in csv_reader:
        try:
            paper_name = row[0]
            date = int(row[2])
            time = int(row[3])
            close = float(row[4])
            volume = int(row[5])
            
            data.conn.execute("INSERT INTO StockData VALUES (?, ?, ?, ?, ?)",
                     (None, paper_name, date * 1000000 + time, close, volume))
                     
            if paper_name not in data.stocks:
                data.stocks.add(paper_name)
                
        except ValueError:
            continue

def persist_stocks():
    for stock in data.stocks:
        data.conn.execute("INSERT INTO Stocks VALUES (?)", [stock])

setup_database()
