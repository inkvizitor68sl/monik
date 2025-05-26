mysql -e "create database `monik`;"
mysql -e "CREATE USER 'monik'@'localhost' IDENTIFIED BY 'monik';"
mysql -e "GRANT ALL ON `monik`.* to 'monik'@'localhost';"
