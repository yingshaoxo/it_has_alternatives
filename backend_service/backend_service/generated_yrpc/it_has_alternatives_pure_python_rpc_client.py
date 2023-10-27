from .it_has_alternatives_objects import *

from typing import Any, Callable
import json
from urllib import request


def _send_a_post(url: str, data: dict, headers: dict | None=None) -> str:
    a_request = request.Request(url, method="POST")
    a_request.add_header('Content-Type', 'application/json')
    if headers != None:
        for key, value in headers.items():
            a_request.add_header(key, value)
    data = json.dumps(data, indent=4)
    data = data.encode("utf-8", errors="ignore")
    r_ = request.urlopen(a_request, data=data)
    content = r_.read().decode("utf-8", errors="ignore")
    return content


class Client_it_has_alternatives:
    def __init__(self, service_url: str, headers: dict[str, Any] | None = None, error_handle_function: Callable[[str], None] | None = None, special_error_key: str = "__yingshaoxo's_error__", interceptor_function: Callable[[dict], None] | None = None):
        if (service_url.endswith("/")):
            service_url = service_url[:-1]
        self._service_url = service_url 

        if headers == None:
            headers = {}
        self._header = headers

        def _default_error_handle_function(error_message: str):
            print(f"errors: {error_message}")
        if error_handle_function == None:
            error_handle_function = _default_error_handle_function
        self._error_handle_function = error_handle_function

        self._special_error_key = special_error_key

        def _default_interceptor_function(data: dict):
            pass
        if interceptor_function == None:
            interceptor_function = _default_interceptor_function
        self._interceptor_function = interceptor_function

    def _get_reponse_or_error_by_url_path_and_input(self, sub_url: str, input_dict: dict[str, Any]):
        the_url = f"{self._service_url}/it_has_alternatives/{sub_url}/"
        try:
            response = _send_a_post(url=the_url, data=input_dict, headers=self._header)
            json_response = json.loads(response)
            self._interceptor_function(json_response)
            return json_response
        except Exception as e: 
            return {self._special_error_key: str(e)}

    def get_special_jwt(self, item: Get_Special_JWT_Request, ignore_error: bool | None=None) -> Get_Special_JWT_Response | None:
        result = self._get_reponse_or_error_by_url_path_and_input("get_special_jwt", item.to_dict())
        if self._special_error_key in result.keys():
            if ((ignore_error == None) or ((ignore_error != None) and (not ignore_error))):
                self._error_handle_function(result[self._special_error_key])
            return None
        else:
            return Get_Special_JWT_Response().from_dict(result)

    def is_jwt_ok(self, item: is_JWT_ok_Request, ignore_error: bool | None=None) -> is_JWT_ok_Response | None:
        result = self._get_reponse_or_error_by_url_path_and_input("is_jwt_ok", item.to_dict())
        if self._special_error_key in result.keys():
            if ((ignore_error == None) or ((ignore_error != None) and (not ignore_error))):
                self._error_handle_function(result[self._special_error_key])
            return None
        else:
            return is_JWT_ok_Response().from_dict(result)

    def get_invitation_code(self, item: Get_invitation_code_request, ignore_error: bool | None=None) -> Get_invitation_code_response | None:
        result = self._get_reponse_or_error_by_url_path_and_input("get_invitation_code", item.to_dict())
        if self._special_error_key in result.keys():
            if ((ignore_error == None) or ((ignore_error != None) and (not ignore_error))):
                self._error_handle_function(result[self._special_error_key])
            return None
        else:
            return Get_invitation_code_response().from_dict(result)

    def search_alternatives(self, item: Search_Alternative_Request, ignore_error: bool | None=None) -> Search_Alternative_Response | None:
        result = self._get_reponse_or_error_by_url_path_and_input("search_alternatives", item.to_dict())
        if self._special_error_key in result.keys():
            if ((ignore_error == None) or ((ignore_error != None) and (not ignore_error))):
                self._error_handle_function(result[self._special_error_key])
            return None
        else:
            return Search_Alternative_Response().from_dict(result)

    def get_an_object(self, item: Get_an_object_Request, ignore_error: bool | None=None) -> Get_an_object_Response | None:
        result = self._get_reponse_or_error_by_url_path_and_input("get_an_object", item.to_dict())
        if self._special_error_key in result.keys():
            if ((ignore_error == None) or ((ignore_error != None) and (not ignore_error))):
                self._error_handle_function(result[self._special_error_key])
            return None
        else:
            return Get_an_object_Response().from_dict(result)

    def add_alternative(self, item: Add_Object_Request, ignore_error: bool | None=None) -> Add_Object_Response | None:
        result = self._get_reponse_or_error_by_url_path_and_input("add_alternative", item.to_dict())
        if self._special_error_key in result.keys():
            if ((ignore_error == None) or ((ignore_error != None) and (not ignore_error))):
                self._error_handle_function(result[self._special_error_key])
            return None
        else:
            return Add_Object_Response().from_dict(result)

    def update_alternative(self, item: Update_Object_Request, ignore_error: bool | None=None) -> Update_Object_Response | None:
        result = self._get_reponse_or_error_by_url_path_and_input("update_alternative", item.to_dict())
        if self._special_error_key in result.keys():
            if ((ignore_error == None) or ((ignore_error != None) and (not ignore_error))):
                self._error_handle_function(result[self._special_error_key])
            return None
        else:
            return Update_Object_Response().from_dict(result)

    def delete_alternative(self, item: Delete_Object_Request, ignore_error: bool | None=None) -> Delete_Object_Response | None:
        result = self._get_reponse_or_error_by_url_path_and_input("delete_alternative", item.to_dict())
        if self._special_error_key in result.keys():
            if ((ignore_error == None) or ((ignore_error != None) and (not ignore_error))):
                self._error_handle_function(result[self._special_error_key])
            return None
        else:
            return Delete_Object_Response().from_dict(result)

    def download_backup_data(self, item: Download_backup_data_request, ignore_error: bool | None=None) -> Download_backup_data_response | None:
        result = self._get_reponse_or_error_by_url_path_and_input("download_backup_data", item.to_dict())
        if self._special_error_key in result.keys():
            if ((ignore_error == None) or ((ignore_error != None) and (not ignore_error))):
                self._error_handle_function(result[self._special_error_key])
            return None
        else:
            return Download_backup_data_response().from_dict(result)

    def upload_backup_data(self, item: Upload_backup_data_request, ignore_error: bool | None=None) -> Upload_backup_data_response | None:
        result = self._get_reponse_or_error_by_url_path_and_input("upload_backup_data", item.to_dict())
        if self._special_error_key in result.keys():
            if ((ignore_error == None) or ((ignore_error != None) and (not ignore_error))):
                self._error_handle_function(result[self._special_error_key])
            return None
        else:
            return Upload_backup_data_response().from_dict(result)