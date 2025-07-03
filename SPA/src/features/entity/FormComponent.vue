<script setup>
import { useUserStore } from "@/features/user/store";
import { useEntityStore } from "@/features/entity/store";
import { defineProps, defineEmits } from "vue";
import AddressComponent from "@/features/entity/AddressComponent.vue";
import ContactComponent from "@/features/entity/ContactComponent.vue";
import NotesComponent from "@/features/common/NotesComponent.vue";
import { useRecordStore } from "@/features/records/store";

BeforeMounted(async () => {
  if (props.mode === "show" && props.id !== null) {
    try {
      request = await api.get(`${route}/${props.id}`);
      entity.value = request.result;
      changeMode();
    } catch {
      alert("Erro ao buscar os dados nos nossos serivdores.");
    }
  }
});

const route = "/entity";

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

async function handlerUpdate() {
  await submitForm();
  changeMode();
}

async function deleteEntity(entity_id_given = null) {
  try {
    if (entity_id_given === null) {
    }
    await api.delete(`${route}/${entity.value.id}`);
    entityStore.removeEntity(entity.value.id);
    close();
  } catch {
    alert(`Falha na tentativa de deletar ${setting.entity_title}!`);
  }
}
async function submitForm() {
  if (props.mode === "create") {
    entity.value.notes = notes.value;
    try {
      const request = await api.post("/entity", entity.value);
      const result = request.result.id;
      data = {
        id: result,
        name: entity.value.name,
        email: entity.value.email,
        document: entity.value.document,
        type_tag: entity.value.type_tag,
        document_type: entity.value.document_type,
        status: entity.value.status,
      };
      entityStore.addEntity(data);
    } catch {
      alert(`Falha na tentativa de criar ${setting.entity_title}!`);
    }
  } else {
    entity.value.id = props.id;
    try {
      const request = await api.put(route, entity.value);
      entity.value.id = request.result.id;
      entityStore.updateEntity(entity.value);
    } catch {
      alert("Falha na tentativa de atualizar!");
    }
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
        <div class="mb-3 row">
          <label for="email" class="col-sm-2 col-form-label">Email</label>
          <div class="col-sm-10">
            <input
              type="text"
              :readonly="isReadOnly"
              v-model="entity.email"
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
              <option v-for="(option, index) in setting.relationship" :key="index" :value="option">
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
