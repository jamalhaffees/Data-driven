import pyodbc

server = 'LAPTOP-3G5OJ9V6\SQLEXPRESS'
database = 'SwagLabs'
query = 'SELECT username, userpassword, assertion FROM users'

def get_query_data(server, database, query):
    db = pyodbc.connect('Driver=(SQL Server);Server=%s;Database=%s;Trusted_Connection=yes;'% (server, database))
    Cursor=db.cursor()
    Cursor.execute(query)
    return Cursor.fetchall()

login_form_parameters = get_query_data(server, database, query)