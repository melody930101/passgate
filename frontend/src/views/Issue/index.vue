<template>
  <div class="issue-page">
    <van-nav-bar
      title="出票"
      left-text="管理电影"
      right-text="历史"
      @click-left="showDrawer = true"
      @click-right="$router.push('/issue/history')"
    />
    <van-empty
      v-if="!loading && activeMovies.length === 0"
      description="暂无可用电影，请先点击「管理电影」新增"
      image="search"
    >
      <van-button type="primary" @click="showDrawer = true">管理电影</van-button>
    </van-empty>
    <van-form v-else @submit="onSubmit">
      <van-cell-group inset>
        <van-field
          v-model="form.movieText"
          is-link
          readonly
          label="选择电影"
          placeholder="请选择电影"
          :rules="[{ required: true, message: '请选择电影' }]"
          @click="showPicker = true"
        />
        <van-field
          v-model="form.phone"
          type="tel"
          label="学生手机号"
          placeholder="请输入手机号"
          :rules="[{ required: true, message: '请输入手机号' }]"
        />
        <van-field
          v-model="form.quantity"
          type="digit"
          label="购票张数"
          placeholder="1"
          :rules="[{ required: true, message: '请输入张数' }]"
        />
      </van-cell-group>
      <div class="btn-wrap">
        <van-button block type="primary" native-type="submit" :loading="loading">
          生成二维码
        </van-button>
      </div>
    </van-form>

    <div v-if="ticketResult" ref="qrDisplayRef">
      <QRDisplay
        :movie-name="ticketResult.movie_name"
        :phone="ticketResult.phone"
        :quantity="ticketResult.quantity"
        :end-date="ticketResult.end_date"
        :qr-base64="ticketResult.qr_base64"
        @continue="resetForm"
      />
    </div>

    <van-popup v-model:show="showPicker" position="bottom">
      <van-picker
        :columns="movieColumns"
        @confirm="onMovieSelect"
        @cancel="showPicker = false"
      />
    </van-popup>

    <MovieDrawer v-model:show="showDrawer" @refresh="loadActiveMovies" />
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, nextTick } from 'vue'
import { showToast, showConfirmDialog } from 'vant'
import { getActiveMovies } from '@/api/movies'
import { checkUnusedTickets, createTicket } from '@/api/tickets'
import { validatePhone, validateQuantity } from '@/utils/validator'
import QRDisplay from '@/components/QRDisplay.vue'
import MovieDrawer from './MovieDrawer.vue'

const showDrawer = ref(false)
const showPicker = ref(false)
const loading = ref(false)
const ticketResult = ref(null)
const qrDisplayRef = ref(null)

const activeMovies = ref([])
const form = reactive({
  movieId: null,
  movieText: '',
  phone: '',
  quantity: '1'
})

const movieColumns = ref([])

async function loadActiveMovies() {
  try {
    const list = await getActiveMovies()
    activeMovies.value = list
    movieColumns.value = list.map(m => ({
      text: `${m.name} (${m.start_date} ~ ${m.end_date})`,
      value: m.id
    }))
  } catch {
    activeMovies.value = []
    movieColumns.value = []
  }
}

function onMovieSelect({ selectedOptions }) {
  const opt = selectedOptions[0]
  if (opt) {
    form.movieId = opt.value
    form.movieText = opt.text
  }
  showPicker.value = false
}

async function onSubmit() {
  const r1 = validatePhone(form.phone)
  if (!r1.valid) {
    showToast(r1.message)
    return
  }
  const r2 = validateQuantity(form.quantity)
  if (!r2.valid) {
    showToast(r2.message)
    return
  }
  if (!form.movieId) {
    showToast('请选择电影')
    return
  }

  try {
    const checkRes = await checkUnusedTickets({
      movie_id: form.movieId,
      phone: form.phone.trim()
    })
    if (checkRes.has_unused) {
      try {
        await showConfirmDialog({
          title: '提示',
          message: `该手机号在此电影下已有 ${checkRes.count} 张未核销票，是否继续出票？`
        })
      } catch {
        return
      }
    }
  } catch (e) {
    showToast('检查失败，请重试')
    return
  }

  loading.value = true
  try {
    const res = await createTicket({
      movie_id: form.movieId,
      phone: form.phone.trim(),
      quantity: Number(form.quantity) || 1
    })
    ticketResult.value = res
    showToast('出票成功')
    nextTick(() => {
      qrDisplayRef.value?.scrollIntoView({ behavior: 'smooth' })
    })
  } catch (e) {
    showToast(e.response?.data?.detail || '生成失败，请重试')
  } finally {
    loading.value = false
  }
}

function resetForm() {
  ticketResult.value = null
  form.movieId = null
  form.movieText = ''
  form.phone = ''
  form.quantity = '1'
}

onMounted(loadActiveMovies)
</script>

<style scoped>
.issue-page { background: #f5f5f7; min-height: 100%; }
.btn-wrap { margin: 16px; }
</style>
