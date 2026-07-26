"""
🌐 Buddy AI Chatbot - Web Version (Streamlit)
A beautiful browser-based AI chatbot using Groq's free API

Features:
- 💬 Modern chat interface with message bubbles
- ⚡ Real-time responses with typing indicator
- 📊 Token counter & response time
- 💾 Auto-save conversations
- 🎨 Customizable colors and personality
- 📱 Works on mobile too!

Author: Your Name
Version: 1.0.0 (Web Edition)
"""

import streamlit as st
from groq import Groq
import os
from datetime import datetime
import json
import time
from dotenv import load_dotenv

# ──────────────────────────────────────────────
# CONFIGURATION
# ──────────────────────────────────────────────

# Load environment variables from .env file
load_dotenv()

# Page configuration - MUST be first Streamlit command
st.set_page_config(
    page_title="Buddy AI Chatbot",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="expanded"
)

# ──────────────────────────────────────────────
# CUSTOM CSS FOR BEAUTIFUL UI
# ──────────────────────────────────────────────

st.markdown("""
<style>
    /* Main background */
    .main {
        background-color: #f5f5f5;
    }
    
    /* User messages */
    .user-message {
        background-color: #007bff;
        color: white;
        padding: 12px 18px;
        border-radius: 20px;
        margin-bottom: 8px;
        max-width: 80%;
        margin-left: auto;
        word-wrap: break-word;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Bot messages */
    .bot-message {
        background-color: white;
        color: #333;
        padding: 12px 18px;
        border-radius: 20px;
        margin-bottom: 8px;
        max-width: 80%;
        word-wrap: break-word;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Header styling */
    .header-text {
        text-align: center;
        font-size: 2.5rem;
        font-weight: bold;
        background: linear-gradient(90deg, #007bff, #28a745);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────
# SIDEBAR - SETTINGS & INFO
# ──────────────────────────────────────────────

with st.sidebar:
    st.title("⚙️ Settings")
    
    # API Key input (if not in .env)
    api_key = os.getenv("GROQ_API_KEY", "")
    if not api_key:
        api_key = st.text_input("🔑 Enter your Groq API Key:", type="password")
        if api_key:
            os.environ["GROQ_API_KEY"] = api_key
    
    # Chatbot name
    bot_name = os.getenv("CHATBOT_NAME", "Buddy")
    new_name = st.text_input("🤖 Bot Name:", value=bot_name)
    
    # Personality selection
    personalities = {
        "Friendly & Helpful": "You are a friendly and helpful AI assistant named {name}. You answer questions clearly and concisely.",
        "Professional": "You are a professional AI assistant named {name}. You provide detailed, well-structured responses.",
        "Casual & Fun": "You are a fun and casual AI assistant named {name}. You use emojis and keep things light!",
        "Coding Expert": "You are an expert programming assistant named {name}. You specialize in code examples and technical explanations."
    }
    
    selected_personality = st.selectbox(
        "🎭 Personality:",
        options=list(personalities.keys()),
        index=0
    )
    
    # Model selection
    models = [
        "llama-3.3-70b-versatile",
        "llama-3.1-8b-instant",
        "mixtral-8x7b-32768"
    ]
    selected_model = st.selectbox("🧠 Model:", models, index=0)
    
    st.divider()
    
    # Session stats
    st.subheader("📊 Session Stats")
    
    if 'message_count' not in st.session_state:
        st.session_state.message_count = 0
    if 'total_tokens' not in st.session_state:
        st.session_state.total_tokens = 0
    if 'start_time' not in st.session_state:
        st.session_state.start_time = time.time()
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Messages", st.session_state.message_count)
    with col2:
        st.metric("Tokens", st.session_state.total_tokens)
    
    session_time = int(time.time() - st.session_state.start_time)
    minutes = session_time // 60
    seconds = session_time % 60
    st.metric("Session Time", f"{minutes}m {seconds}s")
    
    st.divider()
    
    # Action buttons
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.session_state.message_count = 0
        st.session_state.total_tokens = 0
        st.session_state.start_time = time.time()
        st.rerun()
    
    if st.button("💾 Save Conversation", use_container_width=True):
        save_conversation()
        st.success("✅ Conversation saved!")
    
    st.divider()
    
    # Instructions
    st.markdown("""
    ### 📖 How to Use
    1. Type your message below
    2. Press Enter or click Send
    3. Wait for AI response!
    
    ---
    *Made with ❤️ using Streamlit + Groq*
    """)

# ──────────────────────────────────────────────
# HELPER FUNCTIONS
# ──────────────────────────────────────────────

def get_system_prompt():
    """Generate system prompt based on selected personality"""
    base_prompt = personalities.get(selected_personality, personalities["Friendly & Helpful"])
    return base_prompt.format(name=new_name)


def initialize_groq_client():
    """Initialize Groq client with API key"""
    key = os.getenv("GROQ_API_KEY", api_key)
    if not key:
        st.error("❌ Please enter your Groq API key in the sidebar!")
        st.stop()
    return Groq(api_key=key)


def save_conversation():
    """Save conversation to JSON file"""
    if 'messages' not in st.session_state or len(st.session_state.messages) == 0:
        return
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"chats/web_chat_{timestamp}.json"
    
    # Ensure chats directory exists
    os.makedirs("chats", exist_ok=True)
    
    chat_data = {
        "timestamp": timestamp,
        "model": selected_model,
        "personality": selected_personality,
        "messages": [
            {"role": msg["role"], "content": msg["content"]}
            for msg in st.session_state.messages
        ]
    }
    
    try:
        with open(filename, "w") as f:
            json.dump(chat_data, f, indent=2)
        return filename
    except Exception as e:
        st.error(f"Error saving: {e}")
        return None


def count_tokens(text):
    """Simple token estimation (rough approximation)"""
    return len(text.split()) * 1.3


# ──────────────────────────────────────────────
# MAIN CHAT INTERFACE
# ──────────────────────────────────────────────

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display header
st.markdown(f'<p class="header-text">💬 {new_name}</p>', unsafe_allow_html=True)
st.markdown("---")

# Display chat messages
chat_container = st.container()

with chat_container:
    for message in st.session_state.messages:
        role = message["role"]
        content = message["content"]
        
        if role == "user":
            st.markdown(f'<div class="user-message">👤 {content}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="bot-message">🤖 {content}</div>', unsafe_allow_html=True)

# Chat input at the bottom
st.markdown("---")

# Use form to handle submission
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_area(
        "Type your message here...",
        height=100,
        placeholder="Ask me anything... 🚀",
        label_visibility="collapsed"
    )
    
    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        submitted = st.form_submit_button("Send 💬", use_container_width=True, type="primary")
    with col2:
        clear_btn = st.form_submit_button("Clear 🗑️", use_container_width=True)

# Handle form submissions
if submitted and user_input.strip():
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.session_state.message_count += 1
    
    # Rerun to display user message immediately
    st.rerun()

if clear_btn:
    st.session_state.messages = []
    st.session_state.message_count = 0
    st.session_state.total_tokens = 0
    st.session_state.start_time = time.time()
    st.rerun()

# Generate AI response for last user message (if not already responded)
if st.session_state.messages:
    last_message = st.session_state.messages[-1]
    
    # If last message is from user and we haven't responded yet
    if last_message["role"] == "user":
        # Show loading indicator
        with st.spinner("🤔 Thinking..."):
            try:
                # Initialize client
                client = initialize_groq_client()
                
                # Build message list for API
                api_messages = [
                    {"role": "system", "content": get_system_prompt()}
                ]
                
                # Add recent conversation history (last 10 messages for context)
                for msg in st.session_state.messages[-10:]:
                    api_messages.append({
                        "role": msg["role"],
                        "content": msg["content"]
                    })
                
                # Call Groq API
                start_time = time.time()
                
                response = client.chat.completions.create(
                    model=selected_model,
                    messages=api_messages,
                    temperature=0.7,
                    max_tokens=1024,
                    top_p=0.9,
                )
                
                end_time = time.time()
                response_time = round((end_time - start_time), 2)
                
                # Extract response
                ai_response = response.choices[0].message.content
                
                # Count tokens used
                tokens_used = response.usage.total_tokens if hasattr(response, 'usage') else count_tokens(ai_response)
                st.session_state.total_tokens += tokens_used
                
                # Add assistant message to history
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": ai_response
                })
                st.session_state.message_count += 1
                
                # Auto-save every 5 messages
                if st.session_state.message_count % 5 == 0:
                    save_conversation()
                
                # Rerun to display response
                st.rerun()
            
            except Exception as e:
                error_msg = f"❌ Error: {str(e)}"
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": error_msg
                })
                st.error(error_msg)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; font-size: 0.9em;'>
    🔒 Your API key stays on your device • 💬 Chats saved locally • 🚀 Powered by Groq AI
</div>
""", unsafe_allow_html=True)