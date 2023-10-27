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
    # yingshaoxo: I strongly recommend you use enum as a string type in other message data_model
    # for example, `Sort_By.dislike.value`
    like = "like"
    dislike = "dislike"

        
@dataclass()
class A_User(YRPC_OBJECT_BASE_CLASS):
    id: str | None = None
    create_time_in_10_numbers_timestamp_format: int | None = None
    email: str | None = None
    password: str | None = None
    jwt: str | None = None
    level: int | None = None
    parent_email: str | None = None
    children_email_list: list[str] | None = None
    invitation_counting: int | None = None
    invitation_code_list: list[str] | None = None
    last_login_time_in_10_numbers_timestamp_format: int | None = None

    _property_name_to_its_type_dict = {
        "id": str,
        "create_time_in_10_numbers_timestamp_format": int,
        "email": str,
        "password": str,
        "jwt": str,
        "level": int,
        "parent_email": str,
        "children_email_list": str,
        "invitation_counting": int,
        "invitation_code_list": str,
        "last_login_time_in_10_numbers_timestamp_format": int,
    }

    @dataclass()
    class _key_string_dict:
        id: str = "id"
        create_time_in_10_numbers_timestamp_format: str = "create_time_in_10_numbers_timestamp_format"
        email: str = "email"
        password: str = "password"
        jwt: str = "jwt"
        level: str = "level"
        parent_email: str = "parent_email"
        children_email_list: str = "children_email_list"
        invitation_counting: str = "invitation_counting"
        invitation_code_list: str = "invitation_code_list"
        last_login_time_in_10_numbers_timestamp_format: str = "last_login_time_in_10_numbers_timestamp_format"

    def from_dict(self, dict: dict[str, Any]):
        new_variable: A_User = super().from_dict(dict)
        return new_variable


@dataclass()
class An_Object(YRPC_OBJECT_BASE_CLASS):
    id: str | None = None
    name: str | None = None
    description: str | None = None
    level: int | None = None
    likes: int | None = None
    dislikes: int | None = None
    alternative_id_list: list[str] | None = None
    create_time_in_10_numbers_timestamp_format: int | None = None
    update_time_in_10_numbers_timestamp_format: int | None = None

    _property_name_to_its_type_dict = {
        "id": str,
        "name": str,
        "description": str,
        "level": int,
        "likes": int,
        "dislikes": int,
        "alternative_id_list": str,
        "create_time_in_10_numbers_timestamp_format": int,
        "update_time_in_10_numbers_timestamp_format": int,
    }

    @dataclass()
    class _key_string_dict:
        id: str = "id"
        name: str = "name"
        description: str = "description"
        level: str = "level"
        likes: str = "likes"
        dislikes: str = "dislikes"
        alternative_id_list: str = "alternative_id_list"
        create_time_in_10_numbers_timestamp_format: str = "create_time_in_10_numbers_timestamp_format"
        update_time_in_10_numbers_timestamp_format: str = "update_time_in_10_numbers_timestamp_format"

    def from_dict(self, dict: dict[str, Any]):
        new_variable: An_Object = super().from_dict(dict)
        return new_variable


@dataclass()
class Get_Special_JWT_Request(YRPC_OBJECT_BASE_CLASS):
    email: str | None = None
    password: str | None = None
    invitation_code: str | None = None

    _property_name_to_its_type_dict = {
        "email": str,
        "password": str,
        "invitation_code": str,
    }

    @dataclass()
    class _key_string_dict:
        email: str = "email"
        password: str = "password"
        invitation_code: str = "invitation_code"

    def from_dict(self, dict: dict[str, Any]):
        new_variable: Get_Special_JWT_Request = super().from_dict(dict)
        return new_variable


@dataclass()
class Get_Special_JWT_Response(YRPC_OBJECT_BASE_CLASS):
    error: str | None = None
    encrypted_jwt: str | None = None

    _property_name_to_its_type_dict = {
        "error": str,
        "encrypted_jwt": str,
    }

    @dataclass()
    class _key_string_dict:
        error: str = "error"
        encrypted_jwt: str = "encrypted_jwt"

    def from_dict(self, dict: dict[str, Any]):
        new_variable: Get_Special_JWT_Response = super().from_dict(dict)
        return new_variable


@dataclass()
class is_JWT_ok_Request(YRPC_OBJECT_BASE_CLASS):
    jwt: str | None = None

    _property_name_to_its_type_dict = {
        "jwt": str,
    }

    @dataclass()
    class _key_string_dict:
        jwt: str = "jwt"

    def from_dict(self, dict: dict[str, Any]):
        new_variable: is_JWT_ok_Request = super().from_dict(dict)
        return new_variable


@dataclass()
class is_JWT_ok_Response(YRPC_OBJECT_BASE_CLASS):
    error: str | None = None
    ok: bool | None = None
    is_admin: bool | None = None

    _property_name_to_its_type_dict = {
        "error": str,
        "ok": bool,
        "is_admin": bool,
    }

    @dataclass()
    class _key_string_dict:
        error: str = "error"
        ok: str = "ok"
        is_admin: str = "is_admin"

    def from_dict(self, dict: dict[str, Any]):
        new_variable: is_JWT_ok_Response = super().from_dict(dict)
        return new_variable


@dataclass()
class Get_invitation_code_request(YRPC_OBJECT_BASE_CLASS):


    _property_name_to_its_type_dict = {

    }

    @dataclass()
    class _key_string_dict:
        pass

    def from_dict(self, dict: dict[str, Any]):
        new_variable: Get_invitation_code_request = super().from_dict(dict)
        return new_variable


@dataclass()
class Get_invitation_code_response(YRPC_OBJECT_BASE_CLASS):
    error: str | None = None
    invitation_code: str | None = None

    _property_name_to_its_type_dict = {
        "error": str,
        "invitation_code": str,
    }

    @dataclass()
    class _key_string_dict:
        error: str = "error"
        invitation_code: str = "invitation_code"

    def from_dict(self, dict: dict[str, Any]):
        new_variable: Get_invitation_code_response = super().from_dict(dict)
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


@dataclass()
class Download_backup_data_request(YRPC_OBJECT_BASE_CLASS):


    _property_name_to_its_type_dict = {

    }

    @dataclass()
    class _key_string_dict:
        pass

    def from_dict(self, dict: dict[str, Any]):
        new_variable: Download_backup_data_request = super().from_dict(dict)
        return new_variable


@dataclass()
class Download_backup_data_response(YRPC_OBJECT_BASE_CLASS):
    error: str | None = None
    file_name: str | None = None
    file_bytes_in_base64_format: str | None = None

    _property_name_to_its_type_dict = {
        "error": str,
        "file_name": str,
        "file_bytes_in_base64_format": str,
    }

    @dataclass()
    class _key_string_dict:
        error: str = "error"
        file_name: str = "file_name"
        file_bytes_in_base64_format: str = "file_bytes_in_base64_format"

    def from_dict(self, dict: dict[str, Any]):
        new_variable: Download_backup_data_response = super().from_dict(dict)
        return new_variable


@dataclass()
class Upload_backup_data_request(YRPC_OBJECT_BASE_CLASS):
    file_bytes_in_base64_format: str | None = None

    _property_name_to_its_type_dict = {
        "file_bytes_in_base64_format": str,
    }

    @dataclass()
    class _key_string_dict:
        file_bytes_in_base64_format: str = "file_bytes_in_base64_format"

    def from_dict(self, dict: dict[str, Any]):
        new_variable: Upload_backup_data_request = super().from_dict(dict)
        return new_variable


@dataclass()
class Upload_backup_data_response(YRPC_OBJECT_BASE_CLASS):
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
        new_variable: Upload_backup_data_response = super().from_dict(dict)
        return new_variable