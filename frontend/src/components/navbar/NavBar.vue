<script setup>
</script>

<template>
  <div class="navbar bg-base-100 shadow-sm">
    <div class="flex-1 navbar-start">
      <router-link :to="{name: 'home-index'}" class="btn btn-ghost text-xl">基于多智能体的研究助手</router-link>
    </div>
    <div class="flex-none">
      <ul class="menu menu-horizontal px-1">
        <li>
          <router-link :to="{name: 'chat-index'}" active-class="btn-active" class="btn btn-ghost">研究界面</router-link>
        </li>
        <li>
          <router-link :to="{name: 'user-login-index'}" active-class="btn-active" class="btn btn-ghost">登录</router-link>
        </li>
        <li>
          <router-link :to="{name: 'user-register-index'}" active-class="btn-active" class="btn btn-ghost">注册</router-link>
        </li>
      </ul>
    </div>
  </div>
</template>
