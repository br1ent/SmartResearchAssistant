<script setup>
import { computed } from 'vue'
import { useUserStore } from '@/stores/user.js'
import { Bot } from '@lucide/vue'

const props = defineProps({
  role: { type: String, required: true },
})

const userStore = useUserStore()

const photoUrl = computed(() => {
  if (props.role !== 'user') return ''
  const p = userStore.photo
  if (!p) return ''
  if (p.startsWith('http')) return p
  return 'http://localhost:8000' + p
})

const initial = computed(() => {
  return userStore.username?.charAt(0)?.toUpperCase() || 'U'
})
</script>

<template>
  <!-- 用户头像 -->
  <div
    v-if="role === 'user'"
    class="w-8 h-8 rounded-full overflow-hidden shrink-0 ring-2 ring-base-300"
  >
    <img v-if="photoUrl" :src="photoUrl" class="w-full h-full object-cover" alt="" />
    <div v-else class="w-full h-full bg-primary text-primary-content flex items-center justify-center text-sm font-bold">
      {{ initial }}
    </div>
  </div>

  <!-- AI 头像 -->
  <div
    v-else
    class="w-8 h-8 rounded-full bg-neutral text-neutral-content flex items-center justify-center shrink-0"
  >
    <Bot class="w-4 h-4" />
  </div>
</template>
