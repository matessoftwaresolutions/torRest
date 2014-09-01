# coding: utf-8
from python_rest_handler.prh_async import AsyncRestRequestHandler
from tornado import gen
from tornado.web import RequestHandler
from tornado_rest_handler.motorengine import MotorEngineDataManager
import python_rest_handler
import tornado

class TornadoRestHandler(RequestHandler, AsyncRestRequestHandler):
    async_decorator = gen.coroutine 
    
    @gen.coroutine 
    def get(self, instance_id=None):
        if hasattr(self, "rest_handler"):
            yield self.rest_handler.get(instance_id=instance_id)
        else:
            super().get()
            
    @gen.coroutine
    def post(self, instance_id=None):
        if hasattr(self, "rest_handler"):
            yield self.rest_handler.post(instance_id=instance_id)
        else:
            super().post()

    @gen.coroutine
    def put(self, instance_id):
        if hasattr(self, "rest_handler"):
            yield self.rest_handler.put(instance_id=instance_id)
        else:
            super().put()
    
    @gen.coroutine
    def delete(self, instance_id):
        if hasattr(self, "rest_handler"):
            yield self.rest_handler.delete(instance_id=instance_id)
        else:
            super().delete()

    # NOT ASYNC
    def raise_error(self, code):
        if code == 403:
            raise tornado.web.HTTPError(code, 'Not enough permissions to perform this action')
        elif code == 404:
            raise tornado.web.HTTPError(code, 'Object not found')
        elif code == 405:
            raise tornado.web.HTTPError(code, 'Method Not Allowed')
        else:
            raise tornado.web.HTTPError(code)

    # NOT ASYNC         
    def get_request_uri(self):
        return self.request.uri

    # NOT ASYNC
    def get_request_data(self):
        data = {}
        for arg in list(self.request.arguments.keys()):
            data[arg] = self.get_argument(arg)
            if data[arg] == '':  # Tornado 3.0+ compatibility
                data[arg] = None
        return data

    # NOT ASYNC
    def redirect(self, url, permanent=False, status=None, **kwargs):
        return super().redirect(url, permanent=permanent, status=status)
    
    # Access Control
    # NOT ASYNC
    def get_current_user(self):
        return None
    
    # NOT ASYNC
    def authorize(self, action, instances=[],
                  instance_id=None, request_data={}, query_filters={}):
        return True
    
def rest_routes(model, data_manager=MotorEngineDataManager, request_handler=TornadoRestHandler, **kwargs):
    return python_rest_handler.rest_routes(model, data_manager, request_handler, **kwargs)

