# -*- coding: utf-8 -*-
from unittest import TestCase
from flask import Flask
from rest import endpoint

app = Flask(__name__)
app.config['TESTING'] = True

@endpoint(app, '/testcases/<int:case_id>/simples')
class SimpleEndpoint(object):

    def __init__(self, case_id):
        self.case_id = case_id

    def all(self):
        return [
            {'case' : self.case_id, 'simple' : 1},
            {'case' : self.case_id, 'simple' : 2},
            {'case' : self.case_id, 'simple' : 3},
        ]

    def one(self, resource_id):
        return {'case' : self.case_id, 'simple' : resource_id}

class TestCore(TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_class(self):
        print 'Resp all: %s' % self.client.get('/testcases/1/simples').data
        print 'Resp one: %s' % self.client.get('/testcases/1/simples/25').data
