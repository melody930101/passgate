<template>
  <div class="tab-layout">
    <div class="tab-content">
      <router-view />
    </div>
    <TabBar />
  </div>
</template>

<script setup>
import TabBar from './TabBar.vue'
</script>

<style scoped>
.tab-layout {
  display: flex;
  flex-direction: column;
  height: 100%;
  padding-bottom: 50px;
}
.tab-content {
  flex: 1;
  overflow: auto;
}
</style>
