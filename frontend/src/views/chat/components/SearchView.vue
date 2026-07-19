<script setup>
import { ref, onMounted } from 'vue'
import { MessageCircle, Search as SearchIcon, ArrowLeft, Loader2 } from '@lucide/vue'
import http from '@/js/http/api.js'
import { useChatStore } from '@/stores/chat.js'

const chatStore = useChatStore()

const searchText = ref('')
const results = ref([])
const loading = ref(false)

const emit = defineEmits(['close', 'selectChat'])

function doSearch() {
  const q = searchText.value.trim()
  if (!q) {
    results.value = chatStore.conversations
    return
  }
  loading.value = true
  http.get('/api/chat/conversations/search', { params: { q } })
    .then(res => {
      results.value = res.data?.data || []
    })
    .catch(() => { results.value = [] })
    .finally(() => { loading.value = false })
}

function selectChat(conv) {
  chatStore.selectConversation(conv)
  emit('selectChat', conv)
  emit('close')
}

onMounted(() => {
  results.value = chatStore.conversations
})
</script>

<template>
  <div class="flex flex-col h-full">
    <div class="p-4 border-b border-base-200 flex items-center gap-3">
      <button class="btn btn-ghost btn-sm btn-circle" @click="$emit('close')">
        <ArrowLeft class="w-4 h-4" />
      </button>
      <div class="relative flex-1">
        <SearchIcon class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-base-content/40" />
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

    <div class="flex-1 overflow-y-auto p-3">
      <div v-if="loading" class="flex items-center justify-center py-8">
        <Loader2 class="w-5 h-5 animate-spin text-base-content/40" />
      </div>
      <div v-else-if="results.length === 0" class="text-sm text-base-content/40 text-center py-8">
        未找到匹配的对话
      </div>
      <div v-else class="flex flex-col gap-1">
        <div
          v-for="conv in results"
          :key="conv.id"
          class="flex items-center gap-3 px-3 py-3 rounded-lg hover:bg-base-200 cursor-pointer transition-colors"
          @click="selectChat(conv)"
        >
          <MessageCircle class="w-5 h-5 shrink-0 text-base-content/40" />
          <div class="flex-1 min-w-0">
            <p class="text-sm font-medium truncate" :title="conv.title">{{ conv.title }}</p>
            <p class="text-xs text-base-content/30">{{ conv.id }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
