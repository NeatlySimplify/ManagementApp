<script setup>
import { useUserStore } from "@/features/user/store";
import { useMovementStore } from "@/features/movement/store";
import { defineProps, defineEmits } from "vue";
import FormInputComponent from "@/features/common/FormInputComponent.vue";
import FormSelectComponent from "@/features/common/FormSelectComponent.vue";
import FormRadioComponent from "@/features/common/FormRadioComponent.vue";
import FormNumberComponent from "@/features/common/FormNumberComponent.vue";
import FormSelectObjectComponent from "@/features/common/FormSelectObjectComponent.vue";

BeforeMounted(async () => {
  if (props.mode === "show" && props.id !== null) {
    payment.value = { ...movementStore.fetchPayment(props.id) };
  }
});

const emit = defineEmits(["close"]);
function close() {
  emit("close");
}

const props = defineProps({
  id: {
    type: [String, null],
    required: false,
  },
  mode: {
    type: String,
    default: "show",
  },
});

const userStore = useUserStore();
const movementStore = useMovementStore();
const settings = userStore.getSettings;

const payment = ref({});

const isReadOnly = ref(true);

const setting = {
  title: settings.movement_title,
  expense: settings.movement_expense_types.sort(),
  income: settings.movement_income_types.sort(),
  cycles: settings.movement_cycle_types.sort(),
};

function changeMode() {
  isReadOnly.value = !isReadOnly.value;
}

function handlerUpdate() {
  submitForm();
  changeMode();
}

function submitForm() {
  movementStore.updatePayment(payment.value);
}

function deletePayment(item) {
  movementStore.removePayment(item.id);
  close();
}
</script>

<template>
  <div class="modal-header">
    <h5 class="modal-title">{{ movement.name }}</h5>
    <button type="button" class="btn-close" @click="close">Sair</button>
  </div>
  <div class="modal-body">
    <div>
      <form @submit.prevent>
        <div v-if="props.mode !== 'show'">
          <FormInputComponent
            title="Nome"
            v-model:placeholder="payment.name"
            :isReadOnly="true"
          ></FormInputComponent>

          <FormInputComponent
            title="Tipo"
            v-model:placeholder="payment.type_tag"
            :isReadOnly="true"
          ></FormInputComponent>

          <FormRadioComponent
            title="Ignore no balanço da conta"
            v-model:placeholder="payment.ignore_in_totals"
            :isReadOnly="isReadOnly"
          ></FormRadioComponent>

          <FormNumberComponent
            :title="'Todal de ' + setting.title"
            v-model:placeholder="payment.value"
            :isReadOnly="isReadOnly"
          ></FormNumberComponent>

          <FormInputComponent
            title="Data de Pagamento"
            v-model:placeholder="payment.payment_date"
            :isReadOnly="isReadOnly"
            type="date"
          ></FormInputComponent>

          <FormInputComponent
            title="Data de Vencimento"
            v-model:placeholder="payment.is_due"
            :isReadOnly="isReadOnly"
            type="date"
          ></FormInputComponent>

          <FormSelectComponent
            title="Categoria"
            :isReadOnly="isReadOnly"
            v-model:placeholder="payment.category"
            :types="
              movement.type_tag === 'Entrada' || movement.type_tag === 'income'
                ? setting.income
                : setting.expense
            "
          ></FormSelectComponent>

          <FormRadioComponent
            title="Status"
            :isReadOnly="isReadOnly"
            v-model:placeholder="payment.status"
          ></FormRadioComponent>

          <FormSelectObjectComponent
            title="Conta Bancária Default"
            :object="userStore.getAllAccounts"
            v-model:placeholder="payment.bank_account"
          ></FormSelectObjectComponent>
        </div>
        <button type="button" v-if="isReadOnly" @click="changeMode()" class="btn btn-secondary">
          Editar
        </button>
        <button type="submit" v-else @click="handlerUpdate()" class="btn btn-secondary">
          Salvar
        </button>
        <button type="button" @click="deletePayment()" class="btn btn-danger">Excluir</button>
      </form>
    </div>
  </div>
  <div class="modal-footer">
    <button type="button" class="btn btn-primary" @click="close">Sair</button>
  </div>
</template>
