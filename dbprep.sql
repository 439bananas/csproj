CREATE USER "musicquiz"@"%" IDENTIFIED BY "musicquiz";
CREATE DATABASE musicquiz;
GRANT ALL PRIVILEGES ON musicquiz.* TO "musicquiz"@"%";
FLUSH PRIVILEGES;