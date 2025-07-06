import js from '@eslint/js'
import { defineConfig } from 'eslint/config'
import vue from 'eslint-plugin-vue'
import tseslint from 'typescript-eslint'
import globals from 'globals'

export default defineConfig([
  {
    ignores: ['**/dist/**', '**/node_modules/**'],
  },
  js.configs.recommended,
  tseslint.configs.recommended,
  vue.configs['flat/recommended'],

  {
    files: ['**/*.js', '**/*.vue', '**/*.ts',],
    languageOptions: {
      ecmaVersion: 'latest',
      sourceType: 'module',
      globals: {
        ...globals.browser,
        ...globals.es2021,
      },
    },
    plugins: {
      vue: vue,
    },
    rules: {
      'vue/no-undef-components': 'error',
      'vue/require-default-prop': 'warn',
      'vue/no-required-prop-with-default': 'error',
      'vue/valid-v-for': 'error',
      'vue/require-v-for-key': 'warn',
      'vue/no-setup-props-reactivity-loss': 'warn',
      'vue/no-unused-refs': 'warn',
      'vue/html-indent': 'off',
      'vue/html-self-closing': 'off',
      'vue-attributes-order': 'off',
      'vue/html-closing-bracket-newline': 'off'
    },
  },
])
