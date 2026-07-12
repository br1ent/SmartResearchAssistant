<script setup>
import { ref, onMounted } from 'vue'
import { MessageCircle, Trash2 } from '@lucide/vue'

const chats = ref([])
const loading = ref(true)

defineEmits(['selectChat'])

onMounted(async () => {
  // TODO: API call to fetch chat history
  chats.value = [
    { id: 1, title: '深度学习在医学影像中的应用', updated_at: '2026-07-12 10:30' },
    { id: 2, title: '自然语言处理最新进展', updated_at: '2026-07-11 14:20' },
    { id: 3, title: '强化学习在机器人控制中的应用', updated_at: '2026-07-10 09:15' },
  ]
  loading.value = false
})
</script>

<template>
  <div class="flex flex-col">
    <h3 class="text-xs font-bold text-base-content/50 uppercase tracking-wider mb-2 px-1">
      最近对话
    </h3>

    <div v-if="loading" class="flex justify-center py-4">
      <span class="loading loading-spinner loading-sm"></span>
    </div>

    <div v-else-if="chats.length === 0" class="text-sm text-base-content/40 text-center py-4">
      暂无对话记录
    </div>

    <div v-else class="flex flex-col gap-1">
      <div
        v-for="chat in chats"
        :key="chat.id"
        class="group flex items-center gap-2 px-2 py-2 rounded-lg hover:bg-base-200 cursor-pointer transition-colors"
        @click="$emit('selectChat', chat)"
      >
        <MessageCircle class="w-4 h-4 shrink-0 text-base-content/40" />
        <div class="flex-1 min-w-0">
          <p class="text-sm truncate">{{ chat.title }}</p>
          <p class="text-xs text-base-content/30">{{ chat.updated_at }}</p>
        </div>
        <button
          class="opacity-0 group-hover:opacity-100 btn btn-ghost btn-xs text-error"
          @click.stop
        >
          <Trash2 class="w-3.5 h-3.5" />
        </button>
      </div>
    </div>
  </div>
</template>
