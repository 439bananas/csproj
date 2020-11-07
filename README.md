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

