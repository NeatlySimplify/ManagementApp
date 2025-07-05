<script setup>
import { defineModel, defineProps } from "vue";

const prop = defineProps({
  title: String,
  isReadOnly: {
    type: Boolean,
    required: false,
  },
});

const placeholder = defineModel("placeholder", { type: Boolean, default: false });
</script>
<template>
  <p class="form-label">{{ prop.title }}</p>
  <div class="btn-group" role="group">
    <input
      type="radio"
      class="btn-check"
      name="btnradio"
      id="btnradio1"
      value="true"
      v-model="placeholder"
      autocomplete="off"
    />
    <label class="btn btn-outline-primary" for="btnradio1">Efetivo</label>

    <input
      type="radio"
      class="btn-check"
      name="btnradio"
      id="btnradio2"
      value="false"
      autocomplete="off"
      v-model="placeholder"
    />
    <label class="btn btn-outline-secondary" for="btnradio2">Não Efetivado</label>
  </div>
</template>
