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

    user = User().create(payload).save()

    data = {
      'name': user.name,
      'username': user.username,
    }

    return response(201, data)
  except (ValidationError, IntegrityError) as error:
    return response(400, {'message': repr(error)})
  except Exception as error:
    return response(500, {'message': repr(error)})
