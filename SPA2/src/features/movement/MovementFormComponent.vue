<script setup>
import { useUserStore } from "@/features/user/store";
import { useMovementStore } from "@/features/movement/store";
import { defineProps, defineEmits } from "vue";
import NotesComponent from "@/features/common/NotesComponent.vue";
import FormInputComponent from "@/features/common/FormInputComponent.vue";
import FormSelectComponent from "@/features/common/FormSelectComponent.vue";
import FormRadioComponent from "@/features/common/FormRadioComponent.vue";
import FormNumberComponent from "@/features/common/FormNumberComponent.vue";
import FormSelectObjectComponent from "@/features/common/FormSelectObjectComponent.vue";
import PaymentTableComponent from "@/features/common/PaymentTableComponent.vue";
import { useRecordStore } from "@/features/records/store";

BeforeMounted(async () => {
  if (props.mode === "show" && props.id !== null) {
    movement.value = { ...movementStore.fetchMovement(props.id) };
    changeMode();
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
const recordStore = useRecordStore();
const settings = userStore.getSettings;

const movement = ref({});

const isReadOnly = ref(true);

const setting = {
  title: settings.movement_title,
  expense: settings.movement_expense_types.sort(),
  types: settings.movement_types.sort(),
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

function deleteMovement() {
  movementStore.removeMovement(movement.value.id);
  close();
}
function submitForm() {
  if (props.mode === "create") {
    if (recordStore.placeholder !== "") {
      movement.value.record = recordStore.placeholder;
      recordStore.placeholder = "";
      movementStore.createMovement(movement.value);
    }
    if (!movement.value.bank_account) {
      movement.value.bank_account = setting.default_bank_account;
    }
    movementStore.createMovement(movement.value);
  } else {
    movementStore.updateMovement(movement.value);
  }
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
            v-model:placeholder="movement.name"
            :required="true"
            :isReadOnly="isReadOnly"
          ></FormInputComponent>

          <FormSelectComponent
            :title="'Tipos de ' + setting.title"
            v-model:placeholder="movement.type_tag"
            :required="true"
            :types="setting.types"
          ></FormSelectComponent>

          <FormSelectComponent
            :title="'Intervalo de Parcelas de ' + setting.title"
            v-model:placeholder="movement.cycle"
            :required="true"
            :types="setting.cycles"
          ></FormSelectComponent>

          <FormNumberComponent
            title="Intervalo de Tempo Personalizado"
            min="2"
            max="360"
            step="1"
            v-model:placeholder="movement.unique"
            :isReadOnly="isReadOnly"
            v-if="movement.cycle === 'Personalizado'"
          ></FormNumberComponent>

          <FormNumberComponent
            title="Numero de Parcelas"
            min="1"
            max="120"
            step="1"
            v-model:placeholder="movement.parts"
            :required="true"
            :isReadOnly="isReadOnly"
          ></FormNumberComponent>

          <FormRadioComponent
            title="Ignore no balanço da conta"
            v-model:placeholder="movement.ignore_in_totals"
            :isReadOnly="isReadOnly"
          ></FormRadioComponent>

          <FormNumberComponent
            :title="'Todal de ' + setting.title"
            v-model:placeholder="movement.total"
            min="0"
            step="0.01"
            :isReadOnly="isReadOnly"
          ></FormNumberComponent>

          <FormInputComponent
            title="Primeira data de Pagamento"
            v-model:placeholder="movement.payment_date"
            :isReadOnly="isReadOnly"
            type="date"
          ></FormInputComponent>

          <FormInputComponent
            title="Primeira data de Vencimento"
            v-model:placeholder="movement.is_due"
            :isReadOnly="isReadOnly"
            :required="true"
            type="date"
          ></FormInputComponent>

          <FormSelectComponent
            title="Categoria"
            :isReadOnly="isReadOnly"
            v-model:placeholder="movement.category"
            :types="
              movement.type_tag === 'Entrada' || movement.type_tag === 'income'
                ? setting.income
                : setting.expense
            "
          ></FormSelectComponent>

          <FormRadioComponent
            title="Status"
            :isReadOnly="isReadOnly"
            v-model:placeholder="movement.status"
          ></FormRadioComponent>

          <FormSelectObjectComponent
            title="Conta Bancária Default"
            :object="userStore.getAllAccounts"
            v-model:placeholder="movement.bank_account"
          ></FormSelectObjectComponent>
        </div>
        <NotesComponent :notes="movement.notes" :isReadOnly="isReadOnly" />
        <div v-if="isReadOnly">
          <br />
          <PaymentTableComponent v-model:payments="movement.payment"></PaymentTableComponent>
        </div>

        <button type="button" v-if="isReadOnly" @click="changeMode()" class="btn btn-secondary">
          Editar
        </button>
        <button type="submit" v-else @click="handlerUpdate()" class="btn btn-secondary">
          Salvar
        </button>
        <button type="button" @click="deleteMovement()" class="btn btn-danger">Excluir</button>
      </form>
    </div>
  </div>
  <div class="modal-footer">
    <button type="button" class="btn btn-primary" @click="close">Sair</button>
  </div>
</template>
