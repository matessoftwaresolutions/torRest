# coding: utf-8
from python_rest_handler.data_managers.mongoengine import MongoEngineDataManager
from tornado.testing import AsyncTestCase
from tornado_rest_handler.trh import rest_routes, TornadoRestHandler
from unittest.mock import Mock
import python_rest_handler
import tornado


# All tests moved to the python-rest-handler library

class Model(object):
    pass



class TemplatePathTests(AsyncTestCase):
    def test_rest_routes(self):
        cls = rest_routes(Model)[0][1]
        self.assertEquals(True, issubclass(cls, TornadoRestHandler))
        self.assertEquals(True, issubclass(cls, tornado.web.RequestHandler))
        self.assertEquals(True, issubclass(cls, python_rest_handler.RestRequestHandler))

        self.assertEquals(MongoEngineDataManager, cls.data_manager)

        self.assertEquals('model/', cls.template_path)
        self.assertEquals('list.html', cls.list_template)
        self.assertEquals('edit.html', cls.edit_template)
        self.assertEquals('show.html', cls.show_template)
        self.assertEquals('/', cls.redirect_pos_action)
