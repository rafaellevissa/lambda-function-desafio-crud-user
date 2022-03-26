import os
import json
import jwt
from jsonschema import validate, ValidationError
from lib.hash import Hash
from lib.user import User
from lib.schemas import login_schema
from lib.utils import response
from lib.session import Session
from datetime import datetime, timedelta, timezone


def handler(event, context):
  try:
    payload = json.loads(event['body'])

    validate(instance=payload, schema=login_schema)

    user = User().find_by_username(payload['username'])
    not_found = 'The user was not found'

    if not user:
      raise Exception(not_found)
    
    password_match = Hash().check(
      payload['password'],
      user['password']
    )
    
    if not password_match:
      raise Exception(not_found)

    access_token_dict = {
      **user,
      'exp': datetime.now(tz=timezone.utc) + timedelta(hours=1)
    }

    access_token = jwt.encode(access_token_dict, os.environ['JWT_SECRET'], algorithm="HS256").decode('utf8')

    data = {'access_token': access_token}

    Session().put({
      'token': access_token,
      'requisitor': user['username'],
      'requisitor_id': str(user['id'])
    })

    return response(200, data)
  except ValidationError as error:
    return response(400, {'message': repr(error)})
  except Exception as error:
    return response(500, {'message': repr(error)})
