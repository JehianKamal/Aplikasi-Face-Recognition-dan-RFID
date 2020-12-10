import sqlite3

conn = sqlite3.connect('FacaBase.db')
cursor = conn.cursor()
cursor.execute("DROP TABLE IF EXISTS EMPLOYEE")
sql = '''CREATE TABLE EMPLOYEE(FIRST_NAME CHAR(20) NOT NULL, LAST_NAME CHAR(20))'''
cursor.execute(sql)
print("Success")
conn.commit()
conn.close()
