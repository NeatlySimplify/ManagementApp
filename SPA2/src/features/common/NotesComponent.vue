<script setup>
import { ref, defineProps, defineModel } from "vue";

defineProps({ isReadOnly });

const notes = defineModel("notes");

const notesPlaceholder = ref({});
const editNoteFlag = ref(false);
const oldNoteKey = ref("");

function cleanNotePlaceholder() {
  notesPlaceholder.value.key = "";
  notesPlaceholder.value.text = "";
  editNoteFlag.value = false;
  oldNoteKey.value = "";
}
function insertNote() {
  const key = notesPlaceholder.value.key.trim();
  const text = notesPlaceholder.value.text.trim();

  if (!key || !text) return;

  notes.value[key] = text;

  cleanNotePlaceholder();
}
function deleteNote(key) {
  delete notes.value[key];
}
function editNote() {
  deleteNote(oldNoteKey.value);
  insertNote();
  cleanNotePlaceholder();
}
function takeNote(text, key) {
  notesPlaceholder.value.key = key;
  notesPlaceholder.value.text = text;
  editNoteFlag.value = true;
  oldNoteKey.value = key;
}
</script>
<template>
  <div class="border rounded">
    <h5>Notas:</h5>
    <div v-if="isReadOnly">
      <div class="input-group mb-3">
        <span class="input-group-text">Título</span>
        <input type="text" class="form-control" v-model="notesPlaceholder.key" maxlength="40" />
      </div>
      <div class="input-group">
        <span class="input-group-text">Nota:</span>
        <textarea class="form-control" v-model="notesPlaceholder.text" />
      </div>
      <button v-if="!editNoteFlag" class="btn btn-outline-primary" @click="insertNote()">
        Salvar
      </button>
      <button v-else class="btn btn-outline-primary" @click="editNote()">Salvar</button>
    </div>

    <ol class="list-group list-group">
      <li v-for="(text, key) in notes" :key="key">
        <div class="ms-2 me-auto">
          <div class="fw-bold">{{ key }}</div>
          <span v-if="!isReadOnly" class="border" @click="deleteNote(key)">&#10060;</span>
          <p>{{ text }}</p>
          <button v-if="!isReadOnly" class="btn btn-outline-secondary" @click="takeNote(text, key)">
            Editar Nota
          </button>
        </div>
      </li>
    </ol>
  </div>
</template>
