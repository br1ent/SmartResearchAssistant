<script setup>
import { ref } from 'vue'
import { MessageSquarePlus, Search } from '@lucide/vue'

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
      <Search class="w-5 h-5 shrink-0" />
      <span>搜索对话</span>
    </button>
  </div>
</template>
