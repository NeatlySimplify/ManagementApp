<script setup>
// import { useUserStore } from "@/features/user/store";
// import { defineProps } from "vue";
// import { defineEmits } from "vue";
// import NotesComponent from "@/features/common/NotesComponent.vue";
// import FormInputComponent from "@/features/common/FormInputComponent";
// import FormNumberComponent from "@/features/common/FormNumberComponent";
// import FormSelectComponent from "@/features/common/FormSelectComponent";
// import FormRadioComponent from "@/features/common/FormRadioComponent";

// BeforeMounted(async () => {
//   if (props.mode === "show") {
//     try {
//       request = await api.get(`${route}/${props.id}`);
//       record.value = request.result;
//       changeMode();
//     } catch {
//       alert("Erro ao buscar os dados nos nossos serivdores.");
//     }
//   }
// });

// defineEmits(["close"]);

// const props = defineProps({
//   id,
//   mode,
// });
// const userStore = useUserStore();
// const settings = userStore.getSettings;

// const account = ref({});

// const isReadOnly = ref(true);

// const setting = {
//   types: settings.bank_account_types.sort(),
// };

// function changeMode() {
//   isReadOnly.value = !isReadOnly.value;
// }

// async function handlerUpdate() {
//   await submitForm();
//   changeMode();
// }

// async function deleteAccount(id) {
//   userStore.removeBankAccount()
// }
// async function submitForm() {
//   if (props.mode === "create") {
//     zeroingVars();
//     entity_data.value.notes = notes.value;
//     try {
//       request = await api.post("/entity", entity.value);
//       result = request.result.id;
//       data = {
//         id: result,
//         name: entity.value.name,
//         email: entity.value.email,
//         document: entity.value.document,
//         type_tag: entity.value.type_tag,
//         document_type: entity.value.document_type,
//         status: entity.value.status,
//       };
//       entityStore.addEntity(cleanEntity(data));
//     } catch {
//       alert(`Falha na tentativa de criar ${setting.entity_title}!`);
//     }
//   } else {
//     entity.value.id = props.id;
//     try {
//       request = await api.put(route, entity.value);
//       entity.value.id = request.result.id;
//       entityStore.updateEntity(cleanEntity(entity.value));
//     } catch {
//       alert("Falha na tentativa de atualizar!");
//     }
//   }
// }
</script>

<!-- <template>
  <div class="modal-header">
    <h5 class="modal-title">{{ entity.name }}</h5>
    <button type="button" class="btn-close" @click="$emit('close')">Sair</button>
  </div>
  <div class="modal-body">
    <div>
      <form @submit.prevent>
        <div class="mb-3 row">
          <label for="email" class="col-sm-2 col-form-label">Email</label>
          <div class="col-sm-10">
            <input
              type="text"
              :readonly="isReadOnly"
              v-model="entity.value.email"
              class="form-control-plaintext"
              id="email"
            />
          </div>
        </div>

        <div class="mb-3 row">
          <label for="type_tag" class="col-sm-2 col-form-label">Tipo de {{ setting.title }}</label>
          <div class="col-sm-10">
            <select v-if="!isReadOnly" v-model="entity.type_tag">
              <option selected></option>
              <option v-for="(option, index) in setting.types" :key="index" :value="option">
                {{ option }}
              </option>
            </select>
            <input
              type="text"
              v-else
              readonly
              v-model="entity.type_tag"
              class="form-control-plaintext"
              id="type_tag"
            />
          </div>
        </div>

        <div class="mb-3 row">
          <label for="document_type" class="col-sm-2 col-form-label"
            >Tipo de {{ setting.title }}</label
          >
          <div class="col-sm-10">
            <select v-if="!isReadOnly" v-model="entity.document_type">
              <option select></option>
              <option v-for="(option, index) in setting.documents" :key="index" :value="option">
                {{ option }}
              </option>
            </select>
            <input
              type="text"
              v-else
              readonly
              v-model="entity.document_type"
              class="form-control-plaintext"
              id="document_type"
            />
          </div>
        </div>

        <div class="mb-3 row">
          <label for="sex" class="col-sm-2 col-form-label">Sexo</label>
          <div class="col-sm-10">
            <select v-if="!isReadOnly" v-model="entity.sex">
              <option selected></option>
              <option v-for="(option, index) in setting.sex" :key="index" :value="option">
                {{ option }}
              </option>
            </select>
            <input
              type="text"
              readonly
              v-else
              :value="entity.sex"
              class="form-control-plaintext"
              id="sex"
            />
          </div>
        </div>

        <div class="mb-3 row">
          <label for="relatioship_status" class="col-sm-2 col-form-label">Estado Cívil</label>
          <div class="col-sm-10">
            <select v-if="!isReadOnly" v-model="entity.relationship_status">
              <option selected></option>
              <option
                v-for="(option, index) in setting.relationship_status"
                :key="index"
                :value="option"
              >
                {{ option }}
              </option>
            </select>
            <input
              type="text"
              v-else
              readonly
              :value="entity.relationship_status"
              class="form-control-plaintext"
              id="relationship_status"
            />
          </div>
        </div>

        <div class="mb-3 row">
          <label for="birth" class="col-sm-2 col-form-label">Data de Nascimento</label>
          <div class="col-sm-10">
            <input
              type="date"
              :readonly="isReadOnly"
              v-model="entity.birth"
              class="form-control-plaintext"
              id="birth"
            />
          </div>
        </div>
        <AddressComponent :entity="entity" :isReadOnly="isReadOnly" />
        <ContactComponent :entity="entity" :isReadOnly="isReadOnly" />
        <NotesComponent :notes="entity.notes" :isReadOnly="isReadOnly" />

        <button type="button" v-if="isReadOnly" @click="changeMode()" class="btn btn-secondary">
          Editar
        </button>
        <button type="submit" v-else @click="handlerUpdate()" class="btn btn-secondary">
          Salvar
        </button>
        <button type="button" @click="deleteEntity()" class="btn btn-danger">Excluir</button>
      </form>
    </div>
  </div>
  <div class="modal-footer">
    <button type="button" class="btn btn-primary" @click="$emit('close')">Sair</button>
  </div>
</template> -->
