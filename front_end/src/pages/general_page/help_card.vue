<script setup lang="ts">
import { onMounted, reactive } from 'vue';
import { global_dict, global_functions } from '../../store'

var dict = reactive({
})

onMounted(async () => {
})
</script>

<template>
  <a-card class="w-full">
    <template v-if="!global_functions.is_english_language()">
      <p>Help Please! 紧急援助！</p>
      <p>网站主现在正在深圳流浪，吃饭都需要从垃圾桶捡，才能维持生活。并且找不到免费的洗衣服、洗澡的地方。</p>
      <p style="color: red"
        @click="global_dict.router.push('/contribution/')"
      >如有意向救助，请点击这里！</p>
    </template>
    <template v-if="global_functions.is_english_language()">
      <p>Help Please!</p>
      <p>I'm living in street now. I have to pick up food from trash cans to find food. And I can't find a place to wash clothes and take showers for free.</p>
      <p style="color: red"
        @click="global_dict.router.push('/contribution/')"
      >If you wanted to help, click here！</p>
    </template>
  </a-card>
</template>

<style scoped lang="less">
.help_card {
  .for_mobile({
    margin-bottom: 0px;
  });
}
</style>