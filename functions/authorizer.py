import jwt
import os

def generate_policy_document(effect: str, method_arn: str) -> dict:
  assert effect
  assert method_arn

  policy_document = {
    'Version': "2012-10-17",
    'Statement': [
      {
        'Action': "execute-api:Invoke",
        'Effect': effect,
        'Resource': method_arn
      }
    ]
  }

  return policy_document

def generate_auth_response(principal_id, effect, method_arn):
  policy_document = generate_policy_document(effect, method_arn)

  return {
    'principalId': principal_id,
    'policyDocument': policy_document
  }

def handler(event, context):
  try:
    token = 'authorizationToken' in event and event['authorizationToken'].replace('Bearer ', '')
    method_arn = event.get('methodArn')

    if not token or not method_arn:
      raise Exception()

    user = jwt.decode(token, os.environ['JWT_SECRET'], algorithms=["HS256"])

    if isinstance(user, dict) and 'id' in user:
      return generate_auth_response(user['id'], 'Allow', method_arn)
    else:
      return generate_auth_response(user.get('id'), 'Deny', method_arn)
  except:
    return "Unauthorized"
