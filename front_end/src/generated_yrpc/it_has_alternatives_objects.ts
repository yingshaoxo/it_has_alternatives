const _ygrpc_official_types = ["string", "number", "boolean"];

const _general_to_dict_function = (object: any): any => {
    let the_type = typeof object
    if (the_type == "object") {
        if (object == null) {
            return null
        } else if (Array.isArray(object)) {
            let new_list: any[] = []
            for (const one of object) {
                new_list.push(_general_to_dict_function(one))
            }
            return new_list
        } else {
            let keys = Object.keys(object);
            if (keys.includes("_key_string_dict")) {
                // custom message type
                let new_dict: any = {}
                keys = keys.filter((e) => !["_property_name_to_its_type_dict", "_key_string_dict"].includes(e));
                for (const key of keys) {
                    new_dict[key] = _general_to_dict_function(object[key])
                    // the enum will become a string in the end, so ignore it
                }
                return new_dict
            }
        }
    } else {
        if (_ygrpc_official_types.includes(typeof object)) {
            return object
        } else {
            return null
        }
    }
    return null
};

const _general_from_dict_function = (old_object: any, new_object: any): any => {
    let the_type = typeof new_object
    if (the_type == "object") {
        if (Array.isArray(new_object)) {
            //list
            let new_list: any[] = []
            for (const one of new_object) {
                new_list.push(structuredClone(_general_from_dict_function(old_object, one)))
            }
            return new_list
        } else {
            // dict or null
            if (new_object == null) {
                return null
            } else {
                let keys = Object.keys(old_object);
                if (keys.includes("_key_string_dict")) {
                    keys = Object.keys(old_object._property_name_to_its_type_dict)
                    for (const key of keys) {
                        if (Object.keys(new_object).includes(key)) {
                            console.log((typeof old_object._property_name_to_its_type_dict[key]))
                            if ((typeof old_object._property_name_to_its_type_dict[key]) == "string") {
                                // default value type
                                old_object[key] = new_object[key]
                            } else {
                                // custom message type || enum
                                if (
                                    (typeof old_object._property_name_to_its_type_dict[key]).includes("class") || 
                                    (typeof old_object._property_name_to_its_type_dict[key]).includes("function")
                                ) {
                                    // custom message type || a list of custom type
                                    var reference_object = new (old_object._property_name_to_its_type_dict[key])()
                                    old_object[key] = structuredClone(_general_from_dict_function(reference_object, new_object[key]))
                                } else {
                                    // enum
                                    if (Object.keys(new_object).includes(key)) {
                                        old_object[key] = new_object[key]
                                    } else {
                                        old_object[key] = null
                                    }
                                }
                            }
                        } 
                    }
                } else {
                    return null
                }
            }
        }
    } 
    return old_object
}

enum Sort_By {
    like = "like",
    dislike = "dislike",
}

export interface _An_Object {
    id: string | null;
    name: string | null;
    description: string | null;
    likes: number | null;
    dislikes: number | null;
    alternative_id_list: string[] | null;
}

export class An_Object {
    id: string | null = null;
    name: string | null = null;
    description: string | null = null;
    likes: number | null = null;
    dislikes: number | null = null;
    alternative_id_list: string[] | null = null;

    _property_name_to_its_type_dict = {
            id: "string",
            name: "string",
            description: "string",
            likes: "number",
            dislikes: "number",
            alternative_id_list: "string",
    };

    _key_string_dict = {
        id: "id",
        name: "name",
        description: "description",
        likes: "likes",
        dislikes: "dislikes",
        alternative_id_list: "alternative_id_list",
    };

    to_dict(): _An_Object {
        return _general_to_dict_function(this);
    }

    _clone(): An_Object {
        let clone = Object.assign(Object.create(Object.getPrototypeOf(this)), this)
        return clone
    }

    from_dict(item: _An_Object): An_Object {
        let an_item = new An_Object()
        let new_dict = _general_from_dict_function(an_item, item)

        for (const key of Object.keys(new_dict)) {
            let value = new_dict[key]
            //@ts-ignore
            this[key] = value
            //@ts-ignore
            an_item[key] = value
        }

        return an_item
    }
}


export interface _Search_Alternative_Request {
    key_words: string | null;
    keywords_of_name: string | null;
    keywords_of_description: string | null;
    sort_by: Sort_By | null;
    page_size: number | null;
    page_number: number | null;
}

export class Search_Alternative_Request {
    key_words: string | null = null;
    keywords_of_name: string | null = null;
    keywords_of_description: string | null = null;
    sort_by: Sort_By | null = null;
    page_size: number | null = null;
    page_number: number | null = null;

    _property_name_to_its_type_dict = {
            key_words: "string",
            keywords_of_name: "string",
            keywords_of_description: "string",
            sort_by: Sort_By,
            page_size: "number",
            page_number: "number",
    };

    _key_string_dict = {
        key_words: "key_words",
        keywords_of_name: "keywords_of_name",
        keywords_of_description: "keywords_of_description",
        sort_by: "sort_by",
        page_size: "page_size",
        page_number: "page_number",
    };

    to_dict(): _Search_Alternative_Request {
        return _general_to_dict_function(this);
    }

    _clone(): Search_Alternative_Request {
        let clone = Object.assign(Object.create(Object.getPrototypeOf(this)), this)
        return clone
    }

    from_dict(item: _Search_Alternative_Request): Search_Alternative_Request {
        let an_item = new Search_Alternative_Request()
        let new_dict = _general_from_dict_function(an_item, item)

        for (const key of Object.keys(new_dict)) {
            let value = new_dict[key]
            //@ts-ignore
            this[key] = value
            //@ts-ignore
            an_item[key] = value
        }

        return an_item
    }
}


export interface _Search_Alternative_Response {
    error: string | null;
    alternative_object_list: An_Object[] | null;
}

export class Search_Alternative_Response {
    error: string | null = null;
    alternative_object_list: An_Object[] | null = null;

    _property_name_to_its_type_dict = {
            error: "string",
            alternative_object_list: An_Object,
    };

    _key_string_dict = {
        error: "error",
        alternative_object_list: "alternative_object_list",
    };

    to_dict(): _Search_Alternative_Response {
        return _general_to_dict_function(this);
    }

    _clone(): Search_Alternative_Response {
        let clone = Object.assign(Object.create(Object.getPrototypeOf(this)), this)
        return clone
    }

    from_dict(item: _Search_Alternative_Response): Search_Alternative_Response {
        let an_item = new Search_Alternative_Response()
        let new_dict = _general_from_dict_function(an_item, item)

        for (const key of Object.keys(new_dict)) {
            let value = new_dict[key]
            //@ts-ignore
            this[key] = value
            //@ts-ignore
            an_item[key] = value
        }

        return an_item
    }
}


export interface _Get_an_object_Request {
    id: string | null;
    name: string | null;
}

export class Get_an_object_Request {
    id: string | null = null;
    name: string | null = null;

    _property_name_to_its_type_dict = {
            id: "string",
            name: "string",
    };

    _key_string_dict = {
        id: "id",
        name: "name",
    };

    to_dict(): _Get_an_object_Request {
        return _general_to_dict_function(this);
    }

    _clone(): Get_an_object_Request {
        let clone = Object.assign(Object.create(Object.getPrototypeOf(this)), this)
        return clone
    }

    from_dict(item: _Get_an_object_Request): Get_an_object_Request {
        let an_item = new Get_an_object_Request()
        let new_dict = _general_from_dict_function(an_item, item)

        for (const key of Object.keys(new_dict)) {
            let value = new_dict[key]
            //@ts-ignore
            this[key] = value
            //@ts-ignore
            an_item[key] = value
        }

        return an_item
    }
}


export interface _Get_an_object_Response {
    error: string | null;
    an_object: An_Object | null;
}

export class Get_an_object_Response {
    error: string | null = null;
    an_object: An_Object | null = null;

    _property_name_to_its_type_dict = {
            error: "string",
            an_object: An_Object,
    };

    _key_string_dict = {
        error: "error",
        an_object: "an_object",
    };

    to_dict(): _Get_an_object_Response {
        return _general_to_dict_function(this);
    }

    _clone(): Get_an_object_Response {
        let clone = Object.assign(Object.create(Object.getPrototypeOf(this)), this)
        return clone
    }

    from_dict(item: _Get_an_object_Response): Get_an_object_Response {
        let an_item = new Get_an_object_Response()
        let new_dict = _general_from_dict_function(an_item, item)

        for (const key of Object.keys(new_dict)) {
            let value = new_dict[key]
            //@ts-ignore
            this[key] = value
            //@ts-ignore
            an_item[key] = value
        }

        return an_item
    }
}


export interface _Add_Object_Request {
    an_object: An_Object | null;
}

export class Add_Object_Request {
    an_object: An_Object | null = null;

    _property_name_to_its_type_dict = {
            an_object: An_Object,
    };

    _key_string_dict = {
        an_object: "an_object",
    };

    to_dict(): _Add_Object_Request {
        return _general_to_dict_function(this);
    }

    _clone(): Add_Object_Request {
        let clone = Object.assign(Object.create(Object.getPrototypeOf(this)), this)
        return clone
    }

    from_dict(item: _Add_Object_Request): Add_Object_Request {
        let an_item = new Add_Object_Request()
        let new_dict = _general_from_dict_function(an_item, item)

        for (const key of Object.keys(new_dict)) {
            let value = new_dict[key]
            //@ts-ignore
            this[key] = value
            //@ts-ignore
            an_item[key] = value
        }

        return an_item
    }
}


export interface _Add_Object_Response {
    error: string | null;
    success: boolean | null;
}

export class Add_Object_Response {
    error: string | null = null;
    success: boolean | null = null;

    _property_name_to_its_type_dict = {
            error: "string",
            success: "boolean",
    };

    _key_string_dict = {
        error: "error",
        success: "success",
    };

    to_dict(): _Add_Object_Response {
        return _general_to_dict_function(this);
    }

    _clone(): Add_Object_Response {
        let clone = Object.assign(Object.create(Object.getPrototypeOf(this)), this)
        return clone
    }

    from_dict(item: _Add_Object_Response): Add_Object_Response {
        let an_item = new Add_Object_Response()
        let new_dict = _general_from_dict_function(an_item, item)

        for (const key of Object.keys(new_dict)) {
            let value = new_dict[key]
            //@ts-ignore
            this[key] = value
            //@ts-ignore
            an_item[key] = value
        }

        return an_item
    }
}


export interface _Update_Object_Request {
    an_object: An_Object | null;
}

export class Update_Object_Request {
    an_object: An_Object | null = null;

    _property_name_to_its_type_dict = {
            an_object: An_Object,
    };

    _key_string_dict = {
        an_object: "an_object",
    };

    to_dict(): _Update_Object_Request {
        return _general_to_dict_function(this);
    }

    _clone(): Update_Object_Request {
        let clone = Object.assign(Object.create(Object.getPrototypeOf(this)), this)
        return clone
    }

    from_dict(item: _Update_Object_Request): Update_Object_Request {
        let an_item = new Update_Object_Request()
        let new_dict = _general_from_dict_function(an_item, item)

        for (const key of Object.keys(new_dict)) {
            let value = new_dict[key]
            //@ts-ignore
            this[key] = value
            //@ts-ignore
            an_item[key] = value
        }

        return an_item
    }
}


export interface _Update_Object_Response {
    error: string | null;
    success: boolean | null;
}

export class Update_Object_Response {
    error: string | null = null;
    success: boolean | null = null;

    _property_name_to_its_type_dict = {
            error: "string",
            success: "boolean",
    };

    _key_string_dict = {
        error: "error",
        success: "success",
    };

    to_dict(): _Update_Object_Response {
        return _general_to_dict_function(this);
    }

    _clone(): Update_Object_Response {
        let clone = Object.assign(Object.create(Object.getPrototypeOf(this)), this)
        return clone
    }

    from_dict(item: _Update_Object_Response): Update_Object_Response {
        let an_item = new Update_Object_Response()
        let new_dict = _general_from_dict_function(an_item, item)

        for (const key of Object.keys(new_dict)) {
            let value = new_dict[key]
            //@ts-ignore
            this[key] = value
            //@ts-ignore
            an_item[key] = value
        }

        return an_item
    }
}


export interface _Delete_Object_Request {
    an_object: An_Object | null;
}

export class Delete_Object_Request {
    an_object: An_Object | null = null;

    _property_name_to_its_type_dict = {
            an_object: An_Object,
    };

    _key_string_dict = {
        an_object: "an_object",
    };

    to_dict(): _Delete_Object_Request {
        return _general_to_dict_function(this);
    }

    _clone(): Delete_Object_Request {
        let clone = Object.assign(Object.create(Object.getPrototypeOf(this)), this)
        return clone
    }

    from_dict(item: _Delete_Object_Request): Delete_Object_Request {
        let an_item = new Delete_Object_Request()
        let new_dict = _general_from_dict_function(an_item, item)

        for (const key of Object.keys(new_dict)) {
            let value = new_dict[key]
            //@ts-ignore
            this[key] = value
            //@ts-ignore
            an_item[key] = value
        }

        return an_item
    }
}


export interface _Delete_Object_Response {
    error: string | null;
    success: boolean | null;
}

export class Delete_Object_Response {
    error: string | null = null;
    success: boolean | null = null;

    _property_name_to_its_type_dict = {
            error: "string",
            success: "boolean",
    };

    _key_string_dict = {
        error: "error",
        success: "success",
    };

    to_dict(): _Delete_Object_Response {
        return _general_to_dict_function(this);
    }

    _clone(): Delete_Object_Response {
        let clone = Object.assign(Object.create(Object.getPrototypeOf(this)), this)
        return clone
    }

    from_dict(item: _Delete_Object_Response): Delete_Object_Response {
        let an_item = new Delete_Object_Response()
        let new_dict = _general_from_dict_function(an_item, item)

        for (const key of Object.keys(new_dict)) {
            let value = new_dict[key]
            //@ts-ignore
            this[key] = value
            //@ts-ignore
            an_item[key] = value
        }

        return an_item
    }
}