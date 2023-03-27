<script setup lang="ts">
import { onMounted, reactive, ref, UnwrapRef } from 'vue';
import { LikeOutlined, DislikeOutlined, PlusOutlined, SearchOutlined, CheckOutlined, EditOutlined } from '@ant-design/icons-vue';

import * as it_has_alternatives_objects from '../generated_yrpc/it_has_alternatives_objects'
import * as it_has_alternatives_rpc from '../generated_yrpc/it_has_alternatives_rpc'

var properties = defineProps<{ master_object: it_has_alternatives_objects.An_Object }>()

var clone_object = (obj: any) =>  JSON.parse(JSON.stringify(obj));

const dict = reactive({
  client: new it_has_alternatives_rpc.Client_it_has_alternatives("http://127.0.0.1:80"),
  column_name: [
    {
      title: 'Name',
      dataIndex: 'name',
      key: 'name',
      align: 'center',
      width: 220,
      ellipsis: true
    },
    {
      title: 'Description',
      dataIndex: 'description',
      key: 'description',
      align: 'center',
      ellipsis: true
    },
    {
      title: 'Like',
      dataIndex: 'likes',
      key: 'likes',
      align: 'center',
      width: 80 
    },
    {
      title: 'Dislike',
      dataIndex: 'dislikes',
      key: 'dislikes',
      align: 'center',
      width: 80 
    },
    {
      title: 'Operations',
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
    var result = await dict.client.search_alternatives(
      request
    )
    dict.data_source = result?.alternative_object_list ?? []
  },
  on_select_change: (selected_row_keys: string[]) => {
      dict.selected_row_keys = selected_row_keys
  },
  add_as_an_alternative_to_the_topest_object: async (object_id_list: string[]) => {
    var the_master_object = clone_object(properties.master_object)

    if (the_master_object.alternative_id_list == null) {
      the_master_object.alternative_id_list = []
    }
    
    for (var new_id of object_id_list) {
      if (!the_master_object.alternative_id_list.includes(new_id)) {
        the_master_object.alternative_id_list.push(new_id)
      }
    }

    await functions.update_an_object(the_master_object)

    dict.selected_row_keys = []
  },
  add_an_object: async (the_object: it_has_alternatives_objects.An_Object) => {
    var request = new it_has_alternatives_objects.Add_Object_Request()
    request.an_object = the_object
    var result = await dict.client.add_alternative(
      request
    )
    console.log(result)
  },
  delete_an_object: async (the_object: it_has_alternatives_objects.An_Object) => {
    var request = new it_has_alternatives_objects.Delete_Object_Request()
    request.an_object = the_object
    var result = await dict.client.delete_alternative(
      request
    )

    await functions.refresh_list()
  },
  update_an_object: async (the_object: it_has_alternatives_objects.An_Object) => {
    var request = new it_has_alternatives_objects.Update_Object_Request()
    request.an_object = the_object
    var result = await dict.client.update_alternative(
      request
    )
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
    var result = await dict.client.update_alternative(
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
      v-model:visible="dict.dialog_visible"
      title="Add"
      style="top: 20px"
      @ok="async ()=>{
        await functions.add_an_object(
          dict.temprary_object_for_edit._clone()
          // new it_has_alternatives_objects.An_Object().from_dict(dict.temprary_object_for_edit.to_dict())
        )

        dict.dialog_visible=false

        await functions.refresh_list()
      }"
    >
    <div class="space-y-[16px]">
      <a-input :placeholder="dict.temprary_object_for_edit._key_string_dict.name" v-model:value="dict.temprary_object_for_edit.name" />
      <a-input :placeholder="dict.temprary_object_for_edit._key_string_dict.description" v-model:value="dict.temprary_object_for_edit.description" />
    </div>
  </a-modal>

  <div class="w-full flex flex-col justify-start">
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
              :label="`Name`"
              :rules="[{ required: false, message: 'input something' }]"
            >
              <a-input v-model:value="dict.temprary_object_for_search.name"></a-input>
            </a-form-item>
          </a-col>
          <!-- <template v-for="(key, index) in Object.keys(dict.temprary_object_for_search)" :key="key">
            <a-col v-if="index<3 && (!key.startsWith('_'))" :span="8">
              <a-form-item
                :name="`${key}`"
                :label="`${key.toUpperCase()}`"
                :rules="[{ required: false, message: 'input something' }]"
              >
                <a-input v-model:value="dict.temprary_object_for_search[key]"></a-input>
              </a-form-item>
            </a-col>
          </template> -->
        </a-row>
        <div class="w-full flex flex-row justify-between">
          <div>
            <a-button class="mr-[10px]" @click="()=>{dict.dialog_visible=true}">
              <div class="flex flex-row place-content-center place-items-center">
                <PlusOutlined class="mr-[8px]"></PlusOutlined>
                Add
              </div>
            </a-button>
            <a-button type="primary" @click="async ()=>{
              await functions.add_as_an_alternative_to_the_topest_object(dict.selected_row_keys)
            }">
              <div class="flex flex-row place-content-center place-items-center">
                <PlusOutlined class="mr-[8px]"></PlusOutlined>
                Add as an alternative to the topest object
              </div>
            </a-button>
          </div>
          <div>
            <a-button type="primary" html-type="submit">
              <div class="flex flex-row place-content-center place-items-center">
                <SearchOutlined class="mr-[8px]" />
                Search
              </div>  
            </a-button>
            <a-button style="margin: 0 8px" @click="() => functions.reset_search_bar()">Clear</a-button>
          </div>
        </div>
      </a-card>
    </a-form>

    <div class="w-full flex flex-row justify-center">
      <a-table bordered :data-source="dict.data_source" :columns="dict.column_name" :pagination="false"
        :rowKey="(record: it_has_alternatives_objects.An_Object)=>record.id"
        :row-selection="{ selectedRowKeys: dict.selected_row_keys, onChange: functions.on_select_change }"
        :customRow="(record: it_has_alternatives_objects.An_Object) => {
          return {
              onClick: (event: PointerEvent) => {
                if (!dict.selected_row_keys.includes(record?.id??'')) {
                  dict.selected_row_keys.push(record?.id??'')
                } else {
                  dict.selected_row_keys = dict.selected_row_keys.filter(an_id => an_id != record.id)
                }
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
                <a-button @click.stop="()=>{}">Delete</a-button>
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

.editable-cell {
  position: relative;
  .editable-cell-input-wrapper,
  .editable-cell-text-wrapper {
    padding-right: 24px;
  }

  .editable-cell-text-wrapper {
    padding: 5px 24px 5px 5px;
  }

  .editable-cell-icon,
  .editable-cell-icon-check {
    position: absolute;
    right: 0;
    width: 20px;
    cursor: pointer;
  }

  .editable-cell-icon {
    margin-top: 4px;
    display: none;
  }

  .editable-cell-icon-check {
    line-height: 28px;
  }

  .editable-cell-icon:hover,
  .editable-cell-icon-check:hover {
    color: #108ee9;
  }

  .editable-add-btn {
    margin-bottom: 8px;
  }
}
.editable-cell:hover .editable-cell-icon {
  display: inline-block;
}
</style>