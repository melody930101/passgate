<template>
  <van-popup
    v-model:show="visible"
    position="left"
    :style="{ width: '85%', height: '100%' }"
  >
    <div class="drawer-header">
      <span>管理电影</span>
      <van-icon name="cross" @click="visible = false" />
    </div>
    <van-list v-if="movies.length">
      <van-swipe-cell v-for="m in movies" :key="m.id">
        <van-cell
          :title="m.name"
          :label="`${m.start_date} ~ ${m.end_date}${m.is_active ? '' : ' (已下架)'}`"
          is-link
          @click="openForm(m)"
        />
        <template v-if="m.is_active" #right>
          <van-button
            square
            type="danger"
            text="下架"
            class="deactivate-btn"
            @click.stop="handleDeactivate(m)"
          />
        </template>
      </van-swipe-cell>
    </van-list>
    <van-empty v-else description="暂无电影" />
    <div class="footer">
      <van-button type="primary" block @click="openForm()">新增电影</van-button>
    </div>
    <MovieForm v-model:show="formVisible" :movie="editingMovie" @saved="onSaved" />
  </van-popup>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { showConfirmDialog, showToast } from 'vant'
import { getAllMovies, deactivateMovie } from '@/api/movies'
import MovieForm from './MovieForm.vue'

const props = defineProps({ show: Boolean })
const emit = defineEmits(['update:show', 'refresh'])

const visible = computed({
  get: () => props.show,
  set: v => emit('update:show', v)
})

const movies = ref([])
const formVisible = ref(false)
const editingMovie = ref(null)

async function loadMovies() {
  try {
    movies.value = await getAllMovies()
  } catch {
    movies.value = []
  }
}

function openForm(m = null) {
  editingMovie.value = m ? { ...m } : null
  formVisible.value = true
}

function onSaved() {
  loadMovies()
  emit('refresh')
}

async function handleDeactivate(m) {
  try {
    await showConfirmDialog({
      title: '确认下架',
      message: `确定要下架「${m.name}」吗？下架后该电影将不出现在出票选择中。`
    })
  } catch {
    return
  }
  try {
    await deactivateMovie(m.id)
    showToast('已下架')
    loadMovies()
    emit('refresh')
  } catch (e) {
    showToast(e.response?.data?.detail || '下架失败')
  }
}

watch(() => props.show, v => v && loadMovies())
</script>

<style scoped>
.drawer-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  border-bottom: 1px solid #eee;
}
.footer { padding: 16px; }
.deactivate-btn { height: 100%; }
</style>
