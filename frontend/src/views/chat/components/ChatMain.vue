<script setup>
import { ref } from 'vue'
import { Send } from '@lucide/vue'
import { useUserStore } from '@/stores/user.js'
import AvatarBox from './AvatarBox.vue'

const userStore = useUserStore()
const inputText = ref('')
const messages = ref([])

function sendMessage() {
  const text = inputText.value.trim()
  if (!text) return

  messages.value.push({
    role: 'user',
    content: text,
    time: new Date().toLocaleTimeString(),
  })

  inputText.value = ''

  // TODO: 调用后端 API 获取 AI 回复
}
</script>

<template>
  <div class="flex flex-col h-full">
    <!-- 欢迎区域 -->
    <div v-if="messages.length === 0" class="flex-1 flex flex-col items-center justify-center px-6">
      <h2 class="text-2xl font-bold mb-2">
        {{ userStore.username }}，今天想研究些什么领域？
      </h2>
      <p class="text-base-content/50 text-center max-w-md">
        请输入一个研究主题，我将为你规划研究任务、搜索资料并生成报告
      </p>
    </div>

    <!-- 消息列表 -->
    <div v-else class="flex-1 overflow-y-auto px-6 py-4 space-y-4">
      <div
        v-for="(msg, i) in messages"
        :key="i"
        class="flex gap-3 items-start"
        :class="msg.role === 'user' ? 'flex-row-reverse' : 'flex-row'"
      >
        <AvatarBox :role="msg.role" />

        <div
          class="max-w-[70%] rounded-2xl px-4 py-2.5"
          :class="msg.role === 'user' ? 'bg-success/20 rounded-tr-md' : 'bg-base-200 rounded-tl-md'"
        >
          <p class="text-sm whitespace-pre-wrap">{{ msg.content }}</p>
          <p class="text-xs mt-1 text-base-content/40 text-right">{{ msg.time }}</p>
        </div>
      </div>
    </div>

    <!-- 输入区域 -->
    <div class="border-t border-base-200 p-4">
      <div class="max-w-4xl mx-auto flex gap-2">
        <input
          v-model="inputText"
          type="text"
          class="input input-bordered flex-1 rounded-full"
          placeholder="输入研究主题..."
          @keydown.enter="sendMessage"
        />
        <button
          class="btn btn-neutral btn-circle"
          :disabled="!inputText.trim()"
          @click="sendMessage"
        >
          <Send class="w-4 h-4" />
        </button>
      </div>
    </div>
  </div>
</template>
