<script setup>
import { defineModel, defineProps } from "vue";

const prop = defineProps({
  title:{
    type: String,
    required: true
  },
  isReadOnly:{
    type: Boolean,
    required: false,
    default: false
  },
  types: {
    type: Array,
    required: true
  },
  require: {
    type: Boolean,
    required: false,
    default: false,
  },
});

const placeholder = defineModel("placeholder", {type: String});
</script>
<template>
  <div class="mb-2 row rounded shadow-sm">
    <label
      for="select"
      class="col-sm-2 form-label"
    >{{ prop.title }}</label>
    <input
      v-if="!prop.isReadOnly"
      id="select"
      v-model="placeholder"
      class="form-control"
      list="datalistOptions"
      :required="require"
    >
    <datalist id="datalistOptions">
      <option
        v-for="(option, index) in prop.types"
        :key="index"
        :value="option"
      >
        {{ option }}
      </option>
    </datalist>
  </div>
</template>
