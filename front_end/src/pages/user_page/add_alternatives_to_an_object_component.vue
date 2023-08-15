<script setup lang="ts">
import { onMounted, reactive, ref, UnwrapRef } from 'vue';
import { LikeOutlined, DislikeOutlined, PlusOutlined, SearchOutlined, CheckOutlined, EditOutlined } from '@ant-design/icons-vue';

import * as it_has_alternatives_objects from '../../generated_yrpc/it_has_alternatives_objects'
import { global_dict, global_functions } from '../../store';

var properties = defineProps<{ master_object: it_has_alternatives_objects.An_Object, parent_refresh_function: any }>()

var clone_object = (obj: any) =>  JSON.parse(JSON.stringify(obj));

const dict = reactive({
  column_name: [
    {
      title: global_dict.t('Name'),
      dataIndex: 'name',
      key: 'name',
      align: 'center',
      width: 120,
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
  data_source: [
  ] as it_has_alternatives_objects.An_Object[],
  selected_row_keys: [] as string[],
  pagination: {
    current: 1,
    size: 10,
    total: 1000,
  },
  adding_dialog_visible: false,
  temprary_object_for_adding: new it_has_alternatives_objects.An_Object(),
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

    await properties.parent_refresh_function()
  },
  on_select_change: (selected_row_keys: string[]) => {
      dict.selected_row_keys = selected_row_keys
  },
  add_as_an_alternative_to_the_topest_object: async (object_id_list: string[]) => {
    console.log(object_id_list)
    var the_master_object = clone_object(properties.master_object)

    if (the_master_object.alternative_id_list == null) {
      the_master_object.alternative_id_list = []
    }
    
    for (var new_id of object_id_list) {
      if (new_id == the_master_object.id) {
        continue
      }
      if (!the_master_object.alternative_id_list.includes(new_id)) {
        the_master_object.alternative_id_list.push(new_id)
      }
    }

    await functions.update_an_object(the_master_object)

    dict.selected_row_keys = []

    await functions.refresh_list()
  },
  add_an_object: async (the_object: it_has_alternatives_objects.An_Object) => {
    var request = new it_has_alternatives_objects.Add_Object_Request()
    request.an_object = the_object
    var result = await global_dict.user_client.add_alternative(
      request
    )

    await functions.refresh_list()
  },
  delete_an_object: async (the_object: it_has_alternatives_objects.An_Object) => {
    var request = new it_has_alternatives_objects.Delete_Object_Request()
    request.an_object = the_object
    var result = await global_dict.user_client.delete_alternative(
      request
    )

    await functions.refresh_list()
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
}

onMounted(async () => {
  await functions.refresh_list()
})
</script>

<template>
  <a-modal
      v-model:visible="dict.adding_dialog_visible"
      :title="global_dict.t(`Add`)"
      :cancelText="global_dict.t('Cancel')"
      :okText="global_dict.t('Ok')"
      style="top: 20px"
      @ok="async ()=>{
        await functions.add_an_object(
          clone_object(dict.temprary_object_for_adding)
          // new it_has_alternatives_objects.An_Object().from_dict(dict.temprary_object_for_edit.to_dict())
        )

        dict.adding_dialog_visible=false

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

  <div class="w-full flex flex-col justify-start">
    <div class="overflow-x-auto">
      <div class="max-md:w-[700px]">
        <a-form
          ref="formRef"
          name="advanced_search"
          class="ant-advanced-search-form"
          :model="dict.temprary_object_for_search"
          @finish="functions.on_search"
        >
          <a-card>
                <a-row :gutter="24">
                  <a-col :span="24">
                    <a-form-item
                      :name="`Name`"
                      :label="global_dict.t('Name')"
                      :rules="[{ required: false, message: 'input something' }]"
                    >
                      <a-input v-model:value="dict.temprary_object_for_search.name"></a-input>
                    </a-form-item>
                  </a-col>
                </a-row>
                <div class="w-full flex flex-row justify-between">
                  <div>
                    <a-button class="mr-[10px]" @click="()=>{dict.adding_dialog_visible=true}">
                      <div class="flex flex-row place-content-center place-items-center">
                        <PlusOutlined class="mr-[8px]"></PlusOutlined>
                        {{ global_dict.t("Add") }}
                      </div>
                    </a-button>
                    <a-button type="primary" @click="async ()=>{
                      await functions.add_as_an_alternative_to_the_topest_object(dict.selected_row_keys)
                    }">
                      <div class="flex flex-row place-content-center place-items-center">
                        <PlusOutlined class="mr-[8px]"></PlusOutlined>
                        {{ global_dict.t("Add_as_an_alternative_to_the_topest_object") }}
                      </div>
                    </a-button>
                  </div>
                  <div>
                    <a-button type="primary" html-type="submit">
                      <div class="flex flex-row place-content-center place-items-center">
                        <SearchOutlined class="mr-[8px]" />
                        {{ global_dict.t("Search") }}
                      </div>  
                    </a-button>
                    <a-button style="margin: 0 8px" @click="() => functions.reset_search_bar()">
                      {{ global_dict.t("Clear") }}
                    </a-button>
                  </div>
                </div>
          </a-card>
        </a-form>
      </div>
    </div>

    <div class="w-full flex flex-row justify-center">
      <a-table bordered :data-source="dict.data_source" :columns="dict.column_name" :pagination="false"
        :scroll="{ x: '1500' }"
        :rowKey="(record: it_has_alternatives_objects.An_Object)=>record.id"
        :row-selection="{ selectedRowKeys: dict.selected_row_keys, onChange: functions.on_select_change }"
        :customRow="(record: it_has_alternatives_objects.An_Object) => {
          return {
              onClick: async (event: PointerEvent) => {
                // if (!dict.selected_row_keys.includes(record?.id??'')) {
                //   dict.selected_row_keys.push(record?.id??'')
                // } else {
                //   dict.selected_row_keys = dict.selected_row_keys.filter(an_id => an_id != record.id)
                // }
                await global_dict.router.push(`/user/object/${record.name}`)
              }
          }
        }"
      >
        <template #bodyCell="{ column, text, record }">
          <template v-if="column.dataIndex === 'operations'">
              <a-popconfirm
                v-if="dict.data_source.length"
                title="Sure to delete?"
                @confirm="(e: any)=>{
                  functions.delete_an_object(record)}"
              >
                <a-button @click.stop="()=>{}">
                  {{ 
                    global_dict.t("Delete")
                  }}
                </a-button>
              </a-popconfirm>
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
        </template>
      </a-table>
    </div>
    
    <a-card :bordered="false"
      style="border-top: 0.001px solid rgba(0, 0, 0, 0.02); border-left: 0.01px solid rgba(0, 0, 0, 0.1); border-right: 0.01px solid rgba(0, 0, 0, 0.1); border-bottom: 0.01px solid rgba(0, 0, 0, 0.2);"
    >
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
      </a-card>
  </div>

  <div class="h-[200px]"></div>
</template>

<style scoped lang="less">
.ant-card-bordered {
  border: 1px solid #f0f0f0;
}
</style>