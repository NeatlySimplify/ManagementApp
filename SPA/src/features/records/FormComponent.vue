<script setup>
  import { useUserStore } from '@/features/user/store'
  import { useRecordStore } from '@/features/records/store'
  import { useEntityStore } from '@/features/entity/store'
  import { defineProps, BeforeMounted, ref } from 'vue'
  import NotesComponent from '@/features/common/NotesComponent.vue'
  import FormInputComponent from '@/features/common/FormInputComponent.vue'
  import FormSelectComponent from '@/features/common/FormSelectComponent.vue'
  import FormRadioComponent from '@/features/common/FormRadioComponent.vue'
  import FormNumberComponent from '@/features/common/FormNumberComponent.vue'
  import FormSelectObjectMultipleComponent from '@/features/common/FormSelectObjectMultipleComponent.vue'
  import MovementTableComponent from '../common/MovementTableComponent.vue'
  import EntityTableComponent from '../common/EntityTableComponent.vue'
  import SchedulerTableComponent from '../common/SchedulerTableComponent.vue'

  BeforeMounted(async () => {
    if (props.mode === 'show' && props.id !== null) {
      record.value = { ...recordStore.fetchRecord(props.id) }
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
  const recordStore = useRecordStore()
  const entityStore = useEntityStore()
  const settings = userStore.getSettings

  const entity = [...entityStore.getAllEntities]

  const record = ref({})

  const isReadOnly = ref(true)

  const setting = {
    title: settings.record_title,
    types: settings.record_types.sort(),
    status: settings.record_status.sort(),
    entity_title: settings.entity_title,
  }

  function changeMode() {
    isReadOnly.value = !isReadOnly.value
  }

  async function handlerUpdate() {
    await submitForm()
    changeMode()
  }

  function deleteRecord() {
    recordStore.removeRecord(record.value.id)
    close()
  }
  function submitForm() {
    if (props.mode === 'create') {
      recordStore.createRecord(record.value)
    } else {
      recordStore.updateRecord(record.value)
    }
  }
</script>

<template>
  <div class="modal-header">
    <h5 class="modal-title">
      {{ record.name }}
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
          v-model:placeholder="record.name"
          title="Nome"
          :required="true"
          :is-read-only="isReadOnly"
        />

        <FormSelectComponent
          v-model:placeholder="record.type_tag"
          :title="'Tipo de ' + setting.title"
          :required="true"
          :is-read-only="isReadOnly"
          :types="setting.types"
        />

        <FormSelectComponent
          v-model:placeholder="record.optional_status"
          :title="'Status de ' + setting.status"
          :is-read-only="isReadOnly"
          :types="setting.status"
        />

        <FormRadioComponent
          v-model:placeholder="record.status"
          title="Esta Ativo ou Arquivado?"
          :is-read-only="isReadOnly"
          :required="true"
        />

        <FormNumberComponent
          v-model:placeholder="record.value"
          :title="'Valor de ' + setting.title"
          :is-read-only="isReadOnly"
          step="0.01"
          min="0"
        />

        <FormSelectObjectMultipleComponent
          v-if="mode === 'create'"
          v-model:placeholder="record.entities"
          :title="setting.entity_title + ' associado(s) a este ' + setting.title"
          :object="entity"
        />
        <NotesComponent
          :notes="record.notes"
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
      <div v-if="mode !== 'create'">
        <br />
        <MovementTableComponent v-model:movement="record.movement" />
        <EntityTableComponent v-model:movement="record.entity" />
        <SchedulerTableComponent v-model:movement="record.event" />
      </div>
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
