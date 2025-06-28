<script setup>
import { ref, onMounted, computed, defineProps } from "vue";
import Vue3Datatable from "@bhplugin/vue3-datatable";
import "@bhplugin/vue3-datatable/dist/style.css";
import { useEntityStore } from "@entity/store";
import { useUserStore } from "@user/store";
import Form from "@entity/FormComponent.vue";
import BareModal from "@/features/common/BareModal.vue";

const entityStore = useEntityStore();
const userStore = useUserStore();
const settings = userStore.getSettings;
const entities = computed(() => entityStore.getAllEntities);

onMounted(() => {
  loadEntities();
  if (props.id !== null) {
    viewEntity(props.id);
  }
});

const props = defineProps({
  id: {
    type: [String, null],
    required: false,
    default: null,
  },
});

const rows = ref(null);
const isModalOpen = ref(false);
const loading = ref(true);
const mode = ref("");
const entity_id = ref("");
const name = ref("");

const cols =
  ref([
    { field: "name", title: "Nome" },
    { field: "email", title: "E-Mail" },
    { field: "type_tag", title: "Tipo" },
    { field: "document", title: "Documento" },
    { field: "status", title: "Ativo" },
    { field: "actions", title: "Actions" },
  ]) || [];

function viewEntity(id) {
  entity_id.value = id;
  name.value = entity.getEntity(id);
  isModalOpen.value = true;
  mode.value = "show";
}
function createEntity() {
  isModalOpen.value = true;
  mode.value = "create";
}

function loadEntities() {
  loading.value = true;
  const entityArray = computed(() =>
    Object.entries(entities).map(([id, entity]) => ({
      id,
      ...entity,
    })),
  );
  rows.value = entityArray.value.entity;

  loading.value = false;
}
function closeModal() {
  isModalOpen.value = false;
}
async function deleteEntity(id) {
  try {
    await api.delete(`${route}/${id}`);
    entityStore.removeEntity(id);
  } catch {
    alert(`Falha na tentativa de deletar`);
  }
}
</script>
<template>
  <p>Hello from Entity</p>
  <div>
    <div class="flex items-center justify-between mb-5">
      <h2 class="text-3xl">{{ setting.entity_title }}</h2>
      <button class="btn btn-outline-secondary d-grid gap-2" @click="createEntity()">
        <span>&#10133;</span> Adicionar nov(a) {{ settings.entity_title }}
      </button>
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
  <BareModal v-if="isModalOpen" :title="name" @close="closeModal">
    <Form :entity="entity_id" :mode="mode"></Form>
  </BareModal>
</template>
