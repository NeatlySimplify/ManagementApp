<script setup>
import { ref } from 'vue'
import FormButtons from './FormButtons.vue'
import api from '@/util/api'
import { useRouter } from 'vue-router'

const email = ref('')
const router = useRouter()
const isLoading = ref(false)

const onSubmit = async () => {
  try {
    await api.post('api/auth/reset-password', email.value)
    isLoading.value = true
    alert('Password reset email sent successfully! Verify your email to get your new password.')
    router.push('/root')
  } catch (err) {
    console.error('Error on request:', err)
    isLoading.value = false
    alert(
      'An error occurred while sending the password reset email. Update the page and try again.',
    )
  }
}
</script>
<template>
  <div class="container">
    <form @submit.prevent="onSubmit">
      <div class="mb-3 row">
        <div class="col-12 col-md-6 mx-auto">
          <label for="sequence" class="col-form-label"
            >Type your email to reset your password:</label
          >
          <input
            type="text"
            class="form-control"
            id="sequence"
            v-model="email"
            placeholder="amilcarlos@hotmail.com"
            required
          />
          <div class="offset-sm-4 col-sm-8 mt-3 mx-auto">
            <FormButtons :isLoading="isLoading"></FormButtons>
          </div>
        </div>
      </div>
    </form>
  </div>
</template>
