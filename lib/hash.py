import bcrypt

class Hash:
  def encrypt(self, plain_text: str):
    hashed_text = bcrypt.hashpw(plain_text.encode('utf8'), bcrypt.gensalt())

    return hashed_text.decode('utf8')

  def check(self, plain_text: str, hashed_text: str):
    return bcrypt.checkpw(
      plain_text.encode('utf8'),
      hashed_text.encode('utf8')
    )

