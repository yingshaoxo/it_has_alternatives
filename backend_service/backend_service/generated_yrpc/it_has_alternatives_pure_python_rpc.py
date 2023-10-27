from .it_has_alternatives_objects import *


from typing import Any
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
import json
import os
from time import sleep


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


def _get_headers_dict_from_string(headers: str) -> dict:
    dic = {}
    for line in headers.split("\n"):
        if line.startswith(("GET", "POST")):
            continue
        point_index = line.find(":")
        dic[line[:point_index].strip()] = line[point_index+1:].strip()
    return dic


def run(service_instance: Service_it_has_alternatives, port: str, html_folder_path: str="", serve_html_under_which_url: str="/"):
    # allow_origins=['*'],
    # allow_credentials=True,
    # allow_methods=["*"],
    # allow_headers=["*"],

    def handle_get_url(sub_url: str, headers: dict[str, str]) -> bytes:
        return b'Hi there, this website is using yrpc (Yingshaoxo remote procedure control module).'

    if (html_folder_path != ""):
        if os.path.exists(html_folder_path) and os.path.isdir(html_folder_path):
            def handle_get_url(sub_url: str, headers: dict[str, str]) -> bytes:
                sub_url = sub_url.strip("/")
                sub_url = sub_url.lstrip(serve_html_under_which_url)
                if sub_url == '':
                    sub_url = 'index.html'
                real_file_path = f"{os.path.join(html_folder_path, sub_url)}"
                if os.path.exists(real_file_path) and os.path.isfile(real_file_path):
                    with open(real_file_path, mode="rb") as f:
                        the_data = f.read()
                else:
                    #return b"Resource not found\n\n(This web service is using YRPC (Yingshaoxo Remote Procedure Call))"
                    sub_url = 'index.html'
                    real_file_path = f"{os.path.join(html_folder_path, sub_url)}"
                    with open(real_file_path, mode="rb") as f:
                        the_data = f.read()
                return the_data

            print(f"The website is running at: http://127.0.0.1:{port}/")
        else:
            print(f"Error: You should give me an absolute html_folder_path than {html_folder_path}")

    def handle_post_url(sub_url: str, headers: dict[str, str], item: dict[str, Any]) -> str:
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

    class WebRequestHandler(BaseHTTPRequestHandler):
        def do_OPTIONS(self):
            self.send_response(200, "ok")
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', '*')
            self.send_header("Access-Control-Allow-Headers", "*")
            self.end_headers()

        def do_GET(self):
            sub_url = self.path
            headers = _get_headers_dict_from_string(self.headers.as_string())

            self.send_response(200)

            self.send_header("Access-Control-Allow-Origin", "*")

            if sub_url.endswith(".html"):
                self.send_header("Content-Type", "text/html")
            elif sub_url.endswith(".css"):
                self.send_header("Content-Type", "text/css")
            elif sub_url.endswith(".js"):
                self.send_header("Content-Type", "text/javascript")

            response = handle_get_url(sub_url, headers)

            self.end_headers()
            self.wfile.write(response)

        def do_POST(self):
            sub_url = self.path
            headers = _get_headers_dict_from_string(self.headers.as_string())

            content_length = headers.get('Content-Length')
            if content_length is None:
                self.wfile.write("What you send is not json".encode("utf-8"))
                return
            else:
                content_length = int(content_length)
            
            if content_length == 0:
                self.wfile.write("What you send is not json".encode("utf-8"))
                return

            request_json_dict = json.loads(self.rfile.read(content_length))

            self.send_response(200)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Content-Type", "application/json")
            self.end_headers()

            response = handle_post_url(sub_url, headers, request_json_dict)

            self.wfile.write(response.encode("utf-8"))

    class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
        pass
    
    # Setting TCP Address
    server_address = ('0.0.0.0', int(port))
    
    # invoking server
    http = ThreadedHTTPServer(server_address, WebRequestHandler)
    
    http.serve_forever()


def run_with_hot_load(watch_path: str, service_instance: Service_it_has_alternatives, port: str, html_folder_path: str="", serve_html_under_which_url: str="/"):
    import multiprocessing
    from auto_everything.develop import Develop
    develop = Develop()

    the_running_process = multiprocessing.Process(target=run, args=(service_instance, port, html_folder_path, serve_html_under_which_url))
    the_running_process.start()

    while True:
        changed = develop.whether_a_folder_has_changed(folder_path=watch_path, type_limiter=[".py", ".html", ".css", ".js"])
        if (changed):
            print("Source code get changed, doing a reloading now...")
            the_running_process.kill()
            while the_running_process.is_alive():
                sleep(1)
            the_running_process = multiprocessing.Process(target=run, args=(service_instance, port, html_folder_path, serve_html_under_which_url))
            the_running_process.start()
        sleep(1)


if __name__ == "__main__":
    service_instance = Service_it_has_alternatives()
    run(service_instance, port="6060")