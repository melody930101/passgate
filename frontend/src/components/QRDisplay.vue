<template>
  <div class="qr-display">
    <div class="success-header">
      <span class="dot" />
      <span class="text">出票成功</span>
    </div>
    <div class="ticket-info">
      <div class="row"><span>电影</span><span>{{ movieName }}</span></div>
      <div class="row"><span>手机</span><span>{{ maskPhone(phone) }}</span></div>
      <div class="row"><span>张数</span><span>{{ quantity }} 张</span></div>
      <div class="row"><span>有效期至</span><span>{{ endDate }}</span></div>
    </div>
    <div class="qr-area">
      <img v-if="qrBase64" :src="qrBase64" alt="二维码" class="qr-img" />
    </div>
    <div class="hint">长按图片可保存或转发</div>
    <van-button plain type="primary" block @click="$emit('continue')">继续出票</van-button>
  </div>
</template>

<script setup>
import { maskPhone } from '@/utils/phone'

defineProps({
  movieName: String,
  phone: String,
  quantity: Number,
  endDate: String,
  qrBase64: String
})

defineEmits(['continue'])
</script>

<style scoped>
.qr-display {
  background: #fff;
  border-radius: 14px;
  padding: 16px;
  margin: 12px;
}
.success-header { display: flex; align-items: center; gap: 6px; margin-bottom: 12px; }
.dot { width: 8px; height: 8px; background: #2ecc71; border-radius: 50%; }
.text { font-size: 13px; font-weight: 600; color: #2ecc71; }
.ticket-info {
  background: #fafafa;
  border-radius: 8px;
  padding: 10px 12px;
  margin-bottom: 12px;
}
.row { display: flex; justify-content: space-between; font-size: 13px; padding: 4px 0; }
.row span:first-child { color: #999; }
.row span:last-child { color: #1a1a2e; font-weight: 500; }
.qr-area { display: flex; justify-content: center; margin-bottom: 10px; }
.qr-img { width: 180px; height: 180px; }
.hint { font-size: 12px; color: #999; text-align: center; margin-bottom: 12px; }
</style>
