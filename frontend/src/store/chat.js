import { defineStore } from 'pinia';
import { v4 as uuidv4 } from 'uuid';

export const useChatStore = defineStore('chat', {
  state: () => ({
    messages: [
      {
        id: uuidv4(),
        sender: 'bot',
        text: '您好！我是企業級智慧助理，很高興為您服務。'
      }
    ],
    isTyping: false,
    ws: null,
    isConnected: false,
    reconnectInterval: 1000,
  }),
  actions: {
    addMessage(message) {
      this.messages.push({
        ...message,
        id: uuidv4(),
      });
    },
    async connectWebSocket() {
      if (this.ws && this.ws.readyState === WebSocket.OPEN) {
        console.log('WebSocket already connected.');
        return;
      }
      
      const wsUrl = import.meta.env.VITE_WEBSOCKET_URL || 'ws://localhost:8000/chat';
      console.log(`Connecting to WebSocket at: ${wsUrl}`);
      
      this.ws = new WebSocket(wsUrl);

      this.ws.onopen = () => {
        console.log('WebSocket connected!');
        this.isConnected = true;
        this.reconnectInterval = 1000;
      };

      this.ws.onmessage = (event) => {
        const message = JSON.parse(event.data);
        this.addMessage({ sender: message.user_id, text: message.text });
        this.isTyping = false;
      };

      this.ws.onclose = (event) => {
        this.isConnected = false;
        console.log('WebSocket disconnected.', event);
        
        // Attempt to reconnect with exponential backoff
        setTimeout(() => {
          console.log('Attempting to reconnect...');
          this.reconnectInterval = Math.min(this.reconnectInterval * 2, 30000); // Cap at 30 seconds
          this.connectWebSocket();
        }, this.reconnectInterval);
      };

      this.ws.onerror = (error) => {
        console.error('WebSocket error:', error);
      };
    },
    sendMessage(text) {
      if (this.ws && this.ws.readyState === WebSocket.OPEN) {
        this.addMessage({ sender: 'user', text });
        this.ws.send(text);
        this.isTyping = true;
      } else {
        console.error('WebSocket is not connected.');
        this.addMessage({ sender: 'bot', text: '服務異常，無法傳送訊息。' });
      }
    },
  },
});
