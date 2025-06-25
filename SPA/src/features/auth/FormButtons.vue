<script setup>
import { useRoute } from 'vue-router'
const route = useRoute()
let props = defineProps({
  isLoading: Boolean,
})
</script>
<template>
  <div v-if="route.name === 'root'" class="d-flex justify-content-evenly">
    <RouterLink
      to="/register"
      class="btn btn-outline-danger btn-lg"
      :class="{ disabled: props.isLoading }"
      >Register</RouterLink
    >
    <button type="button" class="btn btn-primary btn-lg">
      Login <i v-if="props.isLoading" class="fa fa-spinner fa-spin"></i>
    </button>
  </div>
  <div v-else class="d-flex justify-content-evenly">
    <RouterLink
      class="btn btn-outline-danger btn-lg"
      :to="{ name: 'root' }"
      :class="{ disabled: props.isLoading }"
    >
      Cancel
    </RouterLink>
    <button type="button" class="btn btn-outline-primary btn-lg">
      Submit <i v-if="props.isLoading" class="fa fa-spinner fa-spin"></i>
    </button>
  </div>
</template>
