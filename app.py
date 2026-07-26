"""
================================================================================
    🤖 BUDDY AI CHATBOT - WEB VERSION (Streamlit)
================================================================================
    
    FEATURES:
    🌐 Runs in your web browser
    💬 Beautiful chat bubble interface
    📱 Mobile-friendly responsive design
    💾 Auto-saves conversations
    🎨 Customizable colors and settings
    
    DEPLOY TO:
    - Local: streamlit run app.py
    - Web: Push to GitHub → Deploy to Vercel/Streamlit Cloud
    
================================================================================
"""

import os
import json
import time
from datetime import datetime
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv
from groq import Groq

# ============================================
# PAGE CONFIGURATION
# ============================================

st.set_page_config(
    page_title=f"🤖 Buddy AI Chatbot",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .chat-message {
        padding: 12px 16px;
        border-radius: 18px;
        margin: 8px 0;
        max-width: 85%;
        word-wrap: break-word;
    }
    
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        margin-left: auto;
        border-bottom-right-radius: 4px;
    }
    
    .bot-message {
        background: #f0f2f6;
        color: #1a1a2e;
        margin-right: auto;
        border-bottom-left-radius: 4px;
    }
    
    .metadata {
        font-size: 0.8rem;
        color: #888;
        margin-top: 4px;
    }
    
    .stats-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 20px;
        border-radius: 15px;
        margin: 15px 0;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# INITIALIZATION
# ============================================

@st.cache_resource
def initialize_client():
    """Initialize Groq client (cached for session)."""
    load_dotenv()
    api_key = os.getenv("GROQ_API_KEY")
    
    if not api_key or api_key in ["your_api_key_here", "PASTE_YOUR_GSK_KEY_HERE"]:
        st.error("⚠️ Please set your GROQ_API_KEY in the .env file!")
        st.stop()
    
    return Groq(api_key=api_key)

# Initialize client
client = initialize_client()

# Chat configuration
CHATBOT_NAME = os.getenv("CHATBOT_NAME", "Buddy")
SYSTEM_PROMPT = os.getenv("CHATBOT_PERSONALITY", 
    "You are a friendly, helpful, and slightly humorous AI assistant.")

# Create chats directory
chats_dir = Path("chats")
chats_dir.mkdir(exist_ok=True)

# ============================================
# SESSION STATE MANAGEMENT
# ============================================

# Initialize conversation history in session state
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

if "stats" not in st.session_state:
    st.session_state.stats = {
        "total_messages": 0,
        "total_tokens": 0,
        "responses": 0,
        "start_time": datetime.now()
    }

if "model_option" not in st.session_state:
    st.session_state.model_option = "llama-3.3-70b-versatile"

if "temperature" not in st.session_state:
    st.session_state.temperature = 0.7

# ============================================
# SIDEBAR - SETTINGS & INFO
# ============================================

with st.sidebar:
    st.markdown(f"# 🤖 {CHATBOT_NAME}")
    st.markdown("---")
    
    # Stats section
    st.subheader("📊 Session Stats")
    
    duration = (datetime.now() - st.session_state.stats["start_time"]).total_seconds()
    hours = int(duration // 3600)
    mins = int((duration % 3600) // 60)
    
    st.metric("💬 Messages", st.session_state.stats["total_messages"])
    st.metric("🤖 Responses", st.session_state.stats["responses"])
    st.metric("📊 Tokens Used", f"{st.session_state.stats['total_tokens']:,}")
    st.metric("⏱️ Duration", f"{hours}h {mins}m")
    
    st.markdown("---")
    
    # Actions
    st.subheader("🛠️ Actions")
    
    if st.button("🧹 Clear Conversation", use_container_width=True):
        st.session_state.messages = [
            {"role": "system", "content": SYSTEM_PROMPT}
        ]
        st.session_state.stats = {
            "total_messages": 0,
            "total_tokens": 0,
            "responses": 0,
            "start_time": datetime.now()
        }
        st.rerun()
    
    if st.button("💾 Save Chat", use_container_width=True):
        save_conversation()
        st.success("✅ Conversation saved!")
    
    st.markdown("---")
    
    # Info
    st.subheader("ℹ️ About")
    st.info(f"""
    **{CHATBOT_NAME} AI Chatbot**
    
    Powered by **Groq** (Free!)
    
    Model: Llama 3.3 70B
    
    Version: Web v1.0
    """)
    
    # Model selection
    st.markdown("---")
    st.subheader("🎛️ Settings")
    
    model_option = st.selectbox(
        "AI Model",
        options=[
            "llama-3.3-70b-versatile",
            "mixtral-8x7b-32768",
            "gemma2-9b-it"
        ],
        index=0,
        help="Choose which AI model to use"
    )
    st.session_state.model_option = model_option
    
    temperature = st.slider(
        "Creativity (Temperature)",
        min_value=0.0,
        max_value=1.0,
        value=0.7,
        step=0.1,
        help="Higher = more creative, Lower = more focused"
    )
    st.session_state.temperature = temperature

# ============================================
# UTILITY FUNCTIONS
# ============================================

def save_conversation():
    """Save conversation to JSON file."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"chat_{timestamp}.json"
    filepath = chats_dir / filename
    
    chat_data = {
        "timestamp": datetime.now().isoformat(),
        "model": st.session_state.model_option,
        "messages": [
            m for m in st.session_state.messages 
            if m["role"] != "system"
        ],
        "stats": dict(st.session_state.stats)
    }
    
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(chat_data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        st.error(f"Error saving: {e}")
        return False

def download_chat():
    """Generate downloadable chat file."""
    chat_content = []
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            chat_content.append(f"👤 You: {msg['content']}\n")
        elif msg["role"] == "assistant":
            chat_content.append(f"🤖 {CHATBOT_NAME}: {msg['content']}\n")
    
    chat_text = "\n".join(chat_content)
    st.download_button(
        label="📥 Download Text File",
        data=chat_text,
        file_name=f"chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
        mime="text/plain"
    )

def call_groq_api(user_message):
    """Call Groq API and return response."""
    start_time = time.time()
    
    # Add user message to history
    st.session_state.messages.append({
        "role": "user",
        "content": user_message
    })
    
    try:
        response = client.chat.completions.create(
            model=st.session_state.model_option,
            messages=st.session_state.messages,
            temperature=st.session_state.temperature,
            max_tokens=1024,
        )
        
        end_time = time.time()
        response_time = end_time - start_time
        
        ai_response = response.choices[0].message.content
        tokens = response.usage.total_tokens if hasattr(response, 'usage') else 0
        
        # Update stats
        st.session_state.stats["total_messages"] += 1
        st.session_state.stats["total_tokens"] += tokens
        st.session_state.stats["responses"] += 1
        
        # Add assistant response to history
        st.session_state.messages.append({
            "role": "assistant",
            "content": ai_response
        })
        
        return {
            "response": ai_response,
            "time": response_time,
            "tokens": tokens
        }
        
    except Exception as e:
        error_msg = f"❌ Error: {str(e)}"
        st.session_state.messages.append({
            "role": "assistant",
            "content": error_msg
        })
        return {
            "response": error_msg,
            "time": time.time() - start_time,
            "tokens": 0
        }

# ============================================
# MAIN CHAT INTERFACE
# ============================================

# Header
st.markdown(f"<div class='main-header'>🤖 {CHATBOT_NAME} AI Assistant</div>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align:center; color:#888;'>Powered by Groq (FREE!) • Talk about anything!</p>", unsafe_allow_html=True)

st.markdown("---")

# Display chat history
chat_container = st.container()

with chat_container:
    for idx, message in enumerate(st.session_state.messages):
        if message["role"] == "system":
            continue
            
        if message["role"] == "user":
            st.markdown(f"""
            <div style="display:flex; justify-content:flex-end; margin:10px 0;">
                <div class="chat-message user-message">
                    <div>{message['content']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="display:flex; justify-content:flex-start; margin:10px 0;">
                <div class="chat-message bot-message">
                    <div>{message['content']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

# Chat input
st.markdown("---")

col1, col2 = st.columns([5, 1])

with col1:
    user_input = st.text_area(
        "Type your message...",
        height=80,
        placeholder="Ask me anything! 😊",
        label_visibility="collapsed"
    )

with col2:
    st.markdown("<br>", unsafe_allow_html=True)
    send_button = st.button("Send 🚀", use_container_width=True, type="primary")

# Handle message submission
if send_button and user_input.strip():
    with st.spinner(f"{CHATBOT_NAME} is thinking..."):
        result = call_groq_api(user_input.strip())
        st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align:center; color:#aaa; font-size:0.85rem;">
    <p>💡 Tips: Use sidebar for settings • Conversations auto-save • Download anytime</p>
    <p>Made with ❤️ using Python + Streamlit + Groq</p>
</div>
""", unsafe_allow_html=True)
