import mysql.connector

mydb = mysql.connector.connect(
  host="127.0.0.1",
  user="root",
  passwd="mysql123",
  database="mydatabase"
)
mycursor = mydb.cursor()
mycursor.execute("select name,score from mydatabase.participants order by score desc;")
result=mycursor.fetchone()
print(result[0])
