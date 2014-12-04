import os
import sqlite3
from urllib.request import urlopen
import urllib.parse
import urllib.request
import csv
import io
import datetime

DB_PATH = "IntelliStock.sqlite"
ARCHIVE_BASE_URL = "http://hunyadym.hu/stock"
ARCHIVE_LIST = "list.php"

conn = None

def setup_database():
    if os.path.isfile(DB_PATH):
        return
    
    global conn
    conn = sqlite3.connect(DB_PATH)
    conn.execute('''CREATE TABLE StockData (
                    paper_name TEXT,
                    date INTEGER,
                    time INTEGER,
                    close REAL,
                    volume INTEGER);''')
    conn.commit()
    initialize_database()
    
    conn.commit()

def initialize_database():
    urlpath = urlopen(ARCHIVE_BASE_URL + "/" + ARCHIVE_LIST)
    
    files = urlpath.read().decode('utf-8').split()

    for f in files:
        load_from_csv(f)
        
def load_from_csv(csv_path):
    urlpath = urlopen(ARCHIVE_BASE_URL + "/" + csv_path)
    print(csv_path)
    
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
            
            conn.execute("INSERT INTO StockData VALUES (?, ?, ?, ?, ?)",
                     (paper_name, date, time, close, volume))
        except ValueError:
            continue


setup_database()
