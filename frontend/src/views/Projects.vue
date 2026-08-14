<script setup>
import { onMounted, ref } from 'vue'
import { api } from '../api'
const projects=ref([]), name=ref(''), description=ref(''), error=ref('')
async function load(){ projects.value=await api('/projects') }
async function create(){ error.value=''; try{await api('/projects',{method:'POST',body:JSON.stringify({name:name.value,description:description.value})});name.value='';description.value='';await load()}catch(e){error.value=e.message}}
async function rename(p){ const next=prompt('新的项目名称',p.name); if(!next)return; await api(`/projects/${p.id}`,{method:'PUT',body:JSON.stringify({name:next})}); await load() }
async function remove(p){
  // BUG-07: 需求要求删除项目二次确认，这里故意直接删除。
  await api(`/projects/${p.id}`,{method:'DELETE'}); await load()
}
onMounted(load)
</script>
<template><div class="row between"><div><h1>项目</h1><p class="muted">创建项目并进入任务管理。</p></div></div><section class="card"><h3>新建项目</h3><div class="row"><input v-model="name" data-testid="project-name" placeholder="项目名称"><input v-model="description" placeholder="描述"><button data-testid="project-create" @click="create">创建</button></div><p v-if="error" class="error">{{error}}</p></section><section class="card"><div v-for="p in projects" :key="p.id" class="task" :data-testid="`project-${p.id}`"><div><strong>{{p.name}}</strong><div class="muted">{{p.description || '无描述'}}</div></div><RouterLink class="btn secondary" :to="`/projects/${p.id}/tasks`">任务</RouterLink><button class="secondary" @click="rename(p)">改名</button><button class="danger" :data-testid="`project-delete-${p.id}`" @click="remove(p)">删除</button></div></section></template>
