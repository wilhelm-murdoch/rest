# -*- coding: utf-8 -*-
from .handler import EndpointHandler

def endpoint(app, rule):
    def decorator(cls):
        handler = EndpointHandler(rule, cls)
        app.add_url_rule(handler.collection_handler_rule, handler.collection_handler_name, handler.collection_handler)
        app.add_url_rule(handler.resource_handler_rule, handler.resource_handler_name, handler.resource_handler)

    return decorator
