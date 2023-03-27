import { reactive } from 'vue'
import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
import main_search_pageVue from './main_search_page.vue'
import one_object_pageVue from './one_object_page.vue'
import contribution_pageVue from './contribution_page.vue'

const routes: RouteRecordRaw[] = [
  { path: '/', component: main_search_pageVue },
  { path: '/object/:name', component: one_object_pageVue },
  { path: '/contribution/', component: contribution_pageVue },
]

const router = createRouter({
  history: createWebHistory(),
  routes: routes, 
})

export var global_dict = reactive({
    router,
    last_url: ""
})

export var global_functions = {
    reload_when_url_change: () => {
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
}

export default {
    global_dict, 
    global_functions
}