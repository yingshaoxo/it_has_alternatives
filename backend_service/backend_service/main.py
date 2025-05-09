import sys
sys.path.insert(0,'..')

import multiprocessing
import os
import re
from time import sleep
from datetime import datetime
from typing import Any

from auto_everything.base import Terminal
from auto_everything.database import MongoDB
from auto_everything.disk import Disk
from auto_everything.io import IO
from auto_everything.cryptography import Encryption_And_Decryption, Password_Generator, JWT_Tool
from auto_everything.time import Time

import backend_service.generated_yrpc.it_has_alternatives_objects as it_has_alternatives_objects
import backend_service.generated_yrpc.it_has_alternatives_rpc as it_has_alternatives_rpc
import backend_service.configuration as configuration


t = Terminal()
disk = Disk()
io_ = IO()
time_ = Time()

_ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")
if _ADMIN_EMAIL:
    configuration.ADMIN_EMAIL = _ADMIN_EMAIL

_MONGO_DB_URL = os.getenv("MONGO_DB_URL")
if _MONGO_DB_URL:
    configuration.MONGO_DB_URL = _MONGO_DB_URL
mongoDB = MongoDB(configuration.MONGO_DB_URL)

encryption_and_decryption = Encryption_And_Decryption()
secret_dict = encryption_and_decryption.get_secret_alphabet_dict(a_secret_string=configuration.SECRET_TEXT)
password_generator = Password_Generator(configuration.SECRET_TEXT)
jwt_tool = JWT_Tool()

object_database_name = "it_has_alternatives_object"
object_collection = mongoDB.get_database(object_database_name).get_collection(object_database_name) #type: ignore
user_collection = mongoDB.get_database(object_database_name).get_collection("user") #type: ignore


def get_a_user_by_email(email: str) -> it_has_alternatives_objects.A_User | None:
    a_user = user_collection.find_one(
        {
            it_has_alternatives_objects.A_User._key_string_dict.email: email
        }
    )
    if a_user == None:
        return None
    else:
        a_user = it_has_alternatives_objects.A_User().from_dict(a_user)
        return a_user

def update_last_login_time_for_a_user(user_email: str):
    user_collection.update_one(
        {
            it_has_alternatives_objects.A_User._key_string_dict.email: user_email,
        },
        {
            "$set": {
                it_has_alternatives_objects.A_User._key_string_dict.last_login_time_in_10_numbers_timestamp_format: time_.get_current_timestamp_in_10_digits_format(),
            }
        }
    )

def mongodb_item_to_dict(item: Any) -> dict[str, Any]:
    a_dict = {**item}
    del a_dict["_id"]
    return a_dict

def get_invitation_code(email: str, code: str) -> str:
    jwt_string = jwt_tool.my_jwt_encode(data={
        it_has_alternatives_objects.A_User._key_string_dict.email: email,
        "code": code,
    }, a_secret_string_for_integrity_verifying=configuration.SECRET_TEXT, use_md5=True)
    return jwt_string

def decode_invitation_code(jwt_code: str) -> tuple[it_has_alternatives_objects.A_User | None, str | None]:
    data = jwt_tool.my_jwt_decode(jwt_string=jwt_code, a_secret_string_for_integrity_verifying=configuration.SECRET_TEXT)
    if data == None:
        return None, None
    email = data.get(it_has_alternatives_objects.A_User._key_string_dict.email)
    code = data.get("code")
    if email == None or code == None:
        return None, None
    a_user = user_collection.find_one(
        {
            it_has_alternatives_objects.A_User._key_string_dict.email: email
        }
    )
    if a_user == None:
        return None, None
    else:
        a_user = it_has_alternatives_objects.A_User().from_dict(a_user)
        if code in a_user.invitation_code_list:
            return a_user, code
        else:
            return None, None


class Visitor_Service(it_has_alternatives_rpc.Service_it_has_alternatives):
    async def get_special_jwt(self, headers: dict[str, str], item: it_has_alternatives_objects.Get_Special_JWT_Request) -> it_has_alternatives_objects.Get_Special_JWT_Response:
        default_response = it_has_alternatives_objects.Get_Special_JWT_Response()
        try:
            if (item.email != None and item.password != None):
                email = encryption_and_decryption.decode_message(secret_dict, item.email)
                # email = item.email
                if re.match(r"[^@]+@[^@]+\.[^@]+", email) is None:
                    default_response.error = "You should give me an valid email"
                    return default_response
                if item.password.strip() == "":
                    default_response.error = "You should give me an valid password"
                    return default_response

                a_user: Any = user_collection.find_one({
                    it_has_alternatives_objects.A_User._key_string_dict.email: email,
                })
                if (a_user != None):
                    # check if user password match, if not, stop here
                    a_user_2: Any = user_collection.find_one({
                        it_has_alternatives_objects.A_User._key_string_dict.email: email,
                        it_has_alternatives_objects.A_User._key_string_dict.password: item.password
                    })
                    if (a_user_2 == None):
                        default_response.error = "Sorry, you don't have the right password"
                        return default_response
                else:
                    # check if user exists, if not, create a new one
                    if email == configuration.ADMIN_EMAIL:
                        a_new_user = it_has_alternatives_objects.A_User(
                            id=email,
                            create_time_in_10_numbers_timestamp_format=int(datetime.now().timestamp()),
                            email=email,
                            password=item.password,
                            level=0,
                            parent_email=None,
                            children_email_list=[],
                            invitation_counting=0,
                            invitation_code_list=[password_generator.get_random_password(length=12), password_generator.get_random_password(length=12)]
                        )
                        user_collection.insert_one(
                            {
                                **a_new_user.to_dict(),
                            }
                        )
                    else:
                        if item.invitation_code == None:
                            default_response.error = "Sorry, you need invitation code to do the register.\nYou can @yingshaoxo on twitter to get an invitation code if you think you are good enough to be an content leader."
                            return default_response

                        the_parent_user, code = decode_invitation_code(jwt_code=item.invitation_code)
                        if the_parent_user == None or code == None:
                            default_response.error = "Sorry, the one who invite you does not exists or he/she does not have any more invitation chance."
                            return default_response

                        if (the_parent_user.level == None):
                            the_parent_user.level = 0

                        # create a new user
                        a_new_user = it_has_alternatives_objects.A_User(
                            id=email,
                            create_time_in_10_numbers_timestamp_format=time_.get_current_timestamp_in_10_digits_format(),
                            last_login_time_in_10_numbers_timestamp_format=time_.get_current_timestamp_in_10_digits_format(),
                            email=email,
                            password=item.password,
                            level=the_parent_user.level + 1,
                            parent_email=the_parent_user.email,
                            children_email_list=[],
                            invitation_counting=0,
                            invitation_code_list=[password_generator.get_random_password(length=12), password_generator.get_random_password(length=12)]
                        )
                        user_collection.insert_one(
                            {
                                **a_new_user.to_dict(),
                            }
                        )

                        # get new user id and insert it into parent children list
                        if the_parent_user.children_email_list == None:
                            the_parent_user.children_email_list = []
                        if email not in the_parent_user.children_email_list:
                            the_parent_user.children_email_list.append(email)
                        if the_parent_user.invitation_code_list == None:
                            the_parent_user.invitation_code_list = []
                        if the_parent_user.invitation_counting == None:
                            the_parent_user.invitation_counting=0
                        the_parent_user.invitation_code_list = [one for one in the_parent_user.invitation_code_list if one != code]
                        the_parent_user.invitation_counting += 1
                        user_collection.update_one(
                            {
                                it_has_alternatives_objects.A_User._key_string_dict.email: the_parent_user.email,
                            },
                            {
                                "$set": {
                                    it_has_alternatives_objects.A_User._key_string_dict.children_email_list: the_parent_user.children_email_list,
                                    it_has_alternatives_objects.A_User._key_string_dict.invitation_code_list: the_parent_user.invitation_code_list,
                                    it_has_alternatives_objects.A_User._key_string_dict.invitation_counting: the_parent_user.invitation_counting,
                                }
                            }
                        )

                random_string = password_generator.get_random_password(length=10)
                the_jwt_code = jwt_tool.my_jwt_encode(
                    data={
                        it_has_alternatives_objects.A_User._key_string_dict.email: email,
                        "random_string": random_string
                    },
                    a_secret_string_for_integrity_verifying=configuration.SECRET_TEXT,
                    use_md5=True
                )
                the_jwt_code = encryption_and_decryption.encode_message(secret_dict, the_jwt_code)
                user_collection.update_one(
                    {
                        it_has_alternatives_objects.A_User._key_string_dict.email: email,
                    },
                    {
                        "$set": {
                            it_has_alternatives_objects.A_User._key_string_dict.jwt: the_jwt_code,
                            it_has_alternatives_objects.A_User._key_string_dict.last_login_time_in_10_numbers_timestamp_format: time_.get_current_timestamp_in_10_digits_format(),
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

    async def is_jwt_ok(self, headers: dict[str, str], item: it_has_alternatives_objects.is_JWT_ok_Request) -> it_has_alternatives_objects.is_JWT_ok_Response:
        default_response = it_has_alternatives_objects.is_JWT_ok_Response()
        raw_jwt_string = item.jwt

        if raw_jwt_string == None:
            default_response.error = "error, you should give me the jwt string"
            return default_response
        else:
            try:
                user: Any = user_collection.find_one({
                    it_has_alternatives_objects.A_User._key_string_dict.jwt: raw_jwt_string
                })

                if user == None:
                    default_response.error = "error, this jwt is not valid. no user related to it."
                    return default_response

                email = user.get(it_has_alternatives_objects.A_User._key_string_dict.email)
                if (email is None):
                    default_response.error = "error: email do not exists, which shouldn't happen."
                    return default_response
                elif email == configuration.ADMIN_EMAIL:
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

    async def search_alternatives(self, headers: dict[str, str], item: it_has_alternatives_objects.Search_Alternative_Request) -> it_has_alternatives_objects.Search_Alternative_Response:
        default_response = it_has_alternatives_objects.Search_Alternative_Response(error=None, alternative_object_list=[])
        key_words = item.key_words
        if key_words == None:
            key_words = ""

        try:
            result = object_collection.find(
                {
                    it_has_alternatives_objects.An_Object()._key_string_dict.name:
                        {
                            '$regex':f'(.*){re.escape(key_words)}(.*)',
                            "$options": "i"
                        }
                }
            ).sort('_id', -1).skip(item.page_number*item.page_size).limit(item.page_size) # type: ignore

            object_list = []
            for one in result: #type: ignore
                # print(one) #type: ignore
                object_list.append(it_has_alternatives_objects.An_Object().from_dict(one)) #type: ignore
            default_response.alternative_object_list = object_list
        except Exception as e:
            default_response.error = str(e)
        return default_response

    async def get_an_object(self, headers: dict[str, str], item: it_has_alternatives_objects.Get_an_object_Request) -> it_has_alternatives_objects.Get_an_object_Response:
        default_response = it_has_alternatives_objects.Get_an_object_Response()
        try:
            if item.id != None:
                result = object_collection.find(
                    {
                        it_has_alternatives_objects.An_Object()._key_string_dict.id:
                            {
                                '$regex':f'^{item.id}$',
                                "$options": "i"
                            }
                    }
                )
            elif item.name != None:
                result = object_collection.find(
                    {
                        it_has_alternatives_objects.An_Object()._key_string_dict.name: item.name
                    }
                )
            else:
                default_response.error = "You should give id or name"
                return default_response

            object_list = []
            for one in result: #type: ignore
                object_list.append(it_has_alternatives_objects.An_Object().from_dict(one)) #type: ignore

            if (len(object_list) > 0):
                default_response.an_object = object_list[0]

        except Exception as e:
            default_response.error = str(e)
        return default_response

    async def download_backup_data(self, headers: dict[str, str], item: it_has_alternatives_objects.Download_backup_data_request) -> it_has_alternatives_objects.Download_backup_data_response:
        default_response = it_has_alternatives_objects.Download_backup_data_response()

        try:
            temp_saving_folder: str = disk.join_paths(disk.get_the_temp_dir(), "it_has_alternatives_mongodb_backup")
            if not disk.exists(temp_saving_folder):
                disk.create_a_folder(temp_saving_folder)

            mongoDB.backup_mongodb(temp_saving_folder, use_time_as_sub_folder_name=False)

            backup_zip_file = disk.get_a_temp_file_path('backup.zip')
            disk.compress(temp_saving_folder, backup_zip_file)

            the_backup_zip_file_bytes_io = disk.get_bytesio_from_a_file(backup_zip_file)
            base64_string = disk.bytesio_to_base64(bytes_io=the_backup_zip_file_bytes_io)

            default_response.file_name = f"backup_{str(datetime.now())}.zip"
            default_response.file_bytes_in_base64_format = base64_string

            disk.delete_a_file(backup_zip_file)
        except Exception as e:
            print(e)
            default_response.error = str(e)

        return default_response


class User_Service(Visitor_Service):
    async def get_invitation_code(self, headers: dict[str, str], item: it_has_alternatives_objects.Get_invitation_code_request) -> it_has_alternatives_objects.Get_invitation_code_response:
        default_response = it_has_alternatives_objects.Get_invitation_code_response()

        email = headers.get(it_has_alternatives_objects.A_User._key_string_dict.email)
        if email == None:
            default_response.error = "You should put jwt into the header."
            return default_response

        a_user = user_collection.find_one({
            it_has_alternatives_objects.A_User._key_string_dict.email: email,
        })
        if a_user == None:
            default_response.error = "You don't exists, sorry."
            return default_response

        the_dict = mongodb_item_to_dict(a_user)
        a_user = it_has_alternatives_objects.A_User(**the_dict)

        if a_user.invitation_code_list == None:
            a_user.invitation_code_list = []
        if len(a_user.invitation_code_list) <= 0:
            if email == configuration.ADMIN_EMAIL:
                #the admin
                a_user.invitation_code_list=[password_generator.get_random_password(length=12), password_generator.get_random_password(length=12)]
                user_collection.update_one(
                    {
                        it_has_alternatives_objects.A_User._key_string_dict.email: email,
                    },
                    {
                        "$set": {
                            it_has_alternatives_objects.A_User._key_string_dict.invitation_code_list: a_user.invitation_code_list,
                        }
                    }
                )
            else:
                default_response.error = "You don't have any more invitation chance, sorry."
                return default_response

        code = a_user.invitation_code_list[0]
        invitation_code = get_invitation_code(email=email, code=code)
        default_response.invitation_code = invitation_code

        return default_response

    async def add_alternative(self, headers: dict[str, str], item: it_has_alternatives_objects.Add_Object_Request) -> it_has_alternatives_objects.Add_Object_Response:
        default_response = it_has_alternatives_objects.Add_Object_Response()
        try:
            email = headers.get("email")
            if (email == None):
                default_response.error = "You should login before do any operations. (missing josn web token)"
                return default_response

            if (item.an_object == None or item.an_object.name == None or item.an_object.description == None):
                default_response.error = "name and description should have values."
                return default_response

            from_user = get_a_user_by_email(email=email)
            if (from_user == None):
                default_response.error = f"Sorry, user '{email}' does not exists."
                return default_response
            level = from_user.level
            if (level == None):
                default_response.error = f"Sorry, you don't have the level permission to do this. (missing level value in user's object)"
                return default_response
            item.an_object.level = level

            old_object = object_collection.find_one(
                {
                    it_has_alternatives_objects.An_Object()._key_string_dict.name: item.an_object.name,
                }
            )
            if (old_object != None):
                default_response.error = f"Sorry, the object '{item.an_object.name}' you want to add is already in our database."
                return default_response

            item.an_object.create_time_in_10_numbers_timestamp_format = time_.get_current_timestamp_in_10_digits_format()
            item.an_object.update_time_in_10_numbers_timestamp_format = time_.get_current_timestamp_in_10_digits_format()
            result = object_collection.insert_one(
                {
                    **item.an_object.to_dict(), #type: ignore
                    "id": password_generator.get_random_password(length=8) + password_generator.get_password([item.an_object.name+item.an_object.description], length=12)
                },
            )
            the_object_id = str(result.inserted_id)
            print(f"log: inserted a new object: {the_object_id}")
            default_response.success = True
        except Exception as e:
            default_response.error = str(e)
            default_response.success = False
        return default_response

    async def update_alternative(self, headers: dict[str, str], item: it_has_alternatives_objects.Update_Object_Request) -> it_has_alternatives_objects.Update_Object_Response:
        default_response = it_has_alternatives_objects.Update_Object_Response()

        try:
            email = headers.get("email")
            if (email == None):
                default_response.error = "You should login before do any operations. (missing josn web token)"
                return default_response

            if (item.an_object == None or item.an_object.name == None or item.an_object.description == None):
                default_response.error = "name and description should have values."
                return default_response

            from_user = get_a_user_by_email(email=email)
            if (from_user == None):
                default_response.error = f"Sorry, user '{email}' does not exists."
                return default_response
            user_level = from_user.level
            if (user_level == None):
                default_response.error = f"Sorry, you don't have the level permission to do this. (missing level value in user's object)"
                return default_response

            if (item.an_object == None or item.an_object.id == None or item.an_object.name == None):
                default_response.error = "You should give me an id and a name for that object"
                return default_response

            old_object = object_collection.find_one(
                filter={
                    it_has_alternatives_objects.An_Object()._key_string_dict.id: item.an_object.id,
                },
            )
            if (old_object == None):
                default_response.error = "Sorry, the item you want to edit is not exists."
                return default_response
            old_object = it_has_alternatives_objects.An_Object().from_dict(mongodb_item_to_dict(old_object))
            if (old_object.level == None):
                default_response.error = "Sorry, the item you want to edit does not have a level, you may want to create a new one than edit the old one."
                return default_response

            if (old_object.level < user_level):
                default_response.error = f"Sorry, you don't have enough permission to edit this object. It has level of {old_object.level}, your level is {user_level}."
                return default_response

            item.an_object.update_time_in_10_numbers_timestamp_format = time_.get_current_timestamp_in_10_digits_format()
            new_object = item.an_object.to_dict()
            del new_object[it_has_alternatives_objects.An_Object()._key_string_dict.level]
            object_collection.update_one(
                filter={
                    it_has_alternatives_objects.An_Object()._key_string_dict.id: item.an_object.id,
                },
                update={
                    "$set": {
                        **new_object
                    }
                }
            )
        except Exception as e:
            default_response.error = str(e)
            default_response.success = False

        return default_response

    async def delete_alternative(self, headers: dict[str, str], item: it_has_alternatives_objects.Delete_Object_Request) -> it_has_alternatives_objects.Delete_Object_Response:
        default_response = it_has_alternatives_objects.Delete_Object_Response(error=None, success=True)

        try:
            email = headers.get("email")
            if (email == None):
                default_response.error = "You should login before do any operations. (missing josn web token)"
                return default_response

            if (item.an_object == None or item.an_object.name == None or item.an_object.description == None):
                default_response.error = "name and description should have values."
                return default_response

            from_user = get_a_user_by_email(email=email)
            if (from_user == None):
                default_response.error = f"Sorry, user '{email}' does not exists."
                return default_response
            user_level = from_user.level
            if (user_level == None):
                default_response.error = f"Sorry, you don't have the level permission to do this. (missing level value in user's object)"
                return default_response

            if (item.an_object == None or item.an_object.id == None or item.an_object.name == None):
                default_response.error = "You should give me an id and a name for that object"
                return default_response

            old_object = object_collection.find_one(
                filter={
                    it_has_alternatives_objects.An_Object()._key_string_dict.id: item.an_object.id,
                },
            )
            if (old_object == None):
                default_response.error = "Sorry, the item you want to edit is not exists."
                return default_response
            old_object = it_has_alternatives_objects.An_Object().from_dict(mongodb_item_to_dict(old_object))
            if (old_object.level == None):
                default_response.error = "Sorry, the item you want to edit does not have a level, you may want to create a new one than edit the old one."
                return default_response

            if (old_object.level < user_level):
                default_response.error = f"Sorry, you don't have enough permission to edit this object. It has level of {old_object.level}, your level is {user_level}"
                return default_response

            object_collection.delete_one(
                filter={
                    it_has_alternatives_objects.An_Object()._key_string_dict.id: item.an_object.id,
                },
            )
        except Exception as e:
            default_response.error = str(e)
            default_response.success = False

        return default_response


class Admin_Service(User_Service):
    async def download_backup_data(self, headers: dict[str, str], item: it_has_alternatives_objects.Download_backup_data_request) -> it_has_alternatives_objects.Download_backup_data_response:
        default_response = it_has_alternatives_objects.Download_backup_data_response()

        try:
            temp_saving_folder: str = disk.join_paths(disk.get_the_temp_dir(), "it_has_alternatives_mongodb_backup")
            if not disk.exists(temp_saving_folder):
                disk.create_a_folder(temp_saving_folder)

            mongoDB.backup_mongodb(temp_saving_folder, use_time_as_sub_folder_name=False)

            backup_zip_file = disk.get_a_temp_file_path('backup.zip')
            disk.compress(temp_saving_folder, backup_zip_file)

            the_backup_zip_file_bytes_io = disk.get_bytesio_from_a_file(backup_zip_file)
            base64_string = disk.bytesio_to_base64(bytes_io=the_backup_zip_file_bytes_io)

            default_response.file_name = f"backup_it_has_alternatives_{str(datetime.now())}.zip"
            default_response.file_bytes_in_base64_format = base64_string

            disk.delete_a_file(backup_zip_file)
        except Exception as e:
            print(e)
            default_response.error = str(e)

        return default_response

    async def upload_backup_data(self, headers: dict[str, str], item: it_has_alternatives_objects.Upload_backup_data_request) -> it_has_alternatives_objects.Upload_backup_data_response:
        default_response = it_has_alternatives_objects.Upload_backup_data_response()

        try:
            base64_string = item.file_bytes_in_base64_format
            if base64_string == None:
                raise Exception("the 'file_bytes_in_base64_format' shoudn't be None")

            the_backup_zip_file_bytes_io = disk.base64_to_bytesio(base64_string=base64_string)
            backup_zip_file = disk.get_a_temp_file_path('backup.zip')
            disk.save_bytesio_to_file(bytes_io=the_backup_zip_file_bytes_io, file_path=backup_zip_file)

            temp_saving_folder: str = disk.join_paths(disk.get_the_temp_dir(), "it_has_alternatives_mongodb_backup")
            if disk.exists(temp_saving_folder):
                disk.delete_a_folder(temp_saving_folder)
            disk.uncompress(backup_zip_file, temp_saving_folder)

            mongoDB.recover_mongodb(backup_folder_path=temp_saving_folder, use_time_as_sub_folder_name=False)

            default_response.success = True
        except Exception as e:
            print(e)
            default_response.error = str(e)

        return default_response


def run_main_service(port: str):
    from fastapi import FastAPI
    from fastapi import Request, Response, status
    from starlette.responses import FileResponse
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.staticfiles import StaticFiles
    from starlette.datastructures import MutableHeaders
    import uvicorn

    app = FastAPI()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        #print('running in a PyInstaller bundle')
        def resource_path(relative_path: str) -> str:
            if hasattr(sys, '_MEIPASS'):
                return os.path.join(sys._MEIPASS, relative_path) #type: ignore
            return os.path.join(os.path.abspath("."), relative_path)
        vue_html_file_folder = resource_path("./vue")
    else:
        #print('running in a normal Python process')
        vue_html_file_folder = disk.join_paths(disk.get_directory_path(__file__), "./vue")

    visitor_service = it_has_alternatives_rpc.run(Visitor_Service(), "666", only_return_app=True, html_folder_path=vue_html_file_folder)
    user_service = it_has_alternatives_rpc.run(User_Service(), "666", only_return_app=True)
    admin_service = it_has_alternatives_rpc.run(Admin_Service(), "666", only_return_app=True)

    @user_service.middleware("http")
    async def user_auth_middleware(request: Request, call_next):
        raw_jwt_string = request.headers.get("jwt", None)
        if raw_jwt_string == None:
            return Response(
                content="error",
                status_code=status.HTTP_401_UNAUTHORIZED,
                headers={"Content-Type": "text/plain"},
            )
        else:
            user: Any = user_collection.find_one({
                "jwt": raw_jwt_string
            })
            if user == None:
                return Response(
                    content="error",
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    headers={"Content-Type": "text/plain"},
                )

            email = user.get("email")
            if (email is None):
                return Response(
                    content="error: email do not exists, which shouldn't happen",
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    headers={"Content-Type": "text/plain"},
                )
            else:
                update_last_login_time_for_a_user(user_email=email)

                #request.headers["email"] = email
                new_header = MutableHeaders(request._headers)
                new_header["email"] = email
                request._headers = new_header
                request.scope.update(headers=request.headers.raw)

                response = await call_next(request)

                return response

        return Response(
            content="unknow error",
            status_code=status.HTTP_401_UNAUTHORIZED,
            headers={"Content-Type": "text/plain"},
        )

    @admin_service.middleware("http")
    async def admin_auth_middleware(request: Request, call_next):
        raw_jwt_string = request.headers.get("jwt", None)
        if raw_jwt_string == None:
            return Response(
                content="error",
                status_code=status.HTTP_401_UNAUTHORIZED,
                headers={"Content-Type": "text/plain"},
            )
        else:
            user: Any = user_collection.find_one({
                "jwt": raw_jwt_string
            })

            if user == None:
                return Response(
                    content="error",
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    headers={"Content-Type": "text/plain"},
                )

            email = user.get("email")
            if (email is None):
                return Response(
                    content="error: email do not exists, which shouldn't happen",
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    headers={"Content-Type": "text/plain"},
                )
            elif email == configuration.ADMIN_EMAIL:
                update_last_login_time_for_a_user(user_email=email)
                #request.headers["email"] = email

                new_header = MutableHeaders(request._headers)
                new_header["email"] = email
                request._headers = new_header
                request.scope.update(headers=request.headers.raw)

                response = await call_next(request)
                return response
            else:
                return Response(
                    content="sorry, you are not admin",
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    headers={"Content-Type": "text/plain"},
                )

        return Response(
            content="error",
            status_code=status.HTTP_401_UNAUTHORIZED,
            headers={"Content-Type": "text/plain"},
        )

    app.mount("/_admin", admin_service)
    app.mount("/_user", user_service)
    app.mount("/", visitor_service)

    uvicorn.run(app=app, # type: ignore #"src.main:app", 
                host="0.0.0.0",
                port=int(port))


def start():
    process_list = [
        multiprocessing.Process(target=run_main_service, args=("5551",)),
    ]

    for process in process_list:
        process.start()

    print("\n\nWhat is the yingshaoxo@gmail.com password? What you type at the first login is what the password is.\n\n")

    while all([
        one.is_alive()
        for one in process_list
    ]):
        sleep(10)

    # # Wait processes to complete
    # for process in process_list:
    #     process.join()


def main():
    start()


if __name__ == '__main__':
    start()
