<script setup>
import { ref } from 'vue'
import { MessageSquarePlus } from '@lucide/vue'

const emit = defineEmits(['newChat', 'showSearch'])

function onNewChat() {
  emit('newChat')
}
</script>

<template>
  <div class="flex flex-col gap-3">
    <button class="btn btn-ghost w-full justify-start gap-3 px-3" @click="onNewChat">
      <MessageSquarePlus class="w-5 h-5 shrink-0" />
      <span>发起新对话</span>
    </button>

    <button class="btn btn-ghost w-full justify-start gap-3 px-3" @click="$emit('showSearch')">
      <svg class="w-5 h-5 shrink-0" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" d="m21 21-5.197-5.197m0 0A7.5 7.5 0 1 0 5.196 5.196a7.5 7.5 0 0 0 10.607 10.607Z" />
      </svg>
      <span>搜索对话</span>
    </button>
  </div>
</template>
