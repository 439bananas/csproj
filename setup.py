import mysql.connector # https://www.geeksforgeeks.org/mysql-connector-python-module-in-python/ along with line 7
dbusername = open("username.txt", "r").read()
dbpassword = open("password.txt", "r").read()
db = open("db.txt", "r").read()
songnames = open("songwriters.txt", "r").read()
songwriters = open("songwriters.txt", "r").read()
mysql.connector.connect(host='localhost', database=db, user=dbusername password=dbpassword)