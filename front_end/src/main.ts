import { createApp } from 'vue'

// old ie does not have fetch, that's why you use 'isomorphic-fetch' to let it support it
import * as e6p from "es6-promise";
(e6p as any).polyfill();
import 'isomorphic-fetch';

import './style.css'
import App from './App.vue'

import Antd from 'ant-design-vue';
import 'ant-design-vue/dist/antd.css';

import { global_dict, global_functions, i18n } from './store'

createApp(App)
.use(Antd)
.use(i18n)
.use(global_dict.router)
.mount('#app')
