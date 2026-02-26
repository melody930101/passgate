<template>
  <van-nav-bar
    :title="title"
    :left-text="leftText"
    :right-text="rightText"
    :left-arrow="leftArrow"
    @click-left="handleLeft"
    @click-right="handleRight"
  />
</template>

<script setup>
defineProps({
  title: { type: String, default: '' },
  leftText: { type: String, default: '' },
  rightText: { type: String, default: '' },
  leftArrow: { type: Boolean, default: false }
})

const emit = defineEmits(['click-left', 'click-right'])

function handleLeft() {
  emit('click-left')
}
function handleRight() {
  emit('click-right')
}
</script>
