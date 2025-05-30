<script setup>
import { useRouter } from 'vue-router'
import FormButtons from './FormButtons.vue'
import { ref } from 'vue'
import api from '@/util/api'

const router = useRouter()

const data = ref({
  email: '',
  password: '',
})

const onSubmit = async () => {
  try {
    let request = await api.post('api/auth/login', data.value)
    console.log(request.data)
    router.push('board')
  } catch (err) {
    console.error('Error on request:', err)
  }
}
</script>

<template>
  <div class="container-fluid border rounded border-top-0">
    <form @submit.prevent="onSubmit">
      <div class="mb-3 row">
        <label for="inputEmail" class="col-4 col-form-label">Email:</label>
        <div class="col-8">
          <input
            type="email"
            class="form-control"
            v-model="data.email"
            id="inputEmail"
            placeholder="Email"
          />
        </div>
      </div>
      <div class="mb-3 row">
        <label for="inputPassword" class="col-4 col-form-label">Password:</label>
        <div class="col-8">
          <input
            type="password"
            class="form-control"
            v-model="data.password"
            id="inputPassword"
            placeholder="Password"
          />
        </div>
      </div>
      <div class="mb-3 row">
        <div class="offset-sm-4 col-sm-8">
          <FormButtons></FormButtons>
        </div>
      </div>
    </form>
  </div>
</template>
