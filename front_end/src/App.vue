<script setup lang="ts">
import { reactive } from 'vue';
import * as it_has_alternatives_objects from './generated_yrpc/it_has_alternatives_objects'
import * as it_has_alternatives_rpc from './generated_yrpc/it_has_alternatives_rpc'

var dict = reactive({
  client: new it_has_alternatives_rpc.Client_it_has_alternatives("http://127.0.0.1:80"),
  name: "yingshaoxo",
  a_list_of_objects: [] as it_has_alternatives_objects.An_Object[],
  on_add_button_click: async () => {
    var an_object = new it_has_alternatives_objects.An_Object()
    console.log(dict.name)
    an_object.from_dict({
      name: dict.name,
      id: "1",
      description: null,
      likes: 3,
      dislikes: 4,
      alternative_id_list: ["1", "2"]
    })
    var request = new it_has_alternatives_objects.Add_Object_Request()
    request.an_object = an_object
    var result = await dict.client.add_alternative(
      request
    )
    console.log(result)
  },
  refresh_list: async () => {
    var request = new it_has_alternatives_objects.Search_Alternative_Request()
    request.key_words = "yi"
    request.page_number = 0
    request.page_size = 20
    var result = await dict.client.search_alternatives(
      request
    )
    dict.a_list_of_objects = result?.alternative_object_list ?? []
  },
  on_delete_button_click: async (the_object: it_has_alternatives_objects.An_Object) => {
    var request = new it_has_alternatives_objects.Delete_Object_Request()
    request.an_object = the_object
    var result = await dict.client.delete_alternative(
      request
    )
  },
})
</script>

<template>
  <input  @input="event => dict.name = event?.target?.value ?? ''" >
  <button @click="dict.on_add_button_click">Add</button>
  <button @click="dict.refresh_list">Refresh</button>

  <br/>
  <br/>
  <p> -------- </p>
  <br/>
  <br/>

  <li v-for="object in dict.a_list_of_objects">
    {{ object.name }}
    <button @click="dict.on_delete_button_click(object)">Delete</button>
  </li>
</template>

<style scoped>
.logo {
  height: 6em;
  padding: 1.5em;
  will-change: filter;
  transition: filter 300ms;
}
.logo:hover {
  filter: drop-shadow(0 0 2em #646cffaa);
}
.logo.vue:hover {
  filter: drop-shadow(0 0 2em #42b883aa);
}
</style>
