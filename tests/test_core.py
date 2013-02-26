# -*- coding: utf-8 -*-
from unittest import TestCase
from flask import Flask, make_response, request
from rest import API
import json

app = Flask(__name__)
app.config['TESTING'] = True

api = API(app, '/test')

@api.endpoint('stores/<int:store_id>/apples')
class AppleEndpoint(object):

    def __init__(self, store_id):
        self.store_id = store_id

    def all(self):
        return [{'store' : self.store_id, 'apple' : x} for x in xrange(3)]

    def one(self, resource_id):
        return {'store' : self.store_id, 'apple' : resource_id}

@api.endpoint('stores/<int:store_id>/bananas','<int:banana_id>')
class BananaEndpoint(object):

    def __init__(self, store_id):
        self.store_id = store_id

    def make_response(self, o):
        headers = {'Content-Type' : 'application/json'}

        if o:
            body = json.dumps({
                'meta' : {'status' : 'ok'},
                'response' : o
            })
            status = 200
        else:
            body = ''
            status = 204
        if request.method == 'POST':
            status = 201
        return make_response((body, status, headers))

    def all(self):
        return [{'store' : self.store_id, 'banana' : x} for x in xrange(3)]

    def one(self, banana_id):
        return {'store' : self.store_id, 'banana' : banana_id}

class TestCore(TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_simple(self):
        apples = AppleEndpoint(1)

        all_response = self.client.get('/test/stores/1/apples')
        self.assertEqual(all_response.headers['Content-Type'], 'application/json')
        self.assertEqual(apples.all(), json.loads(all_response.data))

        one_response = self.client.get('/test/stores/1/apples/25')
        self.assertEqual(apples.one('25'), json.loads(one_response.data))

    def test_complex_class(self):
        bananas = BananaEndpoint(1)

        all_response = self.client.get('/test/stores/1/bananas')
        self.assertEqual(all_response.headers['Content-Type'], 'application/json')
        self.assertEqual(bananas.all(), json.loads(all_response.data)['response'])

        one_response = self.client.get('/test/stores/1/bananas/25')
        self.assertEqual(bananas.one(25), json.loads(one_response.data)['response'])

    def test_errors(self):
        delete_response = self.client.delete('/test/stores/1/bananas/1')
        self.assertEqual(delete_response.status_code, 405)
        resp = json.loads(delete_response.data)
        self.assertEqual(resp['name'], 'Method Not Allowed')

        unknow_route_response = self.client.get('/test/foo/bar/baz')
        resp = json.loads(unknow_route_response.data)
        self.assertEqual(unknow_route_response.status_code, 404)
        self.assertEqual(resp['name'], 'Not Found')

