# Introduction
I have selected the “music quiz game” project, task 1.\
This project is particularly useful in the real world, mainly for satisfying boredom. However, it does get particularly complex, the more songs there are and the longer each one’s length. This project will be written in Python, which provides access to easily reading/writing files (fs is absolutely HORRIBLE. period), MySQL and other things. Python does the job.\
In each part of my pseudocode, I will write comments on what this code will do for the end user. In Batch, this will be shown with the “rem” command and in Python and Bash, by using “#”

# Prerequisites
* Python (and added to path)
* Git (and added to path)
* A MySQL user (recommended not to use root!) and database. If you want to automate the database creation and preparation, feel free to run “sudo mysql -u root mysql < dbsetup.sql” (https://gist.github.com/439bananas/c3e585424cba6f9b9ee4e730e4e6b0c1)

# Running/configuring
To configure the project, run python3 setup.py in your command line of choice. When run for the first time, the project will create user tables and ask you to set up a master username and password. When rerun, you will be presented with a prompt as to what you wish to do. To add songs, enter “2” followed by “1”. You will then be prompted to enter a song name and its writer.

# README.md
## Description
This file, here.

# setup.bat
## Description
This file installs the necessary dependencies for the end user and downloads the entire project. This will be found at https://nodir.439bananas.com/csproj/setup.bat.

```rem The following line hides the commands that shall be shown
@echo off
OUTPUT “Setting up music game quiz project. This could take a while…”
rem Installing dependencies
INSTALL w/pip mysql.connector
rem Getting code
CLONE https://github.com/439bananas/csproj
```

# setup.sh
## Description
This file works the same way as the above batch file but instead is intended for Linux/MacOS users.

```OUTPUT “Setting up music game quiz project. This could take a while…”
sudo apt-get update # Best to update stuff before installing software 
INSTALL w/pip mysql.connector # Installing dependencies
CLONE https://github.com/439bananas/csproj # Getting code
```

# dbprep.sql
## Description
Prepares the database for use with the project.

```CREATE USER “musicquiz” IDENTIFIED BY “musicquiz”;
CREATE DATABASE “musicquiz”;
GRANT ALL PRIVILEGES ON musicquiz.* TO “musicquiz”@”localhost”;
FLUSH PRIVILEGES;
QUIT;
```

# setup.py
## Description
Creates database tables. If these already exist, then user and song management is presented to the administrator.

```import mysql.connector # W3Schools
use file db.txt as db
use file username.txt as username
use file password.txt as password
use file songnames.txt as songnames
use file songwriters.txt as songwriters
mysql.connector.connect(username, password, db)
# If not users table, create and ask for admin account
IF (!USERS TABLE)
   CREATE TABLE “users”
   INPUT AS “masterusername” “Enter a username. This will be used as an administrator account to manage every user and song.”
   WHILE LENGTH OF masterpassword < 8 OR masterpassword = masterusername
      INPUT AS masterpassword “Enter a strong password.”
      IF LENGTH OF masterpassword < 8 OR masterpassword == masterusername
         OUTPUT “Invalid password!”
   WHILE confirmpassword != masterpassword
      INPUT “Confirm password” AS confirmpassword
      IF confirmpassword != masterpassword
         OUTPUT “Passwords do not match!”
   APPEND TO users masterusername | SHA256(masterpassword) | “admin”
ELSE
   INPUT “Enter an administrator’s username” AS username
   INPUT “Enter their password” AS SHA256(password)
   IF !username IN db.users:1 OR password != password in db.users OR  !admin IN db.users:3:username
      OUTPUT “Invalid username or password”
   ELSE
      OUTPUT “Welcome to the song quiz’s admin panel!”
      INT INPUT AS option “Pick a task you wish to do:\n1\) Manage users\n2\) Manage songs”
      IF option != 1 and option != 2
         OUTPUT “Please select an option between 1 and 2”
      ELSEIF option == 1
         INT INPUT “Pick a task you wish to do:\n1\) Add users\n2\) Remove users\n3\) Change user groups\n4\) Reset passwords” AS option
         IF option !>= 1 and option !>= 4
            OUTPUT “Please select an option between 1 and 4”
         IF option == 1
            WHILE LENGTH OF newpassword < 8 OR newpassword = newusername OR db.users CONTAINS newusername 
               INPUT “Enter the username of the new user” AS newusername
               INPUT “Enter the password of the new user” AS newpassword
               IF db.users CONTAINS newusername
                  OUTPUT “A user with that username already exists!”
               ELSEIF newpassword < 8 OR newpassword = newusername
                  OUTPUT “Invalid password!”
            WHILE admin != yes AND admin != no
               INPUT “Would you like this user to have administrative privileges?” AS admin
               IF admin == “yes”
                  SET colthree TO “admin”
               ELSEIF admin == “no”
                  SET colthree TO “”
               ELSE
                  OUTPUT “You must specify if the user you wish to add should have administrative privileges!”
            APPEND TO users newusername | SHA256(newpassword) | colthree
         IF option == 2
            FOR row IN db.users:1 
               OUTPUT row + “\) “ + db.users:1:row 
            INT INPUT “Which user do you wish to remove (1-“ + LENGTH(db.users) + “? “ AS usertoremove
            INPUT “Are you sure you wish to remove ” + usertoremove + “? They will no longer be able to use the program!” AS confirmation
            IF confirmation == “yes”:
               REMOVE db.users:*:usertoremove
               OUTPUT “Removed user.”
            ELSE:
               OUTPUT “Abort.”
         IF option == 3
            FOR row IN db.users:1 
               OUTPUT row + “\) “ + db.users:1:row + “ | “ + db.users:3:row
            INT INPUT “Which user do you wish to change groups for (toggle, 1-“ + LENGTH(db.users) + “? “ AS usertotoggleadmin
            IF db.users:3:usertotoggleadmin == “admin”
               CHANGE db.users:3:usertotoggleadmin TO “”
            ELSE
               CHANGE db.users:3:usertotoggleadmin TO “admin”
            OUTPUT “Group changed”
         ELSE
            INT INPUT “Whose password do you wish to reset (1-“ + LENGTH(db.users) + “? “ AS usertoresetpassword
            INPUT “Enter a strong password for the user: ” AS newpassword
            WHILE LENGTH OF newpassword < 8 OR newpassword = db.users:1:usertoresetpassword
               INPUT AS newpassword “Enter a strong password.”
               IF LENGTH OF newpassword < 8 OR newpassword == db.users:1:usertoresetpassword
                  OUTPUT “Invalid password!”
               WHILE confirmpassword != newpassword
                  INPUT “Confirm password” AS confirmpassword
                  IF confirmpassword != newpassword
                     OUTPUT “Passwords do not match!”
            OUTPUT “Password reset.”
            CHANGE db.users.2:usertoresetpassword TO SHA256(newpassword)
      ELSE
         INT INPUT “Pick a task you wish to do:\n1\) Add songs\n2\) Remove songs” AS option
         IF option != 1 and option != 2
            OUTPUT “Please select an option between 1 and 2”
         ELIF option == 1
            INPUT “Enter the name of the song which you wish to add ” AS songname
            INPUT “Enter the writer of the song ” AS songwriter
            APPEND songname TO songwriters
            APPEND songwriter TO songwriters
         ELSE
            FOR row IN songwriters
               OUTPUT row + “\) “ + row.content
            INT INPUT “Which song do you wish to remove (1-“ + LENGTH(songwriters) + “? ” AS songtoremove
            INPUT “Are you sure you wish to remove ” + songtoremove + “? The song will no longer be displayed!” AS confirmation
            IF confirmation == “yes”:
               REMOVE songwriters:songtoremove
               OUTPUT “Removed song.”
            ELSE:
               OUTPUT “Abort.”
```

# index.py
## Description
This file is the main game, that’s it.
```import mysql.connector # W3Schools
use file db.txt as db
use file username.txt as username
use file password.txt as password
use file songnames.txt as songnames
use file songwriters.txt as songwriters
mysql.connector.connect(username, password, db)
import math

IF (!USERS TABLE)
   OUTPUT “FATAL: The database does not appear to have been configured! Please run python3 setup.py before rerunning this file.”
   END
ELSE
   fails = 0
   score = 0
   WHILE fails != 2
      songnumber = math.random(0:LINECOUNT(songnames)
      words = SPLIT songnames:songnumber()
      letters = [(word[0] + “_” * (len(word)-1)) + “ “ for word in words] # StackOverflow
      INPUT (“”.join(letters) + “ by ” +  songwriters:songnumber).LOWER() AS song
      IF song == songnames:songnumber
         score =+ 3
         IF fails == 1
            pors = “”
         ELSE
            pors = “s”
         OUTPUT “Your guess was correct! Your score is”, score, “and you have”, fails+2, “attempt” + pors + “ remaining.”
      ELSE
         IF fails = 1
            pors = “”
         ELSE
            pors = “s”
         score =- 1
         fails =+ 1
         OUTPUT “Wrong answer! The answer was ” + songnames:songnumber + “. Your score is”, score, “and you have”, fails+2, “attempt” + pors + “ remaining.”
   OUTPUT “Game over! Your final score was”, score
   END
```