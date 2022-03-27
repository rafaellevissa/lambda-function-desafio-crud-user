from __mocks__.dynamodb import create_dynamodb_schema, insert_dynamodb, item_dynamodb
from lib.session import Session
from moto import mock_dynamodb
import boto3

class TestSession:
  def setup_class(self):
    with mock_dynamodb():
      self.dynamodb = boto3.client('dynamodb')

  def test_put(self):
    with mock_dynamodb():
      self.dynamodb.create_table(
        **create_dynamodb_schema()
      )
      payload = {
        'token': 'NrZGprc2prc2pka3NqZA',
        'requisitor': 'admin',
        'requisitor_id': '1'
      }
      session = Session().put(payload)

      assert isinstance(session, dict)

  def test_get_by_requisitor(self):
    with mock_dynamodb():
      self.dynamodb.create_table(
        **create_dynamodb_schema()
      )

      self.dynamodb.put_item(
        **insert_dynamodb()
      )
      sessions = Session().get_by_requisitor(requisitor_id='1')

    assert isinstance(sessions, list)
    assert len(sessions) > 0
    assert 'id' in sessions[0]
    assert 'token' in sessions[0]
    assert 'requisitor' in sessions[0]
    assert 'created_at' in sessions[0]

  def test_get_by_requisitor_empty(self):
    with mock_dynamodb():
      self.dynamodb.create_table(
        **create_dynamodb_schema()
      )
      sessions = Session().get_by_requisitor(requisitor_id='1')

      assert isinstance(sessions, list)
      assert len(sessions) == 0

