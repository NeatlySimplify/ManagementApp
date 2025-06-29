<script setup>
import { ref, defineProps, onMounted } from "vue";
import { useUserStore } from "@user/store";
import ListInputComponent form "@user/ListInputComponent.vue"

const props = defineProps({
  first_access: {
    type: [Boolean, null],
    required: false,
    default: null,
  },
});


onMounted(() => {
  if (props.first_access !== null) {
    if (props.first_access === false){
      showLists.value = true
    }
    if
  }
});

const showLists = ref(false)
const userStore = useUserStore();
const settings = userStore.getSettings;

const bank_accounts
</script>
<template>
  <form @>
  <div class="container">
    <p class="fs-3">Personalização</p>
    <div class="border rounded row my-3">
      <p class="fs-4">Movement:</p>
      <p class="fs-5">
        Esta palavra "Movement" representa uma movimentação financeira genérica, você pode mudar o
        nome para "Entrada", "Conta", ou qualquer outra coisa que faça sentido para seu uso diário.
      </p>
      <input class="form-control" v-model="custom.movement_title" type="text" />
    </div>

    <div class="border rounded row my-3">
      <p class="fs-4">Record:</p>
      <p class="fs-5">
        Esta palavra "Record" representa uma "Ação" ou "Registro" ou "Serviço", você pode mudar o
        nome para qualquer outra coisa que faça sentido para seu uso diário.
      </p>
      <input class="form-control" v-model="custom.record_title" type="text" />
    </div>

    <div class="border rounded row my-3">
      <p class="fs-4">Entity:</p>
      <p class="fs-5">
        Esta palavra "Entity" representa uma "Entidade" genérica, podendo ser um "Cliente",
        "Organização", "Sócio" você pode mudar o nome para qualquer outra coisa que faça sentido
        para seu uso diário.
      </p>
      <input class="form-control" v-model="custom.entity_title" type="text" />
    </div>
    <div v-if="showLists" class="border rounded row my-3">
      <ListImputComponent v-model:tags="settings.account_types" :title='Conta Bancaria'></ListImputComponent>
      <ListImputComponent v-model:tags="settings.entity_types" :title="`Tipos de ${settings.entity_title}`"></ListImputComponent>
      <ListImputComponent v-model:tags="settings.entity_document_types" :title="`Tipos de Documentos de ${settings.entity_title}`"></ListImputComponent>
      <ListImputComponent v-model:tags="settings.contact_number_types" :title="Tipos de " ></ListImputComponent>
      <ListImputComponent v-model:tags="settings.record_types"></ListImputComponent>
      <ListImputComponent v-model:tags="settings.record_status"></ListImputComponent>
      <ListImputComponent v-model:tags="settings.movement_income_types"></ListImputComponent>
      <ListImputComponent v-model:tags="settings.movement_expense_types"></ListImputComponent>
      <ListImputComponent v-model:tags="settings.scheduler_types"></ListImputComponent>
      <ListImputComponent v-model:tags="settings.relationship_status"></ListImputComponent>
      <ListImputComponent v-model:tags="settings.sex"></ListImputComponent>
    </div>
  </div>
  <button type="submit" >
  <form>
    <div class="my-5">
      <p class="fs-4">Conta Bancária:</p>
    </div>
  </form>
</template>
<script setup>
import api from "@util/api";
import { useUserStore } from "@user/store";
import { useRecordStore } from "@record/store";
import { defineProps } from "vue";

const userStore = useUserStore();
const recordStore = useRecordStore();
const settings = userStore.getSettings;

const record = ref({});

const isReadOnly = ref(true);

const setting = {
  title: settings.record_title,
  types: settings.record_types.sort(),
  documents: settings.record_status.sort(),
};

function changeMode() {
  isReadOnly.value = !isReadOnly.value;
}

async function handlerUpdate() {
  await submitForm();
  changeMode();
}

async function deleteEntity() {
  try {
    await api.delete(`${route}/${entity.value.id}`);
    entityStore.removeEntity(entity.value.id);
    closeModal();
  } catch {
    alert(`Falha na tentativa de deletar ${setting.entity_title}!`);
  }
}
async function submitForm() {
  if (props.mode === "create") {
    zeroingVars();
    entity_data.value.notes = notes.value;
    try {
      request = await api.post("/entity", entity.value);
      result = request.result.id;
      data = {
        id: result,
        name: entity.value.name,
        email: entity.value.email,
        document: entity.value.document,
        type_tag: entity.value.type_tag,
        document_type: entity.value.document_type,
        status: entity.value.status,
      };
      entityStore.addEntity(cleanEntity(data));
    } catch {
      alert(`Falha na tentativa de criar ${setting.entity_title}!`);
    }
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
    <h5 class="modal-title">{{ entity.name }}</h5>
    <button type="button" class="btn-close" @click="$emit('close')">Sair</button>
  </div>
  <div class="modal-body">
    <div>
      <form @submit.prevent>
        <div class="tag-input-container" @click="focusInput">
          <span v-for="(tag, index) in tags" :key="index" class="tag">
            {{ tag }}
            <button class="remove-btn" @click.stop="removeTag(index)">×</button>
          </span>
          <input
            ref="input"
            v-model="inputValue"
            @keydown.enter.prevent="addTag"
            @keydown=","
            @blur="addTag"
            placeholder="Enter email and press Enter"
          />
        </div>

        <div class="mb-3 row">
          <label for="email" class="col-sm-2 col-form-label">Email</label>
          <div class="col-sm-10">
            <input
              type="text"
              :readonly="isReadOnly"
              v-model="entity.value.email"
              class="form-control-plaintext"
              id="email"
            />
          </div>
        </div>

        <div class="mb-3 row">
          <label for="type_tag" class="col-sm-2 col-form-label">Tipo de {{ setting.title }}</label>
          <div class="col-sm-10">
            <select v-if="!isReadOnly" v-model="entity.type_tag">
              <option selected></option>
              <option v-for="(option, index) in setting.types" :key="index" :value="option">
                {{ option }}
              </option>
            </select>
            <input
              type="text"
              v-else
              readonly
              v-model="entity.type_tag"
              class="form-control-plaintext"
              id="type_tag"
            />
          </div>
        </div>

        <div class="mb-3 row">
          <label for="document_type" class="col-sm-2 col-form-label"
            >Tipo de {{ setting.title }}</label
          >
          <div class="col-sm-10">
            <select v-if="!isReadOnly" v-model="entity.document_type">
              <option select></option>
              <option v-for="(option, index) in setting.documents" :key="index" :value="option">
                {{ option }}
              </option>
            </select>
            <input
              type="text"
              v-else
              readonly
              v-model="entity.document_type"
              class="form-control-plaintext"
              id="document_type"
            />
          </div>
        </div>

        <div class="mb-3 row">
          <label for="sex" class="col-sm-2 col-form-label">Sexo</label>
          <div class="col-sm-10">
            <select v-if="!isReadOnly" v-model="entity.sex">
              <option selected></option>
              <option v-for="(option, index) in setting.sex" :key="index" :value="option">
                {{ option }}
              </option>
            </select>
            <input
              type="text"
              readonly
              v-else
              :value="entity.sex"
              class="form-control-plaintext"
              id="sex"
            />
          </div>
        </div>

        <div class="mb-3 row">
          <label for="relatioship_status" class="col-sm-2 col-form-label">Estado Cívil</label>
          <div class="col-sm-10">
            <select v-if="!isReadOnly" v-model="entity.relationship_status">
              <option selected></option>
              <option
                v-for="(option, index) in setting.relationship_status"
                :key="index"
                :value="option"
              >
                {{ option }}
              </option>
            </select>
            <input
              type="text"
              v-else
              readonly
              :value="entity.relationship_status"
              class="form-control-plaintext"
              id="relationship_status"
            />
          </div>
        </div>

        <div class="mb-3 row">
          <label for="birth" class="col-sm-2 col-form-label">Data de Nascimento</label>
          <div class="col-sm-10">
            <input
              type="date"
              :readonly="isReadOnly"
              v-model="entity.birth"
              class="form-control-plaintext"
              id="birth"
            />
          </div>
        </div>
        <AddressComponent :entity="entity" :isReadOnly="isReadOnly" />
        <ContactComponent :entity="entity" :isReadOnly="isReadOnly" />
        <NotesComponent :notes="entity.notes" :isReadOnly="isReadOnly" />

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
    <button type="button" class="btn btn-primary" @click="$emit('close')">Sair</button>
  </div>
</template>
