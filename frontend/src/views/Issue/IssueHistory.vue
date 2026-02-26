<template>
  <div class="history-page">
    <van-nav-bar title="出票历史" left-arrow @click-left="$router.back()" />
    <van-dropdown-menu>
      <van-dropdown-item v-model="filterMovie" :options="movieOptions" @change="onFilterChange" />
      <van-dropdown-item v-model="filterStatus" :options="statusOptions" @change="onFilterChange" />
    </van-dropdown-menu>
    <van-pull-refresh v-model="refreshing" @refresh="onRefresh">
    <van-list v-model:loading="loading" :finished="finished" finished-text="没有更多" @load="loadList">
      <TicketCard
        v-for="t in list"
        :key="t.id"
        :movie-name="t.movie_name"
        :phone="t.phone"
        :quantity="t.quantity"
        :issued-at="t.issued_at"
        :status="t.status"
        :issuer-name="t.issuer_name"
        :show-issuer="userStore.isAdmin"
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
          <van-cell title="状态" :value="statusText(currentTicket.status)" />
        </van-cell-group>
        <div v-if="currentTicket.qr_base64" class="qr-area">
          <img :src="currentTicket.qr_base64" alt="二维码" class="qr-img" />
          <p class="qr-hint">长按图片可保存或转发</p>
        </div>
        <van-button
          v-if="currentTicket.status === 'unused'"
          type="danger"
          block
          class="void-btn"
          @click="voidTicket"
        >
          作废
        </van-button>
      </div>
    </van-action-sheet>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { showToast, showConfirmDialog } from 'vant'
import { getTickets, getTicketDetail, voidTicket as apiVoid } from '@/api/tickets'
import { getAllMovies } from '@/api/movies'
import { useUserStore } from '@/store/user'
import { maskPhone } from '@/utils/phone'
import TicketCard from '@/components/TicketCard.vue'

const userStore = useUserStore()
const router = useRouter()
const list = ref([])
const loading = ref(false)
const finished = ref(false)
const filterMovie = ref(0)
const filterStatus = ref('')
const detailVisible = ref(false)
const currentTicket = ref(null)
const page = ref(1)
const pageSize = 20
const refreshing = ref(false)

const movieOptions = ref([{ text: '全部电影', value: 0 }])
const statusOptions = [
  { text: '全部', value: '' },
  { text: '未核销', value: 'unused' },
  { text: '已核销', value: 'used' },
  { text: '已作废', value: 'voided' }
]

async function loadMovies() {
  const ms = await getAllMovies()
  movieOptions.value = [{ text: '全部电影', value: 0 }, ...ms.map(m => ({ text: m.name, value: m.id }))]
}

async function loadList() {
  if (loading.value) return
  loading.value = true
  try {
    const res = await getTickets({
      page: page.value,
      page_size: pageSize,
      movie_id: filterMovie.value || undefined,
      status: filterStatus.value || undefined
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

function statusText(s) {
  const map = { unused: '未核销', used: '已核销', voided: '已作废' }
  return map[s] || s
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

async function voidTicket() {
  try {
    await showConfirmDialog({ title: '确认作废', message: '确定要作废此票吗？' })
  } catch {
    return
  }
  try {
    await apiVoid(currentTicket.value.id)
    showToast('已作废')
    currentTicket.value.status = 'voided'
    page.value = 1
    finished.value = false
    list.value = []
    loadList()
  } catch (e) {
    showToast(e.response?.data?.detail || '作废失败')
  }
}

onMounted(() => {
  loadMovies()
  loadList()
})
</script>

<style scoped>
.detail-content { padding: 16px; }
.qr-area { text-align: center; margin: 16px 0; }
.qr-img { width: 180px; height: 180px; }
.qr-hint { font-size: 12px; color: #999; margin-top: 8px; }
.void-btn { margin-top: 16px; }
</style>
