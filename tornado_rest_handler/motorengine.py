# coding: utf-8
from python_rest_handler import DataManager
from tornado import gen
 
class MotorEngineDataManager(DataManager):
    
    @gen.coroutine
    def instance_list(self, query_filters={}):
        query_set = self.model.objects
        
        if query_filters:
            query_set = query_set.filter(**query_filters)
            
        results = yield query_set.find_all()
        return results
    
    @gen.coroutine
    def find_instance_by_id(self, instance_id):
        try:
            instance = yield self.model.objects.get(instance_id)
            return instance
        except Exception as e:
            print(e)
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
