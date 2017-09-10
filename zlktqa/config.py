# Author:Clin
import os

DEBUG = True

SECRET_KEY = 'kaierhes'
    #os.urandom(24)

DIALECT = "mysql"
DRIVER = "mysqldb"
USERNAME = "myuser"
PASSWORD = "666333"
HOST = "122.114.197.94"
PORT = "3306"
DATABASE = "zlktqa"

SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(DIALECT,DRIVER,USERNAME,PASSWORD,HOST,PORT,DATABASE)

SQLALCHEMY_TRACK_MODIFICATIONS = False