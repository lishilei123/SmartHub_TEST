<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { api, setToken } from '../api'
const username = ref('admin')
const password = ref('admin123')
const error = ref('')
const router = useRouter()
async function submit(){
  error.value=''
  try{ const data=await api('/login',{method:'POST',body:JSON.stringify({username:username.value,password:password.value})}); setToken(data.token); router.push('/projects') }
  catch(e){ error.value=e.message }
}
</script>
<template><section class="card" style="max-width:430px;margin:70px auto"><h1>登录 MiniTask</h1><p class="muted">演示账号：admin / admin123</p><form @submit.prevent="submit"><div class="card"><input v-model="username" data-testid="username" placeholder="用户名"></div><div class="card"><input v-model="password" data-testid="password" type="password" placeholder="密码"></div><p v-if="error" class="error">{{error}}</p><button data-testid="login-submit">登录</button></form></section></template>
