import pymysql
import os

class Database:
  def __init__(self):
    self.__connection = pymysql.connect(
      host=os.environ['DB_HOST'],
      user=os.environ['DB_USERNAME'],
      password=os.environ['DB_PASSWORD'],
      database=os.environ['DB_DATABASE'],
      connect_timeout=5,
      cursorclass=pymysql.cursors.DictCursor
    )
  
  def get_cursor(self):
    return self.__connection.cursor()

  def commit(self) -> None:
    self.__connection.commit()
