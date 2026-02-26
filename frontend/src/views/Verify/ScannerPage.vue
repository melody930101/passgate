<template>
  <van-popup v-model:show="visible" position="center" :style="{ width: '100%', height: '100%' }">
    <div class="scanner-wrap">
      <div class="scanner-header">
        <van-button plain type="primary" @click="close">取消</van-button>
      </div>
      <div id="qr-reader" ref="scannerRef" class="scanner-area" />
    </div>
  </van-popup>
</template>

<script setup>
import { ref, onUnmounted, watch, nextTick } from 'vue'
import { showToast } from 'vant'
import { Html5Qrcode } from 'html5-qrcode'

const props = defineProps({ show: Boolean })
const emit = defineEmits(['update:show', 'scanned'])

const visible = ref(false)
const scannerRef = ref(null)
let html5QrCode = null

watch(() => props.show, async v => {
  visible.value = v
  if (v) {
    await nextTick()
    startScanner()
  } else {
    stopScanner()
  }
})

function close() {
  visible.value = false
  emit('update:show', false)
  stopScanner()
}

function startScanner() {
  if (!scannerRef.value) return
  html5QrCode = new Html5Qrcode('qr-reader')
  html5QrCode.start(
    { facingMode: 'environment' },
    { fps: 10, qrbox: { width: 250, height: 250 } },
    code => {
      emit('scanned', code)
      close()
    },
    () => {}
  ).catch(err => {
    console.error(err)
    showToast('请在系统设置中允许相机访问')
    close()
  })
}

function stopScanner() {
  if (html5QrCode && html5QrCode.isScanning) {
    html5QrCode.stop()
    html5QrCode = null
  }
}

onUnmounted(stopScanner)
</script>

<style scoped>
.scanner-wrap { height: 100vh; display: flex; flex-direction: column; background: #000; }
.scanner-header { padding: 16px; }
.scanner-area { flex: 1; }
</style>
