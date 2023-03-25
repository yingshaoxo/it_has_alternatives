import { createApp } from 'vue'
import './style.css'
import App from './App.vue'

import { createRouter, createWebHistory } from 'vue-router'
import main_search_pageVue from './main_search_page.vue'
import one_object_pageVue from './one_object_page.vue'

const routes = [
  { path: '/', component: main_search_pageVue },
  { path: '/:name', component: one_object_pageVue },
]

const router = createRouter({
  history: createWebHistory(),
  routes: routes, 
})

createApp(App)
.use(router)
.mount('#app')
