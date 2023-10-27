import { computed, reactive, watch } from 'vue'
import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
import { createI18n, useI18n } from 'vue-i18n'

import contribution_page from './pages/general_page/contribution_page.vue'

import visitor_main_search_page from './pages/visitor_page/main_search_page.vue'
import visitor_one_object_page from './pages/visitor_page/one_object_page.vue'

import user_main_search_page from './pages/user_page/main_search_page.vue'
import user_one_object_page from './pages/user_page/one_object_page.vue'

import admin_page from './pages/admin_page/admin_page.vue'

import * as it_has_alternatives_rpc from './generated_yrpc/it_has_alternatives_rpc'
import * as it_has_alternatives_objects from './generated_yrpc/it_has_alternatives_objects'

import en from './locales/en.json'
import sc from './locales/sc.json'

import zh_CN from 'ant-design-vue/es/locale/zh_CN';
import en_US from 'ant-design-vue/es/locale/en_US';
import dayjs from 'dayjs';
import 'dayjs/locale/zh-cn';
import 'dayjs/locale/en';

const routes: RouteRecordRaw[] = [
  { path: '/', component: visitor_main_search_page },
  { path: '/object/:name', component: visitor_one_object_page },
  { path: '/contribution/', component: contribution_page },

  { path: '/user', component: user_main_search_page },
  { path: '/user/object/:name', component: user_one_object_page },

  { path: '/admin', component: admin_page },
]

const router = createRouter({
  history: createWebHistory(),
  routes: routes, 
})

export const i18n = createI18n({
  legacy: false,
  locale: 'en',
  fallbackLocale: 'en', 
  messages: {
      en,
      sc,
  }
  // messages: {
  //   en: {
  //       hello: '{msg} world'
  //   },
  //   cn: {
  //       hello: '{msg} 世界'
  //   },
  //   //$t('message.hello', { msg: 'hello' })
  // },
})

const interceptor_function = (data: any) => {
    if (Object.keys(data).includes('error')) {
        if (data?.error) {
            global_functions.print(data?.error)
        }
    } else {
        if (data) {
            if (typeof data === 'string') {
                if (data.trim() != "") {
                    global_functions.print(data)
                }
            }
        }
    }
}

let get_host_url = (sub_domain: string) => {
    return `http://127.0.0.1:5551/${sub_domain}`
}
if (import.meta.env.DEV) {
    get_host_url = (sub_domain: string) => {
        return `http://127.0.0.1:5551/${sub_domain}`
    }
} else {
    get_host_url = (sub_domain: string) => {
        return `${window.location.protocol}//${window.location.host}/${sub_domain}`
    }
}

export var global_dict = reactive({
    router,
    visitor_client: new it_has_alternatives_rpc.Client_it_has_alternatives(
            get_host_url(""),
            {
            }, 
            (error_string: string)=>{
                global_functions.print(error_string)
            },
            (data: any)=>{
                interceptor_function(data)
            }
    ),
    user_client: new it_has_alternatives_rpc.Client_it_has_alternatives(
            get_host_url("user"),
            {
                "jwt": localStorage.getItem("jwt")??""
            }, 
            (error_string: string)=>{
                global_functions.print(error_string)
            },
            (data: any)=>{
                interceptor_function(data)
            }
    ),
    admin_client: computed(() => {
        var a_client = new it_has_alternatives_rpc.Client_it_has_alternatives(
            get_host_url("admin"),
            {
                "jwt": localStorage.getItem("jwt")??""
            }, 
            (error_string: string)=>{
                global_functions.print(error_string)
            },
            (data: any)=>{
                interceptor_function(data)
            }
        )
        return a_client
    }),
    t: {} as any,
    locale: {} as any,
    availableLocales: {} as any,
    availableLocales_dict: {
        "en": "English",
        "sc": "中文"
    },
    ant_design_locale: en_US,
    last_url: "",
    special_secret_dict: it_has_alternatives_objects.get_secret_alphabet_dict_("Asking is not a bad thing if the person you ask are comfortable with it."),
    login_dialog_visible: false,
    login_request: new it_has_alternatives_objects.Get_Special_JWT_Request(),
})

export var global_functions = {
    init: () => {
        global_dict.t = useI18n().t
        global_dict.locale = useI18n().locale 
        global_dict.availableLocales = useI18n().availableLocales 

        var the_locale_in_disk = localStorage.getItem("locale")
        if (the_locale_in_disk) {
            global_dict.locale = the_locale_in_disk
        } else {
            if (global_functions.is_en_broswer()) {
                global_dict.locale = "en"
            } else {
                global_dict.locale = "sc"
            }
        }

        var switch_ant_design_language = () => {
            if (global_dict.locale == "sc") {
                dayjs.locale('zh-cn');
                global_dict.ant_design_locale = zh_CN
            } else {
                dayjs.locale('en');
                global_dict.ant_design_locale = en_US
            }
        }
        switch_ant_design_language()

        watch(useI18n().locale, (new_locale: any) => {
            console.log(new_locale)
            localStorage.setItem("locale", new_locale)

            switch_ant_design_language()
        });
    },
    log: (message:any) => {
        console.log(message)
    },
    print: (message: any) => {
        // I'll define this function in App.vue
    },
    make_first_character_upper_case: (text: any) => {
        return text.charAt(0).toUpperCase() + text.slice(1);
    },
    copy_text_to_clipboard: async (text: string) => {
        try {
            var input = document.createElement('textarea');
            input.innerHTML = text;
            document.body.appendChild(input);
            input.select();
            var result = document.execCommand('copy');
            document.body.removeChild(input);
        } catch (e) {
            await navigator.clipboard.writeText(text);
        }
    },
    refresh: () => {
        window.location.reload();
    },
    reload_when_url_change: () => {
        return;
        var check_url_change_function = () => {
            setTimeout(()=>{
                var current_url = window.location.href
                // console.log("url_changed: ", global_dict.last_url, current_url)

                var old_data = localStorage.getItem("global_dict")
                if (old_data != null) {
                    var old_global_dict = JSON.parse(old_data) 
                    if (current_url != old_global_dict.last_url) {
                        window.location.reload();
                    }
                }

                global_dict.last_url = current_url
                localStorage.setItem("global_dict", JSON.stringify(global_dict))
            }, 200)
        }

        document.body.addEventListener('click', ()=>{
            check_url_change_function()
        }, true);

        window.addEventListener('popstate', function (event) {
            check_url_change_function()
        });
    },
    get_current_url: (): string => {
        return window.location.href
    },
    is_en_broswer: ():boolean => {
        let language = window.navigator.language;
        if (language.startsWith("en-")) {
            return true;
        }
        return false;
    },
    is_english_language: ():boolean => {
        return global_dict.locale == "en"
    },
    is_user: async ():Promise<boolean> => {
        var jwt_string = localStorage.getItem("jwt")
        if (jwt_string == null) {
            return false
        } else {
            var request = new it_has_alternatives_objects.is_JWT_ok_Request()
            request.jwt = jwt_string
            const response = await global_dict.visitor_client.is_jwt_ok(request)
            if (response?.ok == true) {
                return true
            }
            return false
        }
    },
    show_dialog_if_it_is_not_user: async () => {
        var is_user = await global_functions.is_user()
        if (is_user == false) {
            global_dict.login_dialog_visible = true
        }
    },
    login: async (request: it_has_alternatives_objects.Get_Special_JWT_Request):Promise<boolean> => {
        var request = new it_has_alternatives_objects.Get_Special_JWT_Request().from_dict(request.to_dict())
        request.email = it_has_alternatives_objects.encode_message_(global_dict.special_secret_dict, (request.email??"").trim()) 
        request.password =  it_has_alternatives_objects.encode_message_(global_dict.special_secret_dict, (request.password??"").trim())
        const response = await global_dict.visitor_client.get_special_jwt(request)
        if (response?.encrypted_jwt) {
            localStorage.setItem("jwt", response.encrypted_jwt)
            return true
        }
        return false
    },
    redirect_to_user_home_page_if_jwt_is_valid: async () => {
        var jwt_string = localStorage.getItem("jwt")
        if (jwt_string == null) {
        } else {
            var request = new it_has_alternatives_objects.is_JWT_ok_Request()
            request.jwt = jwt_string
            const response = await global_dict.visitor_client.is_jwt_ok(request, true)
            if (response?.ok == true) {
                router.push('/user')
            }
        }
    },
}

export default {
    global_dict, 
    global_functions
}
