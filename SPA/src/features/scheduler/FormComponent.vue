<script setup>
import { useUserStore } from "@/features/user/store";
import { defineProps } from "vue";
import NotesComponent from "@/features/common/NotesComponent.vue";
import FormInputComponent from "@/features/common/FormInputComponent.vue";
import FormSelectComponent from "@/features/common/FormSelectComponent.vue";
import FormRadioComponent from "@/features/common/FormRadioComponent.vue";

BeforeMounted(() => {
  if (props.mode === "show" && props.id !== null) {
    scheduler.value = { ...schedulerStore.fetchScheduler(props.id) };
  }
});

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
const settings = userStore.getSettings;
const isReadOnly = ref(true);
const scheduler = ref(null);

const setting = {
  types: settings.scheduler_types.sort(),
};

function changeMode() {
  isReadOnly.value = !isReadOnly.value;
}

async function handlerUpdate() {
  await submitForm();
  changeMode();
}

function deleteRecord() {
  schedulerStore.removeScheduler(scheduler.value.id);
  close();
}
async function submitForm() {
  if (props.mode === "create") {
    schedulerStore.createScheduler(scheduler.value);
  } else {
    schedulerStore.updateScheduler(scheduler.value);
  }
}
</script>

<template>
  <div class="modal-header">
    <h5 class="modal-title">{{ scheduler.name }}</h5>
    <button type="button" class="btn-close" @click="closeModalfunc">Sair</button>
  </div>
  <div class="modal-body">
    <div>
      <form @submit.prevent>
        <FormInputComponent
          title="Nome"
          :required="true"
          :isReadOnly="isReadOnly"
          v-model:placeholder="scheduler.name"
        ></FormInputComponent>

        <FormSelectComponent
          :title="'Tipo de ' + setting.title"
          :required="true"
          :isReadOnly="isReadOnly"
          :types="setting.types"
          v-model:placeholder="scheduler.type_tag"
        ></FormSelectComponent>

        <FormRadioComponent
          title="Esta Ativo ou Arquivado?"
          :isReadOnly="isReadOnly"
          :required="true"
          v-model:placeholder="scheduler.status"
        ></FormRadioComponent>

        <FormInputComponent
          title="Data de Inicio"
          :required="true"
          :isReadOnly="isReadOnly"
          v-model:placeholder="scheduler.date_beginning"
          type="datetime"
        ></FormInputComponent>

        <FormInputComponent
          title="Data do Fim"
          :isReadOnly="isReadOnly"
          v-model:placeholder="scheduler.date_ending"
          type="datetime"
        ></FormInputComponent>

        <NotesComponent :notes="entity.notes" :isReadOnly="isReadOnly" />

        <button type="button" v-if="isReadOnly" @click="changeMode" class="btn btn-secondary">
          Editar
        </button>
        <button type="submit" v-else @click="handlerUpdate" class="btn btn-secondary">
          Salvar
        </button>
        <button type="button" @click="deleteRecord" class="btn btn-danger">Excluir</button>
      </form>
    </div>
  </div>
  <div class="modal-footer">
    <button type="button" class="btn btn-primary" @click="close">Sair</button>
  </div>
</template>
