<script setup>
import { defineProps } from "vue";
import { useUserStore } from "@/features/user/store";
import { useEntityStore } from "@/features/entity/store";

const userStore = useUserStore();
const entityStore = useEntityStore();
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
function updateContact() {
  entityStore.updateContact(contactPlaceholder.value);
  localContact[contactIndex.value] = { ...contactPlaceholder.value };
  cleanAddressPlaceholder();
}

function deleteContact(uuid) {
  entityStore.deleteContact(props.entity.value.id, uuid);
  localContact.value = localContact.value.filter((contact) => contact.id !== uuid);
}

function insertContact() {
  contactPlaceholder.value.id = entityStore.createContact(contactPlaceholder.value);
  localContact.value.push({ ...contactPlaceholder.value });
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
