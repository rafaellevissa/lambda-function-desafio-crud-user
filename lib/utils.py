import json
import jwt
import os

def response(status: int, body: dict) -> dict:
  return {
    'statusCode': status,
    'headers': { 
      'Content-Type': 'application/json',
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Credentials': True,
    },
    'body': json.dumps(body)
  }

def auth(event):
  assert isinstance(event['headers'], dict)
  assert isinstance(event['headers']['Authorization'], str)

  token = event['headers']['Authorization'].replace('Bearer ', '')

  return jwt.decode(token, os.environ['JWT_SECRET'], algorithms=["HS256"])