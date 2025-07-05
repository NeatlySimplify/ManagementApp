<script setup>
import { ref, onMounted, computed, defineProps } from "vue";
import { useEntityStore } from "@/features/entity/store";
import { useRouter } from "vue-router";
import { useUserStore } from "@/features/user/store";
import Form from "@/features/entity/FormComponent.vue";
import BareModal from "@/features/common/BareModal.vue";
import DataTableComponent from "@/features/common/DataTableComponent.vue";

const router = useRouter();
const entityStore = useEntityStore();
const userStore = useUserStore();
const settings = userStore.getSettings;
const entities = computed(() => entityStore.getAllEntities);
const route = ref("/entity");

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
  back: {
    type: Boolean,
    required: false,
    default: false,
  },
  filter: {
    type: [String, null],
    required: false,
    default: null,
  },
  term: {
    type: [Boolean, String, null],
    required: false,
    default: null,
  },
});

const rows = ref(null);
const isModalOpen = ref(false);
const loading = ref(true);
const mode = ref("");
const name = ref("");
const entity_id = ref("");

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
  name.value = entityStore.getEntity(id).name;
  isModalOpen.value = true;
  mode.value = "show";
}
function createEntity() {
  isModalOpen.value = true;
  mode.value = "create";
}

function loadEntities() {
  loading.value = true;
  let entityArray = null;
  if (props.filter == "status") {
    entityArray = entityStore.getEntitiesByStatus(props.term);
  } else if (props.filter === "type_tag") {
    entityArray = entityStore.getEntitiesByType(props.term);
  } else {
    entityArray = entities.value;
  }
  rows.value = entityArray.value.entity;

  loading.value = false;
}
function closeModal() {
  isModalOpen.value = false;
  if (props.back) {
    router.back();
  }
}
async function deleteEntity(id) {
  try {
    await api.delete(`${route.value}/${id}`);
    entityStore.removeEntity(id);
  } catch {
    alert(`Falha na tentativa de deletar`);
  }
}
</script>
<template>
  <div>
    <div class="flex items-center justify-between mb-5">
      <h2 class="text-3xl">{{ settings.entity_title }}</h2>
      <button class="btn btn-outline-secondary d-grid gap-2" @click="createEntity()">
        <span>&#10133;</span> Adicionar novo(a) {{ settings.entity_title }}
      </button>
    </div>
    <DataTableComponent
      v-model:rows="rows"
      v-model:cols="cols"
      v-model:loading="loading"
      v-model:route="route"
      @delete_="deleteEntity"
    >
    </DataTableComponent>
  </div>
  <BareModal v-if="isModalOpen" :title="name" @close="closeModal">
    <Form :entity="entity_id" :mode="mode" @close="closeModal"></Form>
  </BareModal>
</template>
