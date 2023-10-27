from .it_has_alternatives_objects import *


from typing import Any
import json
from auto_everything.http_ import Yingshaoxo_Http_Server, Yingshaoxo_Http_Request


class Service_it_has_alternatives:
    def get_special_jwt(self, headers: dict[str, str], item: Get_Special_JWT_Request) -> Get_Special_JWT_Response:
        default_response = Get_Special_JWT_Response()

        try:
            pass
        except Exception as e:
            print(f"Error: {e}")
            #default_response.error = str(e)
            #default_response.success = False

        return default_response

    def is_jwt_ok(self, headers: dict[str, str], item: is_JWT_ok_Request) -> is_JWT_ok_Response:
        default_response = is_JWT_ok_Response()

        try:
            pass
        except Exception as e:
            print(f"Error: {e}")
            #default_response.error = str(e)
            #default_response.success = False

        return default_response

    def get_invitation_code(self, headers: dict[str, str], item: Get_invitation_code_request) -> Get_invitation_code_response:
        default_response = Get_invitation_code_response()

        try:
            pass
        except Exception as e:
            print(f"Error: {e}")
            #default_response.error = str(e)
            #default_response.success = False

        return default_response

    def search_alternatives(self, headers: dict[str, str], item: Search_Alternative_Request) -> Search_Alternative_Response:
        default_response = Search_Alternative_Response()

        try:
            pass
        except Exception as e:
            print(f"Error: {e}")
            #default_response.error = str(e)
            #default_response.success = False

        return default_response

    def get_an_object(self, headers: dict[str, str], item: Get_an_object_Request) -> Get_an_object_Response:
        default_response = Get_an_object_Response()

        try:
            pass
        except Exception as e:
            print(f"Error: {e}")
            #default_response.error = str(e)
            #default_response.success = False

        return default_response

    def add_alternative(self, headers: dict[str, str], item: Add_Object_Request) -> Add_Object_Response:
        default_response = Add_Object_Response()

        try:
            pass
        except Exception as e:
            print(f"Error: {e}")
            #default_response.error = str(e)
            #default_response.success = False

        return default_response

    def update_alternative(self, headers: dict[str, str], item: Update_Object_Request) -> Update_Object_Response:
        default_response = Update_Object_Response()

        try:
            pass
        except Exception as e:
            print(f"Error: {e}")
            #default_response.error = str(e)
            #default_response.success = False

        return default_response

    def delete_alternative(self, headers: dict[str, str], item: Delete_Object_Request) -> Delete_Object_Response:
        default_response = Delete_Object_Response()

        try:
            pass
        except Exception as e:
            print(f"Error: {e}")
            #default_response.error = str(e)
            #default_response.success = False

        return default_response

    def download_backup_data(self, headers: dict[str, str], item: Download_backup_data_request) -> Download_backup_data_response:
        default_response = Download_backup_data_response()

        try:
            pass
        except Exception as e:
            print(f"Error: {e}")
            #default_response.error = str(e)
            #default_response.success = False

        return default_response

    def upload_backup_data(self, headers: dict[str, str], item: Upload_backup_data_request) -> Upload_backup_data_response:
        default_response = Upload_backup_data_response()

        try:
            pass
        except Exception as e:
            print(f"Error: {e}")
            #default_response.error = str(e)
            #default_response.success = False

        return default_response


def run(service_instance: Service_it_has_alternatives, port: str, html_folder_path: str="", serve_html_under_which_url: str="/"):
    def handle_get_url(sub_url: str, headers: dict[str, str]) -> str:
        return 'Hi there, this website is using yrpc (Yingshaoxo remote procedure control module).'

    def handle_post_url(sub_url: str, headers: dict[str, str], item: dict[str, Any]) -> dict | str:
        sub_url = sub_url.strip("/")
        sub_url = sub_url.replace("it_has_alternatives", "", 1)
        sub_url = sub_url.strip("/")
        request_url = sub_url.split("/")[0].strip()

        if (request_url == ""):
            return f"Request url '{request_url}' is empty"
        elif (request_url == "get_special_jwt"):
            correct_item = Get_Special_JWT_Request().from_dict(item)
            return json.dumps((service_instance.get_special_jwt(headers, correct_item)).to_dict())

        elif (request_url == "is_jwt_ok"):
            correct_item = is_JWT_ok_Request().from_dict(item)
            return json.dumps((service_instance.is_jwt_ok(headers, correct_item)).to_dict())

        elif (request_url == "get_invitation_code"):
            correct_item = Get_invitation_code_request().from_dict(item)
            return json.dumps((service_instance.get_invitation_code(headers, correct_item)).to_dict())

        elif (request_url == "search_alternatives"):
            correct_item = Search_Alternative_Request().from_dict(item)
            return json.dumps((service_instance.search_alternatives(headers, correct_item)).to_dict())

        elif (request_url == "get_an_object"):
            correct_item = Get_an_object_Request().from_dict(item)
            return json.dumps((service_instance.get_an_object(headers, correct_item)).to_dict())

        elif (request_url == "add_alternative"):
            correct_item = Add_Object_Request().from_dict(item)
            return json.dumps((service_instance.add_alternative(headers, correct_item)).to_dict())

        elif (request_url == "update_alternative"):
            correct_item = Update_Object_Request().from_dict(item)
            return json.dumps((service_instance.update_alternative(headers, correct_item)).to_dict())

        elif (request_url == "delete_alternative"):
            correct_item = Delete_Object_Request().from_dict(item)
            return json.dumps((service_instance.delete_alternative(headers, correct_item)).to_dict())

        elif (request_url == "download_backup_data"):
            correct_item = Download_backup_data_request().from_dict(item)
            return json.dumps((service_instance.download_backup_data(headers, correct_item)).to_dict())

        elif (request_url == "upload_backup_data"):
            correct_item = Upload_backup_data_request().from_dict(item)
            return json.dumps((service_instance.upload_backup_data(headers, correct_item)).to_dict())

        return f"No API url matchs '{request_url}'"

    def general_handler(request: Yingshaoxo_Http_Request) -> dict | str:
        response = f"No handler for {request.url}"
        if request.method == "GET":
            response = handle_get_url(request.url, request.headers)
        elif request.method == "POST":
            response = handle_post_url(request.url, request.headers, json.loads(request.payload))
        return response

    router = {
        r"(.*)": general_handler,
    }

    yingshaoxo_http_server = Yingshaoxo_Http_Server(router=router)
    yingshaoxo_http_server.start(host="0.0.0.0", port=int(port), html_folder_path=html_folder_path, serve_html_under_which_url=serve_html_under_which_url)


if __name__ == "__main__":
    service_instance = Service_it_has_alternatives()
    run(service_instance, port="6060")