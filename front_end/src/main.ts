import { createApp } from 'vue'
import './style.css'
import App from './App.vue'

import { global_dict, global_functions, i18n } from './store'

createApp(App)
.use(i18n)
.use(global_dict.router)
.mount('#app')
