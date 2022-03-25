import json
import jwt
import os

def response(status: int, body: dict) -> dict:
  return {
    'statusCode': status,
    'headers': { 'Content-Type': 'application/json' },
    'body': json.dumps(body)
  }

def auth(event):
  assert isinstance(event['headers'], dict)
  assert isinstance(event['headers']['Authorization'], str)

  token = event['headers']['Authorization'].replace('Bearer ', '')

  return jwt.decode(token, os.environ['JWT_SECRET'])