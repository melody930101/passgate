<template>
  <div class="profile-page">
    <van-nav-bar title="个人" />
    <div class="hero">
      <div class="avatar">
        <van-icon name="user-o" size="32" color="#fff" />
      </div>
      <div class="name">{{ userStore.name || '用户' }}</div>
      <div class="role-badge" :class="userStore.isAdmin ? 'admin' : 'staff'">
        {{ userStore.isAdmin ? '管理员' : '员工' }}
      </div>
    </div>
    <div class="stats">
      <div class="stat">
        <span class="num">{{ stats.issued_today }}</span>
        <span class="label">今日出票（张）</span>
      </div>
      <div class="stat">
        <span class="num">{{ stats.checked_today }}</span>
        <span class="label">今日核销（张）</span>
      </div>
    </div>
    <van-cell-group inset>
      <van-cell title="修改密码" is-link @click="$router.push('/profile/password')" />
      <van-cell title="退出登录" is-link class="logout" @click="logout" />
    </van-cell-group>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { showConfirmDialog, showToast } from 'vant'
import { getTodayStats } from '@/api/stats'
import { useUserStore } from '@/store/user'

const userStore = useUserStore()
const router = useRouter()
const stats = ref({ issued_today: 0, checked_today: 0 })

async function loadStats() {
  try {
    const res = await getTodayStats()
    stats.value = res
  } catch {
    stats.value = { issued_today: 0, checked_today: 0 }
  }
}

async function logout() {
  try {
    await showConfirmDialog({ title: '确认退出', message: '确定要退出登录吗？' })
  } catch {
    return
  }
  userStore.logout()
  showToast('已退出')
  router.replace('/login')
}

onMounted(loadStats)
</script>

<style scoped>
.profile-page { background: #f5f5f7; min-height: 100%; }
.hero {
  background: linear-gradient(160deg, #1a1a2e 0%, #2d2d44 100%);
  padding: 24px 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
}
.avatar {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  background: linear-gradient(135deg, #E63946, #c1121f);
  display: flex;
  align-items: center;
  justify-content: center;
}
.name { font-size: 18px; font-weight: 600; color: #fff; }
.role-badge {
  font-size: 10px; font-weight: 600; letter-spacing: 1px;
  padding: 3px 10px; border-radius: 20px;
}
.role-badge.admin { background: rgba(25,118,210,0.15); color: #1976d2; border: 1px solid rgba(25,118,210,0.3); }
.role-badge.staff { background: rgba(158,158,158,0.15); color: #757575; border: 1px solid rgba(158,158,158,0.3); }
.stats {
  display: flex;
  margin: -16px 16px 0;
  background: #fff;
  border-radius: 14px;
  overflow: hidden;
  box-shadow: 0 4px 16px rgba(0,0,0,0.1);
}
.stat {
  flex: 1;
  padding: 16px;
  text-align: center;
  border-right: 1px solid #f0f0f0;
}
.stat:last-child { border-right: none; }
.num { font-size: 24px; font-weight: 700; color: #E63946; display: block; }
.label { font-size: 11px; color: #999; }
.logout { color: #e74c3c; }
</style>
