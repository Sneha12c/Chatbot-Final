import mysql.connector
mydb=mysql.connector.connect(host="localhost",user="root",passwd="sneha123",database="chatbot")
mycursor=mydb.cursor()