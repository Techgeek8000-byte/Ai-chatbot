"""
Buddy AI Chatbot v3.2 - RELIABLE EDITION
Uses native Streamlit components for maximum compatibility
Works perfectly on Streamlit Cloud!
"""

import streamlit as st
from groq import Groq
import os
from datetime import datetime
import json
import time
from dotenv import load_dotenv

# Configuration
load_dotenv()

st.set_page_config(
    page_title="Buddy AI Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - Minimal and Safe
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
        padding: 2rem;
        margin: -1rem -1rem 1rem -1rem;
        border-radius: 0;
    }
    
    .main-header h1 {
        color: white;
        font-size: 2rem;
        font-weight: 700;
        margin: 0;
    }
    
    .main-header p {
        color: rgba(255,255,255,0.9);
        margin: 0.5rem 0 0 0;
        font-size: 0.95rem;
    }
    
    .welcome-text {
        text-align: center;
        padding: 3rem 1rem;
    }
    
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        max-width: 800px;
        margin: 2rem auto;
    }
    
    .message-user {
        background: linear-gradient(135deg, #3b82f6, #2563eb);
        color: white;
        padding: 1rem 1.25rem;
        border-radius: 18px 18px 4px 18px;
        max-width: 80%;
        margin-left: auto;
        margin-bottom: 1rem;
    }
    
    .message-bot {
        background: white;
        color: #1f2937;
        padding: 1rem 1.25rem;
        border-radius: 18px 18px 18px 4px;
        border: 1px solid #e5e7eb;
        max-width: 80%;
        margin-bottom: 1rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    
    .about-box {
        background: #f9fafb;
        padding: 1.25rem;
        border-radius: 12px;
        border: 1px solid #e5e7eb;
        margin-top: 1rem;
    }
    
    .stat-card {
        background: #f3f4f6;
        padding: 0.75rem;
        border-radius: 8px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'message_count' not in st.session_state:
    st.session_state.message_count = 0
if 'total_tokens' not in st.session_state:
    st.session_state.total_tokens = 0
if 'start_time' not in st.session_state:
    st.session_state.start_time = time.time()

# ═══════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════

with st.sidebar:
    # Logo using columns for clean look
    col_logo1, col_logo2, col_logo3 = st.columns([1, 2, 1])
    with col_logo2:
        st.markdown("""
        <div style='text-align: center; padding: 1.5rem 0;'>
            <div style='width: 60px; height: 60px; background: linear-gradient(135deg, #3b82f6, #2563eb);
                 border-radius: 16px; display: inline-flex; align-items: center; 
                 justify-content: center; margin-bottom: 12px;'>
                <span style='font-size: 32px; color: white; font-weight: bold;'>B</span>
            </div>
            <h2 style='margin: 0; font-size: 1.25rem; color: #111827;'>Buddy AI</h2>
            <p style='margin: 4px 0 0 0; font-size: 0.85rem; color: #6b7280;'>Professional v3.2</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    # Configuration
    st.subheader("⚙️ Configuration")
    
    api_key = os.getenv("GROQ_API_KEY", "")
    if not api_key:
        api_key = st.text_input("🔑 API Key", type="password", help="Get free key at console.groq.com")
        if api_key:
            os.environ["GROQ_API_KEY"] = api_key
    
    bot_name = st.text_input("🤖 Assistant Name", value=os.getenv("CHATBOT_NAME", "Buddy"))
    
    st.divider()
    
    # Personality
    st.subheader("🎭 Personality")
    
    personalities = {
        "Friendly & Helpful": "You are a friendly and helpful AI assistant named {name}. You answer questions clearly.",
        "Professional Expert": "You are a professional expert named {name}. You provide detailed responses.",
        "Creative & Engaging": "You are creative and engaging named {name}. You bring energy to conversations.",
        "Technical Specialist": "You are a technical specialist named {name}. You excel at programming."
    }
    
    selected_personality = st.selectbox(
        "Response Style",
        options=list(personalities.keys())
    )
    
    # Model
    models = {
        "Llama 3.3 70B (Best)": "llama-3.3-70b-versatile",
        "Llama 3.1 8B (Fast)": "llama-3.1-8b-instant",
        "Mixtral 8x7B": "mixtral-8x7b-32768"
    }
    
    selected_model_name = st.selectbox("🧠 AI Model", options=list(models.keys()))
    model_id = models[selected_model_name]
    
    st.divider()
    
    # Stats
    st.subheader("📊 Statistics")
    
    stat_col1, stat_col2 = st.columns(2)
    with stat_col1:
        st.metric("Messages", st.session_state.message_count)
    with stat_col2:
        st.metric("Tokens", st.session_state.total_tokens)
    
    session_time = int(time.time() - st.session_state.start_time)
    minutes = session_time // 60
    seconds = session_time % 60
    st.metric("⏱️ Duration", f"{minutes}m {seconds}s")
    
    st.divider()
    
    # Export
    st.subheader("💾 Export")
    
    exp_col1, exp_col2 = st.columns(2)
    with exp_col1:
        if st.button("📄 TXT", use_container_width=True):
            export_chat("txt")
    with exp_col2:
        if st.button("📋 JSON", use_container_width=True):
            export_chat("json")
    
    st.divider()
    
    # Actions
    st.subheader("🛠️ Actions")
    
    if st.button("🗑️ Clear History", use_container_width=True):
        st.session_state.messages = []
        st.session_state.message_count = 0
        st.session_state.total_tokens = 0
        st.session_state.start_time = time.time()
        st.success("✅ Chat cleared!")
        time.sleep(0.5)
        st.rerun()
    
    if st.button("🔄 Reset All", use_container_width=True):
        st.session_state.clear()
        st.success("✅ Session reset!")
        time.sleep(0.5)
        st.rerun()
    
    st.divider()
    
    # About Section - Using native Streamlit components
    st.subheader("ℹ️ About")
    
    with st.expander("About this app", expanded=False):
        st.markdown("""
        **Buddy AI v3.2** is a professional AI assistant.
        
        **Powered by:** Groq's Llama 3
        
        **Features:**
        - Natural conversation
        - Multiple personalities  
        - Conversation export
        - Privacy-focused design
        
        **Tech Stack:** Python • Streamlit • Groq API
        
        ---
        *Built by **TechGeek8000***
        
        *Version 3.2 Reliable Edition*
        """)

# ═══════════════════════════════════════════
# HELPER FUNCTIONS
# ═══════════════════════════════════════════

def get_system_prompt():
    base_prompt = personalities.get(selected_personality, personalities["Friendly & Helpful"])
    return base_prompt.format(name=bot_name)

def initialize_groq_client():
    key = os.getenv("GROQ_API_KEY", api_key)
    if not key:
        st.error("❌ Please enter your Groq API key in the sidebar.")
        st.stop()
    return Groq(api_key=key)

def count_tokens(text):
    return len(text.split()) * 1.3

def export_chat(format_type="txt"):
    if not st.session_state.messages:
        st.warning("No messages to export.")
        return
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    if format_type == "txt":
        filename = f"chat_{timestamp}.txt"
        content = f"Buddy AI Chat Export\n{'='*40}\n"
        content += f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        content += f"Model: {model_id}\n\n"
        
        for msg in st.session_state.messages:
            role = "YOU" if msg["role"] == "user" else bot_name.upper()
            content += f"\n[{role}]:\n{msg['content']}\n"
        
        st.download_button("Download TXT", data=content, file_name=filename, mime="text/plain")
    
    elif format_type == "json":
        filename = f"chat_{timestamp}.json"
        content = json.dumps({
            "date": datetime.now().isoformat(),
            "model": model_id,
            "messages": st.session_state.messages
        }, indent=2)
        
        st.download_button("Download JSON", data=content, file_name=filename, mime="application/json")

# ═══════════════════════════════════════════
# MAIN INTERFACE
# ═══════════════════════════════════════════

# Header
st.markdown(f"""
<div class='main-header'>
    <h1>{bot_name}</h1>
    <p>AI-Powered Assistant | {selected_model_name.split('(')[0].strip()} | {selected_personality.split(' ')[0]}</p>
</div>
""", unsafe_allow_html=True)

# Main Content
if not st.session_state.messages:
    # Welcome Screen - Using NATIVE Streamlit components only!
    st.markdown("<div class='welcome-text'>", unsafe_allow_html=True)
    
    st.title(f"Welcome to {bot_name}")
    st.write("Your intelligent AI assistant ready to help you.")
    st.write("")
    
    # Feature cards using native Streamlit
    feature_col1, feature_col2, feature_col3 = st.columns(3)
    
    with feature_col1:
        st.info("**💬 Natural Chat**\n\nEngage in fluid conversations on any topic.")
    
    with feature_col2:
        st.success("**⚡ Fast Responses**\n\nGet answers in under one second.")
    
    with feature_col3:
        st.warning("**🔒 Privacy First**\n\nYour conversations stay secure and private.")
    
    feature_col4, feature_col5, feature_col6 = st.columns(3)
    
    with feature_col4:
        st.info("**🧠 Smart & Knowledgeable**\n\nPowered by advanced language models.")
    
    with feature_col5:
        st.success("**🎭 Customizable**\n\nChoose from multiple response styles.")
    
    with feature_col6:
        st.warning("**💾 Export Data**\n\nDownload your conversations anytime.")
    
    st.write("")
    st.caption("👇 Type your message below to start chatting!")
    
    st.markdown("</div>", unsafe_allow_html=True)

else:
    # Display chat messages
    for message in st.session_state.messages:
        role = message["role"]
        content = message["content"]
        
        if role == "user":
            st.markdown(f"<div class='message-user'>{content}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='message-bot'><strong>{bot_name}:</strong><br><br>{content}</div>", unsafe_allow_html=True)

# Input Area
st.divider()

with st.form("chat_form", clear_on_submit=True):
    col_input, col_send = st.columns([6, 1])
    
    with col_input:
        user_input = st.text_area(
            "",
            height=100,
            placeholder=f"Type your message to {bot_name}...",
            label_visibility="collapsed"
        )
    
    with col_send:
        st.markdown("<br><br>", unsafe_allow_html=True)
        submitted = st.form_submit_button("Send 💬", type="primary", use_container_width=True)

# Handle submission
if submitted and user_input.strip():
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.session_state.message_count += 1
    st.rerun()

# Generate AI Response
if st.session_state.messages:
    last_message = st.session_state.messages[-1]
    
    if last_message["role"] == "user":
        has_response = (
            len(st.session_state.messages) >= 2 and 
            st.session_state.messages[-2]["role"] == "assistant"
        )
        
        if not has_response:
            with st.spinner("🤔 Thinking..."):
                try:
                    client = initialize_groq_client()
                    
                    api_messages = [
                        {"role": "system", "content": get_system_prompt()}
                    ]
                    
                    for msg in st.session_state.messages[-10:]:
                        api_messages.append({
                            "role": msg["role"],
                            "content": msg["content"]
                        })
                    
                    start_time = time.time()
                    
                    response = client.chat.completions.create(
                        model=model_id,
                        messages=api_messages,
                        temperature=0.7,
                        max_tokens=2048,
                        top_p=0.9,
                    )
                    
                    end_time = time.time()
                    ai_response = response.choices[0].message.content
                    
                    tokens_used = response.usage.total_tokens if hasattr(response, 'usage') else count_tokens(ai_response)
                    st.session_state.total_tokens += tokens_used
                    
                    st.session_state.messages.append({"role": "assistant", "content": ai_response})
                    st.session_state.message_count += 1
                    
                    st.rerun()
                
                except Exception as e:
                    error_msg = f"❌ Error: {str(e)}"
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})
                    st.error(error_msg)

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; padding: 1rem; color: #9ca3af; font-size: 0.85rem;'>
    Privacy-Focused • Local Storage • Powered by Groq AI • Built by TechGeek8000
</div>
""", unsafe_allow_html=True)
