import pytest
import urllib.request
from bs4 import BeautifulSoup
import re
import sqlite3

import project0

from project0 import project0

def getUrl():
    urlData = urllib.request.urlopen('http://normanpd.normanok.gov/node/657/')
    soupData = BeautifulSoup(urlData, features='html.parser')
    for tag in soupData.find_all('a', href = True):
        pattern = re.compile(r'.*(Arrest%20Summary.pdf)')
        link = re.match(pattern, tag['href'])
        if(link is not None):
            url = tag['href']
            break
    defUrl = 'http://normanpd.normanok.gov'
    url = defUrl + url
    return url

def test_data_download():
    url = getUrl()
    data = project0.dataDownload(url)
    assert isinstance(data.read(), bytes) == True

def test_data_extract():
    url = getUrl()
    data = project0.dataDownload(url)
    rows = project0.dataExtract(data)
    assert isinstance(rows, list) == True
    for i in range(len(rows)):
        assert isinstance(rows[i], list) == True
        assert len(rows[i]) == 9
        
def test_create_table():
    dname = project0.dbCreate()
    dconn = sqlite3.connect(dname)
    dpoint = dconn.cursor()
    query = "SELECT COUNT(*) FROM sqlite_master WHERE type = 'table' and name = 'arrests';"
    dpoint.execute(query)
    value = dpoint.fetchone()
    assert value[0] == 1

def test_insert_data():
    url = getUrl()
    data = project0.dataDownload(url)
    rows = project0.dataExtract(data)
    dname = project0.dbCreate()
    project0.dbInsert(dname, rows)
    dconn = sqlite3.connect(dname)
    dpoint = dconn.cursor()
    dpoint.execute('SELECT COUNT(*) FROM arrests;')
    inserted = dpoint.fetchone()
    assert inserted[0] == len(rows)

def test_status():
    url = getUrl()
    data = project0.dataDownload(url)
    rows = project0.dataExtract(data)
    dname = project0.dbCreate()
    project0.dbInsert(dname, rows)
    outRow = project0.dbStatus(dname)
    splitRow = outRow.split('\u00FE')
    assert isinstance(outRow, str) == True
    assert len(splitRow) == 9
