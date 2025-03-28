from typing import Callable

from .it_has_alternatives_objects import *
from auto_everything.database import Database_Of_Yingshaoxo


def _search_function(self: Any, item_filter: Any, page_number:int|None=None, page_size:int|None=None, start_from:int=0, reverse:bool=False) -> list[dict[str, Any]]:
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


def _raw_search_function(self: Any, one_row_json_string_handler: Callable[[str], dict[str, Any] | None], page_number:int|None=None, page_size:int|None=None, start_from:int=0, reverse:bool=False):
    search_temp_dict = {}
    search_temp_dict["_raw_search_counting"] = 0
    search_temp_dict["_search_counting"] = 0
    if (page_number!=None and page_size != None and start_from != None):
        search_temp_dict["_real_start"] = page_number * page_size
        search_temp_dict["_real_end"] = search_temp_dict["_real_start"] + page_size

    def new_one_row_json_string_handler(a_json_string: str):
        search_temp_dict["_raw_search_counting"] += 1

        if (page_number!=None and page_size != None and start_from != None):
            if search_temp_dict["_raw_search_counting"] < start_from:
                return None

        result = one_row_json_string_handler(a_json_string)

        if result != None:
            search_temp_dict["_search_counting"] += 1

        if (page_number!=None and page_size != None and start_from != None):
            if search_temp_dict["_search_counting"] <= search_temp_dict["_real_start"]:
                return None
            if search_temp_dict["_search_counting"] > search_temp_dict["_real_end"]:
                return None

        return result

    return list(self.database_of_yingshaoxo.raw_search(one_row_json_string_handler=new_one_row_json_string_handler))


def _delete(self, item_filter: Any) -> None:
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


class Yingshaoxo_Database_A_User:
    def __init__(self, database_base_folder: str, use_sqlite: bool = False, global_multiprocessing_shared_dict: Any | None = None, auto_backup: bool = False) -> None:
        self.database_of_yingshaoxo = Database_Of_Yingshaoxo(database_name="A_User", database_base_folder=database_base_folder, use_sqlite=use_sqlite, global_multiprocessing_shared_dict=global_multiprocessing_shared_dict, auto_backup=auto_backup)

    def add(self, item: A_User):
        return self.database_of_yingshaoxo.add(data=item.to_dict())

    def search(self, item_filter: A_User, page_number:int|None=None, page_size:int|None=None, start_from:int=0, reverse:bool=False) -> list[A_User]:
        return [A_User().from_dict(one) for one in _search_function(self=self, item_filter=item_filter, page_number=page_number, page_size=page_size, start_from=start_from, reverse=reverse)]

    def raw_search(self, one_row_json_string_handler: Callable[[str], dict[str, Any] | None], page_number:int|None=None, page_size:int|None=None, start_from:int=0, reverse:bool=False) -> list[A_User]:
        '''
        one_row_json_string_handler: a_function to handle search process. If it returns None, we'll ignore it, otherwise, we'll add the return value into the result list.
        '''
        return [A_User().from_dict(one) for one in _raw_search_function(self=self, one_row_json_string_handler=one_row_json_string_handler, page_number=page_number, page_size=page_size, start_from=start_from, reverse=reverse)]

    def delete(self, item_filter: A_User):
        return _delete(self=self, item_filter=item_filter)

    def update(self, old_item_filter: A_User, new_item: A_User):
        return _update(self=self, old_item_filter=old_item_filter, new_item=new_item)


class Yingshaoxo_Database_An_Object:
    def __init__(self, database_base_folder: str, use_sqlite: bool = False, global_multiprocessing_shared_dict: Any | None = None, auto_backup: bool = False) -> None:
        self.database_of_yingshaoxo = Database_Of_Yingshaoxo(database_name="An_Object", database_base_folder=database_base_folder, use_sqlite=use_sqlite, global_multiprocessing_shared_dict=global_multiprocessing_shared_dict, auto_backup=auto_backup)

    def add(self, item: An_Object):
        return self.database_of_yingshaoxo.add(data=item.to_dict())

    def search(self, item_filter: An_Object, page_number:int|None=None, page_size:int|None=None, start_from:int=0, reverse:bool=False) -> list[An_Object]:
        return [An_Object().from_dict(one) for one in _search_function(self=self, item_filter=item_filter, page_number=page_number, page_size=page_size, start_from=start_from, reverse=reverse)]

    def raw_search(self, one_row_json_string_handler: Callable[[str], dict[str, Any] | None], page_number:int|None=None, page_size:int|None=None, start_from:int=0, reverse:bool=False) -> list[An_Object]:
        '''
        one_row_json_string_handler: a_function to handle search process. If it returns None, we'll ignore it, otherwise, we'll add the return value into the result list.
        '''
        return [An_Object().from_dict(one) for one in _raw_search_function(self=self, one_row_json_string_handler=one_row_json_string_handler, page_number=page_number, page_size=page_size, start_from=start_from, reverse=reverse)]

    def delete(self, item_filter: An_Object):
        return _delete(self=self, item_filter=item_filter)

    def update(self, old_item_filter: An_Object, new_item: An_Object):
        return _update(self=self, old_item_filter=old_item_filter, new_item=new_item)


class Yingshaoxo_Database_Excutor_it_has_alternatives:
    def __init__(self, database_base_folder: str, use_sqlite: bool = False, global_multiprocessing_shared_dict: Any | None = None, auto_backup: bool = False):
        self._database_base_folder = database_base_folder
        self.A_User = Yingshaoxo_Database_A_User(database_base_folder=self._database_base_folder, use_sqlite=use_sqlite, global_multiprocessing_shared_dict=global_multiprocessing_shared_dict, auto_backup=auto_backup)
        self.An_Object = Yingshaoxo_Database_An_Object(database_base_folder=self._database_base_folder, use_sqlite=use_sqlite, global_multiprocessing_shared_dict=global_multiprocessing_shared_dict, auto_backup=auto_backup)


if __name__ == "__main__":
    database_excutor = Yingshaoxo_Database_Excutor_it_has_alternatives(database_base_folder="/home/yingshaoxo/CS/auto_everything/example/database/yingshaoxo_database")