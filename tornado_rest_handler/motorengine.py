# coding: utf-8
from python_rest_handler import DataManager
from tornado import gen

class Yield(Exception):
    def __init__(self, future, callback):
        self.future = future
        self.callback = callback

    def resume(self):
        self.callback(self.future)

class MotorEngineDataManager(DataManager):
    __asynchronous__ = True
    @gen.coroutine
    def instance_list(self, query_filters={}, access_control_filters={}):
        query_set = self.model.objects
        
        if query_filters:
            query_set = query_set.filter(**query_filters)
        if access_control_filters:
            query_set = query_set.filter(**access_control_filters)
            
        results = yield query_set.find_all()
        return results
    
    @gen.coroutine
    def find_instance_by_id(self, instance_id):
        try:
            instance = self.instance_list().get(pk=instance_id)
            instance._id = instance_id
            return instance
        
        except self.model.DoesNotExist:
            self.handler.raise_error(404)

    @gen.coroutine
    def save_instance(self, data):
        instance = self.model(**data)
        yield instance.save()
        return instance

    @gen.coroutine
    def update_instance(self, instance, data):
        for key, value in data.items():
            setattr(instance, key, value)

        yield instance.save()
        return instance

    @gen.coroutine
    def delete_instance(self, instance):
        yield instance.delete()
