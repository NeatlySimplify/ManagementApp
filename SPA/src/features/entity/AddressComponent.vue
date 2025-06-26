<script>
import { defineProps } from 'vue';

const props = defineProps({
  address,
  entity,
  isReadOnly
})
</script>
<template>
  <div class="border rounded">
    <div v-if="!isReadOnly">
      <div>
        <div class="col-sm-10 input-group">
          <span class="input-group-text">Estado</span>
          <input
            type="text"
            :value="addressPlaceholder.state"
            class="form-control-plaintext"
          />
        </div>
        <div class="col-sm-10 input-group">
          <span class="input-group-text">Cidade</span>
          <input
            type="text"
            :value="addressPlaceholder.city"
            class="form-control-plaintext"
          />
        </div>
        <div class="col-sm-10 input-group">
          <span class="input-group-text">Bairro</span>
          <input
            type="text"
            :value="addressPlaceholder.district"
            class="form-control-plaintext"
          />
        </div>
        <div class="col-sm-10 input-group">
          <span class="input-group-text">Rua</span>
          <input
            type="text"
            :value="addressPlaceholder.street"
            class="form-control-plaintext"
          />
        </div>
        <div class="col-sm-10 input-group">
          <span class="input-group-text">Número</span>
          <input
            type="text"
            :value="addressPlaceholder.number"
            class="form-control-plaintext"
          />
        </div>
        <div class="col-sm-10 input-group">
          <span class="input-group-text">Complemento</span>
          <textarea rows="2" :value="addressPlaceholder.complement"></textarea>
        </div>
        <button class="btn btn-outline-primary" @click="saveAddress()">Salvar</button>
        <button class="btn btn-outline-warning" @click="cleanAddressPlaceholder()">Limpar</button>
    </div>
    <div v-for="(item, index) in entity_data.value.address" :key="index" class="mb-3 row">
      <div v-if="!isReadOnly">
        <button class="btn btn-outline-secondary"  @click="takeAddress(item.id)">Editar</button>
        <button class="btn btn-outline-danger" @click="deleteAddress(item.id)">Excluir</button>
      </div>
      <div>
        <div class="col-sm-10 input-group">
          <span class="input-group-text">Estado</span>
          <input
            type="text"
            readonly
            :value="item.state"
            class="form-control-plaintext"
          />
        </div>
        <div class="col-sm-10 input-group">
          <span class="input-group-text">Cidade</span>
          <input
            type="text"
            readonly
            :value="item.city"
            class="form-control-plaintext"
          />
        </div>
        <div class="col-sm-10 input-group">
          <span class="input-group-text">Bairro</span>
          <input
            type="text"
            readonly
            :value="item.district"
            class="form-control-plaintext"
          />
        </div>
        <div class="col-sm-10 input-group">
          <span class="input-group-text">Rua</span>
          <input
            type="text"
            readonly
            :value="item.street"
            class="form-control-plaintext"
          />
        </div>
        <div class="col-sm-10 input-group">
          <span class="input-group-text">Número</span>
          <input
            type="text"
            readonly
            :value="item.number"
            class="form-control-plaintext"
          />
        </div>
        <div class="col-sm-10 input-group">
          <span class="input-group-text">Complemento</span>
          <textarea rows="2" readonly :value="item.complement"></textarea>
        </div>
      </div>
  
    </div>
  </div>
</template>