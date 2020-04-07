import mysql.connector

mydb = mysql.connector.connect(
  host="127.0.0.1",
  user="root",
  passwd="mysql123",
  database="mydatabase"
)
mycursor = mydb.cursor()
mycursor.execute("UPDATE participants SET score='120' where name='anshika'")
mydb.commit()
print(mycursor.rowcount,"record affected")
