<template>
  <van-tabbar v-model="active" route>
    <van-tabbar-item to="/issue" icon="description">出票</van-tabbar-item>
    <van-tabbar-item to="/verify" icon="scan">检票</van-tabbar-item>
    <van-tabbar-item to="/profile" icon="user-o">个人</van-tabbar-item>
  </van-tabbar>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const active = computed(() => {
  const p = route.path
  if (p.startsWith('/issue')) return 0
  if (p.startsWith('/verify')) return 1
  if (p.startsWith('/profile')) return 2
  return 0
})
</script>
