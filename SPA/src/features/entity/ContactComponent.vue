<script setup>
import { defineProps } from "vue";
import { useUserStore } from "../user/store";

const userStore = useUserStore();
const settings = userStore.getSettings;
const contactTypes = settings.contact_number_types.sort();

const props = defineProps({
  entity,
  isReadonly,
});

const contactPlaceholder = ref({});
const updateFlag = ref(false);
const contactIndex = ref(null);
const localContact = ref([]);

function cleanContactPlaceholder() {
  contactPlaceholder.value = {};
  updateFlag.value = false;
  contactIndex.value = null;
}

function takeContact(index) {
  contactIndex.value = index;
  contactPlaceholder.value = { ...localContact[index] };

  updateFlag.value = true;
}
async function updateContact() {
  try {
    await api.put("/entity/contact", contactPlaceholder.value);
    localContact[contactIndex.value] = { ...contactPlaceholder.value };
    cleanAddressPlaceholder();
  } catch {
    alert("Falha na tentativa de Atalizar os dados de endereço");
  }
}
async function deleteContact(uuid) {
  try {
    await api.delete(`/${props.entity.value.id}/address/`, { params: { contact: uuid } });
    localContact.value = localContact.value.filter((contact) => contact.id !== uuid);
  } catch {
    alert("Falha na tentativa de Atalizar os dados de endereço");
  }
}
async function insertContact() {
  try {
    const request = await api.post("/entity/contact", contactPlaceholder.value);
    contactPlaceholder.value.id = request.result.id;
    localContact.value.push({ ...contactPlaceholder.value });
  } catch {
    alert("Erro ao inserir os dados nos nossos serivdores.");
  }
}
onMounted(() => {
  if (props.entity?.value?.phone) {
    localContact.value = props.entity.value.phone.map((ph) => ({ ...ph }));
  }
});
</script>

<template>
  <div class="border rounded">
    <div v-if="!isReadOnly">
      <div class="col-sm-10 input-group">
        <span class="input-group-text">Tipo de Número</span>
        <select v-model="contactPlaceholder.type_tag">
          <option selected></option>
          <option v-for="(option, index) in contactTypes" :key="index" :value="option">
            {{ option }}
          </option>
        </select>
      </div>
      <div class="col-sm-10 input-group">
        <span class="input-group-text">Número de Telefone</span>
        <input type="text" v-model="contactPlaceholder.number" class="form-control-plaintext" />
      </div>
      <div class="col-sm-10 input-group">
        <span class="input-group-text">Complemento</span>
        <textarea rows="2" v-model="contactPlaceholder.complement"></textarea>
      </div>
      <button class="btn btn-outline-primary" v-if="!updateFlag" @click="insertContact()">
        Salvar
      </button>
      <button class="btn btn-outline-primary" v-else @click="updateContact()">Salvar</button>
      <button class="btn btn-outline-warning" @click="cleanContactPlaceholder()">Limpar</button>
    </div>
    <div v-for="(item, index) in localContact" :key="index" class="mb-3 row">
      <div v-if="!isReadOnly">
        <button class="btn btn-outline-secondary" @click="takeContact(index)">Editar</button>
        <button class="btn btn-outline-danger" @click="deleteContact(item.id)">Excluir</button>
      </div>
      <div class="col-sm-10">
        <p>Tipo de Número</p>
        <div class="input-group">
          <input type="text" readonly :value="item.type_tag" class="form-control-plaintext" />
        </div>
      </div>
      <div class="col-sm-10">
        <p>Número de Telefone</p>
        <div class="input-group">
          <input type="text" readonly :value="item.number" class="form-control-plaintext" />
        </div>
      </div>
      <div class="col-sm-10">
        <p>Informações Complementares</p>
        <div class="input-group">
          <textarea readonly rows="2" :value="item.complement" class="form-control-plaintext" />
        </div>
      </div>
    </div>
  </div>
</template>
