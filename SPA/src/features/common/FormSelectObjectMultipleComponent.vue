<script setup>
  import { defineProps, defineModel, ref } from 'vue'

  const selectedOptions = defineModel('selectedOptions', { type: Array })
  const props = defineProps({
    title: { type: String, required: true },
    object: { type: Array, required: true },
  })

  const shown_value = ref([])
  const input_value = ref('')

  function add() {
    // Find object by matching name
    const selectedObject = props.object.find((item) => item.name === input_value.value)

    if (!selectedObject) {
      // no match found, do nothing or notify user
      input_value.value = ''
      return
    }

    // Prevent duplicates by checking if id already selected
    if (!selectedOptions.value.includes(selectedObject.id)) {
      selectedOptions.value.push(selectedObject.id)
      shown_value.value.push(selectedObject.name)
    }

    input_value.value = '' // reset input
  }

  function remove(index) {
    selectedOptions.value.splice(index, 1)
    shown_value.value.splice(index, 1)
  }
</script>

<template>
  <div class="mb-3 row">
    <div class="col-2">
      <label
        for="exampleDataList"
        class="form-label"
        >{{ props.title }}</label>
    </div>
    <div class="col-10">
      <span
        v-for="(item, index) in shown_value"
        :key="index"
        class="btn btn-outline-secondary btn-sm me-2"
      >
        {{ item }}
        <button
          type="button"
          class="btn-close ms-1"
          @click="remove(index)"
        ></button>
      </span>

      <input
        id="exampleDataList"
        v-model="input_value"
        class="form-control mt-2"
        list="datalistOptions"
        placeholder="Type and press enter or select"
        @keydown.enter.prevent="add"
      />
    </div>

    <datalist id="datalistOptions">
      <option
        v-for="item in props.object"
        :key="item.id"
        :value="item.name"
      >
        {{ item.name }}
      </option>
    </datalist>
  </div>
</template>
