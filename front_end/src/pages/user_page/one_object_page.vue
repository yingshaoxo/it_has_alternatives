<script setup lang="ts">
import { useRoute, useRouter } from 'vue-router';

import { onActivated, onMounted, reactive, ref, UnwrapRef } from 'vue';
import { LikeOutlined, DislikeOutlined, PlusOutlined, ShareAltOutlined, SearchOutlined, CheckOutlined, EditOutlined } from '@ant-design/icons-vue';

import * as it_has_alternatives_objects from '../../generated_yrpc/it_has_alternatives_objects'

import add_alternatives_to_an_object_component from './add_alternatives_to_an_object_component.vue'
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
      ellipsis: true,
      fixed: 'left'
    },
    {
      title: global_dict.t('Description'),
      dataIndex: 'description',
      key: 'description',
      align: 'center',
      width: 420,
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
  edit_dialog_visible: false,
  temprary_object_for_adding: new it_has_alternatives_objects.An_Object(),
})

const functions = {
  get_one_object: async (object_name: string): Promise<it_has_alternatives_objects.An_Object | null> => {
    var request = new it_has_alternatives_objects.Get_an_object_Request()
    request.name = object_name
    var result = await global_dict.visitor_client.get_an_object(
      request
    )
    if (result?.an_object != null) {
      return result?.an_object
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
  update_an_object: async (the_object: it_has_alternatives_objects.An_Object) => {
    var request = new it_has_alternatives_objects.Update_Object_Request()
    request.an_object = the_object
    var result = await global_dict.user_client.update_alternative(
      request
    )

    await functions.refresh_list()
  },
  vote_an_object: async (the_object: it_has_alternatives_objects.An_Object, up: boolean) => {
    if (the_object?.likes == null) {
      the_object.likes = 0
    }
    if (the_object?.dislikes == null) {
      the_object.dislikes = 0
    }
    if (up) {
      the_object.likes += 1
    } else {
      the_object.dislikes += 1
    }

    var request = new it_has_alternatives_objects.Update_Object_Request()
    request.an_object = the_object
    var result = await global_dict.user_client.update_alternative(
      request
    )

    await functions.refresh_list()
  },
  delete_an_object_from_alternative_list: async (the_object: it_has_alternatives_objects.An_Object) => {
    dict.object.alternative_id_list = dict.object.alternative_id_list?.filter((id) => id != the_object.id) ?? []

    await functions.update_an_object(dict.object)

    await functions.refresh_list()
  },
}

onMounted(async () => {
  if (Array.isArray(route.params?.name)) {
    dict.object_name = route.params?.name[0]
  } else {
    dict.object_name = route.params?.name??""
  }


  var is_user = await global_functions.is_user()
  if (is_user) {
    await functions.refresh_list()
  } else {
    await global_dict.router.push(`/object/${dict.object_name}`)
    // await global_functions.show_dialog_if_it_is_not_user()
  }
})
</script>

<template>
  <a-button type="primary" shape="circle" class="my_float_button"
    @click="async () => {
        await global_functions.copy_text_to_clipboard(global_functions.get_current_url().replace('/user/o', '/o'))
        global_functions.print('Current website url has been copied into clipboard, now you can share it for free.')
    }"
  >
    <template #icon><ShareAltOutlined /></template>
  </a-button>

  <div class="flex flex-col place-content-center place-items-center"
  >
    <div class="container_css max-w-[1366px]">
      <div class="px-[0px]">
        <div class="flex flex-row justify-start mb-[20px]">
          <div class="main_item_icon_css" style="background-color: rgba(124, 179, 5, 0.5);"></div>
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
              <div class="prose-sm dark:prose-invert">
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
                await global_dict.router.push(`/user/object/${dict.alternative_dict[an_id]?.name}`)
                global_functions.refresh()
              }"
            >
                {{ dict.alternative_dict[an_id]?.name }}
            </div>
          </template>
          <div class="flex flex-row justify-start mb-[20px]">
            <div class="sub_item_icon_css w-[148px] h-[148px]" style="background-color: rgba(124, 179, 5, 0.5);"></div>
            <div class="w-full h-full ml-[20px] flex flex-col justify-start">
              <div class="w-full h-full flex flex-col justify-between">
                <!-- <div class="text-lg mb-[20px]"> -->
                <div class="mb-[20px] prose-sm dark:prose-invert sub_item_description">
                  <!-- {{ dict.alternative_dict[an_id]?.description }} -->
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

      <a-modal
        v-model:visible="dict.edit_dialog_visible"
        :title="global_dict.t('Edit')"
        :cancelText="global_dict.t('Cancel')"
        :okText="global_dict.t('Ok')"
        style="top: 20px"
        @ok="async ()=>{
          await functions.update_an_object(
            dict.temprary_object_for_adding
          )

          dict.edit_dialog_visible=false

          await functions.refresh_list()
        }"
      >
        <div class="space-y-[16px]">
          <a-input :placeholder="dict.temprary_object_for_adding._key_string_dict.name" v-model:value="dict.temprary_object_for_adding.name" />
          <!-- <a-input :placeholder="dict.temprary_object_for_adding._key_string_dict.description" v-model:value="dict.temprary_object_for_adding.description" /> -->
          <a-textarea
            v-model:value="dict.temprary_object_for_adding.description"
            :placeholder="dict.temprary_object_for_adding._key_string_dict.description"
            auto-size
          />
        </div>
      </a-modal>

      <a-table bordered :data-source="dict.object.alternative_id_list?.map((an_id: string) => dict.alternative_dict[an_id])" :columns="dict.column_name" :pagination="false"
        :scroll="{ x: '1500' }"
      >
        <template #bodyCell="{ column, text, record }">
          <template v-if="['name', 'description'].includes(column.dataIndex)">
            <div class="editable-cell">
              <div class="editable-cell-text-wrapper">
                {{ text || ' ' }}
              </div>
            </div>
          </template>
          <template v-else-if="column.dataIndex === 'likes'">
            <div class="flex flex-row place-content-center place-items-center unselectable">
              <div class="mr-[4px]">
                {{ record?.likes??'0' }}
              </div>
              <LikeOutlined class="hover:text-red-400" 
                @click.stop="functions.vote_an_object(record, true)"
              />
            </div>
          </template>
          <template v-else-if="column.dataIndex === 'dislikes'">
            <div class="flex flex-row place-content-center place-items-center unselectable">
              <div class="mr-[4px]">
                {{ record?.dislikes??'0' }}
              </div>
              <DislikeOutlined class="hover:text-red-400" 
                @click.stop="functions.vote_an_object(record, false)"
              />
            </div>
          </template>
          <template v-else-if="column.dataIndex === 'operations'">
            <a-button class="w-[80px] mb-[12px]" @click.stop="()=>{
              dict.temprary_object_for_adding = record
              dict.edit_dialog_visible=true
            }">
              {{ global_dict.t("Edit") }}
            </a-button>
            <div
              @click.stop="(e:any) => {
                e.preventDefault(); e.stopPropagation(); e.nativeEvent.stopImmediatePropagation(); 
              }"
            >
              <a-popconfirm
                title="Sure to delete?"
                @confirm="functions.delete_an_object_from_alternative_list(record)"
              >
                <a-button class="w-[80px]">
                  {{ global_dict.t("Delete") }}
                </a-button>
              </a-popconfirm>
            </div>
          </template>
        </template>
      </a-table>

      <div class="h-[100px]"></div>

      <add_alternatives_to_an_object_component 
        :master_object="dict.object"
        :parent_refresh_function="functions.refresh_list"
      ></add_alternatives_to_an_object_component>
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

  min-width: 148px;
  min-height: 148px;
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
}
.sub_item_icon_css {
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

  min-width: 140px;
  min-height: 140px;
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

.my_float_button {
	position:fixed;
  z-index: 99;

	width:40px;
	height:40px;

	bottom:40px;
	right:40px;

	border-radius:50px;
	box-shadow: 2px 2px 3px #999;

  border-color: transparent;
	background-color:#F8BBD0;

  opacity: 0.8;
}
</style>
