<script setup>
  import { useUserStore } from '@/features/user/store'
  import { useMovementStore } from '@/features/movement/store'
  import { defineProps, defineEmits, BeforeMounted, ref } from 'vue'
  import FormInputComponent from '@/features/common/FormInputComponent.vue'
  import FormSelectComponent from '@/features/common/FormSelectComponent.vue'
  import FormRadioComponent from '@/features/common/FormRadioComponent.vue'
  import FormNumberComponent from '@/features/common/FormNumberComponent.vue'
  import FormSelectObjectComponent from '@/features/common/FormSelectObjectComponent.vue'

  BeforeMounted(async () => {
    if (props.mode === 'show' && props.id !== null) {
      payment.value = { ...movementStore.fetchPayment(props.id) }
    }
  })

  const emit = defineEmits(['close'])
  function close() {
    emit('close')
  }

  const props = defineProps({
    id: {
      type: [String, null],
      required: false,
      default: null,
    },
    mode: {
      type: String,
      default: 'show',
    },
  })

  const userStore = useUserStore()
  const movementStore = useMovementStore()
  const settings = userStore.getSettings

  const payment = ref({})

  const isReadOnly = ref(true)

  const setting = {
    title: settings.movement_title,
    expense: settings.movement_expense_types.sort(),
    income: settings.movement_income_types.sort(),
    cycles: settings.movement_cycle_types.sort(),
  }

  function changeMode() {
    isReadOnly.value = !isReadOnly.value
  }

  function handlerUpdate() {
    submitForm()
    changeMode()
  }

  function submitForm() {
    movementStore.updatePayment(payment.value)
  }

  function deletePayment(item) {
    movementStore.removePayment(item.id)
    close()
  }
</script>

<template>
  <div class="modal-header">
    <h5 class="modal-title">
      {{ movement.name }}
    </h5>
    <button
      type="button"
      class="btn-close"
      @click="close"
    >
      Sair
    </button>
  </div>
  <div class="modal-body">
    <div>
      <form @submit.prevent>
        <div v-if="props.mode !== 'show'">
          <FormInputComponent
            v-model:placeholder="payment.name"
            title="Nome"
            :is-read-only="true"
          />

          <FormInputComponent
            v-model:placeholder="payment.type_tag"
            title="Tipo"
            :is-read-only="true"
          />

          <FormRadioComponent
            v-model:placeholder="payment.ignore_in_totals"
            title="Ignore no balanço da conta"
            :is-read-only="isReadOnly"
          />

          <FormNumberComponent
            v-model:placeholder="payment.value"
            :title="'Todal de ' + setting.title"
            :is-read-only="isReadOnly"
          />

          <FormInputComponent
            v-model:placeholder="payment.payment_date"
            title="Data de Pagamento"
            :is-read-only="isReadOnly"
            type="date"
          />

          <FormInputComponent
            v-model:placeholder="payment.is_due"
            title="Data de Vencimento"
            :is-read-only="isReadOnly"
            type="date"
          />

          <FormSelectComponent
            v-model:placeholder="payment.category"
            title="Categoria"
            :is-read-only="isReadOnly"
            :types="
              movement.type_tag === 'Entrada' || movement.type_tag === 'income'
                ? setting.income
                : setting.expense
            "
          />

          <FormRadioComponent
            v-model:placeholder="payment.status"
            title="Status"
            :is-read-only="isReadOnly"
          />

          <FormSelectObjectComponent
            v-model:placeholder="payment.bank_account"
            title="Conta Bancária Default"
            :object="userStore.getAllAccounts"
          />
        </div>
        <button
          v-if="isReadOnly"
          type="button"
          class="btn btn-secondary"
          @click="changeMode()"
        >
          Editar
        </button>
        <button
          v-else
          type="submit"
          class="btn btn-secondary"
          @click="handlerUpdate()"
        >
          Salvar
        </button>
        <button
          type="button"
          class="btn btn-danger"
          @click="deletePayment()"
        >
          Excluir
        </button>
      </form>
    </div>
  </div>
  <div class="modal-footer">
    <button
      type="button"
      class="btn btn-primary"
      @click="close"
    >
      Sair
    </button>
  </div>
</template>
