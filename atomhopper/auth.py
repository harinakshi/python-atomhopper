#!/usr/bin/env python

import requests
import json

STAGING_ENDPOINT = 'https://staging.identity.api.rackspacecloud.com/v2.0/tokens'
ENDPOINT = 'https://identity-internal.api.rackspacecloud.com/v2.0/tokens'
HEADERS = { 'Content-type':'application/json', 'Accept':'application/json' }

class CredentialError(Exception):
  def __init__(self, message):
    Exception.__init__(self, message)


class TokenError(Exception):
  def __init__(self, message):
    Exception.__init__(self, message)


def authenticate(user, password, endpoint=ENDPOINT, headers=HEADERS):
    credentials = json.dumps({ 'auth': {
            'passwordCredentials' : {
                    'username': user, 'password': password } } })
    return requests.get(endpoint, data=credentials, headers=headers)

def get_token(token, user, password, authurl):
    if token is None:
        if None in (user, password):
            raise CredentialError, 'No token or authentication information provided'
        else:
            results = authenticate(user, password, authurl)
            results.raise_for_status()
            token = results.json()[u'access'][u'token'][u'id']
    if not validate_token(token, authurl):
        raise TokenError, 'Invalid token'
    return token

def validate_token(token, endpoint=ENDPOINT):
    return True

