<script setup>
  import { useUserStore } from '@/features/user/store'
  import { useMovementStore } from '@/features/movement/store'
  import { defineProps, defineEmits, BeforeMounted, ref } from 'vue'
  import NotesComponent from '@/features/common/NotesComponent.vue'
  import FormInputComponent from '@/features/common/FormInputComponent.vue'
  import FormSelectComponent from '@/features/common/FormSelectComponent.vue'
  import FormRadioComponent from '@/features/common/FormRadioComponent.vue'
  import FormNumberComponent from '@/features/common/FormNumberComponent.vue'
  import FormSelectObjectComponent from '@/features/common/FormSelectObjectComponent.vue'
  import PaymentTableComponent from '@/features/common/PaymentTableComponent.vue'
  import { useRecordStore } from '@/features/records/store'

  BeforeMounted(async () => {
    if (props.mode === 'show' && props.id !== null) {
      movement.value = { ...movementStore.fetchMovement(props.id) }
      changeMode()
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
  const recordStore = useRecordStore()
  const settings = userStore.getSettings

  const movement = ref({})

  const isReadOnly = ref(true)

  const setting = {
    title: settings.movement_title,
    expense: settings.movement_expense_types.sort(),
    types: settings.movement_types.sort(),
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

  function deleteMovement() {
    movementStore.removeMovement(movement.value.id)
    close()
  }
  function submitForm() {
    if (props.mode === 'create') {
      if (recordStore.placeholder !== '') {
        movement.value.record = recordStore.placeholder
        recordStore.placeholder = ''
        movementStore.createMovement(movement.value)
      }
      if (!movement.value.bank_account) {
        movement.value.bank_account = setting.default_bank_account
      }
      movementStore.createMovement(movement.value)
    } else {
      movementStore.updateMovement(movement.value)
    }
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
            v-model:placeholder="movement.name"
            title="Nome"
            :required="true"
            :is-read-only="isReadOnly"
          />

          <FormSelectComponent
            v-model:placeholder="movement.type_tag"
            :title="'Tipos de ' + setting.title"
            :required="true"
            :types="setting.types"
          />

          <FormSelectComponent
            v-model:placeholder="movement.cycle"
            :title="'Intervalo de Parcelas de ' + setting.title"
            :required="true"
            :types="setting.cycles"
          />

          <FormNumberComponent
            v-if="movement.cycle === 'Personalizado'"
            v-model:placeholder="movement.unique"
            title="Intervalo de Tempo Personalizado"
            min="2"
            max="360"
            step="1"
            :is-read-only="isReadOnly"
          />

          <FormNumberComponent
            v-model:placeholder="movement.parts"
            title="Numero de Parcelas"
            min="1"
            max="120"
            step="1"
            :required="true"
            :is-read-only="isReadOnly"
          />

          <FormRadioComponent
            v-model:placeholder="movement.ignore_in_totals"
            title="Ignore no balanço da conta"
            :is-read-only="isReadOnly"
          />

          <FormNumberComponent
            v-model:placeholder="movement.total"
            :title="'Todal de ' + setting.title"
            min="0"
            step="0.01"
            :is-read-only="isReadOnly"
          />

          <FormInputComponent
            v-model:placeholder="movement.payment_date"
            title="Primeira data de Pagamento"
            :is-read-only="isReadOnly"
            type="date"
          />

          <FormInputComponent
            v-model:placeholder="movement.is_due"
            title="Primeira data de Vencimento"
            :is-read-only="isReadOnly"
            :required="true"
            type="date"
          />

          <FormSelectComponent
            v-model:placeholder="movement.category"
            title="Categoria"
            :is-read-only="isReadOnly"
            :types="
              movement.type_tag === 'Entrada' || movement.type_tag === 'income'
                ? setting.income
                : setting.expense
            "
          />

          <FormRadioComponent
            v-model:placeholder="movement.status"
            title="Status"
            :is-read-only="isReadOnly"
          />

          <FormSelectObjectComponent
            v-model:placeholder="movement.bank_account"
            title="Conta Bancária Default"
            :object="userStore.getAllAccounts"
          />
        </div>
        <NotesComponent
          :notes="movement.notes"
          :is-read-only="isReadOnly"
        />
        <div v-if="isReadOnly">
          <br />
          <PaymentTableComponent v-model:payments="movement.payment" />
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
          @click="deleteMovement()"
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
