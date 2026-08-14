<script setup>
import { onMounted, ref } from 'vue'
import { api } from '../api'
const data=ref({projects:0,tasks:0,completed:0,unfinished:0})
onMounted(async()=>data.value=await api('/dashboard'))
</script>
<template><h1>Dashboard</h1><p class="muted">项目和任务统计。</p><div class="grid"><div class="card"><div class="muted">项目数</div><div class="stat" data-testid="dashboard-projects">{{data.projects}}</div></div><div class="card"><div class="muted">任务数</div><div class="stat" data-testid="dashboard-tasks">{{data.tasks}}</div></div><div class="card"><div class="muted">已完成</div><div class="stat" data-testid="dashboard-completed">{{data.completed}}</div></div><div class="card"><div class="muted">未完成</div><div class="stat">{{data.unfinished}}</div></div></div></template>
