import sys
sys.path.insert(0,'..')

import multiprocessing
import os
import re
from time import sleep
from typing import Any

from auto_everything.base import Terminal
from auto_everything.database import MongoDB
from auto_everything.disk import Disk
from auto_everything.cryptography import EncryptionAndDecryption, Password_Generator
from auto_everything.cryptography import JWT_Tool

import backend_service.generated_yrpc.it_has_alternatives_objects as it_has_alternatives_objects
import backend_service.generated_yrpc.it_has_alternatives_rpc as it_has_alternatives_rpc
import backend_service.configuration as configuration


t = Terminal()
disk = Disk()

_MONGO_DB_URL = os.getenv("MONGO_DB_URL")
if _MONGO_DB_URL:
    configuration.MONGO_DB_URL = _MONGO_DB_URL
mongoDB = MongoDB(configuration.MONGO_DB_URL)

encryption_and_decryption = EncryptionAndDecryption()
secret_dict = encryption_and_decryption.get_secret_alphabet_dict(a_secret_string=configuration.SECRET_TEXT)
password_generator = Password_Generator(configuration.SECRET_TEXT)
jwt_tool = JWT_Tool()

object_database_name = "it_has_alternatives_object"
user_database_name = "user"
object_collection = mongoDB.get_database(object_database_name).get_collection(object_database_name) #type: ignore
user_collection = mongoDB.get_database(object_database_name).get_collection(user_database_name) #type: ignore


class Visitor_Service(it_has_alternatives_rpc.Service_it_has_alternatives):
    async def get_special_jwt(self, item: it_has_alternatives_objects.Get_Special_JWT_Request) -> it_has_alternatives_objects.Get_Special_JWT_Response:
        default_response = it_has_alternatives_objects.Get_Special_JWT_Response()
        try:
            if (item.email != None and item.password != None):
                email = encryption_and_decryption.decode_message(secret_dict, item.email)
                # email = item.email
                if re.match(r"[^@]+@[^@]+\.[^@]+", email) is None:
                    default_response.error = "You should give me an valid email"
                    return default_response
                
                if email != "yingshaoxo@gmail.com":
                    default_response.error = "Sorry, this page is for admin only"
                    return default_response
                
                a_user: Any = user_collection.find_one({
                    "email": email,
                })
                if (a_user != None):
                    # check if user password match, if not, stop here
                    a_user_2: Any = user_collection.find_one({
                        "email": email,
                        "password": item.password
                    })
                    if (a_user_2 == None):
                        default_response.error = "Sorry, you don't have the right password"
                        return default_response
                else:
                    # check if user exists, if not, create a new one
                    user_collection.insert_one(
                        {
                            "email": email,
                            "password": item.password
                        }
                    )

                random_string = password_generator.get_random_password(length=10)
                the_jwt_code = jwt_tool.my_jwt_encode(
                    data={
                        "email": email,
                        "random_string": random_string
                    }, 
                    a_secret_string_for_integrity_verifying=configuration.SECRET_TEXT,
                    use_md5=True
                )
                the_jwt_code = encryption_and_decryption.encode_message(secret_dict, the_jwt_code)
                user_collection.update_one(
                    {
                        "email": email,
                    },
                    {
                        "$set": {
                            "jwt": the_jwt_code
                        }
                    }
                )
                default_response.encrypted_jwt = the_jwt_code
                return default_response
            else:
                default_response.error = "You should give me email and password"
                return default_response
        except Exception as e:
            default_response.error = str(e)
        return default_response

    async def is_jwt_ok(self, item: it_has_alternatives_objects.is_JWT_ok_Request) -> it_has_alternatives_objects.is_JWT_ok_Response:
        default_response = it_has_alternatives_objects.is_JWT_ok_Response()
        raw_jwt_string = item.jwt

        if raw_jwt_string == None:
            default_response.error = "error, you should give me the jwt string"
            return default_response
        else:
            try:
                user: Any = user_collection.find_one({
                    "jwt": raw_jwt_string
                })

                if user == None:
                    default_response.error = "error, this jwt is not valid. no user related to it."
                    return default_response

                email = user.get("email")
                if (email is None):
                    default_response.error = "error: email do not exists, which shouldn't happen."
                    return default_response
                elif email == "yingshaoxo@gmail.com": 
                    default_response.is_admin = True
                    default_response.ok = True
                    return default_response
                else:
                    default_response.is_admin = False
                    default_response.ok = True
                    return default_response
            except Exception as e:
                print(f"error: {e}")
                default_response.error = str(e)
                return default_response

    async def search_alternatives(self, item: it_has_alternatives_objects.Search_Alternative_Request) -> it_has_alternatives_objects.Search_Alternative_Response:
        default_response = it_has_alternatives_objects.Search_Alternative_Response(error=None, alternative_object_list=[])
        key_words = item.key_words
        if key_words == None:
            key_words = ""

        try:
            result = object_collection.find(
                {
                    it_has_alternatives_objects.An_Object()._key_string_dict.name: 
                        {
                            '$regex':f'(.*){key_words}(.*)',
                            "$options": "i"
                        }
                }
            ).skip(item.page_number*item.page_size).limit(item.page_size) # type: ignore

            object_list = []
            for one in result: #type: ignore
                # print(one) #type: ignore
                object_list.append(it_has_alternatives_objects.An_Object().from_dict(one)) #type: ignore
            default_response.alternative_object_list = object_list
        except Exception as e:
            default_response.error = str(e)
        return default_response

    async def get_an_object(self, item: it_has_alternatives_objects.Get_an_object_Request) -> it_has_alternatives_objects.Get_an_object_Response:
        default_response = it_has_alternatives_objects.Get_an_object_Response()
        try:
            result = object_collection.find(
                {
                    it_has_alternatives_objects.An_Object()._key_string_dict.id: 
                        {
                            '$regex':f'^{item.id}$',
                            "$options": "i"
                        }
                }
            )

            object_list = []
            for one in result: #type: ignore
                object_list.append(it_has_alternatives_objects.An_Object().from_dict(one)) #type: ignore
            
            if (len(object_list) > 0):
                default_response.an_object = object_list[0]
        except Exception as e:
            default_response.error = str(e)
        return default_response


class User_Service(Visitor_Service):
    pass


class Admin_Service(User_Service):
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


def run_visitor_grpc_service(port: str):
    vue_html_file_folder = disk.join_paths(disk.get_directory_name(__file__), "./vue")  

    service_instance = Visitor_Service()
    it_has_alternatives_rpc.run(service_instance, port=port, html_folder_path=vue_html_file_folder)


def run_admin_grpc_service(port: str):
    service_instance = Admin_Service()
    it_has_alternatives_rpc.run(service_instance, port=port)


def run_restful_service(port: str):
    from fastapi import FastAPI
    from fastapi import Request, Response, status
    from starlette.responses import FileResponse 
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.staticfiles import StaticFiles
    import uvicorn

    app = FastAPI()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/v1/jwt_auth_gateway/", response_model=str)
    async def v1_jwt_auth_gateway(request: Request, response: Response):
        raw_jwt_string = request.headers.get("jwt", None)
        if raw_jwt_string == None:
            response.status_code = status.HTTP_401_UNAUTHORIZED
            return "error"
        else:
            user: Any = user_collection.find_one({
                "jwt": raw_jwt_string
            })

            if user == None:
                response.status_code = status.HTTP_401_UNAUTHORIZED
                return "error"

            email = user.get("email")
            if (email is None):
                response.status_code = status.HTTP_401_UNAUTHORIZED
                return "error: email do not exists, which shouldn't happen"
            else:
                response.headers.update({
                    "email": email
                })
                response.status_code = status.HTTP_202_ACCEPTED
                return "ok"

    @app.get("/v1/admin_jwt_auth_gateway/", response_model=str)
    async def v1_admin_jwt_auth_gateway(request: Request, response: Response):
        raw_jwt_string = request.headers.get("jwt", None)
        if raw_jwt_string == None:
            response.status_code = status.HTTP_401_UNAUTHORIZED
            return "error"
        else:
            user: Any = user_collection.find_one({
                "jwt": raw_jwt_string
            })

            if user == None:
                response.status_code = status.HTTP_401_UNAUTHORIZED
                return "error"

            email = user.get("email")
            if (email is None):
                response.status_code = status.HTTP_401_UNAUTHORIZED
                return "error: email do not exists, which shouldn't happen"
            elif email == "yingshaoxo@gmail.com": 
                response.headers.update({
                    "email": email
                })
                response.status_code = status.HTTP_202_ACCEPTED
                return 'ok'
            else:
                response.status_code = status.HTTP_401_UNAUTHORIZED
                return "sorry, you are not admin"

    uvicorn.run(app=app, # type: ignore #"src.main:app", 
                host="0.0.0.0",
                port=int(port)) 


def start():
    process_0 = multiprocessing.Process(target=run_restful_service, args=("5550",))
    process_1 = multiprocessing.Process(target=run_visitor_grpc_service, args=("5551",))
    process_2 = multiprocessing.Process(target=run_admin_grpc_service, args=("5552",))

    process_0.start()
    process_1.start()
    process_2.start()

    while all([
        process_0.is_alive(),
        process_1.is_alive(),
        process_2.is_alive()
    ]):
        sleep(10)

    # # Wait processes to complete
    # process_0.join()
    # process_1.join()
    # process_2.join()


def main():
    start()


if __name__ == '__main__':
    start()