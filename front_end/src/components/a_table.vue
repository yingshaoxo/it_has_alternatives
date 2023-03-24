<script setup lang="ts">
import { onMounted, reactive, ref, UnwrapRef } from 'vue';
import { CheckOutlined, EditOutlined } from '@ant-design/icons-vue';

import * as it_has_alternatives_objects from '../generated_yrpc/it_has_alternatives_objects'
import * as it_has_alternatives_rpc from '../generated_yrpc/it_has_alternatives_rpc'

var clone_object = (obj: any) =>  JSON.parse(JSON.stringify(obj));

const dict = reactive({
  client: new it_has_alternatives_rpc.Client_it_has_alternatives("http://127.0.0.1:80"),
  column_name: [
    {
      title: 'Name',
      dataIndex: 'name',
      key: 'name',
    },
    {
      title: 'Description',
      dataIndex: 'description',
      key: 'description',
    },
    {
      title: 'Likes',
      dataIndex: 'likes',
      key: 'likes',
    },
    {
      title: 'Dislikes',
      dataIndex: 'dislikes',
      key: 'dislikes',
    },
    {
      title: 'Operations',
      dataIndex: 'operations',
      key: 'operations',
    },
  ],
  data_source: [
  ] as it_has_alternatives_objects.An_Object[],
  editable_data: {} as UnwrapRef<Record<string, it_has_alternatives_objects.An_Object>>,
  dialog_visible: false,
  temprary_object_for_edit: new it_has_alternatives_objects.An_Object(),
})

const functions = {
  refresh_list: async () => {
    var request = new it_has_alternatives_objects.Search_Alternative_Request()
    request.key_words = "yi"
    request.page_number = 0
    request.page_size = 20
    var result = await dict.client.search_alternatives(
      request
    )
    dict.data_source = result?.alternative_object_list ?? []
  },
  add_an_object: async (the_object: it_has_alternatives_objects.An_Object) => {
    // var an_object = new it_has_alternatives_objects.An_Object()
    // an_object.from_dict({
    //   name: "",
    //   id: "1",
    //   description: null,
    //   likes: 3,
    //   dislikes: 4,
    //   alternative_id_list: ["1", "2"]
    // })
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
}

const edit = async (name: string) => {
  dict.editable_data![name] = clone_object(dict.data_source.filter(item => name === item.name)[0])
  console.log(dict.editable_data![name])
}

const save = async (name: string) => {
  if ((dict.editable_data) && (dict.data_source)) {
    Object.assign(dict.data_source.filter(item => name === item.name)[0], dict.editable_data[name]);

    var an_object = new it_has_alternatives_objects.An_Object()
    await functions.update_an_object(an_object.from_dict(dict.editable_data[name])) 

    delete dict.editable_data[name];

    await functions.refresh_list()
  }
};

onMounted(async () => {
  await functions.refresh_list()
})
</script>

<template>
  <div class="w-full flex justify-end">
    <a-button type="primary" class="mb-[16px]" @click="()=>{dict.dialog_visible=true}">Add</a-button>
  </div>

  <a-modal
      v-model:visible="dict.dialog_visible"
      title="Add"
      style="top: 20px"
      @ok="async ()=>{
        await functions.add_an_object(
          // dict.temprary_object_for_edit._clone()
          new it_has_alternatives_objects.An_Object().from_dict(dict.temprary_object_for_edit.to_dict())
        )

        dict.dialog_visible=false

        await functions.refresh_list()
      }"
    >
      <a-input :placeholder="dict.temprary_object_for_edit._key_string_dict.name" v-model:value="dict.temprary_object_for_edit.name" />
      <a-input :placeholder="dict.temprary_object_for_edit._key_string_dict.description" v-model:value="dict.temprary_object_for_edit.description" />
  </a-modal>

  <a-table class="w-screen" bordered :data-source="dict.data_source" :columns="dict.column_name">
    <template #bodyCell="{ column, text, record }">
      <template v-if="column.dataIndex === 'name'">
        <div class="editable-cell">
          <div v-if="dict.editable_data && dict.editable_data[record.name]" class="editable-cell-input-wrapper">
            <a-input v-model:value="dict.editable_data[record.name].name" @pressEnter="save(record.name)" />
            <check-outlined class="editable-cell-icon-check" @click="save(record.name)" />
          </div>
          <div v-else class="editable-cell-text-wrapper">
            {{ text || ' ' }}
            <edit-outlined class="editable-cell-icon" @click="edit(record.name)" />
          </div>
        </div>
      </template>
      <template v-else-if="column.dataIndex === 'operations'">
        <a-popconfirm
          v-if="dict.data_source.length"
          title="Sure to delete?"
          @confirm="functions.delete_an_object(record)"
        >
          <a-button>Delete</a-button>
        </a-popconfirm>
      </template>
    </template>
  </a-table>
</template>

<style lang="less">
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