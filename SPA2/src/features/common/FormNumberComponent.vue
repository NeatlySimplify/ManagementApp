<script setup>
import { defineModel, defineProps } from "vue";

const prop = defineProps({
  title: {
    type: String,
    required: false,
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

const placeholder = defineModel("placeholder");
</script>
<template>
  <div class="mb-3 row">
    <label for="input" class="col-sm-2 col-form-label">{{ prop.title }}</label>
    <div class="col-sm-10">
      <input
        type="number"
        :readonly="prop.isReadOnly"
        v-model="placeholder"
        :min="prop.min"
        :required="required"
        :max="prop.max"
        :step="prop.step"
        class="form-control-plaintext"
        id="input"
      />
    </div>
  </div>
</template>
