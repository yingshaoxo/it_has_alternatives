from .it_has_alternatives_objects import *


from fastapi import APIRouter, FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse 
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os


router = APIRouter()


class Service_it_has_alternatives:
    async def get_special_jwt(self, item: Get_Special_JWT_Request) -> Get_Special_JWT_Response:
        return Get_Special_JWT_Response()

    async def is_jwt_ok(self, item: is_JWT_ok_Request) -> is_JWT_ok_Response:
        return is_JWT_ok_Response()

    async def search_alternatives(self, item: Search_Alternative_Request) -> Search_Alternative_Response:
        return Search_Alternative_Response()

    async def get_an_object(self, item: Get_an_object_Request) -> Get_an_object_Response:
        return Get_an_object_Response()

    async def add_alternative(self, item: Add_Object_Request) -> Add_Object_Response:
        return Add_Object_Response()

    async def update_alternative(self, item: Update_Object_Request) -> Update_Object_Response:
        return Update_Object_Response()

    async def delete_alternative(self, item: Delete_Object_Request) -> Delete_Object_Response:
        return Delete_Object_Response()


def init(service_instance: Any):
    @router.post("/get_special_jwt/", tags=["it_has_alternatives"])
    async def get_special_jwt(item: Get_Special_JWT_Request) -> Get_Special_JWT_Response:
        item = Get_Special_JWT_Request().from_dict(item.to_dict())
        return (await service_instance.get_special_jwt(item)).to_dict()

    @router.post("/is_jwt_ok/", tags=["it_has_alternatives"])
    async def is_jwt_ok(item: is_JWT_ok_Request) -> is_JWT_ok_Response:
        item = is_JWT_ok_Request().from_dict(item.to_dict())
        return (await service_instance.is_jwt_ok(item)).to_dict()

    @router.post("/search_alternatives/", tags=["it_has_alternatives"])
    async def search_alternatives(item: Search_Alternative_Request) -> Search_Alternative_Response:
        item = Search_Alternative_Request().from_dict(item.to_dict())
        return (await service_instance.search_alternatives(item)).to_dict()

    @router.post("/get_an_object/", tags=["it_has_alternatives"])
    async def get_an_object(item: Get_an_object_Request) -> Get_an_object_Response:
        item = Get_an_object_Request().from_dict(item.to_dict())
        return (await service_instance.get_an_object(item)).to_dict()

    @router.post("/add_alternative/", tags=["it_has_alternatives"])
    async def add_alternative(item: Add_Object_Request) -> Add_Object_Response:
        item = Add_Object_Request().from_dict(item.to_dict())
        return (await service_instance.add_alternative(item)).to_dict()

    @router.post("/update_alternative/", tags=["it_has_alternatives"])
    async def update_alternative(item: Update_Object_Request) -> Update_Object_Response:
        item = Update_Object_Request().from_dict(item.to_dict())
        return (await service_instance.update_alternative(item)).to_dict()

    @router.post("/delete_alternative/", tags=["it_has_alternatives"])
    async def delete_alternative(item: Delete_Object_Request) -> Delete_Object_Response:
        item = Delete_Object_Request().from_dict(item.to_dict())
        return (await service_instance.delete_alternative(item)).to_dict()


def run(service_instance: Any, port: str, html_folder_path: str="", serve_html_under_which_url: str="/"):
    init(service_instance=service_instance)

    app = FastAPI()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(
        router,
        prefix="/it_has_alternatives",
    )

    if (html_folder_path != ""):
        if os.path.exists(html_folder_path) and os.path.isdir(html_folder_path):
            app.mount(serve_html_under_which_url, StaticFiles(directory=html_folder_path, html = True), name="web")
            @app.get(serve_html_under_which_url, response_model=str)
            async def index_page():
                return FileResponse(os.path.join(html_folder_path, 'index.html'))
            @app.exception_handler(404) #type: ignore
            async def custom_404_handler(_, __): #type: ignore
                return FileResponse(os.path.join(html_folder_path, 'index.html'))
            print(f"The website is running at: http://127.0.0.1:{port}/")
        else:
            print(f"Error: You should give me an absolute html_folder_path than {html_folder_path}")

    print(f"You can see the docs here: http://127.0.0.1:{{port}}/docs")
    uvicorn.run( #type: ignore
        app=app,
        host="0.0.0.0",
        port=int(port)
    ) 


if __name__ == "__main__":
    service_instance = Service_it_has_alternatives()
    run(service_instance, port="6060")