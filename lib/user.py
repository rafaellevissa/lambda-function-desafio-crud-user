from lib.database import Database
from lib.hash import Hash

class User(Database):
  def __init__(self):
    super().__init__()
    self.username = None
    self.name = None
    self.password = None

  def create(self, payload: dict):
    self.username = payload['username']
    self.name = payload['name']
    self.password = Hash().encrypt(payload['password'])

    return self

  def save(self):
    cursor = self.get_cursor()
    cursor.execute(
      "INSERT INTO users (name, username, password) VALUES (%s, %s, %s)",
      (self.name, self.username, self.password)
    )
    self.commit()

    cursor.close()

    return self

  def find_by_username(self, username: str) -> dict:
    cursor = self.get_cursor()

    cursor.execute("SELECT * FROM users WHERE username = %s", username)

    return cursor.fetchone()

