<template>
  <van-cell
    :title="movieName"
    :label="`${maskPhone(phone)} · ${quantity}张 · ${issuedAt}`"
    is-link
    @click="$emit('click')"
  >
    <template #right-icon>
      <van-tag :type="statusTagType">{{ statusText }}</van-tag>
    </template>
    <template v-if="showIssuer && issuerName" #label>
      {{ maskPhone(phone) }} · {{ quantity }}张 · {{ issuedAt }} · {{ issuerName }}
    </template>
  </van-cell>
</template>

<script setup>
import { computed } from 'vue'
import { maskPhone } from '@/utils/phone'

const props = defineProps({
  movieName: String,
  phone: String,
  quantity: Number,
  issuedAt: String,
  status: String, // unused | used | voided
  issuerName: { type: String, default: '' },
  showIssuer: { type: Boolean, default: false }
})

const statusText = computed(() => {
  const map = { unused: '未核销', used: '已核销', voided: '已作废' }
  return map[props.status] || props.status
})

const statusTagType = computed(() => {
  const map = { unused: 'warning', used: 'success', voided: 'danger' }
  return map[props.status] || 'default'
})
</script>
