<script setup lang="ts">
import { onMounted, reactive } from 'vue';
import contribution_cn from './components/contribution_cn.vue';
import contribution_en from './components/contribution_en.vue';

import { global_dict, global_functions } from './store'

var dict = reactive({
  component_list: [] as any[]
})

onMounted(async () => {
  if (global_functions.is_en_broswer()) {
    dict.component_list = [
      contribution_en, contribution_cn
    ]
  } else {
    dict.component_list = [
      contribution_cn, contribution_en
    ]
  }
})
</script>

<template>
  <div class="flex flex-col place-content-center place-items-center">
    <div class="container_css max-w-[1366px] px-[16px]"
      v-if="dict.component_list.length > 0"
    >
      <!-- 
        Three products: Nudle, Shaqima, Server Fee 
        AD & consult contact: yingshaoxo@gmail.com || twitter @yingshaoxo || 17508265307 
      -->

      <div class="h-[30px]"></div>

      <component v-bind:is="dict.component_list[0]"></component>
      
      <div class="h-[50px]"></div>
      <a-divider style="height: 0.5px; background-color: rgba(124, 179, 5, 0.5)" />
      <div class="h-[50px]"></div>

      <component v-bind:is="dict.component_list[1]"></component>

      <div class="h-[30px]"></div>
    </div>
  </div>
</template>

<style scoped lang="less">
</style>