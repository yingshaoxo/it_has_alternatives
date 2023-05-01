<script setup lang="ts">
import { onMounted, reactive, ref, UnwrapRef } from 'vue';

import * as it_has_alternatives_objects from '../../generated_yrpc/it_has_alternatives_objects'

import { global_dict, global_functions } from '../../store'

import { UploadOutlined } from '@ant-design/icons-vue';
import message from 'ant-design-vue/lib/message';

const dict = reactive({
  upload_file_list: []
})

const functions = {
  download_base64_file: (base64Data: string, fileName: string) => {
     const linkSource = `data:application/octet-stream;base64,${base64Data}`;
     const downloadLink = document.createElement("a");
     downloadLink.href = linkSource;
     downloadLink.download = fileName;
     downloadLink.click();
  },
  download_backup_zip_file: async () => {
    var request = new it_has_alternatives_objects.Download_backup_data_request()
    var result = await global_dict.admin_client.download_backup_data(
      request
    )
    if (result?.file_bytes_in_base64_format) {
      functions.download_base64_file(result?.file_bytes_in_base64_format, result?.file_name??'backup.zip')
    }
  },
  upload_backup_zip_file: async (base64_file_string: string) => {
    var request = new it_has_alternatives_objects.Upload_backup_data_request()
    request.file_bytes_in_base64_format = base64_file_string
    var result = await global_dict.admin_client.upload_backup_data(
      request
    )
    if (result?.success) {
      message.success(`File uploaded successfully`);
    } else {
      message.error(`File upload failed`);
    }
  },
  file_to_base64: async (a_file: File) => {
    let a_function = 
      (file: File) => new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = () => {
          let base64_string = String(reader.result).split(",")[1]
          resolve(base64_string)
        };
        reader.onerror = error => reject(error);
      })
      return (await a_function(a_file) as string)
  },
  handle_local_before_file_upload: async (file: any) => {
    let file_object = file
    let base64_string = await functions.file_to_base64(file_object)
    await functions.upload_backup_zip_file(base64_string) 
    return true
  },
}

onMounted(async () => {
})
</script>

<template>
  <div class="flex flex-col justify-center items-center">
    <div class="mt-[30px] mb-[50px]">hi, admin!</div>

    <div
      class="flex flex-row"
    >
      <a-button 
        class="w-[250px] mr-[30px]"
        type="primary"
        @click="functions.download_backup_zip_file"
      >Download Backup Data</a-button>

      <a-upload
        accept=".zip"
        name="file"
        v-model:file-list="dict.upload_file_list"
        :showUploadList="false"
        :customRequest="async () => { }"
        :beforeUpload="(file: File, filelist: any[]) => functions.handle_local_before_file_upload(file)"
      >
        <a-button
          class="w-[250px]"
        >
          <upload-outlined></upload-outlined>
          Click to Upload a Backup File
        </a-button>
      </a-upload>
    </div>
  </div>
</template>

<style scoped lang="less">
</style>