<template>
  <div class="verify-page">
    <van-nav-bar title="检票" right-text="历史" @click-right="$router.push('/verify/history')" />
    <div class="scan-area">
      <div class="scan-btn" @click="startScan" role="button">
        <van-icon name="scan" size="40" color="#fff" />
        <span>开始检票</span>
      </div>
      <p class="hint">点击按钮扫描学生二维码</p>
    </div>
    <ScannerPage v-model:show="showScanner" @scanned="onScanned" />
    <VerifyResultModal
      v-model:show="resultVisible"
      :success="result.success"
      :title="result.title"
      :details="result.details"
    />
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { showToast } from 'vant'
import { verifyTicket } from '@/api/tickets'
import VerifyResultModal from '@/components/VerifyResultModal.vue'
import ScannerPage from './ScannerPage.vue'

const resultVisible = ref(false)
const result = reactive({ success: false, title: '', details: [] })
const showScanner = ref(false)

function startScan() {
  showScanner.value = true
}

function onScanned(code) {
  verifyTicket({ ticket_code: code })
    .then(res => {
      result.success = res.success
      result.title = res.title || (res.success ? '核销成功' : '核销失败')
      result.details = res.details || []
      resultVisible.value = true
    })
    .catch(e => {
      showToast(e.response?.data?.detail || '核销失败')
    })
}
</script>

<style scoped>
.verify-page { background: #f5f5f7; min-height: 100%; }
.scan-area {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px;
}
.scan-btn {
  width: 160px;
  height: 160px;
  border-radius: 50%;
  background: linear-gradient(135deg, #E63946, #c1121f);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 8px;
  color: #fff;
  font-weight: 600;
  box-shadow: 0 16px 40px rgba(230, 57, 70, 0.4);
}
.hint { margin-top: 20px; font-size: 12px; color: #999; }
</style>
