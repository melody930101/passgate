<template>
  <van-popup
    v-model:show="visible"
    position="bottom"
    round
    :style="{ padding: '20px 20px 28px' }"
  >
    <div class="sheet-handle" />
    <div class="result-status" :class="success ? 'success' : 'fail'">
      <div class="icon">{{ success ? '✅' : '❌' }}</div>
      <span class="title">{{ title }}</span>
    </div>
    <div v-if="details && details.length" class="details">
      <div v-for="(d, i) in details" :key="i" class="row">
        <span class="key">{{ d.key }}</span>
        <span class="val">{{ d.val }}</span>
      </div>
    </div>
    <van-button type="primary" block @click="handleConfirm">确认</van-button>
  </van-popup>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  show: Boolean,
  success: Boolean,
  title: String,
  details: { type: Array, default: () => [] }
})

const visible = computed({
  get: () => props.show,
  set: (v) => emit('update:show', v)
})

const emit = defineEmits(['update:show', 'confirm'])

function handleConfirm() {
  visible.value = false
  emit('confirm')
}
</script>

<style scoped>
.sheet-handle {
  width: 36px; height: 4px;
  background: #e0e0e0;
  border-radius: 2px;
  margin: 0 auto 16px;
}
.result-status { display: flex; align-items: center; gap: 10px; margin-bottom: 16px; }
.result-status .icon { font-size: 24px; }
.result-status.success .title { color: #2ecc71; font-weight: 700; }
.result-status.fail .title { color: #e74c3c; font-weight: 700; }
.details {
  background: #f8f8f8;
  border-radius: 10px;
  padding: 12px;
  margin-bottom: 16px;
}
.row { display: flex; justify-content: space-between; font-size: 13px; padding: 4px 0; }
.key { color: #999; }
.val { color: #1a1a2e; font-weight: 500; }
</style>
