<template>
  <div ref="messageContainer" class="flex-1 overflow-y-auto p-4 space-y-4">
    <div
      v-for="message in chatStore.messages"
      :key="message.id"
      :class="['flex', message.sender === 'user' ? 'justify-end' : 'justify-start']"
    >
      <div
        :class="[
          'max-w-[75%] rounded-xl p-3 shadow-md',
          message.sender === 'user'
            ? 'bg-indigo-500 text-white rounded-br-none'
            : 'bg-slate-200 text-slate-800 rounded-bl-none'
        ]"
      >
        <p>{{ message.text }}</p>
      </div>
    </div>
    <div v-if="chatStore.isTyping" class="flex justify-start">
      <div class="max-w-[75%] rounded-xl p-3 shadow-md bg-slate-200 text-slate-800 rounded-bl-none">
        <p class="animate-pulse">助理正在輸入中...</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, nextTick } from 'vue';
import { useChatStore } from '../store/chat';

const chatStore = useChatStore();
const messageContainer = ref(null);

watch(
  () => chatStore.messages,
  () => {
    nextTick(() => {
      if (messageContainer.value) {
        messageContainer.value.scrollTop = messageContainer.value.scrollHeight;
      }
    });
  },
  { deep: true }
);
</script>
