# -*- coding: utf-8 -*-
from flask import request
import inspect

class BaseHandler(object):

    def __init__(self, cls):
        self.cls = cls

    def _args_to_init_and_method_args(self, args):
        init_arg_names = inspect.getargspec(self.cls.__init__).args
        init_arg_names.remove('self')

        in_args = args.copy()

        init_kwargs = {}
        for arg, val in in_args.items():
            if arg in init_arg_names:
                init_kwargs[arg] = val
                del in_args[arg]

        return init_kwargs, in_args

class CollectionHandler(BaseHandler):

    def __call__(self, **kwargs):
        init_args, method_args = self._args_to_init_and_method_args(kwargs)

        instance = self.cls(**init_args)

        try:
            if request.method == 'GET':
                return str(instance.all(**method_args))
        except AttributeError:
            raise 

        return ''

class ResourceHandler(BaseHandler):

    def __call__(self, **kwargs):
        init_args, method_args = self._args_to_init_and_method_args(kwargs)

        instance = self.cls(**init_args)

        try:
            if request.method == 'GET':
                return str(instance.one(**method_args))
        except AttributeError:
            raise 

        return ''

class EndpointHandler(object):

    def __init__(self, rule, cls):
        self.rule = rule
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
        return '{}/<resource_id>'.format(self.rule)
