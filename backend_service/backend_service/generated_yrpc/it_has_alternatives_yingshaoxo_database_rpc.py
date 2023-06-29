from .it_has_alternatives_objects import *
from auto_everything.database import Database_Of_Yingshaoxo


def _search_function(self: Any, item_filter: Any, page_number:int|None=None, page_size:int|None=None, start_from:int=0, reverse:bool=False):
    search_temp_dict = {}
    search_temp_dict["_raw_search_counting"] = 0
    search_temp_dict["_search_counting"] = 0
    if (page_number!=None and page_size != None and start_from != None):
        search_temp_dict["_real_start"] = page_number * page_size
        search_temp_dict["_real_end"] = search_temp_dict["_real_start"] + page_size

    item_dict = item_filter.to_dict()

    def one_row_dict_filter(a_dict_: dict[str, Any]):
        search_temp_dict["_raw_search_counting"] += 1

        if (page_number!=None and page_size != None and start_from != None):
            if search_temp_dict["_raw_search_counting"] < start_from:
                return None

        result = True
        for key, value in item_dict.items():
            if value == None:
                # ignore None value because it is not defined
                continue
            if key not in a_dict_.keys():
                result = False
                break
            else:
                value2 = a_dict_.get(key)
                if value == value2:
                    continue
                else:
                    result = False
                    break

        final_result = None
        if result == True:
            search_temp_dict["_search_counting"] += 1
            final_result = a_dict_
        else:
            final_result = None

        if (page_number!=None and page_size != None and start_from != None):
            if search_temp_dict["_search_counting"] <= search_temp_dict["_real_start"]:
                return None
            if search_temp_dict["_search_counting"] > search_temp_dict["_real_end"]:
                return None
        
        return final_result

    return self.database_of_yingshaoxo.search(one_row_dict_handler=one_row_dict_filter)


def _delete(self, item_filter: Any):
    item_dict = item_filter.to_dict()
    def one_row_dict_filter(a_dict_: dict[str, Any]):
        result = True
        for key, value in item_dict.items():
            if value == None:
                # ignore None value because it is not defined
                continue
            if key not in a_dict_.keys():
                result = False
                break
            else:
                value2 = a_dict_.get(key)
                if value == value2:
                    continue
                else:
                    result = False
                    break
        return result
    self.database_of_yingshaoxo.delete(one_row_dict_filter=one_row_dict_filter)


def _update(self, old_item_filter: Any, new_item: Any):
    item_dict = old_item_filter.to_dict()
    def one_row_dict_handler(a_dict_: dict[str, Any]):
        result = True
        for key, value in item_dict.items():
            if value == None:
                # ignore None value because it is not defined
                continue
            if key not in a_dict_.keys():
                result = False
                break
            else:
                value2 = a_dict_.get(key)
                if value == value2:
                    continue
                else:
                    result = False
                    break
        if result == True:
            new_object = {
                key:value for key, value
                in new_item.to_dict().items()
                if value != None
            }
            a_dict_.update(new_object)
            return a_dict_
        else:
            return None
    self.database_of_yingshaoxo.update(one_row_dict_handler=one_row_dict_handler)


class Yingshaoxo_Database_Get_Special_JWT_Response:
    def __init__(self, database_base_folder: str) -> None:
        self.database_of_yingshaoxo = Database_Of_Yingshaoxo(database_name="Get_Special_JWT_Response", database_base_folder=database_base_folder)

    def add(self, item: Get_Special_JWT_Response):
        self.database_of_yingshaoxo.add(data=item.to_dict())

    def search(self, item_filter: Get_Special_JWT_Response, page_number:int|None=None, page_size:int|None=None, start_from:int=0, reverse:bool=False):
        return _search_function(self=self, item_filter=item_filter, page_number=page_number, page_size=page_size, start_from=start_from, reverse=reverse)

    def delete(self, item_filter: Get_Special_JWT_Response):
        return _delete(self=self, item_filter=item_filter)
    
    def update(self, old_item_filter: Get_Special_JWT_Response, new_item: Get_Special_JWT_Response):
        return _update(self=self, old_item_filter=old_item_filter, new_item=new_item)


class Yingshaoxo_Database_Get_Special_JWT_Request:
    def __init__(self, database_base_folder: str) -> None:
        self.database_of_yingshaoxo = Database_Of_Yingshaoxo(database_name="Get_Special_JWT_Request", database_base_folder=database_base_folder)

    def add(self, item: Get_Special_JWT_Request):
        self.database_of_yingshaoxo.add(data=item.to_dict())

    def search(self, item_filter: Get_Special_JWT_Request, page_number:int|None=None, page_size:int|None=None, start_from:int=0, reverse:bool=False):
        return _search_function(self=self, item_filter=item_filter, page_number=page_number, page_size=page_size, start_from=start_from, reverse=reverse)

    def delete(self, item_filter: Get_Special_JWT_Request):
        return _delete(self=self, item_filter=item_filter)
    
    def update(self, old_item_filter: Get_Special_JWT_Request, new_item: Get_Special_JWT_Request):
        return _update(self=self, old_item_filter=old_item_filter, new_item=new_item)


class Yingshaoxo_Database_is_JWT_ok_Response:
    def __init__(self, database_base_folder: str) -> None:
        self.database_of_yingshaoxo = Database_Of_Yingshaoxo(database_name="is_JWT_ok_Response", database_base_folder=database_base_folder)

    def add(self, item: is_JWT_ok_Response):
        self.database_of_yingshaoxo.add(data=item.to_dict())

    def search(self, item_filter: is_JWT_ok_Response, page_number:int|None=None, page_size:int|None=None, start_from:int=0, reverse:bool=False):
        return _search_function(self=self, item_filter=item_filter, page_number=page_number, page_size=page_size, start_from=start_from, reverse=reverse)

    def delete(self, item_filter: is_JWT_ok_Response):
        return _delete(self=self, item_filter=item_filter)
    
    def update(self, old_item_filter: is_JWT_ok_Response, new_item: is_JWT_ok_Response):
        return _update(self=self, old_item_filter=old_item_filter, new_item=new_item)


class Yingshaoxo_Database_is_JWT_ok_Request:
    def __init__(self, database_base_folder: str) -> None:
        self.database_of_yingshaoxo = Database_Of_Yingshaoxo(database_name="is_JWT_ok_Request", database_base_folder=database_base_folder)

    def add(self, item: is_JWT_ok_Request):
        self.database_of_yingshaoxo.add(data=item.to_dict())

    def search(self, item_filter: is_JWT_ok_Request, page_number:int|None=None, page_size:int|None=None, start_from:int=0, reverse:bool=False):
        return _search_function(self=self, item_filter=item_filter, page_number=page_number, page_size=page_size, start_from=start_from, reverse=reverse)

    def delete(self, item_filter: is_JWT_ok_Request):
        return _delete(self=self, item_filter=item_filter)
    
    def update(self, old_item_filter: is_JWT_ok_Request, new_item: is_JWT_ok_Request):
        return _update(self=self, old_item_filter=old_item_filter, new_item=new_item)


class Yingshaoxo_Database_Get_invitation_code_request:
    def __init__(self, database_base_folder: str) -> None:
        self.database_of_yingshaoxo = Database_Of_Yingshaoxo(database_name="Get_invitation_code_request", database_base_folder=database_base_folder)

    def add(self, item: Get_invitation_code_request):
        self.database_of_yingshaoxo.add(data=item.to_dict())

    def search(self, item_filter: Get_invitation_code_request, page_number:int|None=None, page_size:int|None=None, start_from:int=0, reverse:bool=False):
        return _search_function(self=self, item_filter=item_filter, page_number=page_number, page_size=page_size, start_from=start_from, reverse=reverse)

    def delete(self, item_filter: Get_invitation_code_request):
        return _delete(self=self, item_filter=item_filter)
    
    def update(self, old_item_filter: Get_invitation_code_request, new_item: Get_invitation_code_request):
        return _update(self=self, old_item_filter=old_item_filter, new_item=new_item)


class Yingshaoxo_Database_Get_invitation_code_response:
    def __init__(self, database_base_folder: str) -> None:
        self.database_of_yingshaoxo = Database_Of_Yingshaoxo(database_name="Get_invitation_code_response", database_base_folder=database_base_folder)

    def add(self, item: Get_invitation_code_response):
        self.database_of_yingshaoxo.add(data=item.to_dict())

    def search(self, item_filter: Get_invitation_code_response, page_number:int|None=None, page_size:int|None=None, start_from:int=0, reverse:bool=False):
        return _search_function(self=self, item_filter=item_filter, page_number=page_number, page_size=page_size, start_from=start_from, reverse=reverse)

    def delete(self, item_filter: Get_invitation_code_response):
        return _delete(self=self, item_filter=item_filter)
    
    def update(self, old_item_filter: Get_invitation_code_response, new_item: Get_invitation_code_response):
        return _update(self=self, old_item_filter=old_item_filter, new_item=new_item)


class Yingshaoxo_Database_Search_Alternative_Response:
    def __init__(self, database_base_folder: str) -> None:
        self.database_of_yingshaoxo = Database_Of_Yingshaoxo(database_name="Search_Alternative_Response", database_base_folder=database_base_folder)

    def add(self, item: Search_Alternative_Response):
        self.database_of_yingshaoxo.add(data=item.to_dict())

    def search(self, item_filter: Search_Alternative_Response, page_number:int|None=None, page_size:int|None=None, start_from:int=0, reverse:bool=False):
        return _search_function(self=self, item_filter=item_filter, page_number=page_number, page_size=page_size, start_from=start_from, reverse=reverse)

    def delete(self, item_filter: Search_Alternative_Response):
        return _delete(self=self, item_filter=item_filter)
    
    def update(self, old_item_filter: Search_Alternative_Response, new_item: Search_Alternative_Response):
        return _update(self=self, old_item_filter=old_item_filter, new_item=new_item)


class Yingshaoxo_Database_Search_Alternative_Request:
    def __init__(self, database_base_folder: str) -> None:
        self.database_of_yingshaoxo = Database_Of_Yingshaoxo(database_name="Search_Alternative_Request", database_base_folder=database_base_folder)

    def add(self, item: Search_Alternative_Request):
        self.database_of_yingshaoxo.add(data=item.to_dict())

    def search(self, item_filter: Search_Alternative_Request, page_number:int|None=None, page_size:int|None=None, start_from:int=0, reverse:bool=False):
        return _search_function(self=self, item_filter=item_filter, page_number=page_number, page_size=page_size, start_from=start_from, reverse=reverse)

    def delete(self, item_filter: Search_Alternative_Request):
        return _delete(self=self, item_filter=item_filter)
    
    def update(self, old_item_filter: Search_Alternative_Request, new_item: Search_Alternative_Request):
        return _update(self=self, old_item_filter=old_item_filter, new_item=new_item)


class Yingshaoxo_Database_Get_an_object_Request:
    def __init__(self, database_base_folder: str) -> None:
        self.database_of_yingshaoxo = Database_Of_Yingshaoxo(database_name="Get_an_object_Request", database_base_folder=database_base_folder)

    def add(self, item: Get_an_object_Request):
        self.database_of_yingshaoxo.add(data=item.to_dict())

    def search(self, item_filter: Get_an_object_Request, page_number:int|None=None, page_size:int|None=None, start_from:int=0, reverse:bool=False):
        return _search_function(self=self, item_filter=item_filter, page_number=page_number, page_size=page_size, start_from=start_from, reverse=reverse)

    def delete(self, item_filter: Get_an_object_Request):
        return _delete(self=self, item_filter=item_filter)
    
    def update(self, old_item_filter: Get_an_object_Request, new_item: Get_an_object_Request):
        return _update(self=self, old_item_filter=old_item_filter, new_item=new_item)


class Yingshaoxo_Database_Get_an_object_Response:
    def __init__(self, database_base_folder: str) -> None:
        self.database_of_yingshaoxo = Database_Of_Yingshaoxo(database_name="Get_an_object_Response", database_base_folder=database_base_folder)

    def add(self, item: Get_an_object_Response):
        self.database_of_yingshaoxo.add(data=item.to_dict())

    def search(self, item_filter: Get_an_object_Response, page_number:int|None=None, page_size:int|None=None, start_from:int=0, reverse:bool=False):
        return _search_function(self=self, item_filter=item_filter, page_number=page_number, page_size=page_size, start_from=start_from, reverse=reverse)

    def delete(self, item_filter: Get_an_object_Response):
        return _delete(self=self, item_filter=item_filter)
    
    def update(self, old_item_filter: Get_an_object_Response, new_item: Get_an_object_Response):
        return _update(self=self, old_item_filter=old_item_filter, new_item=new_item)


class Yingshaoxo_Database_Add_Object_Response:
    def __init__(self, database_base_folder: str) -> None:
        self.database_of_yingshaoxo = Database_Of_Yingshaoxo(database_name="Add_Object_Response", database_base_folder=database_base_folder)

    def add(self, item: Add_Object_Response):
        self.database_of_yingshaoxo.add(data=item.to_dict())

    def search(self, item_filter: Add_Object_Response, page_number:int|None=None, page_size:int|None=None, start_from:int=0, reverse:bool=False):
        return _search_function(self=self, item_filter=item_filter, page_number=page_number, page_size=page_size, start_from=start_from, reverse=reverse)

    def delete(self, item_filter: Add_Object_Response):
        return _delete(self=self, item_filter=item_filter)
    
    def update(self, old_item_filter: Add_Object_Response, new_item: Add_Object_Response):
        return _update(self=self, old_item_filter=old_item_filter, new_item=new_item)


class Yingshaoxo_Database_Add_Object_Request:
    def __init__(self, database_base_folder: str) -> None:
        self.database_of_yingshaoxo = Database_Of_Yingshaoxo(database_name="Add_Object_Request", database_base_folder=database_base_folder)

    def add(self, item: Add_Object_Request):
        self.database_of_yingshaoxo.add(data=item.to_dict())

    def search(self, item_filter: Add_Object_Request, page_number:int|None=None, page_size:int|None=None, start_from:int=0, reverse:bool=False):
        return _search_function(self=self, item_filter=item_filter, page_number=page_number, page_size=page_size, start_from=start_from, reverse=reverse)

    def delete(self, item_filter: Add_Object_Request):
        return _delete(self=self, item_filter=item_filter)
    
    def update(self, old_item_filter: Add_Object_Request, new_item: Add_Object_Request):
        return _update(self=self, old_item_filter=old_item_filter, new_item=new_item)


class Yingshaoxo_Database_Update_Object_Response:
    def __init__(self, database_base_folder: str) -> None:
        self.database_of_yingshaoxo = Database_Of_Yingshaoxo(database_name="Update_Object_Response", database_base_folder=database_base_folder)

    def add(self, item: Update_Object_Response):
        self.database_of_yingshaoxo.add(data=item.to_dict())

    def search(self, item_filter: Update_Object_Response, page_number:int|None=None, page_size:int|None=None, start_from:int=0, reverse:bool=False):
        return _search_function(self=self, item_filter=item_filter, page_number=page_number, page_size=page_size, start_from=start_from, reverse=reverse)

    def delete(self, item_filter: Update_Object_Response):
        return _delete(self=self, item_filter=item_filter)
    
    def update(self, old_item_filter: Update_Object_Response, new_item: Update_Object_Response):
        return _update(self=self, old_item_filter=old_item_filter, new_item=new_item)


class Yingshaoxo_Database_Update_Object_Request:
    def __init__(self, database_base_folder: str) -> None:
        self.database_of_yingshaoxo = Database_Of_Yingshaoxo(database_name="Update_Object_Request", database_base_folder=database_base_folder)

    def add(self, item: Update_Object_Request):
        self.database_of_yingshaoxo.add(data=item.to_dict())

    def search(self, item_filter: Update_Object_Request, page_number:int|None=None, page_size:int|None=None, start_from:int=0, reverse:bool=False):
        return _search_function(self=self, item_filter=item_filter, page_number=page_number, page_size=page_size, start_from=start_from, reverse=reverse)

    def delete(self, item_filter: Update_Object_Request):
        return _delete(self=self, item_filter=item_filter)
    
    def update(self, old_item_filter: Update_Object_Request, new_item: Update_Object_Request):
        return _update(self=self, old_item_filter=old_item_filter, new_item=new_item)


class Yingshaoxo_Database_Delete_Object_Response:
    def __init__(self, database_base_folder: str) -> None:
        self.database_of_yingshaoxo = Database_Of_Yingshaoxo(database_name="Delete_Object_Response", database_base_folder=database_base_folder)

    def add(self, item: Delete_Object_Response):
        self.database_of_yingshaoxo.add(data=item.to_dict())

    def search(self, item_filter: Delete_Object_Response, page_number:int|None=None, page_size:int|None=None, start_from:int=0, reverse:bool=False):
        return _search_function(self=self, item_filter=item_filter, page_number=page_number, page_size=page_size, start_from=start_from, reverse=reverse)

    def delete(self, item_filter: Delete_Object_Response):
        return _delete(self=self, item_filter=item_filter)
    
    def update(self, old_item_filter: Delete_Object_Response, new_item: Delete_Object_Response):
        return _update(self=self, old_item_filter=old_item_filter, new_item=new_item)


class Yingshaoxo_Database_Delete_Object_Request:
    def __init__(self, database_base_folder: str) -> None:
        self.database_of_yingshaoxo = Database_Of_Yingshaoxo(database_name="Delete_Object_Request", database_base_folder=database_base_folder)

    def add(self, item: Delete_Object_Request):
        self.database_of_yingshaoxo.add(data=item.to_dict())

    def search(self, item_filter: Delete_Object_Request, page_number:int|None=None, page_size:int|None=None, start_from:int=0, reverse:bool=False):
        return _search_function(self=self, item_filter=item_filter, page_number=page_number, page_size=page_size, start_from=start_from, reverse=reverse)

    def delete(self, item_filter: Delete_Object_Request):
        return _delete(self=self, item_filter=item_filter)
    
    def update(self, old_item_filter: Delete_Object_Request, new_item: Delete_Object_Request):
        return _update(self=self, old_item_filter=old_item_filter, new_item=new_item)


class Yingshaoxo_Database_Download_backup_data_response:
    def __init__(self, database_base_folder: str) -> None:
        self.database_of_yingshaoxo = Database_Of_Yingshaoxo(database_name="Download_backup_data_response", database_base_folder=database_base_folder)

    def add(self, item: Download_backup_data_response):
        self.database_of_yingshaoxo.add(data=item.to_dict())

    def search(self, item_filter: Download_backup_data_response, page_number:int|None=None, page_size:int|None=None, start_from:int=0, reverse:bool=False):
        return _search_function(self=self, item_filter=item_filter, page_number=page_number, page_size=page_size, start_from=start_from, reverse=reverse)

    def delete(self, item_filter: Download_backup_data_response):
        return _delete(self=self, item_filter=item_filter)
    
    def update(self, old_item_filter: Download_backup_data_response, new_item: Download_backup_data_response):
        return _update(self=self, old_item_filter=old_item_filter, new_item=new_item)


class Yingshaoxo_Database_Download_backup_data_request:
    def __init__(self, database_base_folder: str) -> None:
        self.database_of_yingshaoxo = Database_Of_Yingshaoxo(database_name="Download_backup_data_request", database_base_folder=database_base_folder)

    def add(self, item: Download_backup_data_request):
        self.database_of_yingshaoxo.add(data=item.to_dict())

    def search(self, item_filter: Download_backup_data_request, page_number:int|None=None, page_size:int|None=None, start_from:int=0, reverse:bool=False):
        return _search_function(self=self, item_filter=item_filter, page_number=page_number, page_size=page_size, start_from=start_from, reverse=reverse)

    def delete(self, item_filter: Download_backup_data_request):
        return _delete(self=self, item_filter=item_filter)
    
    def update(self, old_item_filter: Download_backup_data_request, new_item: Download_backup_data_request):
        return _update(self=self, old_item_filter=old_item_filter, new_item=new_item)


class Yingshaoxo_Database_Upload_backup_data_request:
    def __init__(self, database_base_folder: str) -> None:
        self.database_of_yingshaoxo = Database_Of_Yingshaoxo(database_name="Upload_backup_data_request", database_base_folder=database_base_folder)

    def add(self, item: Upload_backup_data_request):
        self.database_of_yingshaoxo.add(data=item.to_dict())

    def search(self, item_filter: Upload_backup_data_request, page_number:int|None=None, page_size:int|None=None, start_from:int=0, reverse:bool=False):
        return _search_function(self=self, item_filter=item_filter, page_number=page_number, page_size=page_size, start_from=start_from, reverse=reverse)

    def delete(self, item_filter: Upload_backup_data_request):
        return _delete(self=self, item_filter=item_filter)
    
    def update(self, old_item_filter: Upload_backup_data_request, new_item: Upload_backup_data_request):
        return _update(self=self, old_item_filter=old_item_filter, new_item=new_item)


class Yingshaoxo_Database_Upload_backup_data_response:
    def __init__(self, database_base_folder: str) -> None:
        self.database_of_yingshaoxo = Database_Of_Yingshaoxo(database_name="Upload_backup_data_response", database_base_folder=database_base_folder)

    def add(self, item: Upload_backup_data_response):
        self.database_of_yingshaoxo.add(data=item.to_dict())

    def search(self, item_filter: Upload_backup_data_response, page_number:int|None=None, page_size:int|None=None, start_from:int=0, reverse:bool=False):
        return _search_function(self=self, item_filter=item_filter, page_number=page_number, page_size=page_size, start_from=start_from, reverse=reverse)

    def delete(self, item_filter: Upload_backup_data_response):
        return _delete(self=self, item_filter=item_filter)
    
    def update(self, old_item_filter: Upload_backup_data_response, new_item: Upload_backup_data_response):
        return _update(self=self, old_item_filter=old_item_filter, new_item=new_item)


class Yingshaoxo_Database_Excutor_it_has_alternatives:
    def __init__(self, database_base_folder: str):
        self._database_base_folder = database_base_folder
        self.Get_Special_JWT_Response = Yingshaoxo_Database_Get_Special_JWT_Response(database_base_folder=self._database_base_folder)
        self.Get_Special_JWT_Request = Yingshaoxo_Database_Get_Special_JWT_Request(database_base_folder=self._database_base_folder)
        self.is_JWT_ok_Response = Yingshaoxo_Database_is_JWT_ok_Response(database_base_folder=self._database_base_folder)
        self.is_JWT_ok_Request = Yingshaoxo_Database_is_JWT_ok_Request(database_base_folder=self._database_base_folder)
        self.Get_invitation_code_request = Yingshaoxo_Database_Get_invitation_code_request(database_base_folder=self._database_base_folder)
        self.Get_invitation_code_response = Yingshaoxo_Database_Get_invitation_code_response(database_base_folder=self._database_base_folder)
        self.Search_Alternative_Response = Yingshaoxo_Database_Search_Alternative_Response(database_base_folder=self._database_base_folder)
        self.Search_Alternative_Request = Yingshaoxo_Database_Search_Alternative_Request(database_base_folder=self._database_base_folder)
        self.Get_an_object_Request = Yingshaoxo_Database_Get_an_object_Request(database_base_folder=self._database_base_folder)
        self.Get_an_object_Response = Yingshaoxo_Database_Get_an_object_Response(database_base_folder=self._database_base_folder)
        self.Add_Object_Response = Yingshaoxo_Database_Add_Object_Response(database_base_folder=self._database_base_folder)
        self.Add_Object_Request = Yingshaoxo_Database_Add_Object_Request(database_base_folder=self._database_base_folder)
        self.Update_Object_Response = Yingshaoxo_Database_Update_Object_Response(database_base_folder=self._database_base_folder)
        self.Update_Object_Request = Yingshaoxo_Database_Update_Object_Request(database_base_folder=self._database_base_folder)
        self.Delete_Object_Response = Yingshaoxo_Database_Delete_Object_Response(database_base_folder=self._database_base_folder)
        self.Delete_Object_Request = Yingshaoxo_Database_Delete_Object_Request(database_base_folder=self._database_base_folder)
        self.Download_backup_data_response = Yingshaoxo_Database_Download_backup_data_response(database_base_folder=self._database_base_folder)
        self.Download_backup_data_request = Yingshaoxo_Database_Download_backup_data_request(database_base_folder=self._database_base_folder)
        self.Upload_backup_data_request = Yingshaoxo_Database_Upload_backup_data_request(database_base_folder=self._database_base_folder)
        self.Upload_backup_data_response = Yingshaoxo_Database_Upload_backup_data_response(database_base_folder=self._database_base_folder)


if __name__ == "__main__":
    database_excutor = Yingshaoxo_Database_Excutor_it_has_alternatives(database_base_folder="/home/yingshaoxo/CS/auto_everything/example/database/yingshaoxo_database")