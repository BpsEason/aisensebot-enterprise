<template>
  <div class="flex flex-col flex-1 overflow-hidden">
    <MessageList />
    <MessageInput />
  </div>
</template>

<script setup>
import MessageList from './MessageList.vue';
import MessageInput from './MessageInput.vue';
</script>
