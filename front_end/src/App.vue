<script setup lang="ts">
import { onBeforeMount, onMounted, reactive } from 'vue';
import { global_functions } from './store';

import { notification } from 'ant-design-vue';

var dict = reactive({
})

onBeforeMount(() => {
  global_functions.init()
  global_functions.reload_when_url_change()

  global_functions.print = (message: string) => {
    console.log(message)
    notification.open({
        message: null,
        description: message,
        duration: 0,
        onClick: () => {
            // console.log('Notification Clicked!');
        }
    })
  }
})

onMounted(()=>{
})
</script>

<template>
  <router-view></router-view>
</template>

<style scoped lang="less">
</style>
