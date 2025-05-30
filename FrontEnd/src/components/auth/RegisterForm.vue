<script setup>
import { ref, watch, computed } from 'vue'
import FormButtons from './FormButtons.vue'
import api from '@/util/api'

const form_switch = ref(null)
const form = ref({
  name: '',
  type: form_switch.value,
  identification: '',
  password: '',
  confirm_pw: '',
})

const passwordValid = computed(() =>
  /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{6,20}$/.test(form.value.password),
)

watch(form_switch, (newVal) => {
  form.value.identification = ''
  form.value.type = newVal
})

const onSubmit = async () => {
  if (form.value.password !== form.value.confirm_pw) {
    alert('Passwords do not match.')
    return
  }
  let formData = {
    name: form.value.name,
    type: form.value.type,
    identification: form.value.type.identification,
    password: form.value.password,
  }
  try {
    let response = await api.post('api/auth/register', formData)
    console.log('Success:', response.data)
  } catch (err) {
    console.error('Error on request:', err)
  }
}
</script>
<template>
  <div class="container">
    <form @submit.prevent="onSubmit">
      <div class="mb-3 row">
        <label for="inputName" class="col-4 col-form-label">Name</label>
        <div class="col-8">
          <input
            type="text"
            class="form-control"
            id="inputName"
            placeholder="Name"
            v-model="form.name"
            required
            minlength="4"
            maxlength="100"
          />
        </div>
      </div>

      <div class="mb-3 row">
        <p class="col-4 col-form-label">Type of User:</p>
        <div class="form-check">
          <input
            class="form-check-input"
            v-model="form_switch"
            value="cnpj"
            type="radio"
            id="type1"
          />
          <label class="form-check-label" for="type1"> Organization </label>
        </div>
        <div class="form-check">
          <input
            class="form-check-input"
            type="radio"
            value="cpf"
            v-model="form_switch"
            id="type2"
          />
          <label class="form-check-label" for="type2"> Individual </label>
        </div>
      </div>

      <div class="mb-3 row" v-if="form_switch === 'cnpj'">
        <label for="inputCNPJ" class="col-4 col-form-label">CNPJ</label>
        <div class="col-8">
          <input type="text" class="form-control" id="inputCNPJ" v-model="form.identification" />
        </div>
      </div>

      <div class="mb-3 row" v-if="form_switch === 'cpf'">
        <label for="inputCPF" class="col-4 col-form-label">CPF</label>
        <div class="col-8">
          <input type="text" class="form-control" id="inputCPF" v-model="form.identification" />
        </div>
      </div>

      <div class="mb-3 row">
        <div class="col-12 col-md-6">
          <div class="row">
            <label for="password" class="col-4 col-form-label">Password</label>
            <div class="col-8">
              <input type="text" class="form-control" id="password" v-model="form.password" />
              <p v-if="form.password && !passwordValid">
                Password must include uppercase, lowercase, and number.
              </p>
            </div>
          </div>
        </div>
        <div class="col-12 col-md-6">
          <div class="row">
            <label for="confirmPassword" class="col-4 col-form-label">Confirm Password</label>
            <div class="col-8">
              <input
                type="password"
                class="form-control"
                id="confirmPassword"
                v-model="form.confirm_pw"
              />
            </div>
          </div>
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
