CREATE USER "musicquiz"@"localhost" IDENTIFIED BY "musicquiz";
CREATE DATABASE musicquiz;
GRANT ALL PRIVILEGES ON musicquiz.* TO "musicquiz"@"localhost";
FLUSH PRIVILEGES;