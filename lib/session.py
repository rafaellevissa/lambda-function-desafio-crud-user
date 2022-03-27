import boto3
import uuid
from datetime import datetime

class Session:
  def __init__(self):
    self.table = "hitbel_sessions"
    self.client = boto3.client('dynamodb')

  def get_by_requisitor(self, requisitor_id: str) -> list:
    assert isinstance(requisitor_id, str)

    response = self.client.scan(
      TableName=self.table,
      FilterExpression='requisitor_id = :requisitor_id',
      ExpressionAttributeValues={
        ':requisitor_id': {
          'S': requisitor_id
        }
      }
    )

    return list(map(self.__prettier, response['Items']))

  def __prettier(self, item: dict) -> dict:
    assert isinstance(item, dict)

    return {
      'id': item['id']['S'],
      'token': item['token']['S'],
      'requisitor': item['requisitor']['S'],
      'requisitor_id': item['requisitor_id']['S'],
      'created_at': item['created_at']['S']
    }

  def put(self, payload: dict):
    assert isinstance(payload, dict)
    assert isinstance(payload.get('token'), str)
    assert isinstance(payload.get('requisitor'), str)
    assert isinstance(payload.get('requisitor_id'), str)

    return self.client.put_item(
      TableName=self.table,
      Item={
        'id': {
          'S': str(uuid.uuid4())
        },
        'token': {
          'S': payload['token']
        },
        'requisitor': {
          'S': payload['requisitor']
        },
        'requisitor_id': {
          'S': payload['requisitor_id']
        },
        'created_at': {
          'S': datetime.now().isoformat()
        }
      },
    )