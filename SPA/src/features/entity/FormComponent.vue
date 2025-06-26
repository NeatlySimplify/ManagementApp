<script setup>
import api from "@util/api";
import { useUserStore } from "@user/store";
import { useEntityStore } from "@entity/store";
import { defineProps } from "vue";
import { defineEmits } from "vue";

const props = defineProps({
  id,
  mode,
});

let isReadOnly = prop.mode;
const change = ref(false);
const editNoteFlag = ref(false);
const oldNoteKey = ref("");

const emit = defineEmits(["change"]);

const userStore = useUserStore();
const entityStore = useEntityStore();
const settings = userStore.getSettings;
const values = {
  title: settings.entity_title,
  types: settings.entity_types.sort(),
  document_types: settings.document_types.sort(),
  contact_number: settings.contact_number_types.sort(),
};

const PFPJ = ref(null);
const notes = ref({});
const notesPlaceholder = ref({});
const entity_data = ref({});
const uniqueMode = ref(null);
const addressPlaceholder = ref({});
const addressIdEdit = ref('')
const phonePlaceholder = ref({});

function onChange() {
  change.value = true;
  emit("change", change);
}

function zeroingVars() {
  if (PFPJ.value === "PJ") {
    entity_data.value.sex = "";
    entity_data.value.birth = "";
    entity_data.value.relationship_status = "";
  }
  if (entity_data.value.phone.length === 0) {
    entity_data.value.phone = null;
  }
  if (entity_data.value.address.length === 0) {
    entity_data.value.address = null;
  }
}

function cleanEntity(data) {
  return {
    ...data,
    address: data.address?.map(({ city, state }) => ({ city, state })) ?? [],
    phone: data.phone?.map(({ number }) => ({ number })) ?? [],
  };
}

function changeMode() {
  if (entity_data.value.sex !== null) {
    PFPJ.value = "PF";
  }
  isReadOnly = false;
}

function cleanNotePlaceholder() {
  notesPlaceholder.value.key = "";
  notesPlaceholder.value.text = "";
  editNoteFlag.value = false;
  oldNoteKey.value = '';
}
function insertNote() {
  const key = notesPlaceholder.value.key.trim();
  const text = notesPlaceholder.value.text.trim();

  if (!key || !text) return;

  notes.value[key] = text;

  cleanNotePlaceholder();
}
function deleteNote(key) {
  delete notes.value[key];
}
function editNote() {
  insertNote();
  deleteNote(oldNoteKey);
  cleanNotePlaceholder();
}
function takeNote(key) {
  const note = notes[key];
  notesPlaceholder.key = key;
  notesPlaceholder.value = note.value;
  editNoteFlag.value = true;
  oldNoteKey.value = key;
}

function cleanAddressPlaceholder(){
  addressPlaceholder.value = {};
  addressIdEdit.value = '';
}
function takeAddress(id){
  const address =  entity_data.value.address.find(obj => obj.id === id);
  addressPlaceholder.value.state = address.state;
  addressPlaceholder.value.city = address.city;
  addressPlaceholder.value.district = address.district;
  addressPlaceholder.value.street = address.street;
  addressPlaceholder.value.number = address.number;
  addressPlaceholder.value.complement = address.complement;
  addressIdEdit.value = id;
}

function cleanPhonePlaceholder(){}
function takePhone(){}
function deletePhone(){}
function savePhone(id){

}

async function handlerUpdate() {
  await submitForm();
  changeMode();
}

async function deleteEntity() {
  try {
    await api.delete(`${route}/${entity_data.value.id}`);
    entityStore.removeEntity(entity_data.value.id);
  } catch {
    alert(`Falha na tentativa de deletar ${values.title}!`);
  }
}
async function submitForm() {
  if (uniqueMode.value === "create") {
    zeroingVars();
    entity_data.value.notes = notes.value;
    try {
      request = await api.post("/entity", entity_data.value);
      result = request.result.id;
      data = {
        id: result,
        name: entity_data.value.name,
        email: entity_data.value.email,
        govt_id: entity_data.value.govt_id,
        type_entity: entity_data.value.type_entity,
        id_type: entity_data.value.id_type,
        status: entity_data.value.status,
      };
      entityStore.addEntity(cleanEntity(data));
    } catch {
      alert(`Falha na tentativa de criar ${values.title}!`);
    }
  } else {
    entity_data.value.id = props.id;
    try {
      await api.put(route, entity_data.value);
      data = {
        id: result,
        name: entity_data.value.name,
        email: entity_data.value.email,
        govt_id: entity_data.value.govt_id,
        type_entity: entity_data.value.type_entity,
        id_type: entity_data.value.id_type,
        status: entity_data.value.status,
      };
      entityStore.updateEntity(cleanEntity(data));
    } catch {
      alert("Falha na tentativa de atualizar!");
    }
  }
}
async function addressUpdate(id){
  try{
    const address =  entity_data.value.address.find(obj => obj.id === id);
    address.state = addressPlaceholder.value.state;
    address.city = addressPlaceholder.value.city;
    address.district = addressPlaceholder.value.district;
    address.street = addressPlaceholder.value.street;
    address.number = addressPlaceholder.value.number;
    address.complement = addressPlaceholder.value.complement;

    await api.put("/entity/address", address)
    cleanAddressPlaceholder();
  } catch{
    alert("Falha na tentativa de Atalizar os dados de endereço")
  }
}
async function deleteAddress(entity, address){
  try{
    await api.delete(`/${entity}/address/`, {params:{address:address}})
    entity_data.value.address = entity_data.value.address.filter(address => address.id !== id);
  } catch {
    alert("Falha na tentativa de Atalizar os dados de endereço")
  }
}
async function saveAddress(){
  try{
    const request = await api.post("/entity/address", addressPlaceholder.value)
    addressPlaceholder.value.id = request.result.id
    entity_data.value.address.push(addressPlaceholder.value)
  } catch {
    alert("Erro ao inserir os dados nos nossos serivdores.");
  }

}

BeforeMounted(async () => {
  if (uniqueMode.value === "view") {
    try {
      request = await api.get(`${route}/${props.id}`);
      entity_data = request.result;
    } catch {
      alert("Erro ao buscar os dados nos nossos serivdores.");
    }
  }
});
</script>

<template>
  <div class="modal-header">
    <h5 class="modal-title">{{ entity_data.value.name }}</h5>
    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
  </div>
  <div class="modal-body">
    <div>
      <form @submit.prevent>
        <div class="mb-3 row">
          <label for="email" class="col-sm-2 col-form-label">Email</label>
          <div class="col-sm-10">
            <input
              type="text"
              :readonly="isReadOnly"
              v-model="entity_data.value.email"
              class="form-control-plaintext"
              id="email"
            />
          </div>
        </div>

        <div class="mb-3 row">
          <label for="type_entity" class="col-sm-2 col-form-label"
            >Tipo de {{ values.title }}</label
          >
          <div class="col-sm-10">
            <input
              type="text"
              :readonly="isReadOnly"
              v-model="entity_data.value.type_entity"
              class="form-control-plaintext"
              id="type_entity"
            />
          </div>
        </div>

        <div class="mb-3 row">
          <label for="type_id" class="col-sm-2 col-form-label">Tipo de Documento</label>
          <div class="col-sm-10 input-group">
            <span class="input-group-text">{{ entity_data.value.id_type }}</span>
            <input
              type="text"
              :readonly="isReadonly"
              v-model="entity_data.value.govt_id"
              class="form-control-plaintext"
              id="type_id"
            />
          </div>
        </div>

        <div v-if="entity_data.value.sex !== null" class="mb-3 row">
          <label for="sex" class="col-sm-2 col-form-label">Sexo</label>
          <div class="col-sm-10">
            <input
              type="text"
              :readonly="isReadonly"
              v-model="entity_data.value.sex"
              class="form-control-plaintext"
              id="sex"
            />
          </div>
        </div>

        <div v-if="entity_data.value.relationship_status !== null" class="mb-3 row">
          <label for="sex" class="col-sm-2 col-form-label">Estado Cívil</label>
          <div class="col-sm-10">
            <input
              type="text"
              :readonly="isReadonly"
              v-model="entity_data.value.relationship_status"
              class="form-control-plaintext"
              id="relationship_status"
            />
          </div>
        </div>

        <div v-if="entity_data.value.birth !== null" class="mb-3 row">
          <label for="birth" class="col-sm-2 col-form-label">Data de Nascimento</label>
          <div class="col-sm-10">
            <input
              type="text"
              :readonly="isReadonly"
              v-model="entity_data.value.birth"
              class="form-control-plaintext"
              id="birth"
            />
          </div>
        </div>
        <div class="border rounded">
          <div v-for="(item, index) in entity_data.value.phone" :key="index" class="mb-3 row">
            <div class="col-sm-10 input-group">
              <span class="input-group-text">Email</span>
              <input
                type="text"
                :readonly="isReadonly"
                :value="item.email"
                class="form-control-plaintext"
              />
            </div>
            <div class="col-sm-10">
              <p>Números de Telefone</p>
              <div v-for="(number, j) in item.number" :key="j" class="input-group">
                <span class="input-group-text">{{ j }}</span>
                <input
                  type="text"
                  :readonly="isReadonly"
                  :value="number"
                  class="form-control-plaintext"
                />
              </div>
            </div>
            <div class="col-sm-10">
              <p>Dados Adicionais</p>
              <ol class="list-group list-group">
                <li v-for="(note, key) in item.notes" :key="key">
                  <div class="ms-2 me-auto">
                    <div class="fw-bold">{{ key }}</div>
                    {{ text }}
                  </div>
                </li>
              </ol>
            </div>
          </div>
        </div>


        <div class="border rounded">
          <h5>Notas:</h5>
          <div v-if="isReadOnly">
            <div class="input-group mb-3">
              <span class="input-group-text">Título</span>
              <input type="text" class="form-control" maxlength="40" />
            </div>
            <div class="input-group">
              <span class="input-group-text">Nota:</span>
              <textarea class="form-control" />
            </div>
            <button v-if="!editNoteFlag" class="btn btn-outline-primary" @click="insertNote()">
              Salvar
            </button>
            <button v-else class="btn btn-outline-primary" @click="editNote()">Salvar</button>
          </div>

          <ol class="list-group list-group">
            <li v-for="(text, key) in notes" :key="key">
              <div class="ms-2 me-auto">
                <div class="fw-bold">{{ key }}</div>
                <span v-if="isReadOnly" class="border" @click="deleteNote(key)">&#10060;</span>
                <p>{{ text }}</p>
                <button v-if="isReadOnly" class="btn btn-outline-secondary" @click="takeNote(key)">
                  Editar Nota
                </button>
              </div>
            </li>
          </ol>
        </div>
        <button type="button" v-if="isReadOnly" @click="changeMode()" class="btn btn-secondary">
          Editar
        </button>
        <button
          type="submit"
          v-else
          @click="(handlerUpdate(), onChange(true))"
          class="btn btn-secondary"
        >
          Salvar
        </button>
        <button
          type="button"
          @click="deleteEntity()"
          data-bs-dismiss="modal"
          class="btn btn-danger"
        >
          Excluir
        </button>
      </form>
    </div>
  </div>
  <div class="modal-footer">
    <button type="button" data-bs-dismiss="modal" class="btn btn-primary">Sair</button>
  </div>
</template>
