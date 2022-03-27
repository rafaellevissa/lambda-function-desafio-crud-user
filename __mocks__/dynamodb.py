import boto3


def create_dynamodb_schema() -> dict:
  return {
    'TableName': 'hitbel_sessions',
    'KeySchema': [
      {
        'AttributeName': 'id',
        'KeyType': 'HASH'
      },
      {
        'AttributeName': 'token',
        'KeyType': 'RANGE'
      }
    ],
    'AttributeDefinitions': [
      {
        'AttributeName': 'id',
        'AttributeType': 'S'
      },
      {
        'AttributeName': 'token',
        'AttributeType': 'S'
      }
    ],
    'ProvisionedThroughput': {
      'ReadCapacityUnits': 1,
      'WriteCapacityUnits': 1
    }
  }

def insert_dynamodb():
  return {
    'TableName': 'hitbel_sessions',
    'Item': {
      'id': {
        'S': "2c1544c9-29d1-4b3d-a405-231ee465d8fe"
      },
      'token': {
        'S': "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
      },
      'requisitor': {
        'S': "admin"
      },
      'requisitor_id': {
        'S': "1"
      },
      'created_at': {
        'S': "2000-10-31T01:30:00.000-05:00"
      }
    },
  }

def item_dynamodb():
  return {
    'id': {
      'S': "2c1544c9-29d1-4b3d-a405-231ee465d8fe"
    },
    'token': {
      'S': "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
    },
    'requisitor': {
      'S': "admin"
    },
    'requisitor_id': {
      'S': "1"
    },
    'created_at': {
      'S': "2000-10-31T01:30:00.000-05:00"
    }
  }