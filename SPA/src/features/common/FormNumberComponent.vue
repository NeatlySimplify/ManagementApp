<script setup>
import { defineModel, defineProps } from "vue";

const prop = defineProps({
  title: {
    type: String,
    required: true,
  },
  isReadOnly: {
    type: Boolean,
    required: false,
    default: false,
  },
  min: {
    type: [String],
    required: false,
    default: "0",
  },
  max: {
    type: [String, null],
    required: false,
    default: null,
  },
  step: {
    type: String,
    required: false,
    default: "0.01",
  },
  required: {
    type: Boolean,
    required: false,
    default: false,
  },
});

const placeholder = defineModel("placeholder", {type: String});
</script>
<template>
  <div class="mb-3 row rounded shadow-sm">
    <label
      for="input"
      class="col-sm-2 form-label"
    >{{ prop.title }}</label>
    <div class="col-sm-10">
      <input
        id="input"
        v-model="placeholder"
        type="number"
        :readonly="prop.isReadOnly"
        :min="prop.min"
        :required="required"
        :max="prop.max"
        :step="prop.step"
        class="form-control"
      >
    </div>
  </div>
</template>
