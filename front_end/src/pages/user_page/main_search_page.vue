<script setup lang="ts">
import { onMounted, reactive, ref, UnwrapRef } from 'vue';
import { PlusOutlined, SearchOutlined, CheckOutlined, EditOutlined } from '@ant-design/icons-vue';

import * as it_has_alternatives_objects from '../../generated_yrpc/it_has_alternatives_objects'

import { global_dict, global_functions } from '../../store'

import help_card from '../general_page/help_card.vue'
import Language_switch_selection from '../general_page/language_switch_selection.vue';

var clone_object = (obj: any) =>  JSON.parse(JSON.stringify(obj));

const dict = reactive({
  column_name: [
    {
      title: global_dict.t('Name'),
      dataIndex: 'name',
      key: 'name',
      align: 'center',
      width: 220,
      ellipsis: true,
      fixed: 'left',
    },
    {
      title: global_dict.t('Description'),
      dataIndex: 'description',
      key: 'description',
      align: 'center',
      width: 420,
      ellipsis: true,
      // responsive: ["sm"],
    },
    {
      title: global_dict.t('Like'),
      dataIndex: 'likes',
      key: 'likes',
      align: 'center',
      width: 80,
      // responsive: ["lg"]
    },
    {
      title: global_dict.t('Dislike'),
      dataIndex: 'dislikes',
      key: 'dislikes',
      align: 'center',
      width: 80,
      // responsive: ["lg"]
    },
    {
      title: global_dict.t('Operations'),
      dataIndex: 'operations',
      key: 'operations',
      align: 'center',
      width: 120,
      // fixed: 'right',
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
  edit_dialog_visible: false,
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
  add_an_object: async (the_object: it_has_alternatives_objects.An_Object) => {
    var request = new it_has_alternatives_objects.Add_Object_Request()
    request.an_object = the_object
    var result = await global_dict.user_client.add_alternative(
      request
    )
    console.log(result)
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
  },
  on_row_click: async (record: it_has_alternatives_objects.An_Object) => {
    setTimeout(async ()=>{
      // to prevent page jump when doing the editing
      //@ts-ignore
      if (dict.editable_data[record.id]) { 
      } else {
        console.log(record.name)
        await global_dict.router.push(`/user/object/${record.name}`)
      }
    }, 300)
  },
  on_cell_edit_button: async (dataIndex: string, id: string) => {
    dict.what_column_is_in_editing_now = dataIndex
    dict.editable_data![id] = clone_object(dict.data_source.filter(item => id === item.id)[0])
  },
  on_cell_save_action: async (id: string) => {
    if ((dict.editable_data) && (dict.data_source)) {
      Object.assign(dict.data_source.filter(item => id === item.id)[0], dict.editable_data[id]);

      dict.what_column_is_in_editing_now = ""

      var an_object = new it_has_alternatives_objects.An_Object()
      await functions.update_an_object(an_object.from_dict(dict.editable_data[id])) 

      delete dict.editable_data[id];

      await functions.refresh_list()
    }
  },
  get_invitation_code: async () => {
    let request = new it_has_alternatives_objects.Get_invitation_code_request();
    let data = await global_dict.user_client.get_invitation_code(request)
    if (data?.invitation_code == null) {
      if (global_functions.is_english_language()) {
        global_functions.print(`Get invitation code failed.`)
      } else {
        global_functions.print(`获取邀请码失败，你的2次邀请机会可能已经用完了。`)
      }
    } else {
      navigator.clipboard.writeText(data.invitation_code??"")
      global_functions.print(`Your invitation code has been copied into clipboard: \n\n${data.invitation_code}`)
    }
  }
}

onMounted(async () => {
  await functions.refresh_list()

  await global_functions.show_dialog_if_it_is_not_user()
})
</script>

<template>
  <a-modal
      v-model:visible="dict.dialog_visible"
      :title="global_dict.t(`Add`)"
      :cancelText="global_dict.t('Cancel')"
      :okText="global_dict.t('Ok')"
      style="top: 20px"
      @ok="async ()=>{
        await functions.add_an_object(
          clone_object(dict.temprary_object_for_edit)
          // new it_has_alternatives_objects.An_Object().from_dict(dict.temprary_object_for_edit.to_dict())
        )

        dict.dialog_visible=false

        await functions.refresh_list()
      }"
    >
    <div class="space-y-[16px]">
      <a-input :placeholder="dict.temprary_object_for_edit._key_string_dict.name" v-model:value="dict.temprary_object_for_edit.name" />
      <!-- <a-input :placeholder="dict.temprary_object_for_edit._key_string_dict.description" v-model:value="dict.temprary_object_for_edit.description" /> -->
      <a-textarea
        v-model:value="dict.temprary_object_for_edit.description"
        :placeholder="dict.temprary_object_for_edit._key_string_dict.description"
        auto-size
      />
    </div>
  </a-modal>

  <a-modal
      v-model:visible="dict.edit_dialog_visible"
      :title="global_dict.t('Edit')"
      :cancelText="global_dict.t('Cancel')"
      :okText="global_dict.t('Ok')"
      style="top: 20px"
      @ok="async ()=>{
        await functions.update_an_object(
          dict.temprary_object_for_edit
        )

        dict.edit_dialog_visible=false

        await functions.refresh_list()
      }"
    >
      <div class="space-y-[16px]">
        <a-input :placeholder="dict.temprary_object_for_edit._key_string_dict.name" v-model:value="dict.temprary_object_for_edit.name" />
        <!-- <a-input :placeholder="dict.temprary_object_for_edit._key_string_dict.description" v-model:value="dict.temprary_object_for_edit.description" /> -->
        <a-textarea
          v-model:value="dict.temprary_object_for_edit.description"
          :placeholder="dict.temprary_object_for_edit._key_string_dict.description"
          auto-size
        />
      </div>
  </a-modal>

  <div class="h-[50px]"></div>

  <div class="w-full flex flex-col justify-start lg:px-[100px]">
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
              :label="global_dict.t(`Name`)"
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
            <a-button @click="()=>{dict.dialog_visible=true}">
              <div class="flex flex-row justify-center align-middle content-center place-content-center place-items-center">
                <PlusOutlined class="mr-[8px]"></PlusOutlined>
                {{ global_dict.t(`Add`) }}
              </div>
            </a-button>
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
              <div v-if="dict.editable_data && dict.editable_data[record.id] && column.dataIndex==dict.what_column_is_in_editing_now" class="editable-cell-input-wrapper">
                <a-input v-model:value="
                  //@ts-ignore 
                  dict.editable_data[record.id][column.dataIndex]" @pressEnter="functions.on_cell_save_action(record.id)" />
                <check-outlined class="editable-cell-icon-check" @click.stop="functions.on_cell_save_action(record.id)" />
              </div>
              <div v-else class="editable-cell-text-wrapper">
                {{ text || ' ' }}
                <edit-outlined class="editable-cell-icon" @click.stop="functions.on_cell_edit_button(column.dataIndex, record.id)" />
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
          <template v-else-if="column.dataIndex === 'operations'">
            <a-button class="w-[80px] mb-[12px]" @click.stop="()=>{
              dict.temprary_object_for_edit = record
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
                v-if="dict.data_source.length"
                title="Sure to delete?"
                @confirm="functions.delete_an_object(record)"
              >
                <a-button class="w-[80px]">
                  {{ global_dict.t(`Delete`) }}
                </a-button>
              </a-popconfirm>
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

  <div class="h-[200px]"></div>

  <help_card></help_card>

  <a-button @click="async ()=>{
    await functions.get_invitation_code()
  }">{{ global_dict.t("Get invitation code") }}</a-button>

  <div class="page_bottom_space"></div>

  <Language_switch_selection></Language_switch_selection>
</template>

<style scoped lang="less">
.ant-card-bordered {
  border: 1px solid #f0f0f0;
  margin-bottom: 100px;
}

.editable-cell {
  position: relative;
  .editable-cell-text-wrapper {
    // padding-right: 24px;
    // padding: 5px 24px 5px 5px;
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


.page_bottom_space {
  height: 100px;
  .for_mobile({
    height: 50px;
  });
}
</style>