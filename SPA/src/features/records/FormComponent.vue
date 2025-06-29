<script setup>
import api from "@util/api";
import { useUserStore } from "@user/store";
import { useRecordStore } from "@record/store";
import { useEntityStore } from "@entity/store";
import { defineProps, defineModel } from "vue";
import { useRouter } from "vue-router";
import NotesComponent from "@/features/common/NotesComponent.vue";

BeforeMounted(async () => {
  if (props.mode === "show" && props.id !== null) {
    try {
      request = await api.get(`${route}/${props.id}`);
      record.value = request.result;
      controls.value.entity.mode = "show";
      controls.value.scheduler.mode = "show";
      controls.value.movement.mode = "show";

      changeMode();
    } catch {
      alert("Erro ao buscar os dados nos nossos serivdores.");
    }
  }
});
const route = "/record";
const closeModal = defineModel("closeModal");
const router = useRouter();

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
const entity_custom = entity.map((item) => ({ id: item.id, name: item.name }));

const record = ref({});

const isReadOnly = ref(true);
const value_pre = {};

const setting = {
  title: settings.record_title,
  types: settings.record_types.sort(),
  status: settings.record_status.sort(),
  entity_title: settings.entity_title,
};
const searchTerm = ref("");
const selectedOptions = ref([]);
const filteredOptions = computed(() =>
  entity_custom.filter((opt) => opt.name.toLowerCase().includes(searchTerm.value.toLowerCase())),
);

function selectOption(opt) {
  const exists = selectedOptions.value.some((item) => item.id === opt.id);
  if (!exists) {
    selectedOptions.value.push(opt);
  }
  searchTerm.value = ""; // Optional: clear search after selection
}

function changeMode() {
  isReadOnly.value = !isReadOnly.value;
}

async function handlerUpdate() {
  await submitForm();
  changeMode();
}

function closeModalfunc() {
  closeModal.value = !closeModal.value;
}

function createEntity

function getEntity(id) {
  router.push({
    name: "entity",
    params: {
      id: id,
      back: true,
    },
  });
}
function deleteEntity(id){}

function getSchedule(id){}

function deleteSchedule(){}

function getMovement(){}


async function deleteRecord() {
  try {
    await api.delete(`${route}/${record.value.id}`);
    recordStore.removeRecord(record.value.id);
    closeModal();
  } catch {
    alert(`Falha na tentativa de deletar ${setting.record_title}!`);
  }
}
async function submitForm() {
  if (props.mode === "create") {
    const entities = selectedOptions.map((item) => item.id);
    const value = `${value_pre.value.int},${value_pre.value.cent}`;
    try {
      request = await api.post(`${route}`, entity.value);
      result = request.result.id;
      data = {
        id: result,
        name: record.value.name,
        service_id: record.value.service_id,
        optional_status: record.value.optional_status,
        type_tag: record.value.type_tag,
        value: record.value.value,
        status: entity.value.status,
        entities: entities,
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
    <h5 class="modal-title">{{ record.name }}</h5>
    <button type="button" class="btn-close" @click="closeModalfunc">Sair</button>
  </div>
  <div class="modal-body">
    <div>
      <form @submit.prevent>
        <div class="mb-3 row">
          <label for="name" class="col-sm-2 col-form-label">Email</label>
          <div class="col-sm-10">
            <input
              type="text"
              :readonly="isReadOnly"
              v-model="record.name"
              class="form-control-plaintext"
              id="name"
              required
            />
          </div>
        </div>

        <div class="mb-3 row">
          <label for="type_tag" class="col-sm-2 col-form-label">Tipo de {{ setting.title }}</label>
          <div class="col-sm-10">
            <select v-if="!isReadOnly" v-model="record.type_tag" id="type_tag" required>
              <option selected></option>
              <option v-for="(option, index) in setting.types" :key="index" :value="option">
                {{ option }}
              </option>
            </select>
            <input
              type="text"
              v-else
              readonly
              v-model="record.type_tag"
              class="form-control-plaintext"
              id="type_tag"
            />
          </div>
        </div>

        <div class="mb-3 row">
          <label for="optional_status" class="col-sm-2 col-form-label"
            >Status de {{ setting.title }}</label
          >
          <div class="col-sm-10">
            <select v-if="!isReadOnly" v-model="record.optional_status" id="optional_status">
              <option select></option>
              <option v-for="(option, index) in setting.status" :key="index" :value="option">
                {{ option }}
              </option>
            </select>
            <input
              type="text"
              v-else
              readonly
              v-model="record.optional_status"
              class="form-control-plaintext"
              id="optional_status"
            />
          </div>
        </div>

        <div class="mb-3 row">
          <label for="status" class="col-sm-2 col-form-label">Esta Ativo ou Arquivado?</label>
          <div class="col-sm-10">
            <select v-if="!isReadOnly" v-model="record.status" required id="status">
              <option :value="null" disabled selected hidden>-- Select status --</option>
              <option :value="true">Ativo</option>
              <option :value="false">Arquivado</option>
            </select>
            <input
              type="text"
              readonly
              v-else
              :value="record.status"
              class="form-control-plaintext"
              id="status"
            />
          </div>
        </div>

        <div class="mb-3 row">
          <label for="value" class="col-sm-2 col-form-label">Valor de {{ setting.title }}</label>
          <div v-if="!isReadOnly">
            <div class="col-sm-10 input-group">
              <span class="input-group-text">R$</span>
              <input
                type="number"
                step="0.01"
                pattern="[0-9.]*"
                :value="record.value"
                id="value"
                min="0"
              />
            </div>
          </div>
          <div v-else>
            <div class="col-sm-10 input-group">
              <span class="input-group-text">R$</span>
              <input
                type="text"
                readonly
                :value="record.value"
                class="form-control-plaintext"
                id="value"
              />
            </div>
          </div>
        </div>
        <div v-if="mode === 'create'" class="mb-3 row">
          <label for="entities" class="col-sm-2 col-form-label"
            >{{ setting.entity_title }} associado(s) a este {{ setting.title }}</label
          >
          <input v-model="searchTerm" type="text" placeholder="" class="form-control" />

          <!-- Filtered list -->
          <ul
            v-if="entityfilteredOptions.length && searchTerm"
            class="list-group position-absolute w-100 z-3"
          >
            <li
              v-for="opt in filteredOptions"
              :key="String(opt.value)"
              class="list-group-item list-group-item-action"
              @click="selectOption(opt)"
              style="cursor: pointer"
            >
              {{ opt.name }}
            </li>
          </ul>

          <!-- Selected display -->
          <ul v-if="selectedOptions" class="mt-2 list-group">
            <li class="list-group-item" v-for="(option, index) in selectedEntity" :key="index">
              {{ option.name }}
            </li>
            <span class="btn-close" @click="removeEntity(index)"></span>
          </ul>
        </div>
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
        <div id="ENTITY">
          <p class="fs-4">{{ setting.entity_title }} associados com este {{ setting.title }}</p>
          <table class="table table-hover">
            <thead>
              <tr>
                <th scope="col">Nome</th>
                <th scope="col">#</th>
              </tr>
            </thead>
            <tbody class="table-group-divider">
              <tr v-for="(name, id) in record.entity" :key="id">
                <td>{{ name }}</td>
                <td>
                  <div class="dropdown">
                    <button
                      class="btn btn-outline-secondary dropdown-toggle"
                      type="button"
                      data-bs-toggle="dropdown"
                      aria-expanded="false"
                    ></button>
                    <ul class="dropdown-menu">
                      <li>
                        <a class="dropdown-item" @click="getEntity(id)" href="#">Ver Mais!</a>
                      </li>
                      <li>
                        <a class="dropdown-item" href="#" @click="deleteEntity(id)">Excluir!</a>
                      </li>
                    </ul>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        <div id="SCHEDULER"></div>
        <div id="MOVEMENT"></div>
      </div>
    </div>
  </div>
  <div class="modal-footer">
    <button type="button" class="btn btn-primary" @click="closeModalfunc">Sair</button>
  </div>
</template>
