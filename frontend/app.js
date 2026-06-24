// ===== DOM Elements =====
const form = document.getElementById("chat-form");
const queryInput = document.getElementById("query-input");
const tenantSelect = document.getElementById("tenant-select");
const contextToggle = document.getElementById("context-toggle");
const threadIdInput = document.getElementById("thread-id");
const chatWindow = document.getElementById("chat-window");
const clearButton = document.getElementById("clear-button");

// Upload form elements
const uploadForm = document.getElementById("upload-form");
const fileInput = document.getElementById("file-input");
const docNameInput = document.getElementById("doc-name-input");
const uploadStatus = document.getElementById("upload-status");

// Chat history elements
const chatHistory = document.getElementById("chat-history");
const newChatButton = document.getElementById("new-chat-button");

// ===== Chat History Management =====
let conversations = [];
let currentConversationId = null;

function saveConversation() {
  if (!currentConversationId) return;
  
  const existingIndex = conversations.findIndex(c => c.id === currentConversationId);
  const messages = Array.from(chatWindow.querySelectorAll('.message'));
  const preview = messages.length > 0 ? messages[messages.length - 1].textContent.substring(0, 40) : "New conversation";
  
  if (existingIndex >= 0) {
    conversations[existingIndex].preview = preview;
    conversations[existingIndex].timestamp = Date.now();
  } else {
    conversations.push({
      id: currentConversationId,
      preview: preview,
      timestamp: Date.now(),
      messages: []
    });
  }
  
  updateChatHistory();
}

function updateChatHistory() {
  if (conversations.length === 0) {
    chatHistory.innerHTML = '<div class="history-empty"><p>No conversations yet</p></div>';
    return;
  }
  
  chatHistory.innerHTML = '';
  conversations
    .sort((a, b) => b.timestamp - a.timestamp)
    .forEach(conv => {
      const item = document.createElement('div');
      item.className = `history-item ${conv.id === currentConversationId ? 'active' : ''}`;
      item.textContent = conv.preview;
      item.title = conv.preview;
      item.addEventListener('click', () => loadConversation(conv.id));
      chatHistory.appendChild(item);
    });
}

function loadConversation(convId) {
  currentConversationId = convId;
  // Clear chat window and mark active
  clearChatWindow();
  updateChatHistory();
}

function startNewChat() {
  saveConversation();
  currentConversationId = generateId();
  clearChatWindow();
  queryInput.focus();
}

function generateId() {
  return 'conv_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
}

function clearChatWindow() {
  chatWindow.innerHTML = `<div class="chat-empty-state"><div class="empty-state-content"><h2>Welcome to Multi-Tenant RAG</h2><p>Select a tenant, upload documents, and start asking questions</p></div></div>`;
}

// ===== Message Creation =====
function createMessageBubble(role, text) {
  const messageDiv = document.createElement("div");
  messageDiv.className = `message ${role}`;
  
  const contentDiv = document.createElement("div");
  contentDiv.className = "message-content";
  
  const strong = document.createElement("strong");
  strong.textContent = role === "user" ? "You" : "Assistant";
  
  const p = document.createElement("p");
  p.textContent = text;
  
  contentDiv.appendChild(strong);
  contentDiv.appendChild(p);
  messageDiv.appendChild(contentDiv);
  
  return messageDiv;
}

function formatMetadata(metadata = {}) {
  const parts = [];
  if (metadata.title) parts.push(metadata.title);
  if (metadata.page !== undefined) parts.push(`Page ${metadata.page + 1}`);
  if (metadata.page_label) parts.push(metadata.page_label);
  if (metadata.source) parts.push(metadata.source);
  return parts.filter(Boolean).join(" · ");
}

function createContextCard(items) {
  const container = document.createElement("div");
  container.className = "context-card";
  
  const heading = document.createElement("strong");
  heading.textContent = "Retrieved Context";
  container.appendChild(heading);

  items.forEach((item) => {
    const itemCard = document.createElement("div");
    itemCard.className = "context-item";

    const snippet = document.createElement("p");
    snippet.textContent = item.content;
    itemCard.appendChild(snippet);

    const metaRow = document.createElement("div");
    metaRow.className = "context-meta";

    const title = document.createElement("span");
    title.textContent = item.document_name || "Source";
    metaRow.appendChild(title);

    const metadataText = formatMetadata(item.metadata || {});
    if (metadataText) {
      const details = document.createElement("span");
      details.textContent = metadataText;
      metaRow.appendChild(details);
    }

    if (item.similarity !== undefined) {
      const similarity = document.createElement("span");
      similarity.textContent = `${Math.round(item.similarity * 100)}% match`;
      metaRow.appendChild(similarity);
    }

    itemCard.appendChild(metaRow);
    container.appendChild(itemCard);
  });

  return container;
}

// ===== UI Helpers =====
function setLoading(isLoading) {
  const submitButton = form.querySelector("button[type=submit]");
  submitButton.disabled = isLoading;
  submitButton.textContent = isLoading ? "⏳" : "→";
}

function showError(message) {
  if (chatWindow.querySelector(".chat-empty-state")) {
    chatWindow.innerHTML = "";
  }
  
  const errorEl = document.createElement("div");
  errorEl.className = "message bot";
  
  const contentDiv = document.createElement("div");
  contentDiv.className = "message-content";
  
  const strong = document.createElement("strong");
  strong.textContent = "Error";
  
  const p = document.createElement("p");
  p.textContent = message;
  
  contentDiv.appendChild(strong);
  contentDiv.appendChild(p);
  errorEl.appendChild(contentDiv);
  
  chatWindow.appendChild(errorEl);
  chatWindow.scrollTop = chatWindow.scrollHeight;
}

function updateUploadStatus(message, type) {
  uploadStatus.textContent = message;
  uploadStatus.className = `upload-status ${type}`;
}

function clearUploadStatus() {
  uploadStatus.textContent = "";
  uploadStatus.className = "upload-status";
}

// ===== Textarea Auto-Grow =====
function autoGrowTextarea(textarea) {
  textarea.style.height = "auto";
  const newHeight = Math.min(textarea.scrollHeight, 120);
  textarea.style.height = newHeight + "px";
}

queryInput.addEventListener("input", function() {
  autoGrowTextarea(this);
});

queryInput.addEventListener("keydown", function(e) {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    form.dispatchEvent(new Event("submit"));
  } else if (e.key === "Enter" && e.shiftKey) {
    e.preventDefault();
    const start = this.selectionStart;
    const end = this.selectionEnd;
    this.value = this.value.substring(0, start) + "\n" + this.value.substring(end);
    this.selectionStart = this.selectionEnd = start + 1;
    autoGrowTextarea(this);
  }
});

// ===== Event Listeners =====

// Clear chat
clearButton.addEventListener("click", () => {
  clearChatWindow();
  queryInput.value = "";
  threadIdInput.value = "";
  queryInput.style.height = "auto";
  startNewChat();
});

// New chat button
newChatButton.addEventListener("click", () => {
  startNewChat();
  updateChatHistory();
});

// Document upload
uploadForm.addEventListener("submit", async (event) => {
  event.preventDefault();

  if (!fileInput.files.length) {
    updateUploadStatus("Please select a file", "error");
    return;
  }

  const file = fileInput.files[0];
  const tenantId = tenantSelect.value;
  const docName = docNameInput.value.trim();

  const formData = new FormData();
  formData.append("file", file);
  if (docName) {
    formData.append("document_name", docName);
  }

  updateUploadStatus(`Uploading ${file.name}...`, "loading");
  const uploadButton = uploadForm.querySelector("button[type=submit]");
  uploadButton.disabled = true;

  try {
    const response = await fetch("/v1/ingest/file", {
      method: "POST",
      headers: {
        "X-Tenant-ID": tenantId,
      },
      body: formData,
    });

    if (!response.ok) {
      const errorBody = await response.json();
      throw new Error(errorBody.detail || "Upload failed");
    }

    const data = await response.json();
    updateUploadStatus(
      `✓ "${data.document_name}" (${data.chunks} chunks)`,
      "success"
    );

    // Reset form
    fileInput.value = "";
    docNameInput.value = "";

    // Clear status after 5 seconds
    setTimeout(clearUploadStatus, 5000);
  } catch (error) {
    updateUploadStatus(`✗ ${error.message}`, "error");
  } finally {
    uploadButton.disabled = false;
  }
});

// Chat submission
form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const query = queryInput.value.trim();
  if (!query) return;

  // Initialize conversation on first message
  if (!currentConversationId) {
    currentConversationId = generateId();
  }

  const tenantId = tenantSelect.value;
  const includeContext = contextToggle.checked;
  const threadId = threadIdInput.value.trim() || undefined;

  // Remove empty state if present
  const emptyState = chatWindow.querySelector(".chat-empty-state");
  if (emptyState) {
    emptyState.remove();
  }

  // Add user message
  chatWindow.appendChild(createMessageBubble("user", query));
  chatWindow.scrollTop = chatWindow.scrollHeight;

  // Clear input and reset height
  queryInput.value = "";
  queryInput.style.height = "auto";

  setLoading(true);

  try {
    const response = await fetch("/v1/rag/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-Tenant-ID": tenantId,
      },
      body: JSON.stringify({
        query,
        thread_id: threadId,
        include_context: includeContext,
      }),
    });

    if (!response.ok) {
      const errorBody = await response.json();
      throw new Error(errorBody.detail || "Unable to get a response.");
    }

    const data = await response.json();
    chatWindow.appendChild(createMessageBubble("bot", data.answer || "No answer returned."));

    if (includeContext && Array.isArray(data.context) && data.context.length) {
      chatWindow.appendChild(createContextCard(data.context));
    }

    chatWindow.scrollTop = chatWindow.scrollHeight;
    saveConversation();
  } catch (error) {
    showError(error.message);
  } finally {
    setLoading(false);
  }
});

// Initialize
clearChatWindow();
queryInput.focus();
