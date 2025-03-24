# compose/mysql/init/init.sql
Alter user 'dbuser'@'%' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON zoysiadb_project.* TO 'dbuser'@'%';
FLUSH PRIVILEGES;
