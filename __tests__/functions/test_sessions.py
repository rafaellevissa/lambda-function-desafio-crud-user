import json
import boto3
from moto import mock_dynamodb
from __mocks__.dynamodb import create_dynamodb_schema, insert_dynamodb
from functions.sessions import handler

class TestSession:
  def setup_class(self):
    with mock_dynamodb():
      self.client = boto3.client('dynamodb')

  def test_handler_without_event(self):
    response = handler(event={}, context={})
    assert response == {
      'statusCode': 500,
      'headers': {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Credentials': True
      },
      'body': '{"message": "KeyError(\'headers\')"}'
    }
  
  def test_handler(self, mocker):
    with mock_dynamodb():
      environ_mock = {'JWT_SECRET': 'your-256-bit-secret'}
      event = {
        'headers': {
          'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwibmFtZSI6ImFkbWluIiwidXNlcm5hbWUiOiJhZG1pbiIsInBhc3N3b3JkIjoiZDJWM1pYZGxkMlYzWlhkbGQzTnFaSE5yWkdwcmMycHJjMnBrYTNOcVpBIn0.rJFn7a3z85twb3tCf30j7pH4wWpm5rRjsWZ91pRZ9nw',
        }
      }
      user = {
        "id": 1,
        "name": "admin",
        "username": "admin",
        "password": "d2V3ZXdld2V3ZXdld3NqZHNrZGprc2prc2pka3NqZA",
      }

      items = insert_dynamodb()
      session = items['Item']

      self.client.create_table(
        **create_dynamodb_schema()
      )

      self.client.put_item(**items)

      mocker.patch.dict('os.environ', environ_mock)
      
      response = handler(event, context={})

      assert isinstance(response, dict)
      assert response == {
        'statusCode': 200,
        'headers': {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Credentials': True
        },
        'body': json.dumps({
          'user': user,
          'sessions': [
            {
              'id': session['id']['S'],
              'token': session['token']['S'],
              'requisitor': session['requisitor']['S'],
              'requisitor_id': session['requisitor_id']['S'],
              'created_at': session['created_at']['S']
            }
          ]
        })
      }

    

