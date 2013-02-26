# -*- coding: utf-8 -*-

class APIError(Exception):
    pass

class BadRequest(APIError):
    code = 400

class MethodNotAllowed(APIError):
    code = 405

class InternalServerError(APIError):
    code = 500

class NotFound(APIError):
    code = 404
