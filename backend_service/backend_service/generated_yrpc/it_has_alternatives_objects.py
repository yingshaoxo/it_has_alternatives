import copy
from dataclasses import dataclass
from enum import Enum
from typing import Any


_ygrpc_official_types = [int, float, str, bool]


def convert_dict_that_has_enum_object_into_pure_dict(value: Any) -> dict[str, Any] | list[Any] | Any:
    if type(value) is list:
        new_list: list[Any] = []
        for one in value: #type: ignore
            new_list.append(convert_dict_that_has_enum_object_into_pure_dict(value=one)) 
        return new_list
    elif type(value) is dict:
        new_dict: dict[str, Any] = {}
        for key_, value_ in value.items(): #type: ignore
            new_dict[key_] = convert_dict_that_has_enum_object_into_pure_dict(value=value_) #type: ignore
        return new_dict
    else:
        if str(type(value)).startswith("<enum"):
            return value.name
        else:
            if type(value) in _ygrpc_official_types:
                return value
            else:
                # handle custom message data type
                if value == None:
                    return None
                elif str(type(value)).startswith("<class"):
                    return convert_dict_that_has_enum_object_into_pure_dict(
                        value=value.to_dict()
                    )
    return None


def convert_pure_dict_into_a_dict_that_has_enum_object(pure_value: Any, refrence_value: Any) -> Any:
    if type(pure_value) is list:
        new_list: list[Any] = []
        for one in pure_value: #type: ignore
            new_list.append(
                convert_pure_dict_into_a_dict_that_has_enum_object(pure_value=one, refrence_value=refrence_value)
            ) 
        return new_list
    elif type(pure_value) is dict:
        if str(refrence_value).startswith("<class"):
            new_object = refrence_value()
            old_property_list = getattr(new_object, "_property_name_to_its_type_dict")
            for key in old_property_list.keys():
                if key in pure_value.keys():
                    setattr(new_object, key, convert_pure_dict_into_a_dict_that_has_enum_object(pure_value[key], old_property_list[key])) # type: ignore
            return new_object
        else:
            return None
    else:
        if str(refrence_value).startswith("<enum"):
            default_value = None
            for temp_index, temp_value in enumerate(refrence_value._member_names_):
                if temp_value == pure_value:
                    default_value = refrence_value(temp_value) 
                    break
            return default_value
        else:
            if refrence_value in _ygrpc_official_types:
                return pure_value
            else:
                return None


class YRPC_OBJECT_BASE_CLASS:
    def to_dict(self, ignore_null: bool=False) -> dict[str, Any]:
        old_dict = {}
        for key in self._property_name_to_its_type_dict.keys(): #type: ignore
            old_dict[key] = self.__dict__[key] #type: ignore
        new_dict = convert_dict_that_has_enum_object_into_pure_dict(value=old_dict.copy())
        return new_dict.copy() #type: ignore

    def from_dict(self, dict: dict[str, Any]) -> Any:
        new_object = convert_pure_dict_into_a_dict_that_has_enum_object(pure_value=dict.copy(), refrence_value=self.__class__)

        new_object_dict = new_object.__dict__.copy() 
        for key, value in new_object_dict.items():
            if key in self.__dict__:
                setattr(self, key, value)

        return new_object

    def _clone(self) -> Any:
        return copy.deepcopy(self)


class Sort_By(Enum):
    like = "like"
    dislike = "dislike"

        
@dataclass()
class An_Object(YRPC_OBJECT_BASE_CLASS):
    id: str | None = None
    name: str | None = None
    description: str | None = None
    likes: int | None = None
    dislikes: int | None = None
    alternative_id_list: list[str] | None = None

    _property_name_to_its_type_dict = {
        "id": str,
        "name": str,
        "description": str,
        "likes": int,
        "dislikes": int,
        "alternative_id_list": str,
    }

    @dataclass()
    class _key_string_dict:
        id: str = "id"
        name: str = "name"
        description: str = "description"
        likes: str = "likes"
        dislikes: str = "dislikes"
        alternative_id_list: str = "alternative_id_list"

    def from_dict(self, dict: dict[str, Any]):
        new_variable: An_Object = super().from_dict(dict)
        return new_variable


@dataclass()
class Search_Alternative_Request(YRPC_OBJECT_BASE_CLASS):
    key_words: str | None = None
    keywords_of_name: str | None = None
    keywords_of_description: str | None = None
    sort_by: Sort_By | None = None
    page_size: int | None = None
    page_number: int | None = None

    _property_name_to_its_type_dict = {
        "key_words": str,
        "keywords_of_name": str,
        "keywords_of_description": str,
        "sort_by": Sort_By,
        "page_size": int,
        "page_number": int,
    }

    @dataclass()
    class _key_string_dict:
        key_words: str = "key_words"
        keywords_of_name: str = "keywords_of_name"
        keywords_of_description: str = "keywords_of_description"
        sort_by: str = "sort_by"
        page_size: str = "page_size"
        page_number: str = "page_number"

    def from_dict(self, dict: dict[str, Any]):
        new_variable: Search_Alternative_Request = super().from_dict(dict)
        return new_variable


@dataclass()
class Search_Alternative_Response(YRPC_OBJECT_BASE_CLASS):
    error: str | None = None
    alternative_object_list: list[An_Object] | None = None

    _property_name_to_its_type_dict = {
        "error": str,
        "alternative_object_list": An_Object,
    }

    @dataclass()
    class _key_string_dict:
        error: str = "error"
        alternative_object_list: str = "alternative_object_list"

    def from_dict(self, dict: dict[str, Any]):
        new_variable: Search_Alternative_Response = super().from_dict(dict)
        return new_variable


@dataclass()
class Get_an_object_Request(YRPC_OBJECT_BASE_CLASS):
    id: str | None = None
    name: str | None = None

    _property_name_to_its_type_dict = {
        "id": str,
        "name": str,
    }

    @dataclass()
    class _key_string_dict:
        id: str = "id"
        name: str = "name"

    def from_dict(self, dict: dict[str, Any]):
        new_variable: Get_an_object_Request = super().from_dict(dict)
        return new_variable


@dataclass()
class Get_an_object_Response(YRPC_OBJECT_BASE_CLASS):
    error: str | None = None
    an_object: An_Object | None = None

    _property_name_to_its_type_dict = {
        "error": str,
        "an_object": An_Object,
    }

    @dataclass()
    class _key_string_dict:
        error: str = "error"
        an_object: str = "an_object"

    def from_dict(self, dict: dict[str, Any]):
        new_variable: Get_an_object_Response = super().from_dict(dict)
        return new_variable


@dataclass()
class Add_Object_Request(YRPC_OBJECT_BASE_CLASS):
    an_object: An_Object | None = None

    _property_name_to_its_type_dict = {
        "an_object": An_Object,
    }

    @dataclass()
    class _key_string_dict:
        an_object: str = "an_object"

    def from_dict(self, dict: dict[str, Any]):
        new_variable: Add_Object_Request = super().from_dict(dict)
        return new_variable


@dataclass()
class Add_Object_Response(YRPC_OBJECT_BASE_CLASS):
    error: str | None = None
    success: bool | None = None

    _property_name_to_its_type_dict = {
        "error": str,
        "success": bool,
    }

    @dataclass()
    class _key_string_dict:
        error: str = "error"
        success: str = "success"

    def from_dict(self, dict: dict[str, Any]):
        new_variable: Add_Object_Response = super().from_dict(dict)
        return new_variable


@dataclass()
class Update_Object_Request(YRPC_OBJECT_BASE_CLASS):
    an_object: An_Object | None = None

    _property_name_to_its_type_dict = {
        "an_object": An_Object,
    }

    @dataclass()
    class _key_string_dict:
        an_object: str = "an_object"

    def from_dict(self, dict: dict[str, Any]):
        new_variable: Update_Object_Request = super().from_dict(dict)
        return new_variable


@dataclass()
class Update_Object_Response(YRPC_OBJECT_BASE_CLASS):
    error: str | None = None
    success: bool | None = None

    _property_name_to_its_type_dict = {
        "error": str,
        "success": bool,
    }

    @dataclass()
    class _key_string_dict:
        error: str = "error"
        success: str = "success"

    def from_dict(self, dict: dict[str, Any]):
        new_variable: Update_Object_Response = super().from_dict(dict)
        return new_variable


@dataclass()
class Delete_Object_Request(YRPC_OBJECT_BASE_CLASS):
    an_object: An_Object | None = None

    _property_name_to_its_type_dict = {
        "an_object": An_Object,
    }

    @dataclass()
    class _key_string_dict:
        an_object: str = "an_object"

    def from_dict(self, dict: dict[str, Any]):
        new_variable: Delete_Object_Request = super().from_dict(dict)
        return new_variable


@dataclass()
class Delete_Object_Response(YRPC_OBJECT_BASE_CLASS):
    error: str | None = None
    success: bool | None = None

    _property_name_to_its_type_dict = {
        "error": str,
        "success": bool,
    }

    @dataclass()
    class _key_string_dict:
        error: str = "error"
        success: str = "success"

    def from_dict(self, dict: dict[str, Any]):
        new_variable: Delete_Object_Response = super().from_dict(dict)
        return new_variable