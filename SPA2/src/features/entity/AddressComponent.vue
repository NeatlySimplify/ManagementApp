<script setup>
import { defineProps, ref, onMounted } from "vue";
import { useEntityStore } from "@/features/entity/store";

const entityStore = useEntityStore();

const props = defineProps({
  entity: Object,
  isReadOnly: Boolean,
});
const addressPlaceholder = ref({});
const updateFlag = ref(false);
const addressIndex = ref(null);
const localAddress = ref([]);

function cleanAddressPlaceholder() {
  addressPlaceholder.value = {};
  addressIndex.value = null;
  updateFlag.value = false;
}

function takeAddress(index) {
  addressIndex.value = index;
  addressPlaceholder.value = { ...localAddress[index] };

  updateFlag.value = true;
}

function updateAddress() {
  entityStore.updateAddress(addressPlaceholder.value);
  localAddress[addressIndex.value] = { ...addressPlaceholder.value };
  cleanAddressPlaceholder();
}

function deleteAddress(uuid) {
  entityStore.deleteAddress(props.entity.value.id, uuid);
  localAddress.value = localAddress.value.filter((address) => address.id !== uuid);
}

function insertAddress() {
  addressPlaceholder.value.id = entityStore(addressPlaceholder.value);
  localAddress.value.push({ ...addressPlaceholder.value });
}

onMounted(() => {
  if (props.entity?.value?.address) {
    localAddress.value = props.entity.value.address.map((addr) => ({ ...addr }));
  }
});
</script>
<template>
  <div class="border rounded">
    <div v-if="!isReadOnly">
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
        <input type="text" v-model="addressPlaceholder.number" class="form-control-plaintext" />
      </div>
      <div class="col-sm-10 input-group">
        <span class="input-group-text">Complemento</span>
        <textarea rows="2" v-model="addressPlaceholder.complement"></textarea>
      </div>
      <button class="btn btn-outline-primary" v-if="!updateFlag" @click="insertAddress()">
        Salvar
      </button>
      <button class="btn btn-outline-primary" v-else @click="updateAddress()">Salvar</button>
      <button class="btn btn-outline-warning" @click="cleanAddressPlaceholder()">Limpar</button>
    </div>
    <div v-for="(item, index) in localAddress" :key="index" class="mb-3 row">
      <div v-if="!isReadOnly">
        <button class="btn btn-outline-secondary" @click="takeAddress(index)">Editar</button>
        <button class="btn btn-outline-danger" @click="deleteAddress(item.id)">Excluir</button>
      </div>
      <div>
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
  </div>
</template>
