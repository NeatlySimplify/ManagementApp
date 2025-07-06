<script setup>
  import { ref, onMounted, computed, defineProps, watch } from 'vue'
  import { useMovementStore } from '@/features/movement/store'
  import { useRouter } from 'vue-router'
  import PaymentFormComponent from '@/features/movement/PaymentFormComponent.vue'
  import BareModal from '@/features/common/BareModal.vue'
  import DataTableComponent from '@/features/common/DataTableComponent.vue'
  import DatePickerComponent from '@/features/common/DatePickerComponent.vue'

  const router = useRouter()
  const movementStore = useMovementStore()
  const payments = ref({})

  onMounted(() => {
    loadPayment()
    if (props.id !== null) {
      viewPayment(props.id)
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
      default: 'Entrada',
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
  const payment_id = ref('')

  const cols =
    ref([
      { field: 'name', title: 'Nome' },
      { field: 'type_tag', title: 'Tipo' },
      { field: 'value', title: 'Valor' },
      { field: 'status', title: 'Status' },
      { field: 'payment_date', title: 'Data de Pagamento' },
      { field: 'is_due', title: 'Data de Vencimento' },
      { field: 'actions', title: 'Actions' },
    ]) || []

  function viewPayment(id) {
    payment_id.value = id
    name.value = movementStore.getPayment(id).name
    isModalOpen.value = true
    mode.value = 'show'
  }

  function loadPayment() {
    loading.value = true
    payments.value = rows.value = computed(() =>
      movementStore.getPaymentWindow(currentDate, filter_term)
    )
    loading.value = false
  }

  function closeModal() {
    isModalOpen.value = false
    if (props.back) {
      router.back()
    }
  }
  function deletePayment(id) {
    movementStore.removePayment(id)
  }

  watch(filter_term, loadPayment, { immediate: true })
</script>
<template>
  <div>
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
          value="Entrada"
          autocomplete="off"
        />
        <label
          class="btn btn-outline-primary"
          for="btnradio1"
          >Entrada</label>

        <input
          id="btnradio2"
          v-model="filter_term"
          type="radio"
          class="btn-check"
          value="Saída"
          autocomplete="off"
        />
        <label
          class="btn btn-outline-primary"
          for="btnradio2"
          >Saída</label>
      </div>
    </div>
    <div class="row">
      <DatePickerComponent v-model:current-date="currentDate" />
    </div>
    <DataTableComponent
      v-model:rows="rows"
      v-model:cols="cols"
      v-model:loading="loading"
      v-model:route="route"
      @delete_="deletePayment"
    />
  </div>
  <BareModal
    v-if="isModalOpen"
    :title="name"
    @close="closeModal"
  >
    <PaymentFormComponent
      :id="payment_id"
      :mode="mode"
      @close="closeModal"
    />
  </BareModal>
</template>
