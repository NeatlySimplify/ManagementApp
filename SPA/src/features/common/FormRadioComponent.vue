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
function active() {
  if (!prop.isReadOnly) {
    placeholder.value = true;
  }
}
function inactive() {
  if (!prop.isReadOnly) {
    placeholder.value = false;
  }
}
</script>
<template>
  <p class="form-label">{{ prop.title }}</p>
  <div class="btn-group" role="group">
    <input
      type="radio"
      class="btn-check"
      name="btnradio"
      id="btnradio1"
      autocomplete="off"
      @click="active"
      :checked="placeholder"
    />
    <label class="btn btn-outline-primary" for="btnradio1">Efetivo</label>

    <input
      type="radio"
      class="btn-check"
      name="btnradio"
      id="btnradio2"
      autocomplete="off"
      @click="inactive"
      :checked="!placeholder"
    />
    <label class="btn btn-outline-secondary" for="btnradio2">Não Efetivado</label>
  </div>
</template>
