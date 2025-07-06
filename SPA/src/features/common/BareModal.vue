<script setup>
defineProps({
  title: {
    type: String,
    default: "",
  },
});

defineEmits(["close"]);
</script>

<template>
  <div
    class="modal d-block show"
    tabindex="-1"
  >
    <div class="modal-dialog modal-dialog-scrollable modal-lg">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">
            {{ title }}
          </h5>
          <button
            type="button"
            class="btn btn-outline-danger"
            @click="$emit('close')"
          >
            <span>&#10060;</span>
          </button>
        </div>
        <div class="modal-body">
          <slot />
        </div>
      </div>
    </div>
  </div>
</template>
