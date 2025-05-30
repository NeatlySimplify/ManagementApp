<script setup>
import { computed } from 'vue'
import LoginForm from '@/components/auth/LoginForm.vue'
import RegisterForm from '@/components/auth/RegisterForm.vue'
import ForgotPassword from '@/components/auth/ForgotPassword.vue'
import MFAForm from '@/components/auth/MFAForm.vue'
import { useRoute } from 'vue-router'

const route = useRoute()

const formComponent = computed(() => {
  switch (route.name) {
    case 'root':
      return {
        title: 'Login Form',
        component: LoginForm,
      }
    case 'register':
      return {
        title: 'Register Form',
        component: RegisterForm,
      }
    case 'forgot_password':
      return {
        title: 'Forgot your Password',
        component: ForgotPassword,
      }
    case 'mfa':
      return {
        title: 'Multi Factor Authentication',
        component: MFAForm,
      }
    default:
      return {
        title: 'Unknown Page',
        component: null,
      }
  }
})
const title = computed(() => formComponent.value.title)
const form = computed(() => formComponent.value.component)
</script>

<template>
  <div class="container-fluid">
    <div class="row position-relative fullscreen-image">
      <div
        class="col-12 col-md-8 mt-5 text-end text-sm-center position-absolute top-0 start-50 rounded-5 translate-middle-x"
        style="background-color: #ffffff"
      >
        <h1 class="text-center fs-2">{{ title }}</h1>
        <component :is="form"></component>
      </div>
    </div>
  </div>
</template>
<style scoped>
.fullscreen-image {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-image: url('@/assets/images/maxresdefault.jpg'); /* Replace with your image path */
  background-size: cover;
  background-repeat: no-repeat;
}
</style>
