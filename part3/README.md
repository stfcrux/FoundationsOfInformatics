# README #

### Requirements ###

* MySQL Server
* Python 2.7.x
* flask
* flask-bootstrap
* MySQL-python
* pandas 

### Quick setup ###

0. Clone this repository
1. [Install python 2.7.x](https://www.python.org/)
2. Install flask by running the command *pip install flask*
3. Install flask_bootstrap by running the command *pip install flask-bootstrap*
4. Install pandas with *pip install pandas*
5. [Install MySQL Server](https://dev.mysql.com/downloads/mysql/)
6. Install MySQL-python 
-> **Ubuntu**: sudo apt-get install python-mysqldb
-> **OSX**: export PATH=$PATH:/usr/local/mysql/bin && easy_install MySQL-python
-> **Windows**: ??
7. Create the database **flight** using the MySQL query  *CREATE DATABASE flight*
8. Create database tables by running the queries in /dataset/dataset.sql
9. Change the details in MySQLConfig.py to reflect the details of your MySQL server

### Running Webserver ###
1. Let flask know what to run with *export FLASK_APP=main.py*
2. Run flask *flask run* 