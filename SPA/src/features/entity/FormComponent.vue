<script setup>
import { useUserStore } from "@/features/user/store";
import { useEntityStore } from "@/features/entity/store";
import { defineProps, defineEmits } from "vue";
import { useRecordStore } from "@/features/records/store";
import AddressComponent from "@/features/entity/AddressComponent.vue";
import ContactComponent from "@/features/entity/ContactComponent.vue";
import NotesComponent from "@/features/common/NotesComponent.vue";
import FormInputComponent from "@/features/common/FormInputComponent.vue";
import FormSelectComponent from "@/features/common/FormSelectComponent.vue";
import FormRadioComponent from "@/features/common/FormRadioComponent.vue";

BeforeMounted(async () => {
  if (props.mode === "show" && props.id !== null) {
    entity.value = { ...entityStore.fetchEntity(props.id) };
    changeMode();
  }
});

const recordStore = useRecordStore();
const record_placeholder = ref("");

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
const entityStore = useEntityStore();
const settings = userStore.getSettings;

const entity = ref({});

const isReadOnly = ref(true);

const setting = {
  title: settings.entity_title,
  types: settings.entity_types.sort(),
  documents: settings.entity_document_types.sort(),
  relationship: settings.relationship_status.sort(),
  sex: settings.sex.sort(),
};

function changeMode() {
  isReadOnly.value = !isReadOnly.value;
}

function handlerUpdate() {
  submitForm();
  changeMode();
}

function deleteEntity() {
  entityStore.removeEntity(entity.value.id);
  close();
}

function submitForm() {
  if (props.mode === "create") {
    if (recordStore.placeholder !== "") {
      record_placeholder.value = recordStore.placeholder;
      recordStore.placeholder = "";
    }
    entityStore.createEntity(entity.value);
  } else {
    entityStore.updateEntity(entity.value);
  }
}
</script>

<template>
  <div class="modal-header">
    <h5 class="modal-title">{{ entity.name }}</h5>
    <button type="button" class="btn-close" @click="close">Sair</button>
  </div>
  <div class="modal-body">
    <div>
      <form @submit.prevent>
        <FormInputComponent
          title="Email"
          :isReadOnly="isReadOnly"
          :required="true"
          v-model:placeholder="entity.email"
        ></FormInputComponent>

        <FormSelectComponent
          :title="'Tipos de ' + setting.title"
          :isReadOnly="isReadOnly"
          :required="true"
          v-model:placeholder="entity.type_tag"
          :types="setting.types"
        ></FormSelectComponent>

        <FormSelectComponent
          :title="'Tipos de ' + setting.title"
          :isReadOnly="isReadOnly"
          :required="true"
          v-model:placeholder="entity.document_type"
          :types="setting.documents"
        ></FormSelectComponent>

        <FormInputComponent
          title="Documento"
          :isReadOnly="isReadOnly"
          :required="true"
          v-model:placeholder="entity.document"
        ></FormInputComponent>

        <FormRadioComponent
          title="Status"
          :isReadOnly="isReadOnly"
          v-model:placeholder="entity.status"
        ></FormRadioComponent>

        <FormInputComponent
          title="Nome"
          :isReadOnly="isReadOnly"
          :required="true"
          v-model:placeholder="entity.name"
        ></FormInputComponent>

        <FormSelectComponent
          title="Sexo"
          :isReadOnly="isReadOnly"
          v-model:placeholder="entity.sex"
          :types="setting.sex"
        ></FormSelectComponent>

        <FormSelectComponent
          title="Estado Cívil"
          :isReadOnly="isReadOnly"
          v-model:placeholder="entity.relationship_status"
          :types="setting.relationship"
        ></FormSelectComponent>

        <FormInputComponent
          title="Data de Nascimento"
          :isReadOnly="isReadOnly"
          v-model:placeholder="entity.birth"
          type="date"
        ></FormInputComponent>

        <AddressComponent :entity="entity" :isReadOnly="isReadOnly" />
        <ContactComponent :entity="entity" :isReadOnly="isReadOnly" />
        <NotesComponent v-model:notes="entity.notes" :isReadOnly="isReadOnly" />

        <button type="button" v-if="isReadOnly" @click="changeMode()" class="btn btn-secondary">
          Editar
        </button>
        <button type="submit" v-else @click="handlerUpdate()" class="btn btn-secondary">
          Salvar
        </button>
        <button type="button" @click="deleteEntity()" class="btn btn-danger">Excluir</button>
      </form>
    </div>
  </div>
  <div class="modal-footer">
    <button type="button" class="btn btn-primary" @click="close">Sair</button>
  </div>
</template>
