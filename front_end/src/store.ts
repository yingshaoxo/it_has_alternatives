import { computed, reactive, watch } from 'vue'
import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
import { createI18n, useI18n } from 'vue-i18n'

import { notification } from 'ant-design-vue';

import admin_main_search_page from './pages/admin_page/main_search_page.vue'
import admin_one_object_page from './pages/admin_page/one_object_page.vue'
import admin_contribution_page from './pages/admin_page/contribution_page.vue'

import visitor_main_search_page from './pages/visitor_page/main_search_page.vue'
import visitor_one_object_page from './pages/visitor_page/one_object_page.vue'
import visitor_contribution_page from './pages/visitor_page/contribution_page.vue'

import * as it_has_alternatives_rpc from './generated_yrpc/it_has_alternatives_rpc'
import * as it_has_alternatives_objects from './generated_yrpc/it_has_alternatives_objects'

import en from './locales/en.json'
import sc from './locales/sc.json'

const routes: RouteRecordRaw[] = [
  { path: '/', component: visitor_main_search_page },
  { path: '/object/:name', component: visitor_one_object_page },
  { path: '/contribution/', component: visitor_contribution_page },

  { path: '/admin', component: admin_main_search_page },
  { path: '/admin/object/:name', component: admin_one_object_page },
  { path: '/admin/contribution/', component: admin_contribution_page },
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

export var global_dict = reactive({
    router,
    visitor_client: new it_has_alternatives_rpc.Client_it_has_alternatives(
            "https://alternatives.ai-tools-online.xyz", 
            {
            }, 
            (error_string: string)=>{
                console.log(error_string)
                notification.open({
                    message: 'error',
                    description:
                        error_string,
                    onClick: () => {
                        // console.log('Notification Clicked!');
                    }
                })
            }
    ),
    admin_client: computed(() => {
        var a_client = new it_has_alternatives_rpc.Client_it_has_alternatives(
            "https://admin_alternatives.ai-tools-online.xyz", 
            {
                "jwt": localStorage.getItem("jwt")??""
            }, 
            (error_string: string)=>{
                console.log(error_string)
                notification.open({
                    message: 'error',
                    description:
                        error_string,
                    onClick: () => {
                        // console.log('Notification Clicked!');
                    }
                })
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
    last_url: "",
    special_secret_dict: it_has_alternatives_objects.get_secret_alphabet_dict_("Asking is not a bad thing if the person you ask are comfortable with it.")
})

export var global_functions = {
    init: () => {
        global_dict.t = useI18n().t
        global_dict.locale = useI18n().locale 
        global_dict.availableLocales = useI18n().availableLocales 
        // global_dict.locale = "sc"

        var the_locale_in_disk = localStorage.getItem("locale")
        if (the_locale_in_disk) {
            global_dict.locale = the_locale_in_disk
        }

        watch(useI18n().locale, (new_locale: any) => {
            console.log(new_locale)
            localStorage.setItem("locale", new_locale)
        });
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
    is_en_broswer: ():boolean => {
        let language = window.navigator.language;
        if (language.startsWith("en-")) {
            return true;
        }
        return false;
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
    login: async (request: it_has_alternatives_objects.Get_Special_JWT_Request):Promise<boolean> => {
        var request = new it_has_alternatives_objects.Get_Special_JWT_Request().from_dict(request.to_dict())
        request.email = it_has_alternatives_objects.encode_message_(global_dict.special_secret_dict, request.email??"") 
        request.password =  it_has_alternatives_objects.encode_message_(global_dict.special_secret_dict, request.password??"")
        const response = await global_dict.visitor_client.get_special_jwt(request)
        if (response?.encrypted_jwt) {
            localStorage.setItem("jwt", response.encrypted_jwt)
            return true
        }
        return false
    },
    print: (item: any) => {
        console.log(item)
    }
}

export default {
    global_dict, 
    global_functions
}