import mysql.connector # https://www.geeksforgeeks.org/mysql-connector-python-module-in-python/ along with line 7
import getpass # https://pymotw.com/2/getpass/
dbhost = open("dbhost.txt", "r").read()
dbusername = open("username.txt", "r").read()
dbpassword = open("password.txt", "r").read()
dbname = open("db.txt", "r").read()
db = mysql.connector.connect(host=dbhost, database=dbname, user=dbusername, password=dbpassword) # https://www.w3schools.com/python/python_mysql_create_db.asp
cursor = db.cursor()

def admin(username):
  runs = 0
  while True:
    if runs == 0:
      print("Welcome to the song quiz’s admin panel!")
    option = 0
    option = int(input("Pick a task you wish to do:\n1) Manage users\n2) Manage songs\n3) Quit\n"))
    if option < 1 or option > 3:
      print("Please select an option between 1 and 3")
    elif option == 1:
      option = 0
      cursor.execute("SELECT * FROM users;")
      result = cursor.fetchall()
      while option < 1 or option > 5:
        option = int(input("Pick a task you wish to do:\n1) Add users\n2) Remove users\n3) Change user groups\n4) Reset passwords\n5) Back\n"))
        if option < 1 or option > 5:
          print("Please select an option between 1 and 5")
        elif option == 1:
          dupe = False
          newusername = ""
          newpassword = ""
          while len(newpassword) < 8 or newpassword == newusername or dupe == True:
            newusername = input("Enter the username of the new user: ").lower()
            newpassword = getpass.getpass(prompt="Enter the password of the new user:")
            for item in result:
              if newusername == item[0]:
                dupe = True
                break
              else:
                dupe = False
            if dupe == True and not "\\" in newusername and not "\\" in newpassword and not " " in newusername and not " " in newpassword:
              print("A user with that username already exists!")
            if "\\" in newusername or "\\" in newpassword or " " in newusername or " " in newpassword:
              print("You must not have any backslashes or spaces in your username or password!")
            if (newusername == newpassword or len(newpassword) < 8) and (dupe == False) and not "\\" in newusername and not "\\" in newpassword and not " " in newusername and not " " in newpassword:
              print("Invalid password!")
            admin = ""
          while admin != "yes" and admin != "no":
            admin = input("Would you like this user to have administrative privileges? (yes/no) ")
            if admin == "yes":
              adm = True
            elif admin == "no":
              adm = False
            else:
              print("You must specify if the user you wish to add should have administrative privileges!")
            cursor.execute("INSERT INTO users(username, password, admin) VALUES (%s, SHA2(%s, 256), %s)", (newusername, newusername + newpassword, adm)) # https://www.mysqltutorial.org/mysql-insert-statement.aspx https://stackoverflow.com/questions/34712665/mysql-sha256-with-insert-statement
            db.commit()
        elif option == 2:
          option = 0
          cursor.execute("SELECT * FROM users;")
          result = cursor.fetchall()
          admincount = 0
          if len(result) > 1:
            for i in result:
              print(result.index(i) + 1, end=") " + i[0] + "\n")
              if i[2] == 1:
                admincount = admincount + 1
            maxnumtoshow = str(len(result))
            timesasked = 0
            usertoremove = int()
            inrange = False
            while (result[usertoremove-1][2] == 1 and admincount < 1) or (timesasked < 1) or inrange == False:
              usertoremove = int(input("Which user do you wish to remove (1-" + maxnumtoshow + ")? ")) # as per my own wonderful vocabulary, "yucky, yucky, yucky"
              if usertoremove < 1 or usertoremove > len(result):
                print("Please select an option between 1 and " + maxnumtoshow)
              else:
                inrange = True
                if result[usertoremove-1][2] == 1 and admincount < 2:
                  print("There must be at least one administrator!")
                else:
                  confirmation = input("Are you sure you wish to remove " + str(result[usertoremove-1][0]) + "? They will no longer be able to use the program! (yes/no) ")
                  if confirmation == "yes":
                    cursor.execute("DELETE FROM users WHERE username='" + str(result[usertoremove-1][0]) + "'") 
                    db.commit()
                    print("Removed user.")
                    if username == str(result[usertoremove-1][0]):
                      print("You no longer have access to the admin panel. Goodbye.")
                      quit()
                    break
                  else:
                    print("Abort.")
                    break
          else:
            print("There must be at least one user!")
        elif option == 3:
          option = 0
          cursor.execute("SELECT * FROM users;")
          result = cursor.fetchall()
          adm = ""
          inrange = False
          admincount = 0
          for i in result:
            if i[2] == 0:
              adm = ""
            else:
              adm = "admin"
              admincount = admincount + 1
            print(result.index(i) + 1, end=") " + i[0] + " | " + adm + "\n")
          maxnumtoshow = str(len(result))
          usertotoggleadmin = int()
          timesasked = 0
          valid = False
          changed = False
          while (valid == False) or (timesasked < 1) or inrange == False:
            timesasked = timesasked + 1
            usertotoggleadmin = int(input("Which user do you wish to change groups for (toggle, 1-" + maxnumtoshow + ")? "))
            if usertotoggleadmin < 1 or usertotoggleadmin > len(result):
              print("Please select an option between 1 and " + maxnumtoshow)
            else:
              inrange = True
              if result[usertotoggleadmin-1][2] == 1:
                if admincount > 1:
                  valid = True
                  cursor.execute("UPDATE users SET admin = false WHERE username='" + str(result[usertotoggleadmin-1][0]) + "'") 
                  db.commit()
                  changed = True
                  if username == str(result[usertotoggleadmin-1][0]):
                    print("You no longer have access to the admin panel. Goodbye.")
                    quit()
                else:
                  print("There must be at least one administrator!")
              else:
                  cursor.execute("UPDATE users SET admin = true WHERE username='" + str(result[usertotoggleadmin-1][0]) + "'") 
                  db.commit()
                  changed = True
              if changed == True:
                print("Group changed")
                break
        elif option == 4:
          option = 0
          cursor.execute("SELECT * FROM users;")
          result = cursor.fetchall()
          inrange = False
          for i in result:
            print(result.index(i) + 1, end=") " + i[0] + "\n")
          maxnumtoshow = str(len(result))
          usertoresetpassword = int()
          timesasked = 0
          usernametoresetpassword = ""
          newpassword = ""
          confirmpassword = ""
          while len(newpassword) < 8 or newpassword == usernametoresetpassword:
            usertoresetpassword = int(input("Whose password do you wish to reset (1-" + maxnumtoshow + ")? "))
            if usertoresetpassword == "":
              option = 0
              print("Abort.")
              break
            usernametoresetpassword = str(result[usertoresetpassword-1][0])
            newpassword = getpass.getpass(prompt="Enter a strong password for the user:")
            if "\\" in newpassword or " " in newpassword:
              print("You must not have any backslashes or spaces in that user's password!")
            if (usernametoresetpassword == newpassword or len(newpassword) < 8) and not "\\" in usernametoresetpassword and not "\\" in newpassword and not " " in usernametoresetpassword and not " " in newpassword and not newpassword == "":
              print("Invalid password!")
            if usertoresetpassword == "":
              option = 0
              print("Abort.")
              break
          while confirmpassword != newpassword:
            confirmpassword = getpass.getpass(prompt="Confirm password:")
            if confirmpassword != newpassword:
              print("Passwords do not match!")
            else:
              cursor.execute("UPDATE users SET password=SHA2(%s, 256) WHERE username=%s", (usernametoresetpassword + newpassword, usernametoresetpassword))
              db.commit()
              print("Password reset.")
        elif option == 5:
          option = 0
          break
    elif option == 2:
      option = 0
      while option < 1 or option > 3:
        option = int(input("Pick a task you wish to do:\n1) Add songs\n2) Remove songs\n3) Back\n"))
        if option < 1 or option > 3:
          print("Please select an option between 1 and 3")
        if option == 1:
          songname = input("Enter the name of the song which you wish to add: ")
          if songname == "":
            option = 0
            print("Abort.")
            break
          songwriter = input("Enter the writer of the song: ")
          if songwriter == "":
            option = 0
            print("Abort.")
            break
          songnamesa = open("songnames.txt", "a")
          songwritersa = open("songwriters.txt", "a")
          songnamesa.write("\n" + songname)
          songnamesa.close()
          songwritersa.write("\n" + songwriter)
          songwritersa.close()
        elif option == 2:
          songnames = open("songnames.txt", "r+")
          songwriters = open("songwriters.txt", "r+")
          lines = songnames.readlines()
          lines2 = []
          lines3 = songwriters.readlines()
          lines4 = []
          songwriters.close()
          songnames.close()
          songcount = 0
          for i in lines:
            if i != "\n":
              songcount = songcount + 1
              lines2.append(i.strip())
          for i in lines3:
            if i != "\n":
              lines4.append(i.strip())
          songnamescleanup = open("songnames.txt", "w+")
          songwriterscleanup = open("songwriters.txt", "w+")
          for i in lines2:
            songnamescleanup.write(i + "\n")
          for i in lines4:
            songwriterscleanup.write(i + "\n")
          songnamescleanup.close()
          songwriterscleanup.close()
          if len(lines2) == 0:
            print("There are no songs!")
          else:
            for i in range(len(lines2)):
              songid = int(i)
              print(songid + 1, end=") " + lines2[i] + " by " + lines4[songid] + "\n")
            songtoremove = 0
            while songtoremove < 1 or songtoremove > len(lines2):
              songtoremove = int(input("Which song do you wish to remove (1-" + str(len(lines2)) + ")? "))
              if songtoremove < 1 or songtoremove > len(lines2):
                print("Please select an option between 1 and " + str(len(lines2)))
              if songtoremove == "":
                option = 0
                print("Abort.")
                break
            confirmation = input("Are you sure you wish to remove " + lines2[songtoremove-1] + " by " + lines4[songtoremove-1] + "? The song will no longer be displayed! (yes/no) ")
            if confirmation == "yes":
              del lines2[songtoremove-1]
              del lines4[songtoremove-1]
              songnamesrem = open("songnames.txt", "w+")
              songwritersrem = open("songwriters.txt", "w+")
              for i in lines2:
                songnamesrem.write(i + "\n")
              for i in lines4:
                songwritersrem.write(i + "\n")
              songnamesrem.close()
              songwritersrem.close()
              songnames.close()
              songwriters.close()
              print("Removed song.")
            else:
              print("Abort.")
        elif option == 3:
          option = 0
          break
    elif option == 3:
      print("Goodbye.")
      quit()
    runs = runs + 1

def fts():
  cursor.execute("SELECT * FROM users;")
  result = cursor.fetchall()
  dupe = True
  while dupe == True:
    username = input("Enter a username. This will be used as an administrator account to manage every user and song: ").lower()
    if "\\" in username or " " in username:
      print("You must not have any backslashes or spaces in your username!")
      quit()
    if len(result) != 0:
      for item in result:
        if username == item[0]:
          dupe = True
          break
        else:
          dupe = False
    else:
      dupe = False
    if dupe == True and not "\\" in username and not " " in username:
      print("A user with that username already exists!")
  password = ""
  confirmpassword = ""
  while len(password) < 8 or password == username:
    password = getpass.getpass(prompt="Enter a strong password:")
    if len(password) < 8 or password == username:
      print("Invalid password!")
    if "\\" in password or " " in password:
      print("You must not have any backslashes or spaces in your password!")
      quit()
  while confirmpassword != password:
    confirmpassword = getpass.getpass(prompt="Confirm password:")
    if confirmpassword != password:
      print("Passwords do not match!")
    if "\\" in password or " " in password:
      print("You must not have any backslashes or spaces in your password!")
      quit()
  cursor.execute("INSERT INTO users(username, password, admin) VALUES (%s, SHA2(%s, 256), %s)", (username, username + password, True)) # https://www.mysqltutorial.org/mysql-insert-statement.aspx https://stackoverflow.com/questions/34712665/mysql-sha256-with-insert-statement
  db.commit()
  admin(username)

cursor.execute("SHOW TABLES")
admincount = int(0)
tablefound = False
for x in cursor:
  if x[0] == "users": # https://stackoverflow.com/questions/28624796/removing-characters-from-mysql-query-results-in-python
    tablefound = True
if tablefound == False:
  cursor.execute("CREATE TABLE users (username TEXT, password TEXT, admin BOOLEAN)")
  fts()
cursor.execute("SELECT * FROM users;")
result = cursor.fetchall()
if len(result) >= 1:
  for i in result:
    if i[2] == 1:
      admincount = admincount + 1
else:
  fts()
if admincount < 1:
  fts()
else:
  found = False
  while found == False:
    username = input("Enter an administrator’s username: ").lower()
    if "\\" in username or " " in username:
      print("You must not have any backslashes or spaces in your username!")
      quit()
    password = getpass.getpass(prompt="Enter their password:")
    if "\\" in password or " " in password:
      print("You must not have any backslashes or spaces in your password!")
      quit()
    cursor.execute("SELECT * FROM users;")
    result = cursor.fetchall()
    cursor.execute("SELECT SHA2(%s, 256)", (username + password,))
    hashedpass = cursor.fetchall()[0][0]
    for row in result:
      if row[0] == username:
        found = True
      if row[1] != hashedpass:
        found = False
      if row[2] != 1:
        found = False
      if found == True:
        break
    if found == False:
      print("Invalid username or password")
    else:
      admin(username)
