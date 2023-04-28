<script setup lang="ts">
import { onMounted, reactive } from 'vue';
import { global_dict, global_functions } from '../../store'

var dict = reactive({
})

onMounted(async () => {
})
</script>

<template>
  <div class="bottom-[0px] selection">
    <select v-model="global_dict.locale"
      class="text-center border border-gray-300 rounded-full text-gray-600 h-10 px-5 bg-white hover:border-gray-400 focus:outline-none appearance-none"
    >
      <option 
        v-for="locale in global_dict.availableLocales" :key="`locale-${locale}`" :value="locale"
      >
        {{ 
          //@ts-ignore
          global_dict.availableLocales_dict[locale] 
        }}
      </option>
    </select>
  </div>
</template>

<style scoped lang="less">
.selection {
  margin-bottom: 10px !important;
}
</style>