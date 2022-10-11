# These libraries are pre-installed in SN Labs. If running in another environment please uncomment lines below to install them:
# !pip install --force-reinstall ibm_db==3.1.0 ibm_db_sa==0.3.3
# Ensure we don't load_ext with sqlalchemy>=1.4 (incompadible)
# !pip uninstall sqlalchemy==1.4 -y && pip install sqlalchemy==1.3.24
# !pip install ipython-sql
import ibm_db

#Replace the placeholder values with the actuals for your Db2 Service Credentials
dsn_driver = "{IBM DB2 ODBC DRIVER}"
dsn_database = "database"            # e.g. "BLUDB"
dsn_hostname = "hostname"            # e.g.: "dashdb-txn-sbox-yp-dal09-04.services.dal.bluemix.net"
dsn_port = "port"                    # e.g. "50000" 
dsn_protocol = "protocol"            # i.e. "TCPIP"
dsn_uid = "username"                 # e.g. "abc12345"
dsn_pwd = "password"                 # e.g. "7dBZ3wWt9XN6$o0J"
dsn_security = "SSL"              #i.e. "SSL"

#Create database connection
#DO NOT MODIFY THIS CELL. Just RUN it with Shift + Enter
dsn = (
    "DRIVER={0};"
    "DATABASE={1};"
    "HOSTNAME={2};"
    "PORT={3};"
    "PROTOCOL={4};"
    "UID={5};"
    "PWD={6};"
    "SECURITY={7};").format(dsn_driver, dsn_database, dsn_hostname, dsn_port, dsn_protocol, dsn_uid, dsn_pwd,dsn_security)

try:
    conn = ibm_db.connect(dsn, "", "")
    print ("Connected to database: ", dsn_database, "as user: ", dsn_uid, "on host: ", dsn_hostname)

except:
    print ("Unable to connect: ", ibm_db.conn_errormsg() )

#Lets first drop the table INSTRUCTOR in case it exists from a previous attempt
dropQuery = "drop table INSTRUCTOR"

#Now execute the drop statment
dropStmt = ibm_db.exec_immediate(conn, dropQuery)

# Don't worry if you get error (if table DOESN'T exist)
#Construct the Create Table DDL statement 
createQuery = "create table INSTRUCTOR(id INTEGER PRIMARY KEY NOT NULL, fname VARCHAR(20), lname VARCHAR(20), city VARCHAR(20), ccode CHARACTER(2))"

createStmt = ibm_db.exec_immediate(conn, createQuery)

#Construct the query 
insertQuery = "INSERT INTO INSTRUCTOR(id, fname, lname, city, ccode) VALUES(1,'Rav','Ahuja','TORONTO', 'CA'),(2,'Raul','Chong','Markham','CA'),(3,'Hima','Vasudevan','Chicago','US')"

#execute the insert statement
insertStmt = ibm_db.exec_immediate(conn, insertQuery)

#Construct the query that retrieves all rows from the INSTRUCTOR table
selectQuery = "select * from INSTRUCTOR"

#Execute the statement
selectStmt = ibm_db.exec_immediate(conn, selectQuery)

#Fetch the Dictionary (for the first row only) - replace ... with your code
ibm_db.fetch_both(selectStmt)

#Fetch the rest of the rows and print the ID and FNAME for those rows
while ibm_db.fetch_row(selectStmt) != False:
   print (" ID:",  ibm_db.result(selectStmt, 0), " FNAME:",  ibm_db.result(selectStmt, "FNAME"))

# Update Rav's city to MOOSETOWN
alter_statement = "UPDATE INSTRUCTOR SET city = 'MOOSETOWN' WHERE fname = 'Rav'"
stmt = ibm_db.exec_immediate(conn,alter_statement)

## AND NOW PANDAS

import pandas
import ibm_db_dbi
#connection for pandas
pconn = ibm_db_dbi.Connection(conn)
#query statement to retrieve all rows in INSTRUCTOR table
selectQuery = "select * from INSTRUCTOR"

#retrieve the query results into a pandas dataframe
pdf = pandas.read_sql(selectQuery, pconn)

#print just the LNAME for first row in the pandas data frame
pdf.LNAME[0]

#print the entire data frame
pdf

#use the shape method to see how many rows and columns are in the dataframe
pdf.shape  # (3,5)

# Close connection
ibm_db.close(conn)

#NOTE: lowercase column headings given in sample code; not my preferred option.
