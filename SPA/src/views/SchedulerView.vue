<script setup>
  import { ref, onMounted, computed, defineProps } from 'vue'
  import { useSchedulerStore } from '@/features/scheduler/store'
  import { useRouter } from 'vue-router'
  import { useUserStore } from '@/features/user/store'
  import Form from '@/features/scheduler/FormComponent.vue'
  import BareModal from '@/features/common/BareModal.vue'
  import DataTableComponent from '@/features/common/DataTableComponent.vue'
  import CalendarComponent from '@/features/common/CalendarComponent.vue'
  import FormSelectComponent from '@/features/common/FormSelectComponent.vue'

  const router = useRouter()
  const schedulerStore = useSchedulerStore()
  const userStore = useUserStore()
  const settings = userStore.getSettings
  const currentDate = ref(new Date())

  onMounted(() => {
    loadScheduler()
    if (props.id !== null) {
      viewScheduler(props.id)
    }
  })

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
    filterStr: {
      type: [String, null],
      required: false,
      default: null,
    },
    term: {
      type: [Boolean, String, null],
      required: false,
      default: null,
    },
  })
  const filterStr = ref(props.filterStr)
  const term = ref(props.term)
  const rows = ref(null)
  const isModalOpen = ref(false)
  const loading = ref(true)
  const mode = ref('')
  const name = ref('')
  const scheduler_id = ref('')
  const view_string = ref('calendar')

  const cols =
    ref([
      { field: 'name', title: 'Nome' },
      { field: 'type_tag', title: 'Tipo' },
      { field: 'status', title: 'Ativo' },
      { field: 'date_beginning', title: 'Data de Iníncio' },
      { field: 'date_ending', title: 'Data de Fim' },
      { field: 'actions', title: 'Actions' },
    ]) || []

  function viewScheduler(id) {
    scheduler_id.value = id
    name.value = schedulerStore.getEvent(id)
    isModalOpen.value = true
    mode.value = 'show'
  }
  function createScheduler() {
    isModalOpen.value = true
    mode.value = 'create'
  }

  function loadScheduler() {
    if (
      filterStr.value === 'all' ||
      (filterStr.value !== 'all' && view_string.value === 'calendar')
    ) {
      rows.value = computed(() => schedulerStore.getMonthlyEvents(currentDate.value))
    } else {
      rows.value = computed(() => schedulerStore.getEventByType(term.value))
    }
    loading.value = false
  }
  function closeModal() {
    isModalOpen.value = false
    if (props.back) {
      router.back()
    }
  }
  async function deleteScheduler(id) {
    schedulerStore.removeScheduler(id)
  }
</script>
<template>
  <div>
    <div class="flex items-center justify-between mb-5">
      <h2 class="text-3xl">
Evento
</h2>
      <button
        class="btn btn-outline-secondary d-grid gap-2"
        @click="createScheduler()"
      >
        <span>&#10133;</span> Adicionar novo Evento
      </button>
    </div>
    <div>
      <div class="flex items-center justify-between mb-5">
        <h2 class="text-3xl">
Evento
</h2>
        <button
          class="btn btn-outline-secondary d-grid gap-2"
          @click="createScheduler()"
        >
          <span>&#10133;</span> Adicionar novo Evento
        </button>
      </div>
      <div class="row">
        <div
          class="btn-group"
          role="group"
          aria-label="Basic radio toggle button group"
        >
          <input
            id="btnradio1"
            v-model="view_string"
            type="radio"
            class="btn-check"
            value="lista"
            autocomplete="off"
          />
          <label
            class="btn btn-outline-primary"
            for="btnradio1"
            >Lista</label
          >
          <input
            id="btnradio2"
            v-model="view_string"
            type="radio"
            class="btn-check"
            value="calendar"
            autocomplete="off"
          />
          <label
            class="btn btn-outline-primary"
            for="btnradio2"
            >Calendário</label
          >
        </div>
      </div>
      <div v-if="view_string === 'lista'">
        <div class="row">
          <div
            class="btn-group"
            role="group"
            aria-label="Basic radio toggle button group"
          >
            <input
              id="btnradio1"
              v-model="filterStr"
              type="radio"
              class="btn-check"
              value="all"
              autocomplete="off"
            />
            <label
              class="btn btn-outline-primary"
              for="btnradio1"
              >Todos</label
            >
            <input
              id="btnradio2"
              v-model="filterStr"
              type="radio"
              class="btn-check"
              value="type"
              autocomplete="off"
            />
            <label
              class="btn btn-outline-primary"
              for="btnradio2"
              >Por Tipo</label
            >
          </div>
        </div>
        <div
          v-if="filterStr === 'type'"
          class="row"
        >
          <FormSelectComponent
            v-model:placeholder="term"
            title="Tipos de Eventos"
            :is-read-only="false"
            :types="settings.scheduler_types"
            options
          />
          <button
            class="btn btn-primary"
            @click="loadScheduler"
          >
            Pesquisar
          </button>
        </div>
        <DataTableComponent
          v-model:rows="rows"
          v-model:cols="cols"
          v-model:loading="loading"
          v-model:route="route"
          @delete_="deleteScheduler"
        />
      </div>
      <div v-else>
        <CalendarComponent :limited="false" />
      </div>
    </div>
  </div>
  <BareModal
    v-if="isModalOpen"
    :title="name"
    @close="closeModal"
  >
    <Form
      :id="scheduler_id"
      :mode="mode"
      @close="closeModal"
    />
  </BareModal>
</template>
