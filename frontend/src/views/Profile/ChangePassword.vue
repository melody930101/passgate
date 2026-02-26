<template>
  <div class="password-page">
    <van-nav-bar title="修改密码" left-arrow @click-left="$router.back()" />
    <van-form @submit="onSubmit">
      <van-cell-group inset>
        <van-field
          v-model="form.old_password"
          type="password"
          label="当前密码"
          placeholder="请输入当前密码"
          :rules="[{ required: true, message: '请输入当前密码' }]"
        />
        <van-field
          v-model="form.new_password"
          type="password"
          label="新密码"
          placeholder="至少6位"
          :rules="[{ required: true, message: '请输入新密码' }, { min: 6, message: '至少6位' }]"
        />
        <van-field
          v-model="form.confirm_password"
          type="password"
          label="确认新密码"
          placeholder="再次输入新密码"
          :rules="[
            { required: true, message: '请确认新密码' },
            { validator: () => form.new_password === form.confirm_password, message: '两次密码不一致' }
          ]"
        />
      </van-cell-group>
      <div class="btn-wrap">
        <van-button block type="primary" native-type="submit" :loading="loading">
          确 认 修 改
        </van-button>
      </div>
    </van-form>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { showToast } from 'vant'
import { changePassword } from '@/api/auth'

const router = useRouter()
const loading = ref(false)
const form = reactive({
  old_password: '',
  new_password: '',
  confirm_password: ''
})

async function onSubmit() {
  if (form.new_password !== form.confirm_password) {
    showToast('两次密码不一致')
    return
  }
  loading.value = true
  try {
    await changePassword({
      old_password: form.old_password,
      new_password: form.new_password
    })
    showToast('修改成功')
    router.back()
  } catch (e) {
    showToast(e.response?.data?.detail || '修改失败')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.password-page { background: #f5f5f7; min-height: 100%; }
.btn-wrap { margin: 24px 16px 0; }
</style>
