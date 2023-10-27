const _ygrpc_official_types = ["string", "number", "boolean"];

export const clone_object_ = (obj: any) =>  JSON.parse(JSON.stringify(obj));

export const get_secret_alphabet_dict_ = (a_secret_string: string) =>  {
    const ascii_lowercase = "abcdefghijklmnopqrstuvwxyz".split("")
    const number_0_to_9 = "0123456789".split("")

    var new_key = a_secret_string.replace(" ", "").toLowerCase().split("")
    var character_list: string[] = []
    for (var char of new_key) {
        if ((/[a-zA-Z]/).test(char)) {
            if (!character_list.includes(char)) {
                character_list.push(char)
            }
        }
    }

    if (character_list.length >= 26) {
        character_list = character_list.slice(0, 26)
    } else {
        var characters_that_the_key_didnt_cover: string[] = []
        for (var char of ascii_lowercase) {
            if (!character_list.includes(char)) {
                characters_that_the_key_didnt_cover.push(char)
            }
        }
        character_list = character_list.concat(characters_that_the_key_didnt_cover) 
    }

    var final_dict = {} as Record<string, string>

    // for alphabet
    for (let [index, char] of ascii_lowercase.entries()) {
        final_dict[char] = character_list[index]
    }

    // for numbers
    var original_numbers_in_alphabet_format = ascii_lowercase.slice(0, 10) // 0-9 representations in alphabet format
    var secret_numbers_in_alphabet_format = Object.values(final_dict).slice(0, 10)
    var final_number_list = [] as string[]
    for (var index in number_0_to_9) {
        var secret_char = secret_numbers_in_alphabet_format[index]
        if (original_numbers_in_alphabet_format.includes(secret_char)) {
            final_number_list.push(String(original_numbers_in_alphabet_format.findIndex((x) => x===secret_char)))
        }
    }
    if (final_number_list.length >= 10) {
        final_number_list = final_number_list.slice(0, 10)
    } else {
        var numbers_that_didnt_get_cover = [] as string[]
        for (var char of number_0_to_9) {
            if (!final_number_list.includes(char)) {
                numbers_that_didnt_get_cover.push(char)
            }
        }
        final_number_list = final_number_list.concat(numbers_that_didnt_get_cover)
    }
    for (let [index, char] of final_number_list.entries()) {
        final_dict[String(index)] = char
    }

    return final_dict
};

export const encode_message_ = (a_secret_dict: Record<string, string>, message: string):string => {
    var new_message = ""
    for (const char of message) {
        if ((!(/[a-zA-Z]/).test(char)) && (!(/^\d$/).test(char))) {
            new_message += char
            continue
        }
        var new_char = a_secret_dict[char.toLowerCase()]
        if ((/[A-Z]/).test(char)) {
            new_char = new_char.toUpperCase()
        }
        new_message += new_char
    }
    return new_message
}

export const decode_message_ = (a_secret_dict: Record<string, string>, message: string):string => {
    var new_secret_dict = {} as Record<string, string>
    for (var key of Object.keys(a_secret_dict)) {
        new_secret_dict[a_secret_dict[key]] = key
    }
    a_secret_dict = new_secret_dict

    var new_message = ""
    for (const char of message) {
        if ((!(/[a-zA-Z]/).test(char)) && (!(/^\d$/).test(char))) {
            new_message += char
            continue
        }
        var new_char = a_secret_dict[char.toLowerCase()]
        if ((/[A-Z]/).test(char)) {
            new_char = new_char.toUpperCase()
        }
        new_message += new_char
    }
    return new_message
}

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

export enum Sort_By {
    // yingshaoxo: I strongly recommend you use enum as a string type in other message data_model
    like = "like",
    dislike = "dislike",
}

export interface _A_User {
    id: string | null;
    create_time_in_10_numbers_timestamp_format: number | null;
    email: string | null;
    password: string | null;
    jwt: string | null;
    level: number | null;
    parent_email: string | null;
    children_email_list: string[] | null;
    invitation_counting: number | null;
    invitation_code_list: string[] | null;
    last_login_time_in_10_numbers_timestamp_format: number | null;
}

export class A_User {
    id: string | null = null;
    create_time_in_10_numbers_timestamp_format: number | null = null;
    email: string | null = null;
    password: string | null = null;
    jwt: string | null = null;
    level: number | null = null;
    parent_email: string | null = null;
    children_email_list: string[] | null = null;
    invitation_counting: number | null = null;
    invitation_code_list: string[] | null = null;
    last_login_time_in_10_numbers_timestamp_format: number | null = null;

    _property_name_to_its_type_dict = {
            id: "string",
            create_time_in_10_numbers_timestamp_format: "number",
            email: "string",
            password: "string",
            jwt: "string",
            level: "number",
            parent_email: "string",
            children_email_list: "string",
            invitation_counting: "number",
            invitation_code_list: "string",
            last_login_time_in_10_numbers_timestamp_format: "number",
    };

    _key_string_dict = {
        id: "id",
        create_time_in_10_numbers_timestamp_format: "create_time_in_10_numbers_timestamp_format",
        email: "email",
        password: "password",
        jwt: "jwt",
        level: "level",
        parent_email: "parent_email",
        children_email_list: "children_email_list",
        invitation_counting: "invitation_counting",
        invitation_code_list: "invitation_code_list",
        last_login_time_in_10_numbers_timestamp_format: "last_login_time_in_10_numbers_timestamp_format",
    };

    /*
    constructor(id: string | null = null, create_time_in_10_numbers_timestamp_format: number | null = null, email: string | null = null, password: string | null = null, jwt: string | null = null, level: number | null = null, parent_email: string | null = null, children_email_list: string[] | null = null, invitation_counting: number | null = null, invitation_code_list: string[] | null = null, last_login_time_in_10_numbers_timestamp_format: number | null = null) {
            this.id = id
            this.create_time_in_10_numbers_timestamp_format = create_time_in_10_numbers_timestamp_format
            this.email = email
            this.password = password
            this.jwt = jwt
            this.level = level
            this.parent_email = parent_email
            this.children_email_list = children_email_list
            this.invitation_counting = invitation_counting
            this.invitation_code_list = invitation_code_list
            this.last_login_time_in_10_numbers_timestamp_format = last_login_time_in_10_numbers_timestamp_format
    }
    */

    to_dict(): _A_User {
        return _general_to_dict_function(this);
    }

    _clone(): A_User {
        let clone = Object.assign(Object.create(Object.getPrototypeOf(this)), this)
        return clone
    }

    from_dict(item: _A_User): A_User {
        let an_item = new A_User()
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


export interface _An_Object {
    id: string | null;
    name: string | null;
    description: string | null;
    level: number | null;
    likes: number | null;
    dislikes: number | null;
    alternative_id_list: string[] | null;
    create_time_in_10_numbers_timestamp_format: number | null;
    update_time_in_10_numbers_timestamp_format: number | null;
}

export class An_Object {
    id: string | null = null;
    name: string | null = null;
    description: string | null = null;
    level: number | null = null;
    likes: number | null = null;
    dislikes: number | null = null;
    alternative_id_list: string[] | null = null;
    create_time_in_10_numbers_timestamp_format: number | null = null;
    update_time_in_10_numbers_timestamp_format: number | null = null;

    _property_name_to_its_type_dict = {
            id: "string",
            name: "string",
            description: "string",
            level: "number",
            likes: "number",
            dislikes: "number",
            alternative_id_list: "string",
            create_time_in_10_numbers_timestamp_format: "number",
            update_time_in_10_numbers_timestamp_format: "number",
    };

    _key_string_dict = {
        id: "id",
        name: "name",
        description: "description",
        level: "level",
        likes: "likes",
        dislikes: "dislikes",
        alternative_id_list: "alternative_id_list",
        create_time_in_10_numbers_timestamp_format: "create_time_in_10_numbers_timestamp_format",
        update_time_in_10_numbers_timestamp_format: "update_time_in_10_numbers_timestamp_format",
    };

    /*
    constructor(id: string | null = null, name: string | null = null, description: string | null = null, level: number | null = null, likes: number | null = null, dislikes: number | null = null, alternative_id_list: string[] | null = null, create_time_in_10_numbers_timestamp_format: number | null = null, update_time_in_10_numbers_timestamp_format: number | null = null) {
            this.id = id
            this.name = name
            this.description = description
            this.level = level
            this.likes = likes
            this.dislikes = dislikes
            this.alternative_id_list = alternative_id_list
            this.create_time_in_10_numbers_timestamp_format = create_time_in_10_numbers_timestamp_format
            this.update_time_in_10_numbers_timestamp_format = update_time_in_10_numbers_timestamp_format
    }
    */

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


export interface _Get_Special_JWT_Request {
    email: string | null;
    password: string | null;
    invitation_code: string | null;
}

export class Get_Special_JWT_Request {
    email: string | null = null;
    password: string | null = null;
    invitation_code: string | null = null;

    _property_name_to_its_type_dict = {
            email: "string",
            password: "string",
            invitation_code: "string",
    };

    _key_string_dict = {
        email: "email",
        password: "password",
        invitation_code: "invitation_code",
    };

    /*
    constructor(email: string | null = null, password: string | null = null, invitation_code: string | null = null) {
            this.email = email
            this.password = password
            this.invitation_code = invitation_code
    }
    */

    to_dict(): _Get_Special_JWT_Request {
        return _general_to_dict_function(this);
    }

    _clone(): Get_Special_JWT_Request {
        let clone = Object.assign(Object.create(Object.getPrototypeOf(this)), this)
        return clone
    }

    from_dict(item: _Get_Special_JWT_Request): Get_Special_JWT_Request {
        let an_item = new Get_Special_JWT_Request()
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


export interface _Get_Special_JWT_Response {
    error: string | null;
    encrypted_jwt: string | null;
}

export class Get_Special_JWT_Response {
    error: string | null = null;
    encrypted_jwt: string | null = null;

    _property_name_to_its_type_dict = {
            error: "string",
            encrypted_jwt: "string",
    };

    _key_string_dict = {
        error: "error",
        encrypted_jwt: "encrypted_jwt",
    };

    /*
    constructor(error: string | null = null, encrypted_jwt: string | null = null) {
            this.error = error
            this.encrypted_jwt = encrypted_jwt
    }
    */

    to_dict(): _Get_Special_JWT_Response {
        return _general_to_dict_function(this);
    }

    _clone(): Get_Special_JWT_Response {
        let clone = Object.assign(Object.create(Object.getPrototypeOf(this)), this)
        return clone
    }

    from_dict(item: _Get_Special_JWT_Response): Get_Special_JWT_Response {
        let an_item = new Get_Special_JWT_Response()
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


export interface _is_JWT_ok_Request {
    jwt: string | null;
}

export class is_JWT_ok_Request {
    jwt: string | null = null;

    _property_name_to_its_type_dict = {
            jwt: "string",
    };

    _key_string_dict = {
        jwt: "jwt",
    };

    /*
    constructor(jwt: string | null = null) {
            this.jwt = jwt
    }
    */

    to_dict(): _is_JWT_ok_Request {
        return _general_to_dict_function(this);
    }

    _clone(): is_JWT_ok_Request {
        let clone = Object.assign(Object.create(Object.getPrototypeOf(this)), this)
        return clone
    }

    from_dict(item: _is_JWT_ok_Request): is_JWT_ok_Request {
        let an_item = new is_JWT_ok_Request()
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


export interface _is_JWT_ok_Response {
    error: string | null;
    ok: boolean | null;
    is_admin: boolean | null;
}

export class is_JWT_ok_Response {
    error: string | null = null;
    ok: boolean | null = null;
    is_admin: boolean | null = null;

    _property_name_to_its_type_dict = {
            error: "string",
            ok: "boolean",
            is_admin: "boolean",
    };

    _key_string_dict = {
        error: "error",
        ok: "ok",
        is_admin: "is_admin",
    };

    /*
    constructor(error: string | null = null, ok: boolean | null = null, is_admin: boolean | null = null) {
            this.error = error
            this.ok = ok
            this.is_admin = is_admin
    }
    */

    to_dict(): _is_JWT_ok_Response {
        return _general_to_dict_function(this);
    }

    _clone(): is_JWT_ok_Response {
        let clone = Object.assign(Object.create(Object.getPrototypeOf(this)), this)
        return clone
    }

    from_dict(item: _is_JWT_ok_Response): is_JWT_ok_Response {
        let an_item = new is_JWT_ok_Response()
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


export interface _Get_invitation_code_request {

}

export class Get_invitation_code_request {


    _property_name_to_its_type_dict = {

    };

    _key_string_dict = {

    };

    /*
    constructor() {

    }
    */

    to_dict(): _Get_invitation_code_request {
        return _general_to_dict_function(this);
    }

    _clone(): Get_invitation_code_request {
        let clone = Object.assign(Object.create(Object.getPrototypeOf(this)), this)
        return clone
    }

    from_dict(item: _Get_invitation_code_request): Get_invitation_code_request {
        let an_item = new Get_invitation_code_request()
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


export interface _Get_invitation_code_response {
    error: string | null;
    invitation_code: string | null;
}

export class Get_invitation_code_response {
    error: string | null = null;
    invitation_code: string | null = null;

    _property_name_to_its_type_dict = {
            error: "string",
            invitation_code: "string",
    };

    _key_string_dict = {
        error: "error",
        invitation_code: "invitation_code",
    };

    /*
    constructor(error: string | null = null, invitation_code: string | null = null) {
            this.error = error
            this.invitation_code = invitation_code
    }
    */

    to_dict(): _Get_invitation_code_response {
        return _general_to_dict_function(this);
    }

    _clone(): Get_invitation_code_response {
        let clone = Object.assign(Object.create(Object.getPrototypeOf(this)), this)
        return clone
    }

    from_dict(item: _Get_invitation_code_response): Get_invitation_code_response {
        let an_item = new Get_invitation_code_response()
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

    /*
    constructor(key_words: string | null = null, keywords_of_name: string | null = null, keywords_of_description: string | null = null, sort_by: Sort_By | null = null, page_size: number | null = null, page_number: number | null = null) {
            this.key_words = key_words
            this.keywords_of_name = keywords_of_name
            this.keywords_of_description = keywords_of_description
            this.sort_by = sort_by
            this.page_size = page_size
            this.page_number = page_number
    }
    */

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

    /*
    constructor(error: string | null = null, alternative_object_list: An_Object[] | null = null) {
            this.error = error
            this.alternative_object_list = alternative_object_list
    }
    */

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

    /*
    constructor(id: string | null = null, name: string | null = null) {
            this.id = id
            this.name = name
    }
    */

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

    /*
    constructor(error: string | null = null, an_object: An_Object | null = null) {
            this.error = error
            this.an_object = an_object
    }
    */

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

    /*
    constructor(an_object: An_Object | null = null) {
            this.an_object = an_object
    }
    */

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

    /*
    constructor(error: string | null = null, success: boolean | null = null) {
            this.error = error
            this.success = success
    }
    */

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

    /*
    constructor(an_object: An_Object | null = null) {
            this.an_object = an_object
    }
    */

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

    /*
    constructor(error: string | null = null, success: boolean | null = null) {
            this.error = error
            this.success = success
    }
    */

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

    /*
    constructor(an_object: An_Object | null = null) {
            this.an_object = an_object
    }
    */

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

    /*
    constructor(error: string | null = null, success: boolean | null = null) {
            this.error = error
            this.success = success
    }
    */

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


export interface _Download_backup_data_request {

}

export class Download_backup_data_request {


    _property_name_to_its_type_dict = {

    };

    _key_string_dict = {

    };

    /*
    constructor() {

    }
    */

    to_dict(): _Download_backup_data_request {
        return _general_to_dict_function(this);
    }

    _clone(): Download_backup_data_request {
        let clone = Object.assign(Object.create(Object.getPrototypeOf(this)), this)
        return clone
    }

    from_dict(item: _Download_backup_data_request): Download_backup_data_request {
        let an_item = new Download_backup_data_request()
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


export interface _Download_backup_data_response {
    error: string | null;
    file_name: string | null;
    file_bytes_in_base64_format: string | null;
}

export class Download_backup_data_response {
    error: string | null = null;
    file_name: string | null = null;
    file_bytes_in_base64_format: string | null = null;

    _property_name_to_its_type_dict = {
            error: "string",
            file_name: "string",
            file_bytes_in_base64_format: "string",
    };

    _key_string_dict = {
        error: "error",
        file_name: "file_name",
        file_bytes_in_base64_format: "file_bytes_in_base64_format",
    };

    /*
    constructor(error: string | null = null, file_name: string | null = null, file_bytes_in_base64_format: string | null = null) {
            this.error = error
            this.file_name = file_name
            this.file_bytes_in_base64_format = file_bytes_in_base64_format
    }
    */

    to_dict(): _Download_backup_data_response {
        return _general_to_dict_function(this);
    }

    _clone(): Download_backup_data_response {
        let clone = Object.assign(Object.create(Object.getPrototypeOf(this)), this)
        return clone
    }

    from_dict(item: _Download_backup_data_response): Download_backup_data_response {
        let an_item = new Download_backup_data_response()
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


export interface _Upload_backup_data_request {
    file_bytes_in_base64_format: string | null;
}

export class Upload_backup_data_request {
    file_bytes_in_base64_format: string | null = null;

    _property_name_to_its_type_dict = {
            file_bytes_in_base64_format: "string",
    };

    _key_string_dict = {
        file_bytes_in_base64_format: "file_bytes_in_base64_format",
    };

    /*
    constructor(file_bytes_in_base64_format: string | null = null) {
            this.file_bytes_in_base64_format = file_bytes_in_base64_format
    }
    */

    to_dict(): _Upload_backup_data_request {
        return _general_to_dict_function(this);
    }

    _clone(): Upload_backup_data_request {
        let clone = Object.assign(Object.create(Object.getPrototypeOf(this)), this)
        return clone
    }

    from_dict(item: _Upload_backup_data_request): Upload_backup_data_request {
        let an_item = new Upload_backup_data_request()
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


export interface _Upload_backup_data_response {
    error: string | null;
    success: boolean | null;
}

export class Upload_backup_data_response {
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

    /*
    constructor(error: string | null = null, success: boolean | null = null) {
            this.error = error
            this.success = success
    }
    */

    to_dict(): _Upload_backup_data_response {
        return _general_to_dict_function(this);
    }

    _clone(): Upload_backup_data_response {
        let clone = Object.assign(Object.create(Object.getPrototypeOf(this)), this)
        return clone
    }

    from_dict(item: _Upload_backup_data_response): Upload_backup_data_response {
        let an_item = new Upload_backup_data_response()
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