<script setup>
import { ref, onMounted, computed } from "vue";
import Vue3Datatable from "@bhplugin/vue3-datatable";
import "@bhplugin/vue3-datatable/dist/style.css";
import { useEntityStore } from "@entity/store";
import Form from "@entity/FormComponent.vue";
import BareModal from "@/features/BareModal.vue";

const entityStore = useEntityStore();

const entities = computed(() => entityStore.getAllEntities);

const loading = ref(true);

const rows = ref(null);
const isModalOpen = ref(false);

function viewEntity(id) {
  entityId.value = id;
  entityData.value = entityStore.getEntity(id);
  isModalOpen.value = true; // Open the modal
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
const closeModal = () => {
  isModalOpen.value = false;
};
</script>
<template>
  <p>Hello from Entity</p>
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
  <BareModal :isOpen="isModalOpen" :title="Entity" @close="closeModal">
    <Form entity="id" mode="show" @change="value"></Form>
  </BareModal>
</template>
