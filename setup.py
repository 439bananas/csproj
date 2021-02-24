import mysql.connector # https://www.geeksforgeeks.org/mysql-connector-python-module-in-python/ along with line 7
import getpass # https://pymotw.com/2/getpass/
dbhost = open("dbhost.txt", "r").read()
dbusername = open("username.txt", "r").read()
dbpassword = open("password.txt", "r").read()
dbname = open("db.txt", "r").read()
songnames = open("songwriters.txt", "r").read()
songwriters = open("songwriters.txt", "r").read()
db = mysql.connector.connect(host=dbhost, database=dbname, user=dbusername, password=dbpassword) # https://www.w3schools.com/python/python_mysql_create_db.asp
cursor = db.cursor()

def admin():
  count = 0
  while True:
    if count == 0:
      print("Welcome to the song quiz’s admin panel!")
    option = int(input("Pick a task you wish to do:\n1) Manage users\n2) Manage songs\n3) Quit\n"))
    if option != 1 and option != 2:
      print("Please select an option between 1 and 2")
    elif option == 1:
      option = 0
      cursor.execute("SELECT * FROM users;")
      result = cursor.fetchall()
      while option < 1 or option > 4:
        option = int(input("Pick a task you wish to do:\n1) Add users\n2) Remove users\n3) Change user groups\n4) Reset passwords\n5) Quit\n"))
        if option < 1 or option > 4:
          print("Please select an option between 1 and 4")
        elif option == 1:
          dupe = "true"
          newusername = ""
          newpassword = ""
          while len(newpassword) < 8 or newpassword == newusername or dupe == "true":
            newusername = input("Enter the username of the new user: ")
            newpassword = getpass.getpass(prompt="Enter the password of the new user:")
            for item in result:
              if newusername == item[0]:
                dupe = "true"
                break
              else:
                dupe = "false"
            if dupe == "true" and not " " in newusername and not " " in newpassword:
              print("A user with that username already exists!")
            if " " in newusername or " " in newpassword:
              print("You must not have any spaces in your username or password!")
            if (newusername == newpassword or len(newpassword) < 8) and (dupe == "false") and not " " in newusername and not " " in newpassword:
              print("Invalid password!")
            admin = ""
          while admin != "yes" and admin != "no":
            admin = input("Would you like this user to have administrative privileges? (yes/no) ")
            if admin == "yes":
              adm = "true"
            elif admin == "no":
              adm = "false"
            else:
              print("You must specify if the user you wish to add should have administrative privileges!")
            cursor.execute("INSERT INTO users(username,password,admin) VALUES('" + newusername + "', SHA2('" + newpassword + "', 256), " + adm + ")") # https://www.mysqltutorial.org/mysql-insert-statement.aspx https://stackoverflow.com/questions/34712665/mysql-sha256-with-insert-statement
            db.commit()
        elif option == 2:
          cursor.execute("SELECT * FROM users;")
          result = cursor.fetchall()
          for i in result:
            print(result.index(i) + 1, end=") " + i[0] + "\n")
          maxnumtoshow = str(len(result))
          usertoremove = int(input("Which user do you wish to remove (1-" + maxnumtoshow + ")? ")) # as per my own wonderful vocabulary, "yucky, yucky, yucky"
          confirmation = input("Are you sure you wish to remove " + str(result[usertoremove-1][0]) + "? They will no longer be able to use the program! (yes/no) ")
          if confirmation == "yes":
            cursor.execute("DELETE FROM users WHERE username='" + str(result[usertoremove-1][0]) + "'") 
            db.commit()
            print("Removed user.")
          print("Abort.")
        elif option == 3:
          cursor.execute("SELECT * FROM users;")
          result = cursor.fetchall()
          adm = ""
          for i in result:
            if i[2] == 0:
              adm = ""
            else:
              adm = "admin"
            print(result.index(i) + 1, end=") " + i[0] + " | " + adm + "\n")
          maxnumtoshow = str(len(result))
          usertotoggleadmin = int(input("Which user do you wish to change groups for (toggle, 1-" + maxnumtoshow + ")? "))
          print(result)
          # YOU MUST CHECK IF THE USER EXISTS!!!
          #if 1
          #cursor.execute("UPDATE users SET admin 0 WHERE username='" + str(result[usertotoggleadmin-1][2]) + "'") 
          ##db.commit()

          ###on option #5, print("Goodbye.") then quit()
    count = count + 1
          

cursor.execute("SHOW TABLES")
tablefound = "false"
for x in cursor:
  if x[0] == "users": # https://stackoverflow.com/questions/28624796/removing-characters-from-mysql-query-results-in-python
    tablefound = "true"

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
    confirmpassword = getpass.getpass(prompt="Confirm password:")
    if confirmpassword != masterpassword:
      print("Passwords do not match!")
    if " " in masterpassword:
      print("You must not have any spaces in your password!")
      quit()
  cursor.execute("INSERT INTO users(username,password,admin) VALUES('" + masterusername + "', SHA2('" + masterpassword + "', 256), true)") # https://www.mysqltutorial.org/mysql-insert-statement.aspx https://stackoverflow.com/questions/34712665/mysql-sha256-with-insert-statement
  db.commit()
  admin()
else:
  found = "false"
  while found == "false":
    username = input("Enter an administrator’s username: ")
    if " " in username:
      print("You must not have any spaces in your username!")
      quit()
    password = getpass.getpass(prompt="Enter their password:")
    if " " in password:
      print("You must not have any spaces in your password!")
      quit()
    cursor.execute("SELECT * FROM users;")
    result = cursor.fetchall()
    cursor.execute("SELECT SHA2('" + password + "', 256)")
    hashedpass = cursor.fetchall()[0][0]
    for row in result:
      if row[0] == username:
        found = "true"
      if row[1] != hashedpass:
        found = "false"
      if row[2] != 1:
        found = "false"
      if found == "true":
        break
    if found == "false":
      print("Invalid username or password")
    else:
      admin()
