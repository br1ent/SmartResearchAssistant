<script setup>
import { ref } from 'vue'
import { PanelLeft, MessageSquarePlus, Search } from '@lucide/vue'
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
        <!-- 顶部标题栏 -->
        <div class="flex items-center justify-between px-3 py-3 border-b border-base-200">
          <div class="flex items-center gap-3">
            <PanelLeft class="w-5 h-5 shrink-0 text-base-content/60" />
            <span class="font-semibold">多智能体研究</span>
          </div>
          <button class="btn btn-ghost btn-xs btn-circle" @click="sidebarOpen = false" title="收起侧边栏">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 9V5.25A2.25 2.25 0 0 0 13.5 3h-6a2.25 2.25 0 0 0-2.25 2.25v13.5A2.25 2.25 0 0 0 7.5 21h6a2.25 2.25 0 0 0 2.25-2.25V15M12 9l-3 3m0 0 3 3m-3-3h12.75" />
            </svg>
          </button>
        </div>
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
        <button class="btn btn-ghost btn-sm btn-circle" @click="sidebarOpen = true" title="展开侧边栏">
          <PanelLeft class="w-5 h-5" />
        </button>
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
