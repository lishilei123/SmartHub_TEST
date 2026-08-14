<script setup>
import { useRouter } from 'vue-router'
import { getToken, logout } from './api'
const router = useRouter()
function signOut(){ logout(); router.push('/login') }
</script>

<template>
  <header class="topbar">
    <strong>MiniTask</strong>
    <nav v-if="getToken()">
      <RouterLink to="/projects">项目</RouterLink>
      <RouterLink to="/dashboard">Dashboard</RouterLink>
      <button class="link-btn" @click="signOut">退出</button>
    </nav>
  </header>
  <main class="container"><RouterView /></main>
</template>
