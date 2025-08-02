<template>
  <form @submit.prevent="handleSendMessage" class="input-area p-4 border-t border-slate-200 flex items-center gap-2">
    <input
      v-model="messageText"
      type="text"
      placeholder="輸入你的訊息..."
      class="flex-1 p-3 rounded-full border border-slate-300 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition-all"
    />
    <button
      type="submit"
      :disabled="!messageText.trim() || chatStore.isTyping"
      :class="[
        'p-3 rounded-full text-white transition-colors',
        !messageText.trim() || chatStore.isTyping
          ? 'bg-slate-400 cursor-not-allowed'
          : 'bg-indigo-500 hover:bg-indigo-600 active:bg-indigo-700'
      ]"
    >
      <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-send-horizontal"><path d="m3 3 3 9-3 9 19-9Z"/><path d="M6 12h16"/></svg>
    </button>
  </form>
</template>

<script setup>
import { ref } from 'vue';
import { useChatStore } from '../store/chat';

const chatStore = useChatStore();
const messageText = ref('');

const handleSendMessage = () => {
  if (messageText.value.trim()) {
    chatStore.sendMessage(messageText.value);
    messageText.value = '';
  }
};
</script>
