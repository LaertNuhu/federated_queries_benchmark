create user 'mariadb'@localhost identified by '123456';
GRANT ALL PRIVILEGES ON *.* TO 'mariadb'@'%';

FlUSH PRIVILEGES;