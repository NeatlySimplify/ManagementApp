<script setup>
import BareModal from "@/components/BareModal"
import api from '@/api'
import useUserStore from '@/stores/user'
import useEntityStore from '@/stores/entity'
import { defineProps } from "vue"
import { defineEmits } from "vue"


const route = "/api/entity"
defineProps({
  entity,
  mode
})

const isReadOnly = ref(false)
const change = ref(false)

const emit = defineEmits(['change'])

const onChange = (change) => {
  emit('change', change)
}

const userStore = useUserStore()
const entityStore = useEntityStore()
const settings = userStore.getSettings;
const values = {
  title: settings.entity_title,
  types: settings.types.sort(),
  id_types: settings.id_types.sort(),
  contact_number: settings.contact_number_types.sort()
}

const PFPJ = ref(null)
const notes = ref({})
const notesPlaceholder = ref({})
const entity_data = ref({});
const uniqueMode = ref(null)
const addressPlaceholder = ref({})
const phonePlaceholder = ref({})
const showFormAddress = ref(false)
const showFormPhone = ref(false)


const zeroingVars = () => {
  if (PFPJ.value === "PJ") {
    entity_data.value.sex = ''
    entity_data.value.birth = ''
    entity_data.value.relationship_status = ''
  }
  if (entity_data.value.phone.length === 0) {
    entity_data.value.phone = null
  }
  if (entity_data.value.address.length === 0) {
    entity_data.value.address = null
  }
}

function cleanEntity(data){
  return {
    ...data,
    address: data.address?.map(({ city, state }) => ({ city, state })) ?? [],
    phone: data.phone?.map(({ number }) => ({ number })) ?? [],
  };
}

const submitForm = async () => {
  if (uniqueMode.value === 'create') {
    zeroingVars()
    entity_data.value.notes = notes.value
    try {
      request = await api.post(route, entity_data.value)
      result = request.result.id
      data = {
        id: result,
        name: entity_data.value.name,
        email: entity_data.value.email,
        govt_id: entity_data.value.govt_id,
        type_entity: entity_data.value.type_entity,
        id_type: entity_data.value.id_type,
        status: entity_data.value.status,
      }
      entityStore.addEntity(cleanEntity(data))
    } catch {
      alert(`Falha na tentativa de criar ${values.title}!`)
    }
  }
  else {
    entity_data.value.id = props.id
    try {
      await api.put(route, entity_data.value)
      data = {
        id: result,
        name: entity_data.value.name,
        email: entity_data.value.email,
        govt_id: entity_data.value.govt_id,
        type_entity: entity_data.value.type_entity,
        id_type: entity_data.value.id_type,
        status: entity_data.value.status,
      }
      entityStore.updateEntity(cleanEntity(data))
    } catch {
      alert('Falha na tentativa de atualizar!')
    }
  }
}

const changeMode =() => {
  if (entity_data.value.sex !== null){
    PFPJ.value = "PF"
  }
  mode.value = "edit"
}

const deleteEntity = async () => {
  try {
    await api.delete(`${route}/${entity_data.value.id}`)
    entityStore.removeEntity(entity_data.value.id)
  } catch {
    alert(`Falha na tentativa de deletar ${values.title}!`)
  }
}

const cleanNote = () => {
  notesPlaceholder.value.key = ''
  notesPlaceholder.value.text = ''
}

const insertNote = () => {
  const key = notesPlaceholder.value.key.trim()
  const text = notesPlaceholder.value.text.trim()

  if (!key || !text) return

  notes.value[key] = text

  cleanNote()

}

const deleteNote = (key) => {
  delete notes.value[key]
}

const cleanAllNotes = () => {
  notes.value = {}
}

BeforeMounted(async () => {
  if (uniqueMode.value === "view"){
    try {
      request = await api.get(`${route}/${props.id}`)
      entity_data = request.result;

    } catch {
      alert("Erro ao buscar os dados nos nossos serivdores.");
    }
  }
})
</script>

<template>
  <BareModal>
    <div class="modal-header">
      <h5 v-if="uniqueMode.value === 'create'" class="modal-title">Criar Novo(a) {{ values.title }}</h5>
      <h5 v-else class="modal-title">{{ entity_data.value.name }}</h5>
      <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
    </div>
    <div class="modal-body">
      <div v-if="uniqueMode.value === 'view'">
        <form @submit.prevent>

          <div class="mb-3 row">
            <label for="email" class="col-sm-2 col-form-label">Email</label>
            <div class="col-sm-10">
              <input type="text" readonly v-model="entity_data.value.email" class="form-control-plaintext" id="email" />
            </div>
          </div>

          <div class="mb-3 row">
            <label for="type_entity" class="col-sm-2 col-form-label">Tipo de {{ values.title }}</label>
            <div class="col-sm-10">
              <input type="text" readonly v-model="entity_data.value.type_entity" class="form-control-plaintext"
                id="type_entity" />
            </div>
          </div>

          <div class="mb-3 row">
            <label for="type_id" class="col-sm-2 col-form-label">Tipo de Documento</label>
            <div class="col-sm-10 input-group">
              <span class="input-group-text">{{ entity_data.value.id_type }}</span>
              <input type="text" readonly v-model="entity_data.value.govt_id" class="form-control-plaintext"
                id="type_id" />
            </div>
          </div>

          <div v-if="entity_data.value.sex !== null" class="mb-3 row">
            <label for="sex" class="col-sm-2 col-form-label">Sexo</label>
            <div class="col-sm-10">
              <input type="text" readonly v-model="entity_data.value.sex" class="form-control-plaintext" id="sex" />
            </div>
          </div>

          <div v-if="entity_data.value.relationship_status !== null" class="mb-3 row">
            <label for="sex" class="col-sm-2 col-form-label">Estado Cívil</label>
            <div class="col-sm-10">
              <input type="text" readonly v-model="entity_data.value.relationship_status" class="form-control-plaintext"
                id="relationship_status" />
            </div>
          </div>

          <div v-if="entity_data.value.birth !== null" class="mb-3 row">
            <label for="birth" class="col-sm-2 col-form-label">Data de Nascimento</label>
            <div class="col-sm-10">
              <input type="text" readonly v-model="entity_data.value.birth" class="form-control-plaintext" id="birth" />
            </div>
          </div>
          <div class="border rounded">
            <div v-for="(item, index) in entity_data.value.phone" :key="index" class="mb-3 row">
              <div class="col-sm-10 input-group">
                <span class="input-group-text">Email</span>
                <input type="text" readonly :value="item.email" class="form-control-plaintext" />
              </div>
              <div class="col-sm-10">
                <p>Números de Telefone</p>
                <div v-for="(number, j) in item.number" :key="j" class="input-group">
                  <span class="input-group-text">{{ j }}</span>
                  <input type="text" readonly :value="number" class="form-control-plaintext" />
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
            <div v-for="(item, index) in entity_data.value.address" :key="index" class="mb-3 row">
              <div class="col-sm-10 input-group">
                <span class="input-group-text">Estado</span>
                <input type="text" readonly :value="item.state" class="form-control-plaintext" />
              </div>
              <div class="col-sm-10 input-group">
                <span class="input-group-text">Cidade</span>
                <input type="text" readonly :value="item.city" class="form-control-plaintext" />
              </div>
              <div class="col-sm-10 input-group">
                <span class="input-group-text">Bairro</span>
                <input type="text" readonly :value="item.district" class="form-control-plaintext" />
              </div>
              <div class="col-sm-10 input-group">
                <span class="input-group-text">Rua</span>
                <input type="text" readonly :value="item.street" class="form-control-plaintext" />
              </div>
              <div class="col-sm-10 input-group">
                <span class="input-group-text">Número</span>
                <input type="text" readonly :value="item.number" class="form-control-plaintext" />
              </div>
              <div class="col-sm-10 input-group">
                <span class="input-group-text">Complemento</span>
                <textarea rows="2" readonly :value="item.complement"></textarea>
              </div>
            </div>
          </div>

          <div>
            <h5>Notas:</h5>

            <ol class="list-group list-group">
              <li v-for="(text, key) in notes" :key="key">
                <div class="ms-2 me-auto">
                  <div class="fw-bold">{{ key }}</div>
                  {{ text }}
                </div>
              </li>
            </ol>
          </div>
          <button type="button" @click="changeMode" class="btn btn-secondary">Editar</button>
          <button type="button" @click="deleteEntity" data-bs-dismiss="modal" class="btn btn-danger">Excluir</button>
        </form>
      </div>

      <div v-else-if="uniqueMode.value === 'create'">
        <form @submit.prevent="submitForm">
          <div class="mb-3 row">
            <input type="radio" class="btn-check" v-model="PFPJ" name="options-base" id="pf" value="PF"
              autocomplete="off">
            <label class="btn" for="pf">Tipo PF</label>

            <input type="radio" class="btn-check" v-model="PFPJ" name="options-base" id="pj" value="PJ"
              autocomplete="off">
            <label class="btn" for="pj">Tipo PJ</label>
          </div>

          <div class="mb-3 row">
            <label for="name" class="col-sm-2 col-form-label">Nome</label>
            <div class="col-sm-10">
              <input type="text" v-model="entity_data.value.name" required class="form-control-plaintext" id="name" />
            </div>
          </div>

          <div class="mb-3 row">
            <label for="email" class="col-sm-2 col-form-label">Email</label>
            <div class="col-sm-10">
              <input type="text" required v-model="entity_data.value.email" class="form-control-plaintext" id="email" />
            </div>
          </div>

          <div class="mb-3 row">
            <label for="type_entity" class="col-sm-2 col-form-label">Tipo de {{ values.title }}</label>
            <div class="col-sm-10">
              <label for=""></label>
              <select class="form-select" id="type_entity" v-model="entity_data.value.type_entity">
                <option selected></option>
                <option v-for="(type, index) in values.types" :key="index">{{ type }}</option>
              </select>
            </div>
          </div>

          <div v-if="PFPJ === 'PF'">

            <div class="mb-3 row">
              <label for="id_type" class="col-sm-2 col-form-label">Tipo de Documento</label>
              <div class="col-sm-10">
                <label for=""></label>
                <select class="form-select" id="id_type" v-model="entity_data.value.id_type">
                  <option selected></option>
                  <option v-for="(type, index) in values.id_types" :key="index">{{ type }}</option>
                </select>
              </div>
            </div>

            <div class="mb-3 row">
              <label for="document" class="col-sm-2 col-form-label">Documento</label>
              <div class="col-sm-10">
                <input type="text" required class="form-control-plaintext" v-model="entity_data.value.govt_id"
                  id="document" />
              </div>
            </div>

            <div class="mb-3 row">
              <label for="sex" class="col-sm-2 col-form-label">Sexo</label>
              <select class="form-select" id="sex" v-model="entity_data.value.sex">
                <option selected></option>
                <option value="Masculino">Masculino</option>
                <option value="Feminino">Feminino</option>
              </select>
            </div>

            <div class="mb-3 row">
              <label for="relationship_status" class="col-sm-2 col-form-label">Estado Cívil</label>
              <select class="form-select" id="relationship_status" v-model="entity_data.value.relationship_status">
                <option selected></option>
                <option value="Solteiro">Solteiro(a)</option>
                <option value="Casado">Casado(a)</option>
                <option value="Viuvo">Víuvo(a)</option>
                <option value="Separado">Separado(a)</option>
                <option value="Divorciado">Divorciado(a)</option>
                <option value="União Estável">União Estável</option>
              </select>
            </div>

            <div class="mb-3 row">
              <label for="birth_date">Data de Nascimento</label>
              <input type="date" id="birth_date" v-model="entity_data.value.birth">
            </div>

          </div>
          <div v-else-if="PFPJ === 'PJ'">

            <div class="mb-3 row">
              <label for="id_type" class="col-sm-2 col-form-label">Tipo de Documento</label>
              <div class="col-sm-10">
                <label for=""></label>
                <select class="form-select" required id="id_type" v-model="entity_data.value.id_type">
                  <option selected></option>
                  <option v-for="(type, index) in values.id_types" :key="index">{{ type }}</option>
                </select>
              </div>
            </div>

            <div class="mb-3 row">
              <label for="document" class="col-sm-2 col-form-label">Documento</label>
              <div class="col-sm-10">
                <input type="text" required class="form-control-plaintext" v-model="entity_data.value.govt_id"
                  id="document" />
              </div>
            </div>

          </div>

          <div v-else></div>

          <div class="border rounded">
            <h5>Notes:</h5>

            <div>

              <div>
                <label for="note-key" class="col-sm-2 col-form-label">Title</label>
                <div class="col-sm-10">
                  <input type="text" class="form-control-plaintext" v-model="notesPlaceholder.key" id="note-key" />
                </div>
              </div>

              <div>
                <label for="note-text" class="col-sm-2 col-form-label">Nota</label>
                <div class="col-sm-10">
                  <input type="textarea" class="form-control-plaintext" v-model="notesPlaceholder.text"
                    id="note-text" />
                </div>
              </div>

              <button type="button" @click="insertNote" class="btn btn-primary btn">Inserir nota</button>
              <button type="button" @click="cleanNote" class="btn btn-secondary btn-lg">Limpar campos</button>

            </div>

            <ol class="list-group list-group-numbered">
              <li v-for="(text, key) in notes" :key="key">
                <div class="ms-2 me-auto">
                  <div class="fw-bold">{{ key }}</div>
                  {{ text }}
                </div>
                <span @click="deleteNote" class="badge text-bg-danger rounded-pill">&#10007;</span>
              </li>
            </ol>
            <button type="button" @click="cleanAllNotes" class="btn btn-secondary btn">Deletar todas as
              notas</button>
          </div>
          <button type="button" @click="submitForm" data-bs-dismiss="modal" class="btn btn-primary">Salvar
            Entidate</button>
          <button type="reset" class="btn btn-secondary">Limpar formulário</button>
        </form>

        <form @submit.prevent>
          <button type="button" class="btn btn-primary" @click="!showFormPhone">Adicionar número
            de
            telefone</button>
          <div v-show="showFormPhone.value">
            <div class="col-sm-10 input-group">
              <span class="input-group-text">E-mail</span>
              <input type="text" v-model="phonePlaceholder.email" class="form-control-plaintext" />
            </div>
            <div class="col-sm-10">
              <p>Números de Telefone</p>
              <div class="col-sm-10 input-group">
                <span class="input-group-text">Tipo de Número</span>
                <select class="form-select" id="type_entity" v-model="phonePlaceholder.number.type">
                  <option selected></option>
                  <option v-for="(type, index) in values.contact_number" :key="index">{{ type }}</option>
                </select>
              </div>
              <div class="col-sm-10 input-group">
                <span class="input-group-text">Número</span>
                <input type="text" pattern="^\(\d{2}\)\s?(9\s)?\d{4}-\d{4}$" v-model="phonePlaceholder.number.value"
                  class="form-control-plaintext" />
              </div>
              <button type="button" class="btn btn-primary" @click="addNumberToList">Adicionar Número</button>
              <ol>
                <li v-for="(number, key) in phonePlaceholder.number" :key="key">
                  {{ key }} : {{ number }}
                  <span @click="deleteNumberKey(key)" class="badge text-bg-danger rounded-pill">&#10007;</span>
                </li>
              </ol>
            </div>
            <div class="col-sm-10">
              <p>Dados Adicionáis</p>
              <div class="col-sm-10 input-group">
                <span class="input-group-text">Título</span>
                <input type="text" v-model="phonePlaceholder.notes.title" class="form-control-plaintext" />
              </div>
              <div class="col-sm-10 input-group">
                <span class="input-group-text">Texto</span>
                <textarea class="form-control-plaintext" rows="2" v-model="phonePlaceholder.notes.text"></textarea>
              </div>
              <button type="button" class="btn btn-primary" @click="addNoteToList">Adicionar Nota</button>
              <ol>
                <li v-for="(note, key) in phonePlaceholder.notes" :key="key">
                  <div class="ms-2 me-auto">
                    <div class="fw-bold">{{ key }}</div>
                    {{ text }}
                  </div>
                  <span @click="deletebyKey(key, phonePlaceholder.notes)"
                    class="badge text-bg-danger rounded-pill">&#10007;</span>
                </li>
              </ol>
            </div>
            <button type="button" class=" btn btn-primary" @click="saveThisNumber">Salvar Este Número</button>
          </div>

          <div class="border rounded">
            <div v-for="(item, index) in entity_data.value.phone" :key="index" class="mb-3 row">
              <div class="col-sm-10 input-group">
                <span class="input-group-text">Email</span>
                <input type="text" readonly v-model="item.email" class="form-control-plaintext" />
              </div>
              <div class="col-sm-10">
                <p>Números de Telefone</p>
                <ol class="list-group list-group-">
                  <li v-for="(note, key) in phonePlaceholder.notes" :key="key">
                    <div class="ms-2 me-auto">
                      <div class="fw-bold">{{ key }}</div>
                      {{ text }}
                    </div>
                    <span @click="deleteByKey(key, entity_data.value.phone)"
                      class="badge text-bg-danger rounded-pill">&#10007;</span>
                  </li>
                </ol>
              </div>
              <div class="col-sm-10">
                <p>Dados Adicionais</p>
                <ol class="list-group list-group-numbered">
                  <li v-for="(text, key) in phonePlaceholder.number" :key="key">
                    <div class="ms-2 me-auto">
                      <div class="fw-bold">{{ key }}</div>
                      {{ text }}
                    </div>
                    <span @click="deleteByKey(key, phonePlaceholder.number)"
                      class="badge text-bg-danger rounded-pill">&#10007;</span>
                  </li>
                </ol>
              </div>
            </div>
          </div>
          <button type="button" class="btn btn-primary" @click="addNumber">Salvar</button>
        </form>
        <form @submit.prevent>
          <button type="button" class="btn btn-primary" @click="!showFormAddress">Adicionar Endereço</button>
          <div v-show="showFormPhone">
            <div class="col-sm-10 input-group">
              <span class="input-group-text">Estado</span>
              <input type="text" v-model="addressPlaceholder.state" class="form-control-plaintext" />
            </div>
            <div class="col-sm-10 input-group">
              <span class="input-group-text">Cidade</span>
              <input type="text" v-model="addressPlaceholder.city" class="form-control-plaintext" />
            </div>
            <div class="col-sm-10 input-group">
              <span class="input-group-text">Bairro</span>
              <input type="text" v-model="addressPlaceholder.district" class="form-control-plaintext" />
            </div>
            <div class="col-sm-10 input-group">
              <span class="input-group-text">Rua</span>
              <input type="text" v-model="addressPlaceholder.street" class="form-control-plaintext" />
            </div>
            <div class="col-sm-10 input-group">
              <span class="input-group-text">Número</span>
              <input type="number" v-model="addressPlaceholder.number" class="form-control-plaintext" />
            </div>
            <div class="col-sm-10 input-group">
              <span class="input-group-text">Complemento</span>
              <input type="text" v-model="addressPlaceholder.complement" class="form-control-plaintext" />
            </div>
            <div class="col-sm-10 input-group">
              <span class="input-group-text">CEP</span>
              <input type="text" v-model="addressPlaceholder.postal" class="form-control-plaintext" />
            </div>
            <button type="button" class="btn btn-primary" @click="saveThisAddress">Salvar este Endereço</button>
          </div>

          <div class="border rounded">
            <div v-for="(item, key) in entity_data.address" :key="key" class="border rounded">
              <div class="input-group">
                <span class="input-groupt-text">Estado</span>
                <input type="text" readonly :value="item.state">
              </div>
              <div class="input-group">
                <span class="input-groupt-text">Cídade</span>
                <input type="text" readonly :value="item.city">
              </div>
              <div class="input-group">
                <span class="input-groupt-text">Bairro</span>
                <input type="text" readonly :value="item.district">
              </div>
              <div class="input-group">
                <span class="input-groupt-text">Rua</span>
                <input type="text" readonly :value="item.street">
              </div>
              <div class="input-group">
                <span class="input-groupt-text">Número</span>
                <input type="text" readonly :value="item.number">
              </div>
              <div class="input-group">
                <span class="input-groupt-text">CEP</span>
                <input type="text" readonly :value="item.postal">
              </div>
              <div class="input-group">
                <span class="input-groupt-text">Complemento</span>
                <input type="text" readonly :value="item.complement">
              </div>
              <button type="button" class="btn-danger" @click="deleteByKey(key, entity_data.address)"></button>
              <button type="button" class="btn-secondary" @click="editAddress(key, item)"></button>
            </div>
          </div>
          <button type="button" class="btn btn-primary" @click="addNumber">Salvar</button>
        </form>

      </div>
      <div v-else>
        <form @submit.prevent="submitForm">
          <div class="mb-3 row">
            <input type="radio" class="btn-check" v-model="PFPJ" name="options-base" id="pf" value="PF"
              autocomplete="off">
            <label class="btn" for="pf">Tipo PF</label>

            <input type="radio" class="btn-check" v-model="PFPJ" name="options-base" id="pj" value="PJ"
              autocomplete="off">
            <label class="btn" for="pj">Tipo PJ</label>
          </div>

          <div class="mb-3 row">
            <label for="name" class="col-sm-2 col-form-label">Nome</label>
            <div class="col-sm-10">
              <input type="text" v-model="entity_data.value.name" class="form-control-plaintext" id="name" />
            </div>
          </div>

          <div class="mb-3 row">
            <label for="email" class="col-sm-2 col-form-label">Email</label>
            <div class="col-sm-10">
              <input type="text" v-model="entity_data.value.email" class="form-control-plaintext" id="email" />
            </div>
          </div>

          <div class="mb-3 row">
            <label for="type_entity" class="col-sm-2 col-form-label">Tipo de {{ values.title }}</label>
            <div class="col-sm-10">
              <label for=""></label>
              <select class="form-select" id="type_entity" v-model="entity_data.value.type_entity">
                <option selected></option>
                <option v-for="(type, index) in values.types" :key="index">{{ type }}</option>
              </select>
            </div>
          </div>

          <div v-if="PFPJ === 'PF'">

            <div class="mb-3 row">
              <label for="id_type" class="col-sm-2 col-form-label">Tipo de Documento</label>
              <div class="col-sm-10">
                <label for=""></label>
                <select class="form-select" id="id_type" v-model="entity_data.value.id_type">
                  <option selected></option>
                  <option v-for="(type, index) in values.id_types" :key="index">{{ type }}</option>
                </select>
              </div>
            </div>

            <div class="mb-3 row">
              <label for="document" class="col-sm-2 col-form-label">Documento</label>
              <div class="col-sm-10">
                <input type="text" class="form-control-plaintext" v-model="entity_data.value.govt_id" id="document" />
              </div>
            </div>

            <div class="mb-3 row">
              <label for="sex" class="col-sm-2 col-form-label">Sexo</label>
              <select class="form-select" id="sex" v-model="entity_data.value.sex">
                <option selected></option>
                <option value="Masculino">Masculino</option>
                <option value="Feminino">Feminino</option>
              </select>
            </div>

            <div class="mb-3 row">
              <label for="relationship_status" class="col-sm-2 col-form-label">Estado Cívil</label>
              <select class="form-select" id="relationship_status" v-model="entity_data.value.relationship_status">
                <option selected></option>
                <option value="Solteiro">Solteiro(a)</option>
                <option value="Casado">Casado(a)</option>
                <option value="Viuvo">Víuvo(a)</option>
                <option value="Separado">Separado(a)</option>
                <option value="Divorciado">Divorciado(a)</option>
                <option value="União Estável">União Estável</option>
              </select>
            </div>

            <div class="mb-3 row">
              <label for="birth_date">Data de Nascimento</label>
              <input type="date" id="birth_date" v-model="entity_data.value.birth">
            </div>

          </div>
          <div v-else-if="PFPJ === 'PJ'">

            <div class="mb-3 row">
              <label for="id_type" class="col-sm-2 col-form-label">Tipo de Documento</label>
              <div class="col-sm-10">
                <label for=""></label>
                <select class="form-select" id="id_type" v-model="entity_data.value.id_type">
                  <option selected></option>
                  <option v-for="(type, index) in values.id_types" :key="index">{{ type }}</option>
                </select>
              </div>
            </div>

            <div class="mb-3 row">
              <label for="document" class="col-sm-2 col-form-label">Documento</label>
              <div class="col-sm-10">
                <input type="text" class="form-control-plaintext" v-model="entity_data.value.govt_id" id="document" />
              </div>
            </div>

          </div>

          <div v-else></div>

          <div>
            <h5>Notas:</h5>

            <div>

              <div>
                <label for="note-key" class="col-sm-2 col-form-label">Título</label>
                <div class="col-sm-10">
                  <input type="text" class="form-control-plaintext" v-model="notesPlaceholder.key" id="note-key" />
                </div>
              </div>

              <div>
                <label for="note-text" class="col-sm-2 col-form-label">Nota</label>
                <div class="col-sm-10">
                  <input type="textarea" class="form-control-plaintext" v-model="notesPlaceholder.text"
                    id="note-text" />
                </div>
              </div>

              <button type="button" @click="insertNote" class="btn btn-primary btn">Inserir nota</button>
              <button type="button" @click="cleanNote" class="btn btn-secondary btn-lg">Limpar campos</button>

            </div>

            <ol class="list-group list-group-numbered">
              <li v-for="(text, key) in notes" :key="key">
                <div class="ms-2 me-auto">
                  <div class="fw-bold">{{ key }}</div>
                  {{ text }}
                </div>
                <span @click="deleteNote" class="badge text-bg-danger rounded-pill">&#10007;</span>
              </li>
            </ol>
            <button type="button" @click="cleanAllNotes" class="btn btn-secondary btn">Deletar todas as
              notas</button>
          </div>
          <button type="button" @click="submitForm" data-bs-dismiss="modal" class="btn btn-primary">Salvar</button>
        </form>
        <form @submit.prevent>
          <button type="button" class="btn btn-primary" @click="!showFormPhone">Adicionar número
            de
            telefone</button>
          <div v-show="showFormPhone.value">
            <div class="col-sm-10 input-group">
              <span class="input-group-text">E-mail</span>
              <input type="text" v-model="phonePlaceholder.email" class="form-control-plaintext" />
            </div>
            <div class="col-sm-10">
              <p>Números de Telefone</p>
              <div class="col-sm-10 input-group">
                <span class="input-group-text">Tipo de Número</span>
                <select class="form-select" id="type_entity" v-model="phonePlaceholder.number.type">
                  <option selected></option>
                  <option v-for="(type, index) in values.contact_number" :key="index">{{ type }}</option>
                </select>
              </div>
              <div class="col-sm-10 input-group">
                <span class="input-group-text">Número</span>
                <input type="text" pattern="^\(\d{2}\)\s?(9\s)?\d{4}-\d{4}$" v-model="phonePlaceholder.number.value"
                  class="form-control-plaintext" />
              </div>
              <button type="button" class="btn btn-primary" @click="addNumberToList">Adicionar Número</button>
              <ol>
                <li v-for="(number, key) in phonePlaceholder.number" :key="key">
                  {{ key }} : {{ number }}
                  <span @click="deleteNumberKey(key)" class="badge text-bg-danger rounded-pill">&#10007;</span>
                </li>
              </ol>
            </div>
            <div class="col-sm-10">
              <p>Dados Adicionáis</p>
              <div class="col-sm-10 input-group">
                <span class="input-group-text">Título</span>
                <input type="text" v-model="phonePlaceholder.notes.title" class="form-control-plaintext" />
              </div>
              <div class="col-sm-10 input-group">
                <span class="input-group-text">Texto</span>
                <textarea class="form-control-plaintext" rows="2" v-model="phonePlaceholder.notes.text"></textarea>
              </div>
              <button type="button" class="btn btn-primary" @click="addNoteToList">Adicionar Nota</button>
              <ol>
                <li v-for="(note, key) in phonePlaceholder.notes" :key="key">
                  <div class="ms-2 me-auto">
                    <div class="fw-bold">{{ key }}</div>
                    {{ text }}
                  </div>
                  <span @click="deletebyKey(key, phonePlaceholder.notes)"
                    class="badge text-bg-danger rounded-pill">&#10007;</span>
                </li>
              </ol>
            </div>
            <button type="button" class=" btn btn-primary" @click="saveThisNumber">Salvar Este Número</button>
          </div>

          <div class="border rounded">
            <div v-for="(item, index) in entity_data.value.phone" :key="index" class="mb-3 row">
              <div class="col-sm-10 input-group">
                <span class="input-group-text">Email</span>
                <input type="text" readonly v-model="item.email" class="form-control-plaintext" />
              </div>
              <div class="col-sm-10">
                <p>Números de Telefone</p>
                <ol class="list-group list-group-">
                  <li v-for="(note, key) in phonePlaceholder.notes" :key="key">
                    <div class="ms-2 me-auto">
                      <div class="fw-bold">{{ key }}</div>
                      {{ text }}
                    </div>
                    <span @click="deleteByKey(key, entity_data.value.phone)"
                      class="badge text-bg-danger rounded-pill">&#10007;</span>
                  </li>
                </ol>
              </div>
              <div class="col-sm-10">
                <p>Dados Adicionais</p>
                <ol class="list-group list-group-numbered">
                  <li v-for="(text, key) in phonePlaceholder.number" :key="key">
                    <div class="ms-2 me-auto">
                      <div class="fw-bold">{{ key }}</div>
                      {{ text }}
                    </div>
                    <span @click="deleteByKey(key, phonePlaceholder.number)"
                      class="badge text-bg-danger rounded-pill">&#10007;</span>
                  </li>
                </ol>
              </div>
            </div>
          </div>
          <button type="button" class="btn btn-primary" @click="addNumber">Salvar</button>
        </form>
        <form @submit.prevent>
          <button type="button" class="btn btn-primary" @click="!showFormAddress">Adicionar Endereço</button>
          <div v-show="showFormPhone">
            <div class="col-sm-10 input-group">
              <span class="input-group-text">Estado</span>
              <input type="text" v-model="addressPlaceholder.state" class="form-control-plaintext" />
            </div>
            <div class="col-sm-10 input-group">
              <span class="input-group-text">Cidade</span>
              <input type="text" v-model="addressPlaceholder.city" class="form-control-plaintext" />
            </div>
            <div class="col-sm-10 input-group">
              <span class="input-group-text">Bairro</span>
              <input type="text" v-model="addressPlaceholder.district" class="form-control-plaintext" />
            </div>
            <div class="col-sm-10 input-group">
              <span class="input-group-text">Rua</span>
              <input type="text" v-model="addressPlaceholder.street" class="form-control-plaintext" />
            </div>
            <div class="col-sm-10 input-group">
              <span class="input-group-text">Número</span>
              <input type="number" v-model="addressPlaceholder.number" class="form-control-plaintext" />
            </div>
            <div class="col-sm-10 input-group">
              <span class="input-group-text">Complemento</span>
              <input type="text" v-model="addressPlaceholder.complement" class="form-control-plaintext" />
            </div>
            <div class="col-sm-10 input-group">
              <span class="input-group-text">CEP</span>
              <input type="text" v-model="addressPlaceholder.postal" class="form-control-plaintext" />
            </div>
            <button type="button" class="btn btn-primary" @click="saveThisAddress">Salvar este Endereço</button>
          </div>

          <div class="border rounded">
            <div v-for="(item, key) in entity_data.address" :key="key" class="border rounded">
              <div class="input-group">
                <span class="input-groupt-text">Estado</span>
                <input type="text" readonly :value="item.state">
              </div>
              <div class="input-group">
                <span class="input-groupt-text">Cídade</span>
                <input type="text" readonly :value="item.city">
              </div>
              <div class="input-group">
                <span class="input-groupt-text">Bairro</span>
                <input type="text" readonly :value="item.district">
              </div>
              <div class="input-group">
                <span class="input-groupt-text">Rua</span>
                <input type="text" readonly :value="item.street">
              </div>
              <div class="input-group">
                <span class="input-groupt-text">Número</span>
                <input type="text" readonly :value="item.number">
              </div>
              <div class="input-group">
                <span class="input-groupt-text">CEP</span>
                <input type="text" readonly :value="item.postal">
              </div>
              <div class="input-group">
                <span class="input-groupt-text">Complemento</span>
                <input type="text" readonly :value="item.complement">
              </div>
              <button type="button" class="btn-danger" @click="deleteByKey(key, entity_data.address)"></button>
              <button type="button" class="btn-secondary" @click="editAddress(key, item)"></button>
            </div>
          </div>
          <button type="button" class="btn btn-primary" @click="addNumber">Salvar</button>
        </form>
      </div>

    </div>
    <div class="modal-footer">
      <button type="button" data-bs-dismiss="modal" class="btn btn-primary">Sair</button>
    </div>
  </BareModal>
</template>
