<script setup>
import { ref } from 'vue'
import { MessageSquarePlus, Search, PanelLeft, PanelLeftClose } from '@lucide/vue'
import SidebarTool from './components/SidebarTool.vue'
import RecentChats from './components/RecentChats.vue'
import ChatMain from './components/ChatMain.vue'
import SearchView from './components/SearchView.vue'

const sidebarOpen = ref(true)
const showSearch = ref(false)

function onNewChat() {
  showSearch.value = false
}

function onShowSearch() {
  showSearch.value = true
}

function onCloseSearch() {
  showSearch.value = false
}

function onSelectChat(chat) {
  showSearch.value = false
}
</script>

<template>
  <div class="flex h-[calc(100vh-4rem)]">
    <!-- 展开的侧边栏 -->
    <transition name="sidebar">
      <aside
        v-if="sidebarOpen"
        class="w-72 shrink-0 bg-base-200/50 border-r border-base-200 flex flex-col overflow-hidden"
      >
        <div class="p-3 border-b border-base-200">
          <SidebarTool @newChat="onNewChat" @showSearch="onShowSearch" />
        </div>
        <div class="flex-1 overflow-y-auto p-3">
          <RecentChats @selectChat="onSelectChat" />
        </div>
      </aside>
    </transition>

    <!-- 收起时的迷你侧边栏 -->
    <transition name="sidebar-mini">
      <aside
        v-if="!sidebarOpen"
        class="w-14 shrink-0 bg-base-200/50 border-r border-base-200 flex flex-col items-center py-3 gap-3 overflow-hidden"
      >
        <button class="btn btn-ghost btn-sm btn-circle" @click="onNewChat" title="新对话">
          <MessageSquarePlus class="w-5 h-5" />
        </button>
        <button class="btn btn-ghost btn-sm btn-circle" @click="onShowSearch" title="搜索">
          <Search class="w-5 h-5" />
        </button>
      </aside>
    </transition>

    <!-- 右侧主区域 -->
    <main class="flex-1 flex flex-col min-w-0">
      <div class="flex items-center gap-2 px-4 py-2 border-b border-base-200 shrink-0">
        <button class="btn btn-ghost btn-sm btn-circle" @click="sidebarOpen = !sidebarOpen">
          <PanelLeftClose v-if="sidebarOpen" class="w-4 h-4" />
          <PanelLeft v-else class="w-4 h-4" />
        </button>
      </div>

      <SearchView
        v-if="showSearch"
        @close="onCloseSearch"
        @selectChat="onSelectChat"
      />

      <ChatMain v-else />
    </main>
  </div>
</template>

<style scoped>
.sidebar-enter-active,
.sidebar-leave-active {
  transition: width 0.25s ease, opacity 0.2s ease;
}
.sidebar-enter-from,
.sidebar-leave-to {
  width: 0 !important;
  opacity: 0;
  padding: 0;
  border: none;
}

.sidebar-mini-enter-active,
.sidebar-mini-leave-active {
  transition: width 0.25s ease, opacity 0.2s ease;
}
.sidebar-mini-enter-from,
.sidebar-mini-leave-to {
  width: 0 !important;
  opacity: 0;
  padding: 0;
  border: none;
}
</style>
