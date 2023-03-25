<script setup lang="ts">
import { useRoute } from 'vue-router';

import { onMounted, reactive, ref, UnwrapRef } from 'vue';
import { PlusOutlined, SearchOutlined, CheckOutlined, EditOutlined } from '@ant-design/icons-vue';

import * as it_has_alternatives_objects from './generated_yrpc/it_has_alternatives_objects'
import * as it_has_alternatives_rpc from './generated_yrpc/it_has_alternatives_rpc'

var route = useRoute()

var clone_object = (obj: any) =>  JSON.parse(JSON.stringify(obj));

const dict = reactive({
  client: new it_has_alternatives_rpc.Client_it_has_alternatives("http://127.0.0.1:80"),
  object_name: "",
  object: new it_has_alternatives_objects.An_Object()
})

const functions = {
  get_one_object: async (object_name: string): Promise<it_has_alternatives_objects.An_Object | null> => {
    var request = new it_has_alternatives_objects.Search_Alternative_Request()
    request.key_words = object_name
    request.page_number = 0
    request.page_size = 3
    var result = await dict.client.search_alternatives(
      request
    )
    var result_object_list = result?.alternative_object_list ?? []
    if (result_object_list.length > 0) {
      return result_object_list[0]
    } else {
      return null
    }
  },
}

onMounted(async () => {
  if (Array.isArray(route.params?.name)) {
    dict.object_name = route.params?.name[0]
  } else {
    dict.object_name = route.params?.name??""
  }

  dict.object = await functions.get_one_object(dict.object_name)?? new it_has_alternatives_objects.An_Object()
})
</script>

<template>
  <div class="flex flex-row justify-center">
    <div class="container_css max-w-[1366px]">
      <div class="px-[0px]">
        <div class="flex flex-row justify-start mb-[20px]">
          <div class="main_item_icon_css w-[148px] h-[148px]" style="background-color: rgba(124, 179, 5, 0.5);"></div>
          <div class="ml-[20px] flex flex-col justify-between">
            <div class="main_item_title_css">
                {{ dict.object_name }}
            </div>
            <div class="text-lg flex flex-row justify-start mb-[5px] ml-[2px]">
              <div class="mr-[40px]">Like: 999</div>
              <div class="">Dislike: 0</div>
            </div>
          </div>
        </div>
        <div class="w-full flex flex-row justify-start">
            <div class="description_css">
              {{ dict.object.description }}
            </div>
        </div>
      </div>

      <a-divider style="height: 0.5px; background-color: rgba(124, 179, 5, 0.5)" />

      <a-card :bordered="true" style="width: 100%; text-align: left;">
        <!-- bodyStyle="padding-left: 24px; padding-right: 24px"
        headStyle="padding-left: 24px; padding-right: 24px" -->
        <template #title>
          <div class="sub_item_title_css">
              {{ "super yingshaoxo" }}
          </div>
        </template>
        <div class="flex flex-row justify-start mb-[20px]">
          <div class="main_item_icon_css w-[148px] h-[148px]" style="background-color: rgba(124, 179, 5, 0.5);"></div>
          <div class="w-full h-full ml-[20px] flex flex-col justify-start">
            <div class="w-full h-full flex flex-col justify-between">
              <div class="text-lg mb-[20px]">
                The super version of yingshaoxo.
              </div>
              <div class="text-xs flex flex-row justify-start ml-[2px]">
                <div class="mr-[40px]">Like: 999</div>
                <div class="">Dislike: 0</div>
              </div>
            </div>
          </div>
        </div>
      </a-card>
    </div>
  </div>
</template>

<style scoped lang="less">
.container_css {
  width: 100%;
  -webkit-text-size-adjust: 100%;
  font-size: 14px;
  font-family: Arial;
  font-weight: normal;
  line-height: 1.5;
  color: #333;
  -webkit-font-smoothing: antialiased;
  box-sizing: inherit;
  background: #fff;
  border-radius: 5px;
  padding: 20px 25px 5px 25px;
  display: flex;
  flex-direction: column;
  position: relative;
}
.main_item_icon_css {
    -webkit-text-size-adjust: 100%;
    font-size: 14px;
    font-family: Arial;
    font-weight: normal;
    line-height: 1.5;
    -webkit-font-smoothing: antialiased;
    box-sizing: inherit;
    border-style: none;
    display: inline-block;
    vertical-align: middle;
    min-height: 150px;
    min-width: 150px;
}
.main_item_title_css{
    -webkit-text-size-adjust: 100%;
    -webkit-font-smoothing: antialiased;
    box-sizing: inherit;
    font-family: Arial;
    font-style: normal;
    color: inherit;
    text-rendering: optimizeLegibility;
    font-size: 2.14286rem;
    font-weight: 700;
    word-wrap: break-word;
    width: 100%;
    line-height: 2.28571rem;
    flex-grow: 1;
    flex-shrink: 1;
    text-align: left;
}
.sub_item_title_css {
    text-align: left;
    -webkit-text-size-adjust: 100%;
    -webkit-font-smoothing: antialiased;
    list-style-position: outside;
    list-style-type: none;
    cursor: pointer;
    width: 100%;
    box-sizing: inherit;
    font-family: Arial;
    font-style: normal;
    color: rgb(0, 194, 194);
    text-rendering: optimizeLegibility;
    line-height: 1.4;
    font-weight: 700;
    font-size: 1.28571rem;
}
.sub_item_description_css {
    -webkit-text-size-adjust: 100%;
    font-family: Arial;
    font-weight: normal;
    color: #333;
    -webkit-font-smoothing: antialiased;
    list-style-position: outside;
    line-height: 1.6;
    list-style-type: none;
    font-size: inherit;
    box-sizing: inherit;
    width: auto;
    float: none;
    display: -webkit-box;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
    overflow: hidden;
    overflow-wrap: anywhere;
}
.green_text_css {
    -webkit-text-size-adjust: 100%;
    font-family: Arial;
    font-weight: normal;
    -webkit-font-smoothing: antialiased;
    color: #006665;
    font-size: 1rem;
    line-height: 1;
    box-sizing: inherit;
}
.description_css {
  width: 100%;
  -webkit-text-size-adjust: 100%;
  font-family: Arial;
  font-weight: normal;
  line-height: 1.5;
  color: #333;
  -webkit-font-smoothing: antialiased;
  font-size: 1rem;
  box-sizing: inherit;
  display: flex;
  flex-flow: row wrap;
  border: 1px solid #00C2C2;
  border-radius: 5px;
  padding: 1.42857rem 1.78571rem 1.07143rem 1.78571rem !important;
  background: #F5FCFC;
}
</style>