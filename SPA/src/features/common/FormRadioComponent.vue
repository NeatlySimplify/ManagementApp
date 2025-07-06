<script setup>
  import { defineModel, defineProps } from 'vue'

  const prop = defineProps({
    title: {
      type: String,
      required: true,
    },
    isReadOnly: {
      type: Boolean,
      required: true,
    },
  })

  const placeholder = defineModel('placeholder', { type: Boolean, default: false })
</script>
<template>
  <p class="form-label">
    {{ prop.title }}
  </p>
  <div
    class="btn-group"
    role="group"
  >
    <input
      id="btnradio1"
      v-model="placeholder"
      type="radio"
      class="btn-check"
      name="btnradio"
      value="true"
      autocomplete="off"
    />
    <label
      class="btn btn-outline-primary"
      for="btnradio1"
      >Efetivo</label>

    <input
      id="btnradio2"
      v-model="placeholder"
      type="radio"
      class="btn-check"
      name="btnradio"
      value="false"
      autocomplete="off"
    />
    <label
      class="btn btn-outline-secondary"
      for="btnradio2"
      >Não Efetivado</label>
  </div>
</template>
