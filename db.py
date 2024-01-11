import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

MYSQL_HOST = os.getenv('MYSQL_HOST')
MYSQL_USER = os.getenv('MYSQL_USER')
MYSQL_PWD = os.getenv('MYSQL_PWD')
MYSQL_PORT = os.getenv('MYSQL_PORT')

db = mysql.connector.connect(
  host=MYSQL_HOST,
  user=MYSQL_USER,
  passwd=MYSQL_PWD
)

cursorObj = db.cursor()

cursorObj.execute("CREATE DATABASE crmDB")

print("All Done!")
