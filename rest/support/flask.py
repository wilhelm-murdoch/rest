# -*- coding: utf-8 -*-
from werkzeug.exceptions import HTTPException
try:
    import json
except ImportError:
    import simplejson as json

class APIException(HTTPException):

    def __init__(self, code, description=None):
        self.code = code
        super(APIException, self).__init__(str(description))
        
    def get_body(self, environ):
        body = {
            'code' : self.code,
            'name' : self.name,
            'message' : self.get_description(environ)
        }
        return json.dumps(body)
    
    def get_headers(self, environ):
        return [('Content-Type', 'application/json')]