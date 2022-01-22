import mysql.connector

mydb = mysql.connector.connect(
	host="localhost",
	user="root",
	passwd="rootpwd",
	)

mycursor = mydb.cursor()

mycursor.execute("CREATE DATABASE flasker")

mycursor.execute("SHOW DATABASES")
for db in mycursor:
	print(db)