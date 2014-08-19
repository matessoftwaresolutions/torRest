# coding: utf-8
from json.decoder import JSONDecoder
from python_rest_handler.data_managers.mongoengine import MongoEngineDataManager
from python_rest_handler.prh import RestRequestHandler
from tornado.web import RequestHandler
import python_rest_handler
import tornado.web


class TornadoRestHandler(RequestHandler, RestRequestHandler):
    def get(self, instance_id=None, edit=False):
        return self.rest_handler._get(instance_id=instance_id, edit=edit)

    def post(self, instance_id=None, action=None):
        return self.rest_handler._post(instance_id=instance_id, action=action)

    def put(self, instance_id):
        return self.rest_handler._put(instance_id=instance_id)

    def delete(self, instance_id):
        return self.rest_handler._delete(instance_id=instance_id)


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
        # JSON Requests
        data = {}
        content_type = self.request.headers.get("Content-Type", "")
        if content_type.startswith("application/json"):
            try:
                request = self.request.body.decode()
                data = JSONDecoder().decode(request or '{}')
            except ValueError:
                data = {}
        else:
            for arg in list(self.request.arguments.keys()):
                data[arg] = self.get_argument(arg)
                if data[arg] == '':  # Tornado 3.0+ compatibility
                    data[arg] = None
        return data

    def render(self, template_name, **kwargs):
        return super(TornadoRestHandler, self).render(template_name, **kwargs)

    def redirect(self, url, permanent=False, status=None, **kwargs):
        return super(TornadoRestHandler, self).redirect(url, permanent=permanent, status=status)

    def get_current_user(self):
        return super().get_current_user()
    
    def is_authorized(self, action='', instance_id=None, instance=None, query_filters={}, **kwargs):
        return True

def routes(route_list):
    return python_rest_handler.routes(route_list)


def rest_routes(model, data_manager=MongoEngineDataManager, base_handler_type=TornadoRestHandler, **kwargs):
    return python_rest_handler.rest_routes(model, data_manager, base_handler_type, **kwargs)


def activate_plugin(name):
    return python_rest_handler.activate_plugin(name)


def deactivate_plugin(name):
    return python_rest_handler.deactivate_plugin(name)
