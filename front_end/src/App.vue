<script setup lang="ts">
import { onBeforeMount, onMounted, reactive, watch } from 'vue';
import { global_dict, global_functions } from './store';

import { message, notification } from 'ant-design-vue';

var dict = reactive({
})

onBeforeMount(() => {
  global_functions.init()
  global_functions.reload_when_url_change()

  global_functions.print = (msg: string) => {
    console.log(msg)
    notification.open({
        message: null,
        description: msg,
        duration: 5,
        style: {
          // whiteSpace: 'pre',
          zIndex: 999
        },
        onClick: () => {
            // console.log('Notification Clicked!');
        }
    })
  }
})

onMounted(()=>{
  // global_functions.print(global_dict.locale)
})
</script>

<template>
  <div class="global_loading" v-if="global_dict.show_global_loading">
    <a-spin size="large" />
  </div>

  <a-config-provider :locale="global_dict.ant_design_locale"
  >
    <router-view
        v-if="!global_dict.show_global_loading"
    ></router-view>

    <a-modal
        v-if="!global_dict.show_global_loading"
        v-model:visible="global_dict.login_dialog_visible"
        :title="global_dict.t(`Login`) + '/' + global_dict.t(`Register`)"
        :cancelText="global_dict.t('Cancel')"
        :okText="global_dict.t('Ok')"
        style="top: 20px"
        :zIndex="500"
        :closable="false"
        :maskClosable="false"
        :cancelButtonProps="{
          disabled: true
        }"
        @ok="async ()=>{
          var ok = await global_functions.login(global_dict.login_request) 
          //@ts-ignore
          if (ok) {  
            global_dict.login_dialog_visible=false
            global_functions.refresh()
          }
        }"
      >
      <div class="space-y-[16px]">
        <a-input :placeholder="global_functions.make_first_character_upper_case(global_dict.login_request._key_string_dict.email)" v-model:value="global_dict.login_request.email" type="email" />
        <a-input :placeholder="global_functions.make_first_character_upper_case(global_dict.login_request._key_string_dict.password)" v-model:value="global_dict.login_request.password" type="password" />
        <a-input :placeholder="global_functions.make_first_character_upper_case(global_dict.login_request._key_string_dict.invitation_code)" v-model:value="global_dict.login_request.invitation_code" />
      </div>
    </a-modal>
  </a-config-provider>
</template>

<style scoped lang="less">
</style>

<style>
.ant-notification .ant-notification-notice .ant-notification-notice-closable {
  z-index: 999;
}

.global_loading {
  z-index: 666;
  position: absolute;
  margin: 0;
  padding: 0;
  left: 0;
  top: 0;
  
  width: 100vw;
  height: 100%;
  min-height: 100vh;
  /*
  background-color: rgba(0, 0, 0, 0.6);
  */
  background-color: rgba(255, 255, 255, 1);

  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  align-content: center;
}

/* 
.prose {
  color: black !important;
} */
</style>
