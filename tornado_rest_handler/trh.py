# coding: utf-8
from python_rest_handler.data_managers.mongoengine import MongoEngineDataManager
from python_rest_handler.prh import RestRequestHandler
from tornado import gen
from tornado.web import RequestHandler
from tornado_rest_handler.motorengine import Yield
import python_rest_handler
import tornado.web


class TornadoRestHandler(RequestHandler, RestRequestHandler):
    @gen.coroutine
    def get(self, instance_id=None):
        if hasattr(self, "rest_handler"):
            return self.rest_handler._get(instance_id=instance_id)
        else:
            super().get()
            

    @gen.coroutine
    def post(self, instance_id=None):
        if hasattr(self, "rest_handler"):
            return self.rest_handler._post(instance_id=instance_id)
        else:
            super().post()

    @gen.coroutine
    def put(self, instance_id):
        if hasattr(self, "rest_handler"):
            return self.rest_handler._put(instance_id=instance_id)
        else:
            super().put()
    
    @gen.coroutine
    def delete(self, instance_id):
        if hasattr(self, "rest_handler"):
            return self.rest_handler._delete(instance_id=instance_id)
        else:
            super().delete()


    def raise_error(self, code):
        if code == 403:
            raise tornado.web.HTTPError(code, 'Not enough permissions to perform this action')
        elif code == 404:
            raise tornado.web.HTTPError(code, 'Object not found')
        elif code == 405:
            raise tornado.web.HTTPError(code, 'Method Not Allowed')

    def get_request_uri(self):
        return self.request.uri

    def get_request_data(self):
        data = {}
        for arg in list(self.request.arguments.keys()):
            data[arg] = self.get_argument(arg)
            if data[arg] == '':  # Tornado 3.0+ compatibility
                data[arg] = None
        return data

    def redirect(self, url, permanent=False, status=None, **kwargs):
        return super().redirect(url, permanent=permanent, status=status)
    

    # Access Control
    def get_current_user(self):
        return None
    
    def is_authorized(self, action='', instance_id=None, instance=None, query_filters={}, **kwargs):
        return True
    
    def get_access_control_filters(self): 
        return {}

def rest_routes(model, data_manager=MongoEngineDataManager, base_handler_type=TornadoRestHandler, **kwargs):
    return python_rest_handler.rest_routes(model, data_manager, base_handler_type, **kwargs)

