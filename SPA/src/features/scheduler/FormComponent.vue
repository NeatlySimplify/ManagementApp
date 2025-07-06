<script setup>
  import { useUserStore } from '@/features/user/store'
  import { defineProps, BeforeMounted, ref } from 'vue'
  import NotesComponent from '@/features/common/NotesComponent.vue'
  import FormInputComponent from '@/features/common/FormInputComponent.vue'
  import FormSelectComponent from '@/features/common/FormSelectComponent.vue'
  import FormRadioComponent from '@/features/common/FormRadioComponent.vue'
  import { useSchedulerStore } from '@/features/scheduler/store'

  BeforeMounted(() => {
    if (props.mode === 'show' && props.id !== null) {
      scheduler.value = { ...schedulerStore.fetchScheduler(props.id) }
    }
  })

  const props = defineProps({
    id: {
      type: [String, null],
      required: false,
      default: null,
    },
    mode: {
      type: String,
      default: 'show',
    },
  })
  const userStore = useUserStore()
  const schedulerStore = useSchedulerStore()
  const settings = userStore.getSettings
  const isReadOnly = ref(true)
  const scheduler = ref(null)

  const setting = {
    types: settings.scheduler_types.sort(),
  }

  function changeMode() {
    isReadOnly.value = !isReadOnly.value
  }

  async function handlerUpdate() {
    await submitForm()
    changeMode()
  }

  function deleteRecord() {
    schedulerStore.removeScheduler(scheduler.value.id)
    close()
  }
  async function submitForm() {
    if (props.mode === 'create') {
      schedulerStore.createScheduler(scheduler.value)
    } else {
      schedulerStore.updateScheduler(scheduler.value)
    }
  }
</script>

<template>
  <div class="modal-header">
    <h5 class="modal-title">
      {{ scheduler.name }}
    </h5>
    <button
      type="button"
      class="btn-close"
      @click="closeModalfunc"
    >
      Sair
    </button>
  </div>
  <div class="modal-body">
    <div>
      <form @submit.prevent>
        <FormInputComponent
          v-model:placeholder="scheduler.name"
          title="Nome"
          :required="true"
          :is-read-only="isReadOnly"
        />

        <FormSelectComponent
          v-model:placeholder="scheduler.type_tag"
          :title="'Tipo de ' + setting.title"
          :required="true"
          :is-read-only="isReadOnly"
          :types="setting.types"
        />

        <FormRadioComponent
          v-model:placeholder="scheduler.status"
          title="Esta Ativo ou Arquivado?"
          :is-read-only="isReadOnly"
          :required="true"
        />

        <FormInputComponent
          v-model:placeholder="scheduler.date_beginning"
          title="Data de Inicio"
          :required="true"
          :is-read-only="isReadOnly"
          type="datetime"
        />

        <FormInputComponent
          v-model:placeholder="scheduler.date_ending"
          title="Data do Fim"
          :is-read-only="isReadOnly"
          type="datetime"
        />

        <NotesComponent
          :notes="entity.notes"
          :is-read-only="isReadOnly"
        />

        <button
          v-if="isReadOnly"
          type="button"
          class="btn btn-secondary"
          @click="changeMode"
        >
          Editar
        </button>
        <button
          v-else
          type="submit"
          class="btn btn-secondary"
          @click="handlerUpdate"
        >
          Salvar
        </button>
        <button
          type="button"
          class="btn btn-danger"
          @click="deleteRecord"
        >
          Excluir
        </button>
      </form>
    </div>
  </div>
  <div class="modal-footer">
    <button
      type="button"
      class="btn btn-primary"
      @click="close"
    >
      Sair
    </button>
  </div>
</template>
