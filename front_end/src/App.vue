<script setup lang="ts">
import { onMounted, reactive } from 'vue';
import { global_functions } from './store';

var dict = reactive({
})

onMounted(()=>{
  global_functions.reload_when_url_change()
})
</script>

<template>
  <router-view></router-view>
</template>

<style scoped lang="less">
</style>
