import mysql.connector # https://www.geeksforgeeks.org/mysql-connector-python-module-in-python/ along with line 7
import getpass # https://pymotw.com/2/getpass/
dbusername = open("username.txt", "r").read()
dbpassword = open("password.txt", "r").read()
dbname = open("db.txt", "r").read()
songnames = open("songwriters.txt", "r").read()
songwriters = open("songwriters.txt", "r").read()
db = mysql.connector.connect(host='localhost', database=dbname, user=dbusername, password=dbpassword) # https://www.w3schools.com/python/python_mysql_create_db.asp
cursor = db.cursor()

cursor.execute("SHOW TABLES")
tablefound = "false"
for table in cursor:
  if table == "users":
    tablefound = "true"
  else:
    if table != "users":
      tablefound = "false"

if tablefound == "false":
  cursor.execute("CREATE TABLE users (username TEXT, password TEXT, admin BOOLEAN)")

  masterusername = input("Enter a username. This will be used as an administrator account to manage every user and song: ")
  if " " in masterusername:
    print("You must not have any spaces in your username!")
    quit()
  masterpassword = ""
  confirmpassword = ""
  while len(masterpassword) < 8 or masterpassword == masterusername:
    masterpassword = getpass.getpass(prompt="Enter a strong password:")
    if len(masterpassword) < 8 or masterpassword == masterusername:
      print("Invalid password!")
    if " " in masterpassword:
      print("You must not have any spaces in your password!")
      quit()
  while confirmpassword != masterpassword:
    confirmpassword = getpass.getpass(prompt="Confirm password: ")
    if confirmpassword != masterpassword:
      print("Passwords do not match!")
    if " " in masterpassword:
      print("You must not have any spaces in your password!")
      quit()
  cursor.execute("INSERT INTO users VALUES('" + masterusername + "', SHA2('" + masterpassword + "', 256), true);") # https://www.mysqltutorial.org/mysql-insert-statement.aspx https://stackoverflow.com/questions/34712665/mysql-sha256-with-insert-statement
else:
  username = input("Enter an administrator’s username: ")
  if " " in username:
    print("You must not have any spaces in your username!")
    quit()
  password = getpass.getpass(prompt="Enter their password: ")
  if " " in password:
    print("You must not have any spaces in your password!")
    quit()
  cursor.execute("SELECT * FROM users;")
  print(cursor)
