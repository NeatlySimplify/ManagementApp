<script setup>
  import { ref, onMounted, computed, defineProps, watch } from 'vue'
  import { useMovementStore } from '@/features/movement/store'
  import { useRouter } from 'vue-router'
  import { useUserStore } from '@/features/user/store'
  import MovementFormComponent from '@/features/movement/MovementFormComponent.vue'
  import BareModal from '@/features/common/BareModal.vue'
  import DataTableComponent from '@/features/common/DataTableComponent.vue'
  import DatePickerComponent from '@/features/common/DatePickerComponent.vue'

  const router = useRouter()
  const movementStore = useMovementStore()
  const userStore = useUserStore()
  const settings = userStore.getSettings
  const movement = ref({})

  onMounted(() => {
    loadMovement()
    if (props.id !== null) {
      viewMovement(props.id)
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
    term: {
      type: [String],
      required: false,
      default: 'all',
    },
  })

  const filter_term = ref('')
  const currentDate = ref(new Date())
  filter_term.value = ref(props.term)

  const rows = ref(null)
  const isModalOpen = ref(false)
  const loading = ref(true)
  const mode = ref('')
  const name = ref('')
  const movement_id = ref('')

  const cols =
    ref([
      { field: 'type_tag', title: 'Tipo' },
      { field: 'value', title: 'Valor' },
      { field: 'installment', title: 'Parcelas' },
      { field: 'actions', title: 'Actions' },
    ]) || []

  function viewMovement(id) {
    movement_id.value = id
    name.value = movementStore.getMovement(id).name
    isModalOpen.value = true
    mode.value = 'show'
  }
  function createMovement() {
    isModalOpen.value = true
    mode.value = 'create'
  }

  function loadMovement() {
    loading.value = true
    if (filter_term.value === 'all' || filter_term.value === null) {
      movement.value = computed(() => movementStore.getAllMovement)
    } else {
      movement.value = computed(() => movementStore.getActiveMovement(currentDate))
    }
    rows.value = movement.value
    loading.value = false
  }

  function closeModal() {
    isModalOpen.value = false
    if (props.back) {
      router.back()
    }
  }
  function deleteMovement(id) {
    movementStore.removeMovement(id)
  }

  watch(filter_term, loadMovement, { immediate: true })
</script>
<template>
  <div class="row">
    <div class="flex items-center justify-between mb-5">
      <h2 class="text-3xl">
        {{ settings.movement_title }}
      </h2>
      <button
        class="btn btn-outline-secondary d-grid gap-2"
        @click="createMovement()"
      >
        <span>&#10133;</span> Adicionar novo(a) {{ settings.movement_title }}
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
          v-model="filter_term"
          type="radio"
          class="btn-check"
          name="btnradio"
          value="all"
          autocomplete="off"
        />
        <label
          class="btn btn-outline-primary"
          for="btnradio1"
          >Ver Todos</label>

        <input
          id="btnradio2"
          v-model="filter_term"
          type="radio"
          class="btn-check"
          name="btnradio"
          value="filter"
          autocomplete="off"
        />
        <label
          class="btn btn-outline-primary"
          for="btnradio2"
          >Ver Ativos na data de referencia</label>
      </div>
    </div>
    <div
      v-if="filter_term === 'filter'"
      class="row"
    >
      <DatePickerComponent v-model:current-date="currentDate" />
    </div>
    <DataTableComponent
      v-model:rows="rows"
      v-model:cols="cols"
      v-model:loading="loading"
      v-model:route="route"
      @delete_="deleteMovement"
    />
  </div>
  <BareModal
    v-if="isModalOpen"
    :title="name"
    @close="closeModal"
  >
    <MovementFormComponent
      :id="movement_id"
      :mode="mode"
      @close="closeModal"
    />
  </BareModal>
</template>
