<script setup>
  import { useUserStore } from '@/features/user/store'
  import { useEntityStore } from '@/features/entity/store'
  import { defineProps, defineEmits, BeforeMounted, ref } from 'vue'
  import { useRecordStore } from '@/features/records/store'
  import AddressComponent from '@/features/entity/AddressComponent.vue'
  import ContactComponent from '@/features/entity/ContactComponent.vue'
  import NotesComponent from '@/features/common/NotesComponent.vue'
  import FormInputComponent from '@/features/common/FormInputComponent.vue'
  import FormSelectComponent from '@/features/common/FormSelectComponent.vue'
  import FormRadioComponent from '@/features/common/FormRadioComponent.vue'

  BeforeMounted(async () => {
    if (props.mode === 'show' && props.id !== null) {
      entity.value = { ...entityStore.fetchEntity(props.id) }
      changeMode()
    }
  })

  const recordStore = useRecordStore()
  const record_placeholder = ref('')

  const emit = defineEmits(['close'])
  function close() {
    emit('close')
  }

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
  const entityStore = useEntityStore()
  const settings = userStore.getSettings

  const entity = ref({})

  const isReadOnly = ref(true)

  const setting = {
    title: settings.entity_title,
    types: settings.entity_types.sort(),
    documents: settings.entity_document_types.sort(),
    relationship: settings.relationship_status.sort(),
    sex: settings.sex.sort(),
  }

  function changeMode() {
    isReadOnly.value = !isReadOnly.value
  }

  function handlerUpdate() {
    submitForm()
    changeMode()
  }

  function deleteEntity() {
    entityStore.removeEntity(entity.value.id)
    close()
  }

  function submitForm() {
    if (props.mode === 'create') {
      if (recordStore.placeholder !== '') {
        record_placeholder.value = recordStore.placeholder
        recordStore.placeholder = ''
      }
      entityStore.createEntity(entity.value)
    } else {
      entityStore.updateEntity(entity.value)
    }
  }
</script>

<template>
  <div class="modal-header">
    <h5 class="modal-title">
      {{ entity.name }}
    </h5>
    <button
      type="button"
      class="btn-close"
      @click="close"
    >
      Sair
    </button>
  </div>
  <div class="modal-body">
    <div>
      <form @submit.prevent>
        <FormInputComponent
          v-model:placeholder="entity.email"
          title="Email"
          :is-read-only="isReadOnly"
          :required="true"
        />

        <FormSelectComponent
          v-model:placeholder="entity.type_tag"
          :title="'Tipos de ' + setting.title"
          :is-read-only="isReadOnly"
          :required="true"
          :types="setting.types"
        />

        <FormSelectComponent
          v-model:placeholder="entity.document_type"
          :title="'Tipos de ' + setting.title"
          :is-read-only="isReadOnly"
          :required="true"
          :types="setting.documents"
        />

        <FormInputComponent
          v-model:placeholder="entity.document"
          title="Documento"
          :is-read-only="isReadOnly"
          :required="true"
        />

        <FormRadioComponent
          v-model:placeholder="entity.status"
          title="Status"
          :is-read-only="isReadOnly"
        />

        <FormInputComponent
          v-model:placeholder="entity.name"
          title="Nome"
          :is-read-only="isReadOnly"
          :required="true"
        />

        <FormSelectComponent
          v-model:placeholder="entity.sex"
          title="Sexo"
          :is-read-only="isReadOnly"
          :types="setting.sex"
        />

        <FormSelectComponent
          v-model:placeholder="entity.relationship_status"
          title="Estado Cívil"
          :is-read-only="isReadOnly"
          :types="setting.relationship"
        />

        <FormInputComponent
          v-model:placeholder="entity.birth"
          title="Data de Nascimento"
          :is-read-only="isReadOnly"
          type="date"
        />

        <AddressComponent
          :entity="entity"
          :is-read-only="isReadOnly"
        />
        <ContactComponent
          :entity="entity"
          :is-read-only="isReadOnly"
        />
        <NotesComponent
          v-model:notes="entity.notes"
          :is-read-only="isReadOnly"
        />

        <button
          v-if="isReadOnly"
          type="button"
          class="btn btn-secondary"
          @click="changeMode()"
        >
          Editar
        </button>
        <button
          v-else
          type="submit"
          class="btn btn-secondary"
          @click="handlerUpdate()"
        >
          Salvar
        </button>
        <button
          type="button"
          class="btn btn-danger"
          @click="deleteEntity()"
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
