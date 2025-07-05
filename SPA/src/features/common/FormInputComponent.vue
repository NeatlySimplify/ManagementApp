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
  type: {
    type: String,
    required: false,
    default: "text",
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
  <div class="mb-2 row rounded shadow-sm">
    <label for="data" class="col-2 form-label">{{ prop.title }}</label>
    <div class="col-10">
      <input :type="prop.type" :readonly="prop.isReadOnly" v-model="placeholder" :required="required"
        class="form-control" id="data" />
    </div>
  </div>
</template>
