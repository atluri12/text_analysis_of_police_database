# Text Analysis of Norman Police Database

In this project a PDF file is downloaded from the Norman Police Deparatment and the data regarding the arrests is inserted into a SQLite database named 'normanpd.db'. The downloaded PDF file contains the regular arrest reports in the Norman area. The PDF file is cleaned using python and the data is formatted into the form of rows. A random row can be retrieved from the database after inserting the rows into the database. The project is compatible with Python 3.7.2.

### main.py
The main.py file is executed from the *text_analysis_of_police_database* folder after cloning it into the local system using the following command

`pipenv run python project0/main.py --arrests url`

The main.py file takes one argument which is the *url* of the PDF file. The project0 file is imported into main.py and the functions **dataDownload(url), dataExtract(tempFile), dbCreate(), dbInsert(db, incidents)** and **dbStatus(db)** are called with the respective arguments for the execution.

### project0.py
The project0.py file contains the methods to download PDF, extract data, create a database, insert data into database and retrieve a random record. The detailed Functioning of the functions mentioned is as follows:
* #### dataDownload(url)
    The *dataDownload* function takes one argument which is the *url* given to the main.py file. This function opens the url using *urlopen* function from the *urllib.request* package which is exclusive to python 3.7.2. The data is downloaded from the url in the form of *bytes*. This bytes data is stored into a temporary file which is created using the *tempfile* package. The *tempFile = tempfile.TemporaryFile()* statement creates a temporary file with the file pointer tempFile. The bytes data is written into the tempFile and the tempFile pointer is returned to the main.py file.
* #### dataExtract(tempFile)
    The *dataExtract* function takes the tempFile as argument. The data within the temporary file is extracted using the *PyPDF2* package. *pageData = PyPDF2.PdfFileReader(tempFile).getPage(0).extractText()* statement is used to extract the data in the form of a list from the bytes data present in the temporary file. The *PdfFileReader* function of the *PyPDF2* package retrieves the data and the *extractText* function gets the data in the form of text. The data obtained is not formatted and contains excess data which is not required.
    
    The data in a single row can be present in multiple lines, so the excess '\n' must be replaced with a space so as to regard them a single column after parsing. Carefully observing the pattern ' \n' (single space followed by a new line) is replaced with a single space using regular expressions.
    The data is now split using ';' as the delimiter since every row in the PDF file ends with a ';'. The *split()* function can be used to split the data using the delimiter given as the argument to the function (the default delimiter is space).
    
    The excess data at the end is removed by using the *del* function of the list. The first row contains excess information which is the headers of the table. This information is removed by splitting the first row on '\n' and then removing the first 12 elements of the list. The first row is again joined together to maintain the formatting with the other rows.
    Some of the PDF's contain empty spaced in the columns *city, state and zipcode* if the arrestee is a *HOMELESS*. So the columns *arrestee address, city, state and zipcode* are joined together by using the reference from 'https://stackoverflow.com/questions/1142851/merge-some-list-items-in-a-python-list' as follows:
    ```python
    address = ', '.join(pageData[i][6:10])
    pageData[i][6:10] = [address]
    ```
    
    The formatted data is present in the form of list of lists i.e. a list containing the rows present in the PDF file. This formatted data is returned to the main.py file.
* #### dbCreate()
    A database is created using the function *dbCreate*. The database is named *normanpd.db* and contains one table names *arrests*. The *sqlite3* package documented in 'https://docs.python.org/2/library/sqlite3.html' is used to create a sqlite database using python 3.7.2. The sqlite3 package opens the connection creating a normanpd.db database file and the *cursor* and *execute* functions are used to execute the queries within the database from python. Initially the database is checked for any table named arrests and if found the table is dropped. A table arrests is created using the following create statement
    
    `CREATE TABLE IF NOT EXISTS arrests (arrest_time TEXT, case_number TEXT, arrest_location TEXT, offense TEXT, arrestee_name TEXT, arrestee_birthday TEXT, arrestee_address TEXT, status TEXT, officer TEXT);`

    The changes are committed to the database using the *commit* function and if any error caught it will be handled by the try-except statement. The name of the created database is returned to the main.py file.
* #### dbInsert(db, incidents)
    The *dbInsert* function takes two arguments which are the database name from dbCreate function and the incidents data from dataExtract function. This function opens a connection to the database 'normanpd.db' and inserts the rows from the incidents data into the database. The insert query is as follows

    `insertQuery = 'INSERT INTO arrests VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);'`
    
    This query is run for all the rows within the incidents data using a for loop to execute the query as follows

    `point.execute(insertQuery, incidents[i])`

    The changes are committed to the database after the insertion of the data into the database.
* #### dbStatus(db)
    This function *dbStatus* takes one argument which is the database name and retrieves any one random record from the database. The function uses *sqlite3* package to connect to the database. The total number of rows in the table is retrieved and then a random number is generated within the limit (0, rowcount-1). The random number is used to retrieve the row with that number and join the elements within the row using a *thorn*. The thorn is a latin character so it can be represented using *'\u00FE'* as shown in 'http://www.fileformat.info/info/unicode/char/00FE/index.htm'. The joined string is printed to the console and returned to the main.py file.

### setup.py and setup.cfg
The setup.py file is required for finding the packages within the project during the execution. It finds the packages automatically. 

The setup.cfg file is required for running the pytest command to perform tests on the program.

### Pipfile and Pipfile.lock
A virtual environment is created for the execution of this project. This environment is created using *pipenv*c command as following

`pipenv install --python 3.7.2`

This will install a virtual environment with python 3.7.2 within it. Any extra packages such as *PyPDF2*, *bs4* and *pytest* used within the project needs to be installed within the python virtual environment as follows

`pipenv install PyPDF2`

`pipenv install bs4`

`pipenv install pytest`

### test_data.py
The test_data.py file contains the test cases designed to test the functioning of the project0. The test_data.py file when executed runs every test case with the project0 and returns the output of failed and passed test cases. The test_data.py file contains one other function *getUrl()* which makes use of the *BeautifulSoup* package to extract the required arrests url from the norman police department website.
* #### getUrl()
    The *getUrl* function takes no arguments. The getUrl function uses the *urllib.request* package to download the data from the norman police department website ('http://normanpd.normanok.gov/node/657/') in the form of bytes and then the *BeautifulSoup* package is used with the *html.parser* to extract all the url's present within the website as shown in 'https://stackoverflow.com/questions/1080411/retrieve-links-from-web-page-using-python-and-beautifulsoup'. The *re* package is used for applying regular expressions to match the url's with *'Arrest Summary'* keyword and the first matche url is returned by the function.
    ```python
    pattern = re.compile(r'.*(Arrest%20Summary.pdf)')
    link = re.match(pattern, tag['href'])
    ```

There are five test cases specified one each for every function in the project0.py file. The test cases are as follows:
* #### test_data_download()
    The *test_data_download* test case is used to test the *dataDownload* function of the project0.py file. This function executes the dataDownload function and retrieves the returned temporary file pointer. The temporary file is checked if it contains bytes data type using the *isinstance()* function. The isinstance function takes two arguments which are the string or the variable and the data type as referenced from 'https://www.quora.com/What-is-the-Pythonic-way-to-check-if-type-of-a-variable-is-string'. It checks if the first variable is an instance or of the same data type as the second and returns True if it is the same data type and False if it is not. The assert statement tests the condition and triggers an error if the condition is false.
    
    `assert isinstance(data.read(), bytes) == True`

* #### test_data_extract()
    The *test_data_extract* function is used to test the *dataExtract* funtion of the project0.py file. This function executes the function and retrieves the rows data from the dataExtract function. The assert statement in the function checks if the returned data is a list of list and if each element of the list is of length 9.
    ```python
    assert isinstance(rows, list) == True
    for i in range(len(rows)):
        assert isinstance(rows[i], list) == True
        assert len(rows[i]) == 9
    ```

* #### test_create_table()
    The *test_create_table* function is used to test the *dbCreate* function of the project0.py file. This function connects to the database using the database name from the dbCreate function and then retrieves the number of tables with the name = 'arrests' present in the database. This is done using the query as shown in 'https://stackoverflow.com/questions/1601151/how-do-i-check-in-sqlite-whether-a-table-exists'
    
    `SELECT COUNT(*) FROM sqlite_master WHERE type = 'table' and name = 'arrests';`

    The function checks if there exists one table with the name arrests using the assert statement and returns true if it satisfies the condition.
    
    `assert value[0] == 1`

* #### test_insert_data()
    The *test_insert_data* function is used to test the *dbInsert* function of the project0.py file. This function executes the dbInsert function with the parameters db (database name) and rows (rows data from dataExtract). The function connects to the database after the execution of the dbInsert function and retrieves the total number of rows present within the database. The assert statement is used to check if the number of rows obtained from datExtract function is equal to the number of rows inserted into the database.

    `assert inserted[0] == len(rows)`

* #### test_status()
    The *test_status* function is used to test the *dbStatus* function of the project0.py file. This function executes the functions dataDownload, dataExtract, dbCreate, dbInsert and dbStatus functions to get the random record returned by the dbStatus function. The assert statement checks if the returned variable is of the data type string and if the returned row have 9 columns after splitting with the *thorn* character.
    ```python
    assert isinstance(outRow, str) == True
    assert len(splitRow) == 9
    ```
