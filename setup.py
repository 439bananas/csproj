import mysql.connector # https://www.geeksforgeeks.org/mysql-connector-python-module-in-python/ along with line 7
dbusername = open("username.txt", "r").read()
dbpassword = open("password.txt", "r").read()
dbname = open("db.txt", "r").read()
songnames = open("songwriters.txt", "r").read()
songwriters = open("songwriters.txt", "r").read()
db = mysql.connector.connect(host='localhost', database=dbname, user=dbusername password=dbpassword) # https://www.w3schools.com/python/python_mysql_create_db.asp
cursor = db.cursor()

cursor.execute("SHOW TABLES")
tablefound = false
for table in cursor:
  if table == "users":
    tablefound = true
  else
    if table != "users":
      tablefound = false

if tablefound == false:
  cursor.execute("CREATE TABLE users (username TEXT, password TEXT, admin BOOLEAN)")

  masterusername = input("Enter a username. This will be used as an administrator account to manage every user and song.")
  masterpassword = ""
  confirmpassword = ""
  while len(masterpassword) < 8 or masterpassword == masterusername:
    masterpassword = input("Enter a strong password.")
    if len(masterpassword) < 8 or masterpassword == masterusername:
      print("Invalid password!)
  while confirmpassword != masterpassword:
    confirmpassword = input("Confirm password")
    if confirmpassword != masterpassword:
      print("Passwords do not match!")
