<script setup>
import { useUserStore } from "@/features/user/store";
import { useRecordStore } from "@/features/record/store";
import { useEntityStore } from "@/features/entity/store";
import { defineProps } from "vue";
import NotesComponent from "@/features/common/NotesComponent.vue";
import FormInputComponent from "@/features/common/FormInputComponent.vue";
import FormSelectComponent from "@/features/common/FormSelectComponent.vue";
import FormRadioComponent from "@/features/common/FormRadioComponent.vue";
import FormNumberComponent from "@/features/common/FormNumberComponent.vue";
import FormSelectObjectMultipleComponent from "@/features/common/FormSelectObjectMultipleComponent.vue";
import MovementTableComponent from "../common/MovementTableComponent.vue";
import EntityTableComponent from "../common/EntityTableComponent.vue";
import SchedulerTableComponent from "../common/SchedulerTableComponent.vue";

BeforeMounted(async () => {
  if (props.mode === "show" && props.id !== null) {
    record.value = { ...recordStore.fetchRecord(props.id) };
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
const recordStore = useRecordStore();
const entityStore = useEntityStore();
const settings = userStore.getSettings;

const entity = entityStore.getAllEntities;

const record = ref({});

const isReadOnly = ref(true);

const setting = {
  title: settings.record_title,
  types: settings.record_types.sort(),
  status: settings.record_status.sort(),
  entity_title: settings.entity_title,
};

function changeMode() {
  isReadOnly.value = !isReadOnly.value;
}

async function handlerUpdate() {
  await submitForm();
  changeMode();
}

function deleteRecord() {
  recordStore.removeRecord(record.value.id);
  close();
}
async function submitForm() {
  if (props.mode === "create") {
    recordStore.createRecord(record.value);
  } else {
    entity.value.id = props.id;
    try {
      request = await api.put(route, entity.value);
      entity.value.id = request.result.id;
      entityStore.updateEntity(cleanEntity(entity.value));
    } catch {
      alert("Falha na tentativa de atualizar!");
    }
  }
}
</script>

<template>
  <div class="modal-header">
    <h5 class="modal-title">{{ record.name }}</h5>
    <button type="button" class="btn-close" @click="closeModalfunc">Sair</button>
  </div>
  <div class="modal-body">
    <div>
      <form @submit.prevent>
        <FormInputComponent
          title="Nome"
          :required="true"
          :isReadOnly="isReadOnly"
          v-model:placeholder="record.name"
        ></FormInputComponent>

        <FormSelectComponent
          :title="'Tipo de ' + setting.title"
          :required="true"
          :isReadOnly="isReadOnly"
          :types="setting.types"
          v-model:placeholder="record.type_tag"
        ></FormSelectComponent>

        <FormSelectComponent
          :title="'Status de ' + setting.status"
          :isReadOnly="isReadOnly"
          :types="setting.status"
          v-model:placeholder="record.optional_status"
        ></FormSelectComponent>

        <FormRadioComponent
          title="Esta Ativo ou Arquivado?"
          :isReadOnly="isReadOnly"
          :required="true"
          v-model:placeholder="record.status"
        ></FormRadioComponent>

        <FormNumberComponent
          :title="'Valor de ' + setting.title"
          :isReadOnly="isReadOnly"
          step="0.01"
          min="0"
          v-model:placeholder="record.value"
        ></FormNumberComponent>

        <FormSelectObjectMultipleComponent
          :title="setting.entity_title + ' associado(s) a este ' + setting.title"
          :object="entity"
          v-model:placeholder="record.entities"
          v-if="mode === 'create'"
        ></FormSelectObjectMultipleComponent>
        <NotesComponent :notes="entity.notes" :isReadOnly="isReadOnly" />

        <button type="button" v-if="isReadOnly" @click="changeMode" class="btn btn-secondary">
          Editar
        </button>
        <button type="submit" v-else @click="handlerUpdate" class="btn btn-secondary">
          Salvar
        </button>
        <button type="button" @click="deleteRecord" class="btn btn-danger">Excluir</button>
      </form>
      <div v-if="mode !== 'create'">
        <br />
        <MovementTableComponent v-model:movement="record.movement"></MovementTableComponent>
        <EntityTableComponent v-model:movement="record.entity"></EntityTableComponent>
        <SchedulerTableComponent v-model:movement="record.event"></SchedulerTableComponent>
      </div>
    </div>
  </div>
  <div class="modal-footer">
    <button type="button" class="btn btn-primary" @click="close">Sair</button>
  </div>
</template>
