<script setup>
import Vue3Datatable from "@bhplugin/vue3-datatable";
import "@bhplugin/vue3-datatable/dist/style.css";
import { defineModel, defineEmits } from "vue";
import { useRouter } from "vue-router";

const rows = defineModel("rows");
const cols = defineModel("cols");
const loading = defineModel("loading");
const route = defineModel("route");

const deleteData = defineEmits("delete_");

function delete_resource(id) {
  deleteData("delete_", id);
}

function openToggle(id) {
  const router = useRouter();
  router.push(`${route.value}/${id}`);
}
</script>
<template>
  <vue3-datatable
    :rows="rows"
    :columns="cols"
    :loading="loading"
    :sortable="true"
    :columnFilter="true"
  >
    <template #actions="data">
      <div class="flex gap-4">
        <button type="button" class="btn btn-success !py-1" @click="openToggle(data.id)">
          Ver Mais!
        </button>
        <button type="button" class="btn btn-danger !py-1" @click="delete_resource(data.id)">
          Excluir
        </button>
      </div>
    </template>
  </vue3-datatable>
</template>
