<script setup>
import { ref } from "vue";
import Vue3Datatable from "@bhplugin/vue3-datatable";
import "@bhplugin/vue3-datatable/dist/style.css";
import { useEntityStore } from "@/stores/entity";
import EntityForm from "@/components/entity/EntityForm.vue";}

const entityStore = useEntityStore();

const entities = computed(() => entityStore.getAllEntities);

const loading = ref(true);
const change = ref(false);

const rows = ref(null);

function viewEntity(id) {
  router.push(`entity/${id}`);
}

const cols =
  ref([
    { field: "name", title: "Nome" },
    { field: "email", title: "E-Mail" },
    { field: "type_entity", title: "Tipo" },
    { field: "govt_id", title: "Documento" },
    { field: "address.city", title: "Cidade" },
    { field: "status", title: "Ativo" },
    { field: "actions", title: "Actions" },
  ]) || [];

const loadEntities = () => {
  loading.value = true;
  const entityArray = computed(() =>
    Object.entries(entities).map(([id, entity]) => ({
      id, // include id if needed by table
      ...entity,
    })),
  );
  rows.value = entityArray.value.entity;

  loading.value = false;
};
onMounted(() => {
  loadEntities();
});
</script>
<template>
  <div>
    <div class="flex items-center justify-between mb-5">
      <h2 class="text-3xl">{{ setting.entity_title }}</h2>
    </div>

    <vue3-datatable
      :rows="rows"
      :columns="cols"
      :loading="loading"
      :sortable="true"
      :columnFilter="true"
    >
      <template #actions="data">
        <div class="flex gap-4">
          <button type="button" class="btn btn-success !py-1" @click="viewEntity(data.id)">
            Ver Mais!
          </button>
          <button type="button" class="btn btn-danger !py-1" @click="deleteEntity(data.id)">
            Excluir
          </button>
        </div>
      </template>
    </vue3-datatable>
  </div>
  <EntityForm >
</template>
