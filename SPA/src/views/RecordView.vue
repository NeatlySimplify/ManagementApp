<script setup>
  import { ref, onMounted, computed, defineProps, watch } from 'vue'
  import { useRecordStore } from '@/features/records/store'
  import { useRouter } from 'vue-router'
  import { useUserStore } from '@/features/user/store'
  import { useMovementStore } from '@/features/movement/store'
  import FormComponent from '@/features/records/FormComponent.vue'
  import BareModal from '@/features/common/BareModal.vue'
  import DataTableComponent from '@/features/common/DataTableComponent.vue'
  import FormSelectComponent from '@/features/common/FormSelectComponent.vue'
  import FormRadioComponent from '@/features/common/FormRadioComponent.vue'

  const router = useRouter()
  const recordStore = useRecordStore()
  const userStore = useUserStore()
  const setting = userStore.getSettings
  const movementStore = useMovementStore

  onMounted(() => {
    loadRecord()
    if (props.id !== null) {
      viewRecord(props.id)
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
    filter: {
      type: String,
      required: false,
      default: 'all',
    },
    term: {
      type: [String],
      required: false,
      default: '',
    },
    status: {
      type: Boolean,
      required: false,
      default: true,
    },
  })

  const filter_string = ref(props.filterStr)

  const term_string = ref(props.term)
  const status_filter = ref(props.status)

  const rows = ref(null)
  const isModalOpen = ref(false)
  const loading = ref(true)
  const mode = ref('')
  const name = ref('')
  const record_id = ref('')

  const cols =
    ref([
      { field: 'name', title: 'Nome' },
      { field: 'type_tag', title: 'Tipo' },
      { field: 'status', title: 'Ativo' },
      { field: 'optional_status', title: 'Status' },
      { field: 'service_id', title: 'ID' },
      { field: 'actions', title: 'Actions' },
    ]) || []

  function viewRecord(id) {
    record_id.value = id
    name.value = recordStore.getRecord(id).name
    isModalOpen.value = true
    mode.value = 'show'
  }
  function createRecord() {
    isModalOpen.value = true
    mode.value = 'create'
  }

  function loadRecord() {
    if (filter_string.value === 'all') {
      rows.value = computed(() => recordStore.getAllRecords)
    } else if (filter_string.value === 'status') {
      rows.value = computed(() => recordStore.getRecordsByStatus(status_filter.value))
    } else {
      rows.value = computed(() => recordStore.getRecordsByType(term_string.value))
    }
    loading.value = false
  }

  function closeModal() {
    isModalOpen.value = false
    if (props.back) {
      router.back()
    }
  }
  function deleteRecord(id) {
    movementStore.removeRecord(id)
  }

  watch(filter_string, loadRecord, { immediate: true })
</script>
<template>
  <div>
    <div class="flex items-center justify-between mb-5">
      <h2 class="text-3xl">
        {{ settings.record_title }}
      </h2>
      <button
        class="btn btn-outline-secondary d-grid gap-2"
        @click="createRecord()"
      >
        <span>&#10133;</span> Adicionar novo(a) {{ settings.record_title }}
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
          v-model="filter_string"
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
          v-model="filter_string"
          type="radio"
          class="btn-check"
          value="status"
          autocomplete="off"
        />
        <label
          class="btn btn-outline-primary"
          for="btnradio2"
          >Por Status</label
        >

        <input
          id="btnradio2"
          v-model="filter_string"
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
      v-if="filter_string === 'status'"
      class="row"
    >
      <FormRadioComponent
        v-model:placeholder="status_filter"
        :title="'Status de ' + setting.record_title"
        :is-read-only="false"
      />
    </div>
    <div
      v-if="filter_string === 'type'"
      class="row"
    >
      <FormSelectComponent
        v-model:placeholder="term_string"
        :title="'Tipos de ' + setting.record_title"
        :is-read-only="false"
        :types="setting.record_types"
        options
      />
      <button
        class="btn btn-primary"
        @click="loadRecord"
      >
        Pesquisar
      </button>
    </div>
    <DataTableComponent
      v-model:rows="rows"
      v-model:cols="cols"
      v-model:loading="loading"
      v-model:route="route"
      @delete_="deleteRecord"
    />
  </div>
  <BareModal
    v-if="isModalOpen"
    :title="name"
    @close="closeModal"
  >
    <FormComponent
      :id="record_id"
      :mode="mode"
      @close="closeModal"
    />
  </BareModal>
</template>
