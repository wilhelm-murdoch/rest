# -*- coding: utf-8 -*-
from .handler import EndpointHandler, rest_to_flask_exception
from .errors import NotFound

ALL_METHODS = (
    'GET',
    'POST',
    'PUT',
    'DELETE',
    'PATCH'
)

class API(object):
    def __init__(self, app, root):
        self.app = app
        self.root = root

        self.app.register_error_handler(404, rest_to_flask_exception)

    def endpoint(self, rule, resource_id_mapping='<resource_id>'):
        def decorator(cls):
            handler = EndpointHandler('{}/{}'.format(self.root, rule), resource_id_mapping, cls)
            self.app.add_url_rule(handler.collection_handler_rule, handler.collection_handler_name, handler.collection_handler, methods=ALL_METHODS)
            self.app.add_url_rule(handler.resource_handler_rule, handler.resource_handler_name, handler.resource_handler, methods=ALL_METHODS)
            return cls

        return decorator
