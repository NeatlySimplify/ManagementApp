<script setup>
  import { defineProps, defineModel } from 'vue'

  const prop = defineProps({
    title: {
      type: String,
      required: true,
    },
    object: {
      type: Array,
      required: true,
    },
  })
  const placeholder = defineModel('placeholder', { type: String })
</script>
<template>
  <div class="mb-3 row">
    <div class="col-2">
      <label
        for="exampleDataList"
        class="form-label"
        >{{ prop.title }}
      </label>
    </div>
    <div class="col-10">
      <input
        id="exampleDataList"
        v-model="placeholder"
        class="form-control"
        list="datalistOptions"
      />
    </div>
    <datalist id="datalistOptions">
      <option
        v-for="(item, index) in prop.object"
        :key="index"
        :value="item"
      >
        {{ item }}
      </option>
    </datalist>
  </div>
</template>
