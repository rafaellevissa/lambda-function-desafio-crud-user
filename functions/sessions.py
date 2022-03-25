from lib.session import Session
from lib.utils import response
from lib.utils import auth

def handler(event, context):
  try:
    user = auth(event)

    sessions = Session().get_by_requisitor(str(user['id']))

    data = {
      'user': user,
      'sessions': sessions
    }

    return response(200, data)
  except Exception as error:
    return response(500, {'message': repr(error)})
