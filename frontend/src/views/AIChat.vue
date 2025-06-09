<template>
  <div class="ai-chat-container">
    <!-- Left Sidebar -->
    <div class="sidebar">
      <div class="search-box">
        <input type="text" placeholder="Search chat history..." v-model="searchQuery">
      </div>
      <div class="chat-list">
        <!-- Chat Session List -->
        <div v-for="chat in chatList" 
             :key="chat.id" 
             class="chat-item"
             :class="{ active: currentChatId === chat.id }"
             @click="switchChat(chat.id)">
          <div class="chat-info">
            <h4>{{ chat.title }}</h4>
            <p>{{ chat.lastMessage }}</p>
          </div>
          <span class="chat-time">{{ chat.lastTime }}</span>
        </div>
      </div>
    </div>

    <!-- Main Chat Area -->
    <div class="chat-main">
      <div class="chat-header">
        <h2>{{ currentChat?.title || 'New Chat' }}</h2>
        <div class="header-actions">
          <button @click="clearChat" class="btn-clear">Clear Chat</button>
        </div>
      </div>

      <div class="messages-container" ref="messagesContainer">
        <div v-for="message in currentMessages" 
             :key="message.id" 
             class="message"
             :class="{ 'user-message': message.isUser }">
          <div class="message-content">
            <div class="message-text">{{ message.content }}</div>
            <span class="message-time">{{ message.time }}</span>
          </div>
        </div>
        <!-- Loading Animation -->
        <div v-if="isLoading" class="message">
          <div class="message-content loading">
            <div class="loading-dots">
              <span></span>
              <span></span>
              <span></span>
            </div>
          </div>
        </div>
      </div>

      <div class="input-area">
        <div class="input-toolbar">
          <button @click="toggleVoiceInput" class="tool-btn">
            <i class="fas fa-microphone"></i>
          </button>
          <button @click="uploadFile" class="tool-btn">
            <i class="fas fa-paperclip"></i>
          </button>
        </div>
        <div class="input-box">
          <textarea 
            v-model="userInput" 
            @keydown.enter.prevent="sendMessage"
            placeholder="Type a message..."
            rows="3"
            :disabled="isLoading"
          ></textarea>
          <button 
            @click="sendMessage" 
            class="send-btn"
            :disabled="isLoading"
          >Send</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AIChat',
  data() {
    return {
      searchQuery: '',
      chatList: [],
      currentChatId: null,
      userInput: '',
      messages: [],
      isVoiceInputActive: false,
      isLoading: false
    }
  },
  computed: {
    currentChat() {
      return this.chatList.find(chat => chat.id === this.currentChatId)
    },
    currentMessages() {
      return this.messages.filter(msg => msg.chatId === this.currentChatId)
    }
  },
  methods: {
    switchChat(chatId) {
      this.currentChatId = chatId
    },
    async sendMessage() {
      if (!this.userInput.trim() || this.isLoading) return
      
      const message = {
        id: Date.now(),
        chatId: this.currentChatId,
        content: this.userInput,
        isUser: true,
        time: new Date().toLocaleTimeString()
      }
      
      this.messages.push(message)
      this.userInput = ''
      
      // Show loading animation
      this.isLoading = true
      
      // Simulate delayed response
      const delay = Math.floor(Math.random() * (20000 - 10000) + 10000) // Random delay between 10-20 seconds
      await new Promise(resolve => setTimeout(resolve, delay))
      
      // Add error response
      const errorResponse = {
        id: Date.now(),
        chatId: this.currentChatId,
        content: 'Server is busy, please try again later',
        isUser: false,
        time: new Date().toLocaleTimeString()
      }
      
      this.messages.push(errorResponse)
      this.isLoading = false
      
      this.$nextTick(() => {
        this.scrollToBottom()
      })
    },
    toggleVoiceInput() {
      this.isVoiceInputActive = !this.isVoiceInputActive
    },
    uploadFile() {
      // File upload functionality not implemented
    },
    clearChat() {
      this.messages = this.messages.filter(msg => msg.chatId !== this.currentChatId)
    },
    scrollToBottom() {
      const container = this.$refs.messagesContainer
      container.scrollTop = container.scrollHeight
    }
  },
  mounted() {
    // Initialize sample data
    this.chatList = [
      {
        id: 1,
        title: 'New Chat',
        lastMessage: 'Start a new conversation',
        lastTime: 'Just now'
      }
    ]
    this.currentChatId = 1
  }
}
</script>

<style scoped>
.ai-chat-container {
  display: flex;
  height: calc(100vh - 64px);
  background-color: #f5f5f5;
}

.sidebar {
  width: 300px;
  background-color: #fff;
  border-right: 1px solid #e0e0e0;
  display: flex;
  flex-direction: column;
}

.search-box {
  padding: 16px;
  border-bottom: 1px solid #e0e0e0;
}

.search-box input {
  width: 100%;
  padding: 8px;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
}

.chat-list {
  flex: 1;
  overflow-y: auto;
}

.chat-item {
  padding: 16px;
  border-bottom: 1px solid #e0e0e0;
  cursor: pointer;
}

.chat-item:hover {
  background-color: #f5f5f5;
}

.chat-item.active {
  background-color: #e3f2fd;
}

.chat-main {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.chat-header {
  padding: 16px;
  background-color: #fff;
  border-bottom: 1px solid #e0e0e0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.messages-container {
  flex: 1;
  padding: 16px;
  overflow-y: auto;
}

.message {
  margin-bottom: 16px;
  display: flex;
  flex-direction: column;
}

.message.user-message {
  align-items: flex-end;
}

.message-content {
  max-width: 70%;
  padding: 12px;
  border-radius: 8px;
  background-color: #fff;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

.user-message .message-content {
  background-color: #e3f2fd;
}

.message-time {
  font-size: 12px;
  color: #999;
  margin-top: 4px;
}

.input-area {
  padding: 16px;
  background-color: #fff;
  border-top: 1px solid #e0e0e0;
}

.input-toolbar {
  display: flex;
  gap: 8px;
  margin-bottom: 8px;
}

.tool-btn {
  padding: 8px;
  border: none;
  background: none;
  cursor: pointer;
  color: #666;
}

.tool-btn:hover {
  color: #1976d2;
}

.input-box {
  display: flex;
  gap: 8px;
}

textarea {
  flex: 1;
  padding: 12px;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  resize: none;
}

textarea:disabled {
  background-color: #f5f5f5;
  cursor: not-allowed;
}

.send-btn {
  padding: 0 24px;
  background-color: #1976d2;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.send-btn:hover {
  background-color: #1565c0;
}

.send-btn:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.btn-clear {
  padding: 8px 16px;
  background-color: #f5f5f5;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  cursor: pointer;
}

.btn-clear:hover {
  background-color: #e0e0e0;
}

/* Loading Animation Styles */
.loading {
  background-color: #f5f5f5 !important;
  min-width: 60px;
}

.loading-dots {
  display: flex;
  gap: 4px;
  padding: 8px;
}

.loading-dots span {
  width: 8px;
  height: 8px;
  background-color: #1976d2;
  border-radius: 50%;
  animation: bounce 1.4s infinite ease-in-out both;
}

.loading-dots span:nth-child(1) {
  animation-delay: -0.32s;
}

.loading-dots span:nth-child(2) {
  animation-delay: -0.16s;
}

@keyframes bounce {
  0%, 80%, 100% { 
    transform: scale(0);
  } 
  40% { 
    transform: scale(1.0);
  }
}
</style> 