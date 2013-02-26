# -*- coding: utf-8 -*-
from flask import request, make_response
import sys
from .errors import *
from .support.flask import APIException
from werkzeug.exceptions import HTTPException
from .utils import get_argument_names_for_a_function
try:
    import json
except ImportError:
    import simplejson as json

ALLOWED_METHODS_COLLECTION = {
    'GET' : 'all',
    'OPTIONS' : 'all',
    'HEAD' : 'all',
    'POST' : 'create',
    'PUT' : 'update_all',
    'PATCH' : 'update_all_partial',
    'DELETE' : 'delete_all',
}

ALLOWED_METHODS_RESOURCE = {
    'GET' : 'one',
    'OPTIONS' : 'one',
    'HEAD' : 'one',
    'PUT' : 'update',
    'PATCH' : 'updatepartial',
    'DELETE' : 'delete',
}

def rest_to_flask_exception(e):
    return APIException(e.code, e.message)

def raise_rest_to_flask_exception(e):
    _, _, traceback = sys.exc_info()
    raise APIException, (e.code, e.message), traceback

def default_response_converter(response):
    headers = {'Content-Type' : 'application/json'}

    if response:
        body = json.dumps(response)
        status = 200
    else:
        body = ''
        status = 204
    if request.method == 'POST':
        status = 201
    return make_response((body, status, headers))

class BaseHandler(object):

    def __init__(self, cls):
        self.cls = cls

    def _args_to_init_and_method_args(self, args):
        init_arg_names = get_argument_names_for_a_function(self.cls.__init__)
        init_arg_names.remove('self')

        in_args = args.copy()

        init_kwargs = {}
        for arg, val in in_args.items():
            if arg in init_arg_names:
                init_kwargs[arg] = val
                del in_args[arg]

        return init_kwargs, in_args

    def __call__(self, **kwargs):
        init_args, method_args = self._args_to_init_and_method_args(kwargs)
        
        try:
            instance = self.cls(**init_args)

            handler = self.methods_mappings[request.method]
            if not hasattr(instance, handler):
                raise MethodNotAllowed('{} is not allowed'.format(request.method))
            else:
                result = getattr(instance, handler)(**method_args)
                if hasattr(instance, 'make_response'):
                    result = getattr(instance, 'make_response')(result)
                else:
                    result = default_response_converter(result)
                return result
        except APIError, e:
            raise_rest_to_flask_exception(e)
        except HTTPException, e:
            raise
        except Exception, e:
            e = InternalServerError(e)
            raise_rest_to_flask_exception(e)

class CollectionHandler(BaseHandler):
    methods_mappings = ALLOWED_METHODS_COLLECTION

class ResourceHandler(BaseHandler):
    methods_mappings = ALLOWED_METHODS_RESOURCE

class EndpointHandler(object):

    def __init__(self, rule, resource_id_mapping, cls):
        self.rule = rule
        self.resource_id_mapping = resource_id_mapping
        self.cls = cls

    @property
    def collection_handler(self):
        return CollectionHandler(self.cls)

    @property
    def collection_handler_name(self):
        return '{}.{}.collection'.format(self.cls.__module__, self.cls.__name__)

    @property
    def collection_handler_rule(self):
        return self.rule

    @property
    def resource_handler(self):
        return ResourceHandler(self.cls)

    @property
    def resource_handler_name(self):
        return '{}.{}.resource'.format(self.cls.__module__, self.cls.__name__)

    @property
    def resource_handler_rule(self):
        return '{}/{}'.format(self.rule, self.resource_id_mapping)
