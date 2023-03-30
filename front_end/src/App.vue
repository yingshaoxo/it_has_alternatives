<script setup lang="ts">
import { onBeforeMount, onMounted, reactive } from 'vue';
import { global_functions } from './store';

var dict = reactive({
})

onBeforeMount(() => {
  global_functions.init()
  global_functions.reload_when_url_change()
})

onMounted(()=>{
})
</script>

<template>
  <router-view></router-view>
</template>

<style scoped lang="less">
</style>
