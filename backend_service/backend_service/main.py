import os
from auto_everything.base import Terminal
from auto_everything.database import MongoDB
import backend_service.generated_yrpc.it_has_alternatives_objects as it_has_alternatives_objects
import backend_service.generated_yrpc.it_has_alternatives_rpc as it_has_alternatives_rpc
import backend_service.configuration as configuration

_MONGO_DB_URL = os.getenv("MONGO_DB_URL")
if _MONGO_DB_URL:
    configuration.MONGO_DB_URL = _MONGO_DB_URL

t = Terminal()
mongoDB = MongoDB(configuration.MONGO_DB_URL)

object_database_name = "it_has_alternatives_object"
object_collection = mongoDB.get_database(object_database_name).get_collection(object_database_name) #type: ignore

class My_Service_test_protobuff_code(it_has_alternatives_rpc.Service_test_protobuff_code):
    async def search_alternatives(self, item: it_has_alternatives_objects.Search_Alternative_Request) -> it_has_alternatives_objects.Search_Alternative_Response:
        default_response = it_has_alternatives_objects.Search_Alternative_Response(error=None, alternative_object_list=[])
        try:
            result = object_collection.find() # type: ignore
            object_list = []
            for one in result: #type: ignore
                # print(one) #type: ignore
                object_list.append(it_has_alternatives_objects.An_Object().from_dict(one)) #type: ignore
            default_response.alternative_object_list = object_list
        except Exception as e:
            default_response.error = str(e)
        return default_response

    async def add_alternative(self, item: it_has_alternatives_objects.Add_Object_Request) -> it_has_alternatives_objects.Add_Object_Response:
        default_response = it_has_alternatives_objects.Add_Object_Response(error=None, success=True)
        try:
            result = object_collection.insert_one(
                item.an_object.to_dict() #type: ignore
            )
            # print(item.an_object.to_dict()) #type: ignore
            the_object_id = str(result.inserted_id)
            object_collection.update_one(
                filter={
                    it_has_alternatives_objects.An_Object()._key_string_dict.name: item.an_object.name,
                }, 
                update={
                    "$set": {
                        **item.an_object.to_dict(),
                        "id": the_object_id
                    }
                }
            )
        except Exception as e:
            default_response.error = str(e)
            default_response.success = False
        return default_response

    async def update_alternative(self, item: it_has_alternatives_objects.Update_Object_Request) -> it_has_alternatives_objects.Update_Object_Response:
        default_response = it_has_alternatives_objects.Update_Object_Response(error=None, success=True)

        print(item)
        if (item.an_object == None or item.an_object.name == None):
            default_response.error = "You should give me a name for that object"
            default_response.success = False
            return default_response

        try:
            object_collection.update_one(
                filter={
                    it_has_alternatives_objects.An_Object()._key_string_dict.id: item.an_object.id,
                }, 
                update={
                    "$set": {
                        **item.an_object.to_dict()
                    }
                }
            )
        except Exception as e:
            default_response.error = str(e)
            default_response.success = False

        return default_response

    async def delete_alternative(self, item: it_has_alternatives_objects.Delete_Object_Request) -> it_has_alternatives_objects.Delete_Object_Response:
        default_response = it_has_alternatives_objects.Delete_Object_Response(error=None, success=True)

        if (item.an_object == None or item.an_object.name == None):
            default_response.error = "You should give me a name for that object"
            default_response.success = False
            return default_response

        try:
            object_collection.delete_one(
                filter={
                    it_has_alternatives_objects.An_Object()._key_string_dict.name: item.an_object.name,
                }, 
            )
        except Exception as e:
            default_response.error = str(e)
            default_response.success = False

        return default_response

service_instance = My_Service_test_protobuff_code()
it_has_alternatives_rpc.run(service_instance, port="80")

def main():
    pass
