import pytest
from functions.authorizer import generate_auth_response, generate_policy_document, handler

class TestAuthorizer:
  def test_generate_policy_document(self):
    effect = 'Allow'
    method_arn = 'arn:aws:execute-api:us-west-2:123456789012:ymy8tbxw7b'

    policy_document = generate_policy_document(effect, method_arn)

    assert isinstance(policy_document, dict)
    assert policy_document == {
      'Version': "2012-10-17",
      'Statement': [
        {
          'Action': "execute-api:Invoke",
          'Effect': effect,
          'Resource': method_arn
        }
      ]
    }

  def test_generate_policy_document_without_effect(self):
    effect = None
    method_arn = 'arn:aws:execute-api:us-west-2:123456789012:ymy8tbxw7b'

    with pytest.raises(AssertionError):
      generate_policy_document(effect, method_arn)


  def test_generate_policy_document_without_method_arn(self):
    effect = 'Allow'
    method_arn = None

    with pytest.raises(AssertionError):
      generate_policy_document(effect, method_arn)

  def test_generate_policy_document_without_effect_and_method_arn(self):
    effect = None
    method_arn = None

    with pytest.raises(AssertionError):
      generate_policy_document(effect, method_arn)
  
  def test_generate_auth_response(self):
    principal_id = '1'
    effect = 'Allow'
    method_arn = 'arn:aws:execute-api:us-west-2:123456789012:ymy8tbxw7b'

    auth_response = generate_auth_response(principal_id, effect, method_arn)

    assert isinstance(auth_response, dict)
    assert auth_response == {
      'principalId': principal_id,
        'policyDocument': {
          'Version': "2012-10-17",
          'Statement': [
            {
              'Action': "execute-api:Invoke",
              'Effect': effect,
              'Resource': method_arn
            }
          ]
        }
      }

  def test_generate_auth_response_without_principal_id(self):
    principal_id = None
    effect = 'Allow'
    method_arn = 'arn:aws:execute-api:us-west-2:123456789012:ymy8tbxw7b'

    auth_response = generate_auth_response(principal_id, effect, method_arn)

    assert isinstance(auth_response, dict)
    assert auth_response == {
      'principalId': principal_id,
        'policyDocument': {
          'Version': "2012-10-17",
          'Statement': [
            {
              'Action': "execute-api:Invoke",
              'Effect': effect,
              'Resource': method_arn
            }
          ]
        }
      }

  def test_generate_auth_response_without_effect(self):
    principal_id = '1'
    effect = None
    method_arn = 'arn:aws:execute-api:us-west-2:123456789012:ymy8tbxw7b'

    with pytest.raises(AssertionError):
      generate_auth_response(principal_id, effect, method_arn)
  
  def test_generate_auth_response_without_method_arn(self):
    principal_id = '1'
    effect = 'Allow'
    method_arn = None

    with pytest.raises(AssertionError):
      generate_auth_response(principal_id, effect, method_arn)
  
  def test_handler_without_event(self):
    response = handler(event={}, context={})

    assert response == "Unauthorized"

  def test_handler_without_authorization_token(self):
    event = {
      'authorizationToken': '',
    }

    response = handler(event, context={})

    assert response == "Unauthorized"
  
  def test_handler_without_method_arn(self):
    event = {
      'authorizationToken': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwibmFtZSI6ImFkbWluIiwidXNlcm5hbWUiOiJhZG1pbiIsInBhc3N3b3JkIjoiZDJWM1pYZGxkMlYzWlhkbGQzTnFaSE5yWkdwcmMycHJjMnBrYTNOcVpBIn0.rJFn7a3z85twb3tCf30j7pH4wWpm5rRjsWZ91pRZ9nw',
      'methodArn': ''
    }

    response = handler(event, context={})

    assert response == "Unauthorized"

  def test_handler_token_expired(self):
    event = {
      'authorizationToken': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwibmFtZSI6ImFkbWluIiwidXNlcm5hbWUiOiJhZG1pbiIsInBhc3N3b3JkIjoiZDJWM1pYZGxkMlYzWlhkbGQzTnFaSE5yWkdwcmMycHJjMnBrYTNOcVpBIiwiZXhwIjowfQ.hPvTpDABxBCb2CodLJ51OtTwkzE1VW5QTW_BFz83o3I',
      'methodArn': 'arn:aws:execute-api:us-west-2:123456789012:ymy8tbxw7b'
    }

    response = handler(event, context={})

    assert response == "Unauthorized"
  
  def test_handler_token_without_user(self, mocker):
    environ_mock = {'JWT_SECRET': 'your-256-bit-secret'}
    event = {
      'authorizationToken': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYW1lIjoiYWRtaW4ifQ.jmAGPb7YzjEmHE4j47Iy3arOfqpRoQBL2eyXWZInt9w',
      'methodArn': 'arn:aws:execute-api:us-west-2:123456789012:ymy8tbxw7b'
    }

    mocker.patch.dict('os.environ', environ_mock)

    response = handler(event, context={})

    assert response == {
      'principalId': None,
        'policyDocument': {
          'Version': '2012-10-17',
          'Statement': [
            {
              'Action': 'execute-api:Invoke',
              'Effect': 'Deny',
              'Resource': event['methodArn']
            }
          ]
        }
      }

  def test_handler_token_with_user(self, mocker):
    environ_mock = {'JWT_SECRET': 'your-256-bit-secret'}
    event = {
      'authorizationToken': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwibmFtZSI6ImFkbWluIiwidXNlcm5hbWUiOiJhZG1pbiIsInBhc3N3b3JkIjoiZDJWM1pYZGxkMlYzWlhkbGQzTnFaSE5yWkdwcmMycHJjMnBrYTNOcVpBIn0.rJFn7a3z85twb3tCf30j7pH4wWpm5rRjsWZ91pRZ9nw',
      'methodArn': 'arn:aws:execute-api:us-west-2:123456789012:ymy8tbxw7b'
    }

    mocker.patch.dict('os.environ', environ_mock)

    response = handler(event, context={})

    assert response == {
      'principalId': 1,
        'policyDocument': {
          'Version': '2012-10-17',
          'Statement': [
            {
              'Action': 'execute-api:Invoke',
              'Effect': 'Allow',
              'Resource': event['methodArn']
            }
          ]
        }
      }

