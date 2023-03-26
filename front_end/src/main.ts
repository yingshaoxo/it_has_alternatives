import { createApp } from 'vue'
import './style.css'
import App from './App.vue'

import { global_dict } from './store'


createApp(App)
.use(global_dict.router)
.mount('#app')
