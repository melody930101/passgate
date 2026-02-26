<template>
  <div class="history-page">
    <van-nav-bar title="检票历史" left-arrow @click-left="$router.back()" />
    <van-dropdown-menu>
      <van-dropdown-item v-model="filterMovie" :options="movieOptions" @change="onFilterChange" />
      <van-dropdown-item v-model="filterDateRange" :options="dateRangeOptions" @change="onFilterChange" />
    </van-dropdown-menu>
    <div v-if="filterDateRange === 'custom'" class="date-filter-row">
      <van-field
        v-model="startDateStr"
        readonly
        placeholder="开始日期"
        @click="showStartPicker = true"
      />
      <van-field
        v-model="endDateStr"
        readonly
        placeholder="结束日期"
        @click="showEndPicker = true"
      />
      <van-button type="primary" size="small" @click="applyDateFilter">筛选</van-button>
    </div>
    <van-popup v-model:show="showStartPicker" position="bottom">
      <van-date-picker
        v-model="startDateArr"
        title="开始日期"
        :min-date="minDate"
        :max-date="maxDate"
        @confirm="onStartDateConfirm"
      />
    </van-popup>
    <van-popup v-model:show="showEndPicker" position="bottom">
      <van-date-picker
        v-model="endDateArr"
        title="结束日期"
        :min-date="minDate"
        :max-date="maxDate"
        @confirm="onEndDateConfirm"
      />
    </van-popup>
    <van-pull-refresh v-model="refreshing" @refresh="onRefresh">
      <van-list v-model:loading="loading" :finished="finished" finished-text="没有更多" @load="loadList">
        <van-cell
          v-for="t in list"
          :key="t.id"
          :title="t.movie_name"
          :label="`${maskPhone(t.phone)} · ${t.quantity}张 · ${t.checked_at}${userStore.isAdmin && t.checker_name ? ' · ' + t.checker_name : ''}`"
          @click="showDetail(t)"
        />
      </van-list>
    </van-pull-refresh>
    <van-action-sheet v-model:show="detailVisible" title="票务详情">
      <div v-if="currentTicket" class="detail-content">
        <van-cell-group>
          <van-cell title="电影" :value="currentTicket.movie_name" />
          <van-cell title="手机" :value="maskPhone(currentTicket.phone)" />
          <van-cell title="张数" :value="`${currentTicket.quantity} 张`" />
          <van-cell title="出票时间" :value="currentTicket.issued_at" />
          <van-cell title="核销时间" :value="currentTicket.checked_at" />
          <van-cell v-if="userStore.isAdmin && currentTicket.checker_name" title="核销人" :value="currentTicket.checker_name" />
        </van-cell-group>
        <div v-if="currentTicket.qr_base64" class="qr-area">
          <img :src="currentTicket.qr_base64" alt="二维码" class="qr-img" />
          <p class="qr-hint">长按图片可保存或转发</p>
        </div>
      </div>
    </van-action-sheet>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { showToast } from 'vant'
import { getCheckHistory, getTicketDetail } from '@/api/tickets'
import { getAllMovies } from '@/api/movies'
import { useUserStore } from '@/store/user'
import { maskPhone } from '@/utils/phone'

const userStore = useUserStore()
const list = ref([])
const loading = ref(false)
const finished = ref(false)
const filterMovie = ref(0)
const filterDateRange = ref('')
const startDateStr = ref('')
const endDateStr = ref('')
const showStartPicker = ref(false)
const showEndPicker = ref(false)
const detailVisible = ref(false)
const currentTicket = ref(null)
const page = ref(1)
const pageSize = 20
const refreshing = ref(false)

const movieOptions = ref([{ text: '全部电影', value: 0 }])
const dateRangeOptions = [
  { text: '全部日期', value: '' },
  { text: '今天', value: 'today' },
  { text: '最近7天', value: '7d' },
  { text: '最近30天', value: '30d' },
  { text: '自定义', value: 'custom' }
]

const today = new Date()
const minDate = new Date(2020, 0, 1)
const maxDate = new Date(today.getFullYear() + 1, 11, 31)

const startDateArr = ref(['2024', '01', '01'])
const endDateArr = ref([String(today.getFullYear()), String(today.getMonth() + 1).padStart(2, '0'), String(today.getDate()).padStart(2, '0')])

function formatDateArrToStr(arr) {
  if (!arr || arr.length < 3) return ''
  const [y, m, d] = arr
  return `${y}-${String(m).padStart(2, '0')}-${String(d).padStart(2, '0')}`
}

function getDateRangeParams() {
  let start = null
  let end = null
  if (filterDateRange.value === 'today') {
    const d = new Date()
    const s = `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`
    start = s
    end = s
  } else if (filterDateRange.value === '7d') {
    const endD = new Date()
    const startD = new Date(endD)
    startD.setDate(startD.getDate() - 6)
    start = `${startD.getFullYear()}-${String(startD.getMonth() + 1).padStart(2, '0')}-${String(startD.getDate()).padStart(2, '0')}`
    end = `${endD.getFullYear()}-${String(endD.getMonth() + 1).padStart(2, '0')}-${String(endD.getDate()).padStart(2, '0')}`
  } else if (filterDateRange.value === '30d') {
    const endD = new Date()
    const startD = new Date(endD)
    startD.setDate(startD.getDate() - 29)
    start = `${startD.getFullYear()}-${String(startD.getMonth() + 1).padStart(2, '0')}-${String(startD.getDate()).padStart(2, '0')}`
    end = `${endD.getFullYear()}-${String(endD.getMonth() + 1).padStart(2, '0')}-${String(endD.getDate()).padStart(2, '0')}`
  } else if (filterDateRange.value === 'custom' && startDateStr.value && endDateStr.value) {
    start = startDateStr.value
    end = endDateStr.value
  }
  return { start_date: start, end_date: end }
}

function onStartDateConfirm(e) {
  const arr = e?.selectedValues ?? startDateArr.value
  startDateStr.value = formatDateArrToStr(arr)
  showStartPicker.value = false
}

function onEndDateConfirm(e) {
  const arr = e?.selectedValues ?? endDateArr.value
  endDateStr.value = formatDateArrToStr(arr)
  showEndPicker.value = false
}

function applyDateFilter() {
  if (!startDateStr.value || !endDateStr.value) {
    showToast('请选择开始和结束日期')
    return
  }
  if (startDateStr.value > endDateStr.value) {
    showToast('开始日期不能晚于结束日期')
    return
  }
  onFilterChange()
}

async function loadMovies() {
  try {
    const ms = await getAllMovies()
    movieOptions.value = [{ text: '全部电影', value: 0 }, ...ms.map(m => ({ text: m.name, value: m.id }))]
  } catch {
    movieOptions.value = [{ text: '全部电影', value: 0 }]
  }
}

async function loadList() {
  if (loading.value) return
  loading.value = true
  try {
    const { start_date, end_date } = getDateRangeParams()
    const res = await getCheckHistory({
      page: page.value,
      page_size: pageSize,
      movie_id: filterMovie.value || undefined,
      start_date: start_date || undefined,
      end_date: end_date || undefined
    })
    const items = res.items || res.list || res || []
    if (page.value === 1) {
      list.value = items
    } else {
      list.value = [...list.value, ...items]
    }
    finished.value = items.length < pageSize
    page.value++
  } catch {
    list.value = page.value === 1 ? [] : list.value
    finished.value = true
  } finally {
    loading.value = false
    refreshing.value = false
  }
}

function onFilterChange() {
  page.value = 1
  finished.value = false
  list.value = []
  loadList()
}

async function onRefresh() {
  page.value = 1
  finished.value = false
  list.value = []
  await loadList()
}

async function showDetail(t) {
  try {
    const detail = await getTicketDetail(t.id)
    currentTicket.value = detail
    detailVisible.value = true
  } catch (e) {
    showToast(e.response?.data?.detail || '加载详情失败')
  }
}

onMounted(() => {
  loadMovies()
  loadList()
})
</script>

<style scoped>
.date-filter-row {
  display: flex;
  align-items: center;
  padding: 8px 16px;
  gap: 8px;
  background: #fff;
}
.date-filter-row .van-field { flex: 1; }
.detail-content { padding: 16px; }
.qr-area { text-align: center; margin: 16px 0; }
.qr-img { width: 180px; height: 180px; }
.qr-hint { font-size: 12px; color: #999; margin-top: 8px; }
</style>
