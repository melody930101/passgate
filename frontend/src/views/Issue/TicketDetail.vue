<!-- 票务详情 Sheet，可被 IssueHistory 或其他页面复用 -->
<template>
  <van-action-sheet v-model:show="visible" title="票务详情">
    <div v-if="ticket" class="detail-content">
      <van-cell-group>
        <van-cell title="电影" :value="ticket.movie_name" />
        <van-cell title="手机" :value="maskPhone(ticket.phone)" />
        <van-cell title="张数" :value="`${ticket.quantity} 张`" />
        <van-cell title="出票时间" :value="ticket.issued_at" />
        <van-cell title="状态" :value="statusText(ticket.status)" />
      </van-cell-group>
      <img v-if="ticket.qr_base64" :src="ticket.qr_base64" alt="二维码" class="qr-img" />
    </div>
  </van-action-sheet>
</template>

<script setup>
import { computed } from 'vue'
import { maskPhone } from '@/utils/phone'

const props = defineProps({ show: Boolean, ticket: Object })
const emit = defineEmits(['update:show'])

const visible = computed({
  get: () => props.show,
  set: v => emit('update:show', v)
})

function statusText(s) {
  const map = { unused: '未核销', used: '已核销', voided: '已作废' }
  return map[s] || s
}
</script>

<style scoped>
.detail-content { padding: 16px; }
.qr-img { width: 120px; height: 120px; margin-top: 12px; }
</style>
