<script setup lang="ts">
import { onMounted, reactive, ref, UnwrapRef } from 'vue';
import { PlusOutlined, SearchOutlined, CheckOutlined, EditOutlined } from '@ant-design/icons-vue';

import * as it_has_alternatives_objects from '../../generated_yrpc/it_has_alternatives_objects'

import { global_dict, global_functions } from '../../store'

import help_card from '../general_page/help_card.vue'
import Language_switch_selection from '../general_page/language_switch_selection.vue';

const dict = reactive({
  column_name: [
    {
      title: global_dict.t('Name'),
      dataIndex: 'name',
      key: 'name',
      align: 'center',
      ellipsis: true,
      width: 200,
      // fixed: 'left'
    },
    {
      title: global_dict.t('Description'),
      dataIndex: 'description',
      key: 'description',
      align: 'center',
      width: 400,
      ellipsis: true,
      // fixed: 'left'
      responsive: ["sm"]
    },
    {
      title: global_dict.t('Like'),
      dataIndex: 'likes',
      key: 'likes',
      align: 'center',
      width: 80,
      responsive: ["lg"]
    },
    {
      title: global_dict.t('Dislike'),
      dataIndex: 'dislikes',
      key: 'dislikes',
      align: 'center',
      width: 80,
      responsive: ["lg"]
    },
  ],
  data_source: [
  ] as it_has_alternatives_objects.An_Object[],
  editable_data: {} as UnwrapRef<Record<string, it_has_alternatives_objects.An_Object>>,
  pagination: {
    current: 1,
    size: 10,
    total: 1000,
  },
  dialog_visible: false,
  temprary_object_for_edit: new it_has_alternatives_objects.An_Object(),
  temprary_object_for_search: new it_has_alternatives_objects.An_Object(),
  what_column_is_in_editing_now: "",
})

const functions = {
  reset_search_bar: async () => {
    dict.temprary_object_for_search = new it_has_alternatives_objects.An_Object()
    await functions.refresh_list()
  },
  on_search: async (values: any) => {
    await functions.refresh_list()
  },
  refresh_list: async () => {
    var request = new it_has_alternatives_objects.Search_Alternative_Request()
    request.key_words = dict.temprary_object_for_search.name
    request.page_number = dict.pagination.current - 1
    request.page_size = dict.pagination.size
    var result = await global_dict.visitor_client.search_alternatives(
      request
    )
    dict.data_source = result?.alternative_object_list ?? []
  },
  on_row_click: async (record: it_has_alternatives_objects.An_Object) => {
    setTimeout(async ()=>{
      // to prevent page jump when doing the editing
      //@ts-ignore
      if (dict.editable_data[record.id]) { 
      } else {
        console.log(record.name)
        await global_dict.router.push(`/object/${record.name}`)
      }
    }, 300)
  },
}

onMounted(async () => {
  await global_functions.redirect_to_user_home_page_if_jwt_is_valid()
  await functions.refresh_list()
})
</script>

<template>
  <div class="h-[50px]"></div>

  <div class="w-full flex flex-col justify-start lg:px-[100px]">
    <a-form
      ref="formRef"
      name="advanced_search"
      class="search_area ant-advanced-search-form"
      :model="dict.temprary_object_for_search"
      @finish="functions.on_search"
    >
      <a-card>
        <a-row :gutter="24">
          <a-col :span="24">
            <a-form-item
              :name="`Name`"
              :label="global_dict.t(`Name`)"
              :rules="[{ required: false, message: 'input something' }]"
            >
              <a-input v-model:value="dict.temprary_object_for_search.name"></a-input>
            </a-form-item>
          </a-col>
        </a-row>
        <div class="w-full flex flex-row justify-between">
          <div>
          </div>
          <div>
            <a-button type="primary" html-type="submit">
              <div class="flex flex-row justify-center align-middle content-center place-content-center place-items-center">
                <SearchOutlined class="mr-[8px]" />
                {{ global_dict.t(`Search`) }}
              </div>  
            </a-button>
            <a-button style="margin: 0 8px" @click="() => functions.reset_search_bar()">
                {{ global_dict.t(`Clear`) }}
            </a-button>
          </div>
        </div>
      </a-card>
    </a-form>

    <div class="w-full flex flex-row justify-center">
      <a-table class="mb-[24px]" bordered :data-source="dict.data_source" :columns="dict.column_name" :pagination="false"
        :scroll="{ x: '1500' }"
        :customRow="(record: any) => {
          return {
              onClick: (event: PointerEvent) => {
                  functions.on_row_click(record)
              }
          }
        }"
      >
        <template #bodyCell="{ column, text, record }">
          <template v-if="['name', 'description'].includes(column.dataIndex)">
            <div class="editable-cell">
              <div class="editable-cell-text-wrapper">
                {{ text || ' ' }}
              </div>
            </div>
          </template>
          <template v-else-if="['likes', 'dislikes'].includes(column.dataIndex)">
            <div class="editable-cell">
              <div class="editable-cell-text-wrapper">
                {{ text || '0' }}
              </div>
            </div>
          </template>
        </template>
      </a-table>
    </div>
    
    <div class="w-full flex flex-row justify-end">
      <a-pagination
        v-model:current="dict.pagination.current"
        v-model:pageSize="dict.pagination.size"
        show-size-changer
        :total="dict.pagination.total"
        @change="async (page: number, pageSize: number) => {
          dict.pagination.current = page
          dict.pagination.size = pageSize
          await functions.refresh_list()
        }"
      />
    </div>
  </div>

  <div class="space_after_table"></div>

  <help_card></help_card>

  <div class="page_bottom_space"></div>

  <Language_switch_selection></Language_switch_selection>
</template>

<style scoped lang="less">
.ant-card-bordered {
  border: 1px solid #f0f0f0;
}

.search_area {
  .for_mobile({
    margin-bottom: 60px;
  });
}

.space_after_table {
  height: 200px;
  .for_mobile({
    height: 100px;
  });
}

.page_bottom_space {
  height: 100px;
  .for_mobile({
    height: 50px;
  });
}
</style>