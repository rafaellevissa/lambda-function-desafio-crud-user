import json
from pymysql import IntegrityError
from jsonschema import validate, ValidationError
from lib.user import User
from lib.utils import response
from lib.schemas import register_user_schema

def handler(event, context):
  try:
    payload = json.loads(event['body'])

    validate(instance=payload, schema=register_user_schema)

    user =  User().find_by_username(payload['username'])

    if user:
      raise ValueError('The username is registered already')

    user = User().create(payload).save()

    data = {
      'name': user.name,
      'username': user.username,
    }

    return response(201, data)
  except (ValidationError, IntegrityError, ValueError) as error:
    data = {'message': str(error)}
    return response(400, data)
  except Exception as error:
    data = {'message': str(error)}
    return response(500, data)
