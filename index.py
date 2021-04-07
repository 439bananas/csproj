import mysql.connector # https://www.geeksforgeeks.org/mysql-connector-python-module-in-python/ along with line 7
import getpass # https://pymotw.com/2/getpass/
dbhost = open("dbhost.txt", "r").read()
dbusername = open("username.txt", "r").read()
dbpassword = open("password.txt", "r").read()
dbname = open("db.txt", "r").read()
db = mysql.connector.connect(host=dbhost, database=dbname, user=dbusername, password=dbpassword) # https://www.w3schools.com/python/python_mysql_create_db.asp
cursor = db.cursor()
import random

cursor.execute("SHOW TABLES")
tablefound = False
for x in cursor:
  if x[0] == "users": # https://stackoverflow.com/questions/28624796/removing-characters-from-mysql-query-results-in-python
    tablefound = True
if tablefound == False:
  print("FATAL: The database does not appear to have been configured! Please run python3 setup.py before rerunning this file.")
  quit()
else:
  cursor.execute("SELECT * FROM users;")
  result = cursor.fetchall()
  if len(result) < 1:
    print("FATAL: The database does not appear to have been configured! Please run python3 setup.py before rerunning this file.")

found = False
while found == False:
  username = input("Enter your username: ").lower()
  if " " in username:
    print("You must not have any spaces in your username!")
    quit()
  password = getpass.getpass(prompt="Enter your password:")
  if " " in password:
    print("You must not have any spaces in your password!")
    quit()
  cursor.execute("SELECT * FROM users;")
  result = cursor.fetchall()
  cursor.execute("SELECT SHA2('" + username + password + "', 256)")
  hashedpass = cursor.fetchall()[0][0]
  for row in result:
    if row[0] == username:
      found = True
    if row[1] != hashedpass:
      found = False
    if found == True:
        break
  if found == False:
    print("Invalid username or password")
  else:
    songnames = open("songnames.txt", "r+")
    songwriters = open("songwriters.txt", "r+")
    lines = songnames.readlines()
    lines2 = []
    lines3 = songwriters.readlines()
    lines4 = []
    songwriters.close()
    songnames.close()
    for i in lines:
      if i != "\n":
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
      print("FATAL: There are no songs! Please run python3 setup.py before rerunning this file.")
      exit()

    fails = 0
    score = 0
    songnames = open("songnames.txt", "r+")
    songwriters = open("songwriters.txt", "r+")
    lines = songnames.readlines()
    lines2 = songwriters.readlines()
    lines3 = []
    lines4 = []
    for i in lines:
      if i != "\n":
        lines3.append(i.strip())
    for i in lines2:
      if i != "\n":
        lines4.append(i.strip())
    while True:
      songnumber = random.randint(0, len(lines3))
      words = lines3[songnumber-1].split()
      letters = [(word[0] + "_" * (len(word)-1)) + " " for word in words] # StackOverflow
      song = input("".join(letters) + " by " + lines4[songnumber-1] + ": ").lower()
      if song == lines3[songnumber-1].lower():
        score = score + 3
        print("Your guess was correct! Your score is", score)
      else:
        song = input("Try again: ").lower()
        if song == lines3[songnumber-1].lower():
          score = score + 1
          print("Your guess was correct! Your score is", score)
        else:
          print("Game over! Your final score was", score)
          songwriters.close()
          songnames.close()
          exit()