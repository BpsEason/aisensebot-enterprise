<template>
  <div class="h-screen flex items-center justify-center p-4">
    <div class="bg-white rounded-2xl shadow-xl w-full max-w-lg h-full max-h-[800px] flex flex-col">
      <header class="p-4 border-b border-slate-200 flex items-center gap-4">
        <img src="/src/assets/logo.svg" alt="AI Sensebot Logo" class="h-8 w-8 text-indigo-500" />
        <h1 class="text-xl font-bold text-slate-800">AI Sensebot 助理</h1>
      </header>
      <ChatWindow />
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue';
import { useChatStore } from './store/chat';
import ChatWindow from './components/ChatWindow.vue';

const chatStore = useChatStore();

onMounted(() => {
  chatStore.connectWebSocket();
});
</script>
