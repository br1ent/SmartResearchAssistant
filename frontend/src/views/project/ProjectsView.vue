<script setup>
</script>

<template>
  <main class="flex-1 px-5 py-10 max-w-screen-xl mx-auto w-full">
    <div class="flex items-center justify-between mb-6">
      <h1 class="text-2xl font-semibold">项目列表</h1>
      <button class="btn btn-neutral btn-sm">新建项目</button>
    </div>
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      <div class="card bg-base-100 shadow-md border border-base-200">
        <div class="card-body">
          <h3 class="card-title text-base">示例项目</h3>
          <p class="text-sm text-base-content/60">这是一个示例研究项目</p>
          <div class="card-actions justify-end mt-2">
            <button class="btn btn-ghost btn-xs">进入</button>
          </div>
        </div>
      </div>
    </div>
  </main>
</template>
