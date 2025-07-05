<script setup>
import { ref, onMounted, computed, defineProps } from "vue";
import { useSchedulerStore } from "@/features/scheduler/store";
import { useRouter } from "vue-router";
import { useUserStore } from "@/features/user/store";
import Form from "@/features/scheduler/FormComponent.vue";
import BareModal from "@/features/common/BareModal.vue";
import DataTableComponent from "@/features/common/DataTableComponent.vue";
import CalendarComponent from "@/features/common/CalendarComponent.vue";

const router = useRouter();
const schedulerStore = useSchedulerStore();
const userStore = useUserStore();
const settings = userStore.getSettings;

onMounted(() => {
  loadScheduler();
  if (props.id !== null) {
    viewScheduler(props.id);
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
const view_string = ref("calendar");

const cols =
  ref([
    { field: "name", title: "Nome" },
    { field: "type_tag", title: "Tipo" },
    { field: "status", title: "Ativo" },
    { field: "date_beginning", title: "Data de Iníncio" },
    { field: "date_ending", title: "Data de Fim" },
    { field: "actions", title: "Actions" },
  ]) || [];

function viewScheduler(id) {
  entity_id.value = id;
  name.value = entity.getEntity(id);
  isModalOpen.value = true;
  mode.value = "show";
}
function createScheduler() {
  isModalOpen.value = true;
  mode.value = "create";
}

function loadRecord() {
  if (
    filter_string.value === "all" ||
    (filter_string.value !== "all" && view_string.value === "calendar")
  ) {
    rows.value = computed(() => schedulerStore.getMonthlyEvents(currentDate.value));
  } else {
    rows.value = computed(() => schedulerStore.getEventByType(term_string.value));
  }
  loading.value = false;
}
function closeModal() {
  isModalOpen.value = false;
  if (props.back) {
    router.back();
  }
}
async function deleteScheduler(id) {
  schedulerStore.removeScheduler(id);
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
    <div>
      <div class="flex items-center justify-between mb-5">
        <h2 class="text-3xl">{{ settings.entity_title }}</h2>
        <button class="btn btn-outline-secondary d-grid gap-2" @click="createScheduler()">
          <span>&#10133;</span> Adicionar novo(a) {{ settings.record_title }}
        </button>
      </div>
      <div class="row">
        <div class="btn-group" role="group" aria-label="Basic radio toggle button group">
          <input
            type="radio"
            class="btn-check"
            id="btnradio1"
            value="lista"
            v-model="view_string"
            autocomplete="off"
          />
          <label class="btn btn-outline-primary" for="btnradio1">Lista</label>
          <input
            type="radio"
            class="btn-check"
            id="btnradio2"
            value="calendar"
            v-model="view_string"
            autocomplete="off"
          />
          <label class="btn btn-outline-primary" for="btnradio2">Calendário</label>
        </div>
      </div>
      <div v-if="view_string === 'lista'">
        <div class="row">
          <div class="btn-group" role="group" aria-label="Basic radio toggle button group">
            <input
              type="radio"
              class="btn-check"
              id="btnradio1"
              value="all"
              v-model="filter_string"
              autocomplete="off"
            />
            <label class="btn btn-outline-primary" for="btnradio1">Todos</label>
            <input
              type="radio"
              class="btn-check"
              id="btnradio2"
              value="type"
              v-model="filter_string"
              autocomplete="off"
            />
            <label class="btn btn-outline-primary" for="btnradio2">Por Tipo</label>
          </div>
        </div>
        <div class="row" v-if="filter_string === 'type'">
          <FormSelectComponent
            title="Tipos de Eventos"
            v-model:placeholder="term_string"
            :isReadOnly="false"
            :types="setting.scheduler_types"
            options
          ></FormSelectComponent>
          <button class="btn btn-primary" @click="loadRecord">Pesquisar</button>
        </div>
        <DataTableComponent
          v-model:rows="rows"
          v-model:cols="cols"
          v-model:loading="loading"
          v-model:route="route"
          @delete_="deleteScheduler"
        >
        </DataTableComponent>
      </div>
      <div v-else>
        <CalendarComponent :limited="false"></CalendarComponent>
      </div>
    </div>
  </div>
  <BareModal v-if="isModalOpen" :title="name" @close="closeModal">
    <Form :entity="scheduler_id" :mode="mode" @close="closeModal"></Form>
  </BareModal>
</template>
