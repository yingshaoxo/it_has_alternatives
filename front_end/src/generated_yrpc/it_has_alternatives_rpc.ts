import * as it_has_alternatives_objects from './it_has_alternatives_objects'

export class Client_it_has_alternatives {
  /**
   * @param {string} _service_url is something like: "http://127.0.0.1:80" or "https://127.0.0.1"
   * @param {{ [key: string]: string }} _header  http headers, it's a dictionary, liek {'content-type', 'application/json'}
   * @param {Function} _error_handle_function will get called when http request got error, you need to give it a function like: (err: String) {print(err)}
   * @param {Function} _interceptor_function will get called for every response, you need to give it a function like: (data: dict[Any, Any]) {print(data)}
   */
    _service_url: string
    _header: { [key: string]: string } = {}
    _error_handle_function: (error: string) => void = (error: string) => {console.log(error)}
    _special_error_key: string = "__yingshaoxo's_error__"
    _interceptor_function: (data: any) => void = (data: any) => {console.log(data)}

    constructor(service_url: string, header?: { [key: string]: string }, error_handle_function?: (error: string) => void, interceptor_function?: (data: any) => void) {
        if (service_url.endsWith("/")) {
            service_url = service_url.slice(0, service_url.length-1);
        }
        try {
            if (location.protocol === 'https:') {
                if (service_url.startsWith("http:")) {
                    service_url = service_url.replace("http:", "https:")
                }
            } else if (location.protocol === 'http:') {
                if (service_url.startsWith("https:")) {
                    service_url = service_url.replace("https:", "http:")
                }
            }
        } catch (e) {
        }
        this._service_url = service_url
        
        if (header != null) {
            this._header = header
        }

        if (error_handle_function != null) {
            this._error_handle_function = error_handle_function
        }

        if (interceptor_function != null) {
            this._interceptor_function = interceptor_function
        }
    } 

    async _get_reponse_or_error_by_url_path_and_input(sub_url: string, input_dict: { [key: string]: any }): Promise<any> {
        let the_url = `${this._service_url}/it_has_alternatives/${sub_url}/`
        try {
            const response = await fetch(the_url, 
            {
                method: "POST",
                body: JSON.stringify(input_dict),
                headers: {
                    "Content-type": "application/json; charset=UTF-8",
                    ...this._header
                }
            });
            var json_response = await response.json()
            this._interceptor_function(json_response)
            return json_response
        } catch (e) {
            return {[this._special_error_key]: String(e)};
        }
    }

    async get_special_jwt(item: it_has_alternatives_objects.Get_Special_JWT_Request, ignore_error?: boolean): Promise<it_has_alternatives_objects.Get_Special_JWT_Response | null> {
        let result = await this._get_reponse_or_error_by_url_path_and_input("get_special_jwt", item.to_dict())
        if (Object.keys(result).includes(this._special_error_key)) {
            if ((ignore_error == null) || ((ignore_error != null) && (!ignore_error))) {
                this._error_handle_function(result[this._special_error_key])
            }
            return null
        } else {
            return new it_has_alternatives_objects.Get_Special_JWT_Response().from_dict(result)
        }
    }

    async is_jwt_ok(item: it_has_alternatives_objects.is_JWT_ok_Request, ignore_error?: boolean): Promise<it_has_alternatives_objects.is_JWT_ok_Response | null> {
        let result = await this._get_reponse_or_error_by_url_path_and_input("is_jwt_ok", item.to_dict())
        if (Object.keys(result).includes(this._special_error_key)) {
            if ((ignore_error == null) || ((ignore_error != null) && (!ignore_error))) {
                this._error_handle_function(result[this._special_error_key])
            }
            return null
        } else {
            return new it_has_alternatives_objects.is_JWT_ok_Response().from_dict(result)
        }
    }

    async get_invitation_code(item: it_has_alternatives_objects.Get_invitation_code_request, ignore_error?: boolean): Promise<it_has_alternatives_objects.Get_invitation_code_response | null> {
        let result = await this._get_reponse_or_error_by_url_path_and_input("get_invitation_code", item.to_dict())
        if (Object.keys(result).includes(this._special_error_key)) {
            if ((ignore_error == null) || ((ignore_error != null) && (!ignore_error))) {
                this._error_handle_function(result[this._special_error_key])
            }
            return null
        } else {
            return new it_has_alternatives_objects.Get_invitation_code_response().from_dict(result)
        }
    }

    async search_alternatives(item: it_has_alternatives_objects.Search_Alternative_Request, ignore_error?: boolean): Promise<it_has_alternatives_objects.Search_Alternative_Response | null> {
        let result = await this._get_reponse_or_error_by_url_path_and_input("search_alternatives", item.to_dict())
        if (Object.keys(result).includes(this._special_error_key)) {
            if ((ignore_error == null) || ((ignore_error != null) && (!ignore_error))) {
                this._error_handle_function(result[this._special_error_key])
            }
            return null
        } else {
            return new it_has_alternatives_objects.Search_Alternative_Response().from_dict(result)
        }
    }

    async get_an_object(item: it_has_alternatives_objects.Get_an_object_Request, ignore_error?: boolean): Promise<it_has_alternatives_objects.Get_an_object_Response | null> {
        let result = await this._get_reponse_or_error_by_url_path_and_input("get_an_object", item.to_dict())
        if (Object.keys(result).includes(this._special_error_key)) {
            if ((ignore_error == null) || ((ignore_error != null) && (!ignore_error))) {
                this._error_handle_function(result[this._special_error_key])
            }
            return null
        } else {
            return new it_has_alternatives_objects.Get_an_object_Response().from_dict(result)
        }
    }

    async add_alternative(item: it_has_alternatives_objects.Add_Object_Request, ignore_error?: boolean): Promise<it_has_alternatives_objects.Add_Object_Response | null> {
        let result = await this._get_reponse_or_error_by_url_path_and_input("add_alternative", item.to_dict())
        if (Object.keys(result).includes(this._special_error_key)) {
            if ((ignore_error == null) || ((ignore_error != null) && (!ignore_error))) {
                this._error_handle_function(result[this._special_error_key])
            }
            return null
        } else {
            return new it_has_alternatives_objects.Add_Object_Response().from_dict(result)
        }
    }

    async update_alternative(item: it_has_alternatives_objects.Update_Object_Request, ignore_error?: boolean): Promise<it_has_alternatives_objects.Update_Object_Response | null> {
        let result = await this._get_reponse_or_error_by_url_path_and_input("update_alternative", item.to_dict())
        if (Object.keys(result).includes(this._special_error_key)) {
            if ((ignore_error == null) || ((ignore_error != null) && (!ignore_error))) {
                this._error_handle_function(result[this._special_error_key])
            }
            return null
        } else {
            return new it_has_alternatives_objects.Update_Object_Response().from_dict(result)
        }
    }

    async delete_alternative(item: it_has_alternatives_objects.Delete_Object_Request, ignore_error?: boolean): Promise<it_has_alternatives_objects.Delete_Object_Response | null> {
        let result = await this._get_reponse_or_error_by_url_path_and_input("delete_alternative", item.to_dict())
        if (Object.keys(result).includes(this._special_error_key)) {
            if ((ignore_error == null) || ((ignore_error != null) && (!ignore_error))) {
                this._error_handle_function(result[this._special_error_key])
            }
            return null
        } else {
            return new it_has_alternatives_objects.Delete_Object_Response().from_dict(result)
        }
    }

    async download_backup_data(item: it_has_alternatives_objects.Download_backup_data_request, ignore_error?: boolean): Promise<it_has_alternatives_objects.Download_backup_data_response | null> {
        let result = await this._get_reponse_or_error_by_url_path_and_input("download_backup_data", item.to_dict())
        if (Object.keys(result).includes(this._special_error_key)) {
            if ((ignore_error == null) || ((ignore_error != null) && (!ignore_error))) {
                this._error_handle_function(result[this._special_error_key])
            }
            return null
        } else {
            return new it_has_alternatives_objects.Download_backup_data_response().from_dict(result)
        }
    }

    async upload_backup_data(item: it_has_alternatives_objects.Upload_backup_data_request, ignore_error?: boolean): Promise<it_has_alternatives_objects.Upload_backup_data_response | null> {
        let result = await this._get_reponse_or_error_by_url_path_and_input("upload_backup_data", item.to_dict())
        if (Object.keys(result).includes(this._special_error_key)) {
            if ((ignore_error == null) || ((ignore_error != null) && (!ignore_error))) {
                this._error_handle_function(result[this._special_error_key])
            }
            return null
        } else {
            return new it_has_alternatives_objects.Upload_backup_data_response().from_dict(result)
        }
    }
}

export default Client_it_has_alternatives