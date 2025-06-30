<script setup>
import { ref, onMounted, computed } from "vue";
import Vue3Datatable from "@bhplugin/vue3-datatable";
import "@bhplugin/vue3-datatable/dist/style.css";
import { useRecordStore } from "@records/store";
import { useUserStore } from "@/features/user/store";
// import Form from "@record/FormComponent.vue";
// import BareModal from "@/features/common/BareModal.vue";

const recordStore = useRecordStore();
const userStore = useUserStore();

const settings = userStore.getSettings;
const records = computed(() => recordStore.getAllRecords);

onMounted(() => {
  loadRecords();
  if (props.id !== null) {
    viewRecord(props.id);
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
const record_id = ref("");
const name = ref("");

const cols =
  ref([
    { field: "name", title: "Nome" },
    { field: "service_id", title: "ID" },
    { field: "type_tag", title: "Tipo" },
    { field: "status", title: "Ativo" },
    { field: "optional_status", title: "Status" },
    { field: "actions", title: "Actions" },
  ]) || [];

function viewRecord(id) {
  entity_id.value = id;
  name.value = entity.getRecord(id);
  isModalOpen.value = true;
  mode.value = "show";
}
function createRecord() {
  isModalOpen.value = true;
  mode.value = "create";
}

function loadRecords() {
  loading.value = true;
  const recordsArray = computed(() =>
    Object.entries(records).map(([id, record]) => ({
      id,
      ...record,
    })),
  );
  rows.value = recordsArray.value.record;

  loading.value = false;
}
function closeModal() {
  isModalOpen.value = false;
}
async function deleteRecord(id) {
  try {
    await api.delete(`record/${id}`);
    recordStore.removeRecord(id);
  } catch {
    alert(`Falha na tentativa de deletar`);
  }
}
</script>
<template>
  <p>Hello from Records</p>
  <div>
    <div class="flex items-center justify-between mb-5">
      <h2 class="text-3xl">{{ setting.record_title }}</h2>
      <button class="btn btn-outline-secondary d-grid gap-2" @click="createRecord()">
        <span>&#10133;</span> Adicionar nov(a) {{ settings.record_title }}
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
          <button type="button" class="btn btn-success !py-1" @click="viewRecord(data.id)">
            Ver Mais!
          </button>
          <button type="button" class="btn btn-danger !py-1" @click="deleteRecord(data.id)">
            Excluir
          </button>
        </div>
      </template>
    </vue3-datatable>
  </div>
  <!-- <BareModal v-if="isModalOpen" :title="name" @close="closeModal">
    <Form :id="record_id" :mode="mode"></Form>
  </BareModal> -->
</template>
