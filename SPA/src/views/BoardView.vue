<script setup>
  import { useUserStore } from '@/features/user/store'
  import { useMovementStore } from '@/features/movement/store'
  import DatePickerComponent from '@/features/common/DatePickerComponent.vue'
  import { useRecordStore } from '@/features/records/store'
  import LineChartComponent from '@/features/common/LineChartComponent.vue'
  import CalendarComponent from '@/features/common/CalendarComponent.vue'
  import { ref, computed } from 'vue'
  import { RouterLink } from 'vue-router'

  const userStore = useUserStore()
  const movementStore = useMovementStore()
  const recordStore = useRecordStore()
  const settings = userStore.getSettings

  const currentDate = ref(new Date())

  const record_active = computed(() => recordStore.getRecordsByStatus(false))
  const movement_active = computed(() => movementStore.getActiveMovement(currentDate.value))
</script>

<template class="container">
  <DatePickerComponent v-model:current-date="currentDate" />
  <div class="row">
    <div class="card col">
      <LineChartComponent :reference-date="currentDate" />
    </div>
    <div class="card col-12 col-md-6 col-lg-4">
      <ul class="list-group list-group-flush">
        <li class="list-group-item">
          <p>
            {{ settings.record_title }} Ativos
            <span class="badge text-bg-secondary">{{ record_active.length }}</span>
          </p>
          <RouterLink :to="{ name: record }">
Ver Mais...
</RouterLink>
        </li>
        <li class="list-group-item">
          <p>
            {{ settings.movement_title }} Ativos
            <span class="badge text-bg-secondary">{{ movement_active.length }}</span>
          </p>
          <RouterLink :to="{ name: movement }">
Ver Mais...
</RouterLink>
        </li>
      </ul>
    </div>
  </div>
  <div>
    <CalendarComponent
      v-model:current-date="currentDate"
      :limited="true"
    />
    <RouterLink
      :to="{ name: scheduler }"
      class="btn"
    >
      Ver Eventos
    </RouterLink>
  </div>
</template>
