<script setup>
</script>

<template>
  <main class="flex-1 flex items-center justify-center px-5 py-10">
    <div class="card w-full max-w-sm bg-base-100 shadow-xl">
      <div class="card-body">
        <h2 class="card-title text-xl justify-center mb-2">注册</h2>
        <div class="form-control mb-3">
          <label class="label"><span class="label-text">用户名</span></label>
          <input type="text" placeholder="请输入用户名" class="input input-bordered w-full" />
        </div>
        <div class="form-control mb-3">
          <label class="label"><span class="label-text">邮箱</span></label>
          <input type="email" placeholder="you@example.com" class="input input-bordered w-full" />
        </div>
        <div class="form-control mb-4">
          <label class="label"><span class="label-text">密码</span></label>
          <input type="password" placeholder="••••••••" class="input input-bordered w-full" />
        </div>
        <button class="btn btn-primary w-full">注册</button>
        <p class="text-center text-sm mt-3 text-base-content/60">
          已有账号？<router-link to="/login" class="link link-primary">登录</router-link>
        </p>
      </div>
    </div>
  </main>
</template>
