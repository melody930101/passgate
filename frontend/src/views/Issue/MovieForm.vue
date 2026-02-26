<template>
  <van-popup v-model:show="visible" position="bottom" round>
    <van-form @submit="onSubmit">
      <van-field
        v-model="form.name"
        label="电影名称"
        placeholder="请输入"
        :rules="[
          { required: true, message: '请输入电影名称' },
          { validator: (v) => !v || v.length <= 30, message: '电影名称最长30字' }
        ]"
      />
      <van-field
        v-model="form.start_date"
        is-link
        readonly
        label="放映开始日期"
        placeholder="选择日期"
        @click="showDatePicker('start')"
      />
      <van-field
        v-model="form.end_date"
        is-link
        readonly
        label="放映结束日期"
        placeholder="选择日期"
        @click="showDatePicker('end')"
      />
      <van-field v-model="form.price" type="digit" label="优惠价格(元)" placeholder="选填" />
      <van-field
        v-model="form.remark"
        type="textarea"
        label="备注"
        placeholder="选填，最长100字"
        rows="2"
        :rules="[{ validator: (v) => !v || v.length <= 100, message: '备注最长100字' }]"
      />
      <van-button block type="primary" native-type="submit">保存</van-button>
    </van-form>
    <van-date-picker
      v-model:show="pickerVisible"
      v-model="pickerDate"
      type="date"
      :min-date="endDateMinDate"
      title="选择日期"
      @confirm="onDateConfirm"
    />
  </van-popup>
</template>

<script setup>
import { ref, reactive, watch, computed } from 'vue'
import { showToast } from 'vant'
import { createMovie, updateMovie } from '@/api/movies'

const props = defineProps({ show: Boolean, movie: Object })
const emit = defineEmits(['update:show', 'saved'])

const visible = computed({
  get: () => props.show,
  set: v => emit('update:show', v)
})

const form = reactive({
  name: '',
  start_date: '',
  end_date: '',
  price: '',
  remark: ''
})

const pickerVisible = ref(false)
const pickerType = ref('')
const pickerDate = ref(['2024', '01', '01'])

const endDateMinDate = computed(() => {
  if (pickerType.value === 'end' && form.start_date) {
    return new Date(form.start_date)
  }
  return undefined
})

watch(() => props.movie, m => {
  if (m) {
    form.name = m.name || ''
    form.start_date = m.start_date || ''
    form.end_date = m.end_date || ''
    form.price = m.price != null ? String(m.price) : ''
    form.remark = m.remark || ''
  } else {
    Object.assign(form, { name: '', start_date: '', end_date: '', price: '', remark: '' })
  }
}, { immediate: true })

function showDatePicker(type) {
  pickerType.value = type
  const d = (type === 'start' ? form.start_date : form.end_date) || '2024-01-01'
  pickerDate.value = d.split('-')
  pickerVisible.value = true
}

function onDateConfirm({ selectedValues }) {
  const str = selectedValues.join('-')
  if (pickerType.value === 'start') form.start_date = str
  else form.end_date = str
}

async function onSubmit() {
  if (form.end_date && form.start_date && form.end_date < form.start_date) {
    showToast('结束日期须晚于开始日期')
    return
  }
  try {
    if (props.movie?.id) {
      await updateMovie(props.movie.id, form)
    } else {
      await createMovie(form)
    }
    showToast('保存成功')
    visible.value = false
    emit('saved')
  } catch (e) {
    showToast(e.response?.data?.detail || '保存失败')
  }
}
</script>
