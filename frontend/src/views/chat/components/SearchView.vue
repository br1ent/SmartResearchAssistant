<script setup>
import { ref } from 'vue'
import { MessageCircle, Search, ArrowLeft } from '@lucide/vue'

const searchText = ref('')
const chats = ref([
  { id: 1, title: '深度学习在医学影像中的应用', updated_at: '2026-07-12 10:30' },
  { id: 2, title: '自然语言处理最新进展', updated_at: '2026-07-11 14:20' },
  { id: 3, title: '强化学习在机器人控制中的应用', updated_at: '2026-07-10 09:15' },
])
const filtered = ref([...chats.value])
const loading = ref(false)

const emit = defineEmits(['close', 'selectChat'])

function doSearch() {
  const q = searchText.value.trim().toLowerCase()
  if (!q) {
    filtered.value = chats.value
    return
  }
  filtered.value = chats.value.filter(c => c.title.toLowerCase().includes(q))
}

function selectChat(chat) {
  emit('selectChat', chat)
  emit('close')
}
</script>

<template>
  <div class="flex flex-col h-full">
    <!-- 顶部 -->
    <div class="p-4 border-b border-base-200 flex items-center gap-3">
      <button class="btn btn-ghost btn-sm btn-circle" @click="$emit('close')">
        <ArrowLeft class="w-4 h-4" />
      </button>
      <div class="relative flex-1">
        <Search class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-base-content/40" />
        <input
          v-model="searchText"
          type="text"
          class="input input-bordered w-full pl-10"
          placeholder="搜索对话..."
          @input="doSearch"
          ref="searchInput"
          autofocus
        />
      </div>
    </div>

    <!-- 结果列表 -->
    <div class="flex-1 overflow-y-auto p-3">
      <div v-if="filtered.length === 0" class="text-sm text-base-content/40 text-center py-8">
        未找到匹配的对话
      </div>

      <div v-else class="flex flex-col gap-1">
        <div
          v-for="chat in filtered"
          :key="chat.id"
          class="flex items-center gap-3 px-3 py-3 rounded-lg hover:bg-base-200 cursor-pointer transition-colors"
          @click="selectChat(chat)"
        >
          <MessageCircle class="w-5 h-5 shrink-0 text-base-content/40" />
          <div class="flex-1 min-w-0">
            <p class="text-sm font-medium truncate">{{ chat.title }}</p>
            <p class="text-xs text-base-content/30">{{ chat.updated_at }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
