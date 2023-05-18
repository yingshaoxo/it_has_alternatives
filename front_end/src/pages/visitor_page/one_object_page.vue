<script setup lang="ts">
import { useRoute, useRouter } from 'vue-router';

import { onActivated, onMounted, reactive, ref, UnwrapRef } from 'vue';
import { LikeOutlined, DislikeOutlined, PlusOutlined, SearchOutlined, CheckOutlined, EditOutlined } from '@ant-design/icons-vue';

import * as it_has_alternatives_objects from '../../generated_yrpc/it_has_alternatives_objects'

import { global_dict, global_functions } from '../../store'

import snarkdown from 'snarkdown'

var route = useRoute()

var clone_object = (obj: any) =>  JSON.parse(JSON.stringify(obj));

const dict = reactive({
  object_name: "",
  object: new it_has_alternatives_objects.An_Object(),
  alternative_dict: {} as Record<string, it_has_alternatives_objects.An_Object>,
  object_id_to_description_markdown_html_code_dict: {} as Record<string, string>,
  column_name: [
    {
      title: global_dict.t('Name'),
      dataIndex: 'name',
      key: 'name',
      align: 'center',
      width: 220,
      ellipsis: true
    },
    {
      title: global_dict.t('Description'),
      dataIndex: 'description',
      key: 'description',
      align: 'center',
      ellipsis: true
    },
    {
      title: global_dict.t('Like'),
      dataIndex: 'likes',
      key: 'likes',
      align: 'center',
      width: 80 
    },
    {
      title: global_dict.t('Dislike'),
      dataIndex: 'dislikes',
      key: 'dislikes',
      align: 'center',
      width: 80 
    },
    {
      title: global_dict.t('Operations'),
      dataIndex: 'operations',
      key: 'operations',
      align: 'center',
      width: 120
    },
  ],
  dialog_visible: false,
  temprary_object_for_adding: new it_has_alternatives_objects.An_Object(),
})

const functions = {
  get_one_object: async (object_name: string): Promise<it_has_alternatives_objects.An_Object | null> => {
    var request = new it_has_alternatives_objects.Search_Alternative_Request()
    request.key_words = object_name
    request.page_number = 0
    request.page_size = 3
    var result = await global_dict.visitor_client.search_alternatives(
      request
    )
    var result_object_list = result?.alternative_object_list ?? []
    if (result_object_list.length > 0) {
      return result_object_list[0]
    } else {
      return null
    }
  },
  refresh_list: async () => {
    // update the main object
    dict.object = await functions.get_one_object(dict.object_name)?? new it_has_alternatives_objects.An_Object()
    dict.object_id_to_description_markdown_html_code_dict[dict?.object?.id??''] = snarkdown(dict?.object?.description??'')

    // update those objects under the main object
    for (var an_id of dict.object.alternative_id_list??[]) {
      var request = new it_has_alternatives_objects.Get_an_object_Request()
      request.id = an_id
      var response = await global_dict.visitor_client.get_an_object(request)
      if (response?.an_object != null) {
        dict.alternative_dict[an_id] = response.an_object
      } else {
        var new_object = new it_has_alternatives_objects.An_Object()
        new_object.id = an_id
        dict.alternative_dict[an_id] = new_object
      }

      dict.object_id_to_description_markdown_html_code_dict[an_id] = snarkdown(dict?.alternative_dict[an_id]?.description??'')
    }
  },
  vote_an_object: async (the_object: it_has_alternatives_objects.An_Object, up: boolean) => {
    // if (the_object?.likes == null) {
    //   the_object.likes = 0
    // }
    // if (the_object?.dislikes == null) {
    //   the_object.dislikes = 0
    // }
    // if (up) {
    //   the_object.likes += 1
    // } else {
    //   the_object.dislikes += 1
    // }

    // var request = new it_has_alternatives_objects.Update_Object_Request()
    // request.an_object = the_object
    // var result = await global_dict.client.update_alternative(
    //   request
    // )

    // await functions.refresh_list()
  },
  refresh_page: () => {
    location.reload();
  }
}

onMounted(async () => {
  if (Array.isArray(route.params?.name)) {
    dict.object_name = route.params?.name[0]
  } else {
    dict.object_name = route.params?.name??""
  }

  await functions.refresh_list()
})
</script>

<template>
  <a-button 
    v-if="global_functions.get_current_url().includes('/object/')"
    class="bottom_right" 
    type="link"
    @click="async () => {
      await global_dict.router.push(`/user/object/${dict.object_name}`)
      // global_dict.login_dialog_visible = true
    }"
  >{{global_dict.t("Edit")}}</a-button>

  <div class="flex flex-col place-content-center place-items-center">
    <div class="container_css max-w-[1366px]">
      <div class="px-[0px]">
        <div class="flex flex-row justify-start mb-[20px]">
          <div class="main_item_icon_css w-[148px] h-[148px]" style="background-color: rgba(124, 179, 5, 0.5);"></div>
          <div class="ml-[20px] flex flex-col justify-between">
            <div class="main_item_title_css">
                {{ dict.object_name }}
            </div>
            <div class="text-lg flex flex-row justify-start mb-[5px] ml-[2px] text-gray-500">
              <div class="mr-[40px]">{{global_dict.t('Like')}}: {{ dict?.object?.likes??'0' }}</div>
              <div class="">{{global_dict.t('Dislike')}}: {{ dict?.object?.dislikes??'0' }}</div>
            </div>
          </div>
        </div>
        <div class="w-full flex flex-row justify-start">
            <div class="main_description_css">
              <div class="prose prose-sm dark:prose-invert">
                <div v-html="dict.object_id_to_description_markdown_html_code_dict[dict?.object?.id??'']??''">
                </div>
              </div>
            </div>
        </div>
      </div>

      <a-divider style="height: 0.5px; background-color: rgba(124, 179, 5, 0.5)" />

      <div class="space-y-[24px]">
        <a-card :bordered="true" style="width: 100%; text-align: left;"
          v-for="an_id in dict.object?.alternative_id_list??[]"
          v-show="dict.alternative_dict[an_id]?.name"
        >
          <template #title>
            <div class="sub_item_title_css" 
              @click="async ()=>{
                await global_dict.router.push(`/object/${dict.alternative_dict[an_id]?.name}`)
                global_functions.refresh()
              }"
            >
                {{ dict.alternative_dict[an_id]?.name }}
            </div>
          </template>
          <div class="flex flex-row justify-start mb-[20px]">
            <div class="main_item_icon_css w-[148px] h-[148px]" style="background-color: rgba(124, 179, 5, 0.5);"></div>
            <div class="w-full h-full ml-[20px] flex flex-col justify-start">
              <div class="w-full h-full flex flex-col justify-between">
                <div class="mb-[20px] prose prose-sm dark:prose-invert sub_item_description">
                  <div v-html="dict.object_id_to_description_markdown_html_code_dict[an_id??'']??''">
                  </div>
                </div>
                <div class="text-sm flex flex-row justify-start ml-[2px] text-gray-400">
                  <div class="mr-[40px]">{{global_dict.t('Like')}}: {{ dict.alternative_dict[an_id]?.likes??'0' }}</div>
                  <div class="">{{global_dict.t('Dislike')}}: {{ dict.alternative_dict[an_id]?.dislikes??'0' }}</div>
                </div>
              </div>
            </div>
          </div>
        </a-card>
      </div>

      <div class="h-[100px]"></div>

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
  font-weight: 700;
  word-wrap: break-word;
  width: 100%;
  line-height: 2.28571rem;
  flex-grow: 1;
  flex-shrink: 1;
  text-align: left;
  font-size: 2.14286rem;

  .for_mobile({
    font-size: 28px;
  });
}
.main_description_css {
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
  text-align: left;
  word-break: break-word;
  .for_mobile({
    font-size: 28px;
  });
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
  text-rendering: optimizeLegibility;
  line-height: 1.4;
  font-weight: 700;
  font-size: 1.28571rem;
}
.sub_item_description {
  word-break: break-word;
  .for_mobile({
    font-size: 16px;
  });
}
.bottom_right {
  position: absolute;
  bottom: 0;
  right: 0;
}
</style>