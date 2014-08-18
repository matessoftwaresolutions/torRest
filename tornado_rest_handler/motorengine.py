# coding: utf-8
from python_rest_handler import DataManager


class MotorEngineDataManager(DataManager):
    def instance_list(self):
        return self.model.objects.find_all()

    def find_instance_by_id(self, instance_id):
        try:
            return self.instance_list().get(pk=instance_id)
        except self.model.DoesNotExist:
            self.handler.raise_error(404)

    def save_instance(self, data):
        instance = self.model(**data)
        instance.save()
        return instance

    def update_instance(self, instance, data):
        update_query = {}
        for key, value in data.items():
            update_query['set__%s' % key] = value

        instance.update(**update_query)
        return instance

    def delete_instance(self, instance):
        instance.delete()
