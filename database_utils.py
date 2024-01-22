import mysql.connector
def DATABASE():
        database_connection=mysql.connector.connect(host="localhost",user="root",password="qwer1234",database="EMS_BY_RAHUL")
        database_cursor=database_connection.cursor()
        return database_connection,database_cursor
