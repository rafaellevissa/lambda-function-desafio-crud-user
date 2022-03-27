import pytest
from lib.hash import Hash

class TestHash:
  def test_hash_encrypt_plain_text(self, mocker):
    password = '1234'
    expected_value = b'NrZGprc2prc2pka3NqZA'

    mocker.patch('bcrypt.hashpw', return_value=expected_value)

    hashed = Hash().encrypt(password)

    assert hashed == 'NrZGprc2prc2pka3NqZA'
  
  def test_hash_encrypt_fail(self):
    password = 12345

    with pytest.raises(AssertionError):
      Hash().encrypt(password)



