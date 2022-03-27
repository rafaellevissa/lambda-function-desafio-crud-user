import pytest
import jwt
from lib.utils import response, auth

class TestResponse:
  def test_response_payload_dict(self):
    payload = {'message': 'My message'}

    data = response(200, payload)

    assert isinstance(data, dict)
    assert 'statusCode' in data
    assert 'headers' in data
    assert 'body' in data
    assert data['statusCode'] == 200
    assert isinstance(data['body'], str)
    assert isinstance(data['headers'], dict)
    assert payload['message'] in data['body']
  
  def test_response_payload_string(self):
    payload = 'Something wrong happened'
    data = response(500, payload)

    assert isinstance(data, dict)
    assert 'statusCode' in data
    assert 'headers' in data
    assert 'body' in data
    assert data['statusCode'] == 500
    assert isinstance(data['body'], str)
    assert isinstance(data['headers'], dict)
    assert payload in data['body']

class TestAuth:
  def test_auth(self, mocker):
    event_mock = {'headers': {'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwibmFtZSI6ImFkbWluIiwidXNlcm5hbWUiOiJhZG1pbiIsInBhc3N3b3JkIjoiZDJWM1pYZGxkMlYzWlhkbGQzTnFaSE5yWkdwcmMycHJjMnBrYTNOcVpBIn0.rJFn7a3z85twb3tCf30j7pH4wWpm5rRjsWZ91pRZ9nw'}}
    environ_mock = {'JWT_SECRET': 'your-256-bit-secret'}

    mocker.patch.dict('os.environ', environ_mock)

    user = auth(event_mock)

    assert isinstance(user, dict)
    assert user.get('id') == 1
    assert user.get('name') == 'admin'
    assert user.get('username') == 'admin'
    assert user.get('password') == 'd2V3ZXdld2V3ZXdld3NqZHNrZGprc2prc2pka3NqZA'
  
  def test_auth_expired_token(self, mocker):
    event_mock = {'headers': {'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwibmFtZSI6ImFkbWluIiwidXNlcm5hbWUiOiJhZG1pbiIsInBhc3N3b3JkIjoiZDJWM1pYZGxkMlYzWlhkbGQzTnFaSE5yWkdwcmMycHJjMnBrYTNOcVpBIiwiZXhwIjowfQ.hPvTpDABxBCb2CodLJ51OtTwkzE1VW5QTW_BFz83o3I'}}
    environ_mock = {'JWT_SECRET': 'your-256-bit-secret'}

    mocker.patch.dict('os.environ', environ_mock)

    with pytest.raises(jwt.ExpiredSignatureError):
      auth(event_mock)

