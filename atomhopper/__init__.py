#!/usr/bin/env python

__name__         = 'atomhopper'
__version__      = '0.1.0'
__author__       = 'Greg Swift'
__author_email__ = 'greg.swift@rackspace.com'
__license__      = 'ASLv2'

from jinja2 import Environment, PackageLoader
import json
import requests
import keyring

import atomhopper.auth as auth

TEMPLATE = u'generic.j2'
ENDPOINT = u'https://atom.staging.ord1.us.ci.rackspace.net/demo/events'

class AtomFeed(object):
    headers = { 'content-type': 'application/atom+xml' }

    def __init__(self, endpoint, username, **kwargs):
        """
        To authenticate to the feed:
        name: user or tenant identifier
        
        then either of these these parameters for the secret:
        token: existing active auth token
        password: your plaintext password (try to avoid this)
        """
        self.endpoint = endpoint
        token = kwargs.get('token', None)
        password = kwargs.get('password', None)
        auth_endpoint = kwargs.get('auth_endpoint', auth.STAGING_ENDPOINT)
        self.authenticate(token, username, password, auth_endpoint)

    def authenticate(self, token, username, password, auth_endpoint):
        token = auth.get_token(token, username, password, auth_endpoint)
        self.headers['x-auth-token'] = token

    def post(self, data):
        resp = requests.post(self.endpoint, data=data, headers=self.headers)
        resp.raise_for_status()
        self._last_response = resp
        return self._last_response

    def get(self):
        return


class AtomEntry(dict):

    def __init__(self, title, author, email, content, template=TEMPLATE):
        self._set_attribute('title', title)
        self._set_attribute('author', author)
        self._set_attribute('email', email)
        self._content = content
        self._set_attribute('content', json.dumps(content))
        self._template = template
        self._set_attribute('template', self._load_template(template))

    def _set_attribute(self, name, value):
        setattr(self, name, value)
        self[name] = value

    def _load_template(self, template):
        env = Environment(loader=PackageLoader(__name__, 'templates'))
        return env.get_template(template)

    def render(self, template=None, **kwargs):
        if template is None:
            template = self.template
        return template.render(self)



if __name__ == '__main__':

    content = {
        'client': 'kernel.auth',
        'level': 'INFO',
        'content': 'Aug 28 18:55:42 virt-n01 sudo: pam_unix(sudo:session): session closed for user root'
    }

    feed = AtomFeed(ENDPOINT, 'ciengineer', password=keyring.get_password('pyrax','ciengineer'))
    entry = AtomEntry('testing', __author__, __author_email__, content)
    print entry.renger()
    #feed.post(entry.render())