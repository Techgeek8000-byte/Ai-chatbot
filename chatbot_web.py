"""
Buddy AI Chatbot v3.1 - Professional Edition
Clean, working version for Streamlit deployment
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
    page_icon="B",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional CSS Styles
PROFESSIONAL_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .main {
        background-color: #f8fafc;
    }
    
    .app-header {
        background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
        padding: 24px 32px;
        margin: -24px -24px 24px -24px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .app-header h1 {
        color: white;
        font-size: 28px;
        font-weight: 700;
        margin: 0;
    }
    
    .app-header p {
        color: rgba(255,255,255,0.9);
        font-size: 14px;
        margin: 6px 0 0 0;
    }
    
    .welcome-container {
        text-align: center;
        padding: 60px 24px;
        animation: fadeIn 0.6s ease-out;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .welcome-title {
        font-size: 36px;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 12px;
    }
    
    .welcome-subtitle {
        font-size: 16px;
        color: #475569;
        max-width: 500px;
        margin: 0 auto 48px;
        line-height: 1.6;
    }
    
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
        gap: 20px;
        max-width: 900px;
        margin: 0 auto;
    }
    
    .feature-card {
        background: white;
        padding: 28px 24px;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        transition: all 0.25s ease;
        text-align: left;
    }
    
    .feature-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        border-color: #3b82f6;
    }
    
    .feature-icon-wrapper {
        width: 44px;
        height: 44px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 16px;
        font-size: 20px;
    }
    
    .icon-blue { background: #dbeafe; color: #2563eb; }
    .icon-green { background: #d1fae5; color: #059669; }
    .icon-purple { background: #ede9fe; color: #7c3aed; }
    .icon-orange { background: #ffedd5; color: #ea580c; }
    .icon-red { background: #fee2e2; color: #dc2626; }
    .icon-teal { background: #ccfbf1; color: #0d9488; }
    
    .feature-title {
        font-size: 15px;
        font-weight: 600;
        color: #0f172a;
        margin-bottom: 6px;
    }
    
    .feature-desc {
        font-size: 13px;
        color: #475569;
        line-height: 1.5;
    }
    
    .chat-container {
        padding: 0 24px;
        max-width: 900px;
        margin: 0 auto;
    }
    
    .message-wrapper {
        margin-bottom: 16px;
        display: flex;
        gap: 12px;
        animation: slideIn 0.3s ease-out;
    }
    
    @keyframes slideIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .message-avatar {
        width: 36px;
        height: 36px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 14px;
        font-weight: 600;
        flex-shrink: 0;
    }
    
    .avatar-user {
        background: linear-gradient(135deg, #3b82f6, #2563eb);
        color: white;
    }
    
    .avatar-bot {
        background: linear-gradient(135deg, #64748b, #475569);
        color: white;
    }
    
    .message-content {
        flex: 1;
        max-width: calc(100% - 48px);
    }
    
    .bubble-user {
        background: linear-gradient(135deg, #3b82f6, #2563eb);
        color: white;
        padding: 14px 18px;
        border-radius: 18px 18px 4px 18px;
        max-width: fit-content;
        font-size: 14px;
        line-height: 1.6;
    }
    
    .bubble-bot {
        background: white;
        border: 1px solid #e2e8f0;
        padding: 14px 18px;
        border-radius: 18px 18px 18px 4px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        font-size: 14px;
        line-height: 1.6;
        color: #0f172a;
    }
    
    .input-container {
        position: sticky;
        bottom: 0;
        background: white;
        border-top: 1px solid #e2e8f0;
        padding: 20px 24px;
        margin: 32px -24px -24px -24px;
        box-shadow: 0 -4px 20px rgba(0,0,0,0.05);
    }
    
    .input-wrapper {
        max-width: 900px;
        margin: 0 auto;
        display: flex;
        gap: 12px;
        align-items: flex-end;
    }
    
    .sidebar-section {
        margin-bottom: 24px;
    }
    
    .sidebar-label {
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        color: #94a3b8;
        margin-bottom: 12px;
    }
    
    .stats-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 10px;
    }
    
    .stat-item {
        background: #f1f5f9;
        padding: 12px;
        border-radius: 8px;
        text-align: center;
    }
    
    .stat-value {
        font-size: 20px;
        font-weight: 700;
        color: #0f172a;
    }
    
    .stat-label {
        font-size: 11px;
        color: #475569;
        margin-top: 2px;
    }
    
    .about-box {
        background: #f1f5f9;
        border-radius: 12px;
        padding: 20px;
        margin-top: 20px;
    }
    
    .about-title {
        font-size: 13px;
        font-weight: 600;
        color: #0f172a;
        margin-bottom: 12px;
    }
    
    .about-text {
        font-size: 12px;
        color: #475569;
        line-height: 1.7;
    }
    
    .about-text p {
        margin: 0 0 10px 0;
    }
    
    .app-footer {
        text-align: center;
        padding: 24px;
        color: #94a3b8;
        font-size: 12px;
        border-top: 1px solid #e2e8f0;
        margin-top: 40px;
    }
</style>
"""

st.markdown(PROFESSIONAL_CSS, unsafe_allow_html=True)

# Initialize session state
if 'message_count' not in st.session_state:
    st.session_state.message_count = 0
if 'total_tokens' not in st.session_state:
    st.session_state.total_tokens = 0
if 'start_time' not in st.session_state:
    st.session_state.start_time = time.time()
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Sidebar
with st.sidebar:
    # Logo
    st.markdown("""
    <div style='padding: 24px 0 20px; text-align: center;'>
        <div style='width: 56px; height: 56px; background: linear-gradient(135deg, #3b82f6, #2563eb);
             border-radius: 14px; display: inline-flex; align-items: center;
             justify-content: center; margin-bottom: 14px;
             box-shadow: 0 4px 12px rgba(37,99,235,0.25);'>
            <span style='font-size: 28px; color: white; font-weight: bold;'>B</span>
        </div>
        <div style='font-size: 18px; font-weight: 700; color: #0f172a; margin-bottom: 4px;'>Buddy AI</div>
        <div style='font-size: 12px; color: #64748b;'>Professional Assistant v3.1</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    # Configuration
    st.markdown('<p class="sidebar-label">Configuration</p>', unsafe_allow_html=True)
    
    api_key = os.getenv("GROQ_API_KEY", "")
    if not api_key:
        api_key = st.text_input("API Key", type="password", placeholder="Enter Groq API key")
        if api_key:
            os.environ["GROQ_API_KEY"] = api_key
    
    bot_name = st.text_input("Assistant Name", value=os.getenv("CHATBOT_NAME", "Buddy"))
    
    st.divider()
    
    # Personality
    st.markdown('<p class="sidebar-label">Personality Mode</p>', unsafe_allow_html=True)
    
    personalities = {
        "Friendly & Helpful": "You are a friendly and helpful AI assistant named {name}. You answer questions clearly and concisely.",
        "Professional Expert": "You are a professional AI expert named {name}. You provide detailed, well-structured responses.",
        "Creative & Engaging": "You are a creative and engaging AI companion named {name}.",
        "Technical Specialist": "You are a technical specialist named {name}. You excel at programming and technical explanations."
    }
    
    selected_personality = st.selectbox("Response Style", options=list(personalities.keys()), label_visibility="collapsed")
    
    # Model
    models = {
        "Llama 3.3 70B (Recommended)": "llama-3.3-70b-versatile",
        "Llama 3.1 8B (Fast)": "llama-3.1-8b-instant",
        "Mixtral 8x7B": "mixtral-8x7b-32768"
    }
    
    selected_model_name = st.selectbox("AI Model", options=list(models.keys()), label_visibility="collapsed")
    model_id = models[selected_model_name]
    
    st.divider()
    
    # Stats
    st.markdown('<p class="sidebar-label">Session Statistics</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Messages", st.session_state.message_count)
    with col2:
        st.metric("Tokens", st.session_state.total_tokens)
    
    session_time = int(time.time() - st.session_state.start_time)
    minutes = session_time // 60
    seconds = session_time % 60
    st.metric("Duration", f"{minutes}m {seconds}s")
    
    st.divider()
    
    # Export
    st.markdown('<p class="sidebar-label">Export Conversation</p>', unsafe_allow_html=True)
    
    ex_col1, ex_col2 = st.columns(2)
    with ex_col1:
        if st.button("TXT", use_container_width=True):
            export_chat("txt")
    with ex_col2:
        if st.button("JSON", use_container_width=True):
            export_chat("json")
    
    st.divider()
    
    # Actions
    st.markdown('<p class="sidebar-label">Actions</p>', unsafe_allow_html=True)
    
    if st.button("Clear History", use_container_width=True):
        st.session_state.messages = []
        st.session_state.message_count = 0
        st.session_state.total_tokens = 0
        st.session_state.start_time = time.time()
        st.success("Chat cleared")
        time.sleep(0.5)
        st.rerun()
    
    if st.button("Reset Session", use_container_width=True):
        st.session_state.clear()
        st.success("Reset complete")
        time.sleep(0.5)
        st.rerun()
    
    st.divider()
    
    # About
    st.markdown("""
    <div class='about-box'>
        <div class='about-title'>About</div>
        <div class='about-text'>
            <p><strong>Buddy AI v3.1</strong> is a professional AI assistant powered by Groq's Llama 3.</p>
            <p><strong>Features:</strong> Natural conversation, multiple response styles, export capability.</p>
            <p><strong>Tech Stack:</strong> Python, Streamlit, Groq API</p>
            <p style='margin-top: 12px; padding-top: 12px; border-top: 1px solid #e2e8f0;'>
                Built by <strong>TechGeek8000</strong><br>
                <span style='color: #94a3b8;'>Version 3.1 Professional</span>
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Helper Functions
def get_system_prompt():
    base_prompt = personalities.get(selected_personality, personalities["Friendly & Helpful"])
    return base_prompt.format(name=bot_name)

def initialize_groq_client():
    key = os.getenv("GROQ_API_KEY", api_key)
    if not key:
        st.error("Please enter your Groq API key in the sidebar.")
        st.stop()
    return Groq(api_key=key)

def count_tokens(text):
    return len(text.split()) * 1.3

def export_chat(format_type="txt"):
    if 'messages' not in st.session_state or len(st.session_state.messages) == 0:
        st.warning("No messages to export.")
        return
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    if format_type == "txt":
        filename = f"chat_export_{timestamp}.txt"
        content = f"Buddy AI Chat Export\n{'='*50}\n"
        content += f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        content += f"Model: {model_id}\n"
        content += f"Personality: {selected_personality}\n"
        content += f"{'='*50}\n\n"
        
        for msg in st.session_state.messages:
            role = "User" if msg["role"] == "user" else bot_name
            content += f"[{role}]:\n{msg['content']}\n\n"
        
        st.download_button(label="Download TXT", data=content, file_name=filename, mime="text/plain")
    
    elif format_type == "json":
        filename = f"chat_export_{timestamp}.json"
        content = json.dumps({
            "export_date": datetime.now().isoformat(),
            "model": model_id,
            "personality": selected_personality,
            "messages": st.session_state.messages
        }, indent=2)
        
        st.download_button(label="Download JSON", data=content, file_name=filename, mime="application/json")

def show_welcome_screen():
    st.markdown(f"""
    <div class='welcome-container'>
        <div class='welcome-title'>{bot_name}</div>
        <div class='welcome-subtitle'>
            Your intelligent AI assistant ready to help with questions, tasks, and conversations.
        </div>
        
        <div class='feature-grid'>
            <div class='feature-card'>
                <div class='feature-icon-wrapper icon-blue'>
                    <span>&#128172;</span>
                </div>
                <div class='feature-title'>Natural Conversation</div>
                <div class='feature-desc'>Engage in fluid, human-like dialogue on any topic.</div>
            </div>
            
            <div class='feature-card'>
                <div class='feature-icon-wrapper icon-green'>
                    <span>&#9889;</span>
                </div>
                <div class='feature-title'>Fast Responses</div>
                <div class='feature-desc'>Get answers in under one second.</div>
            </div>
            
            <div class='feature-card'>
                <div class='feature-icon-wrapper icon-purple'>
                    <span>&#129504;</span>
                </div>
                <div class='feature-title'>Knowledge Base</div>
                <div class='feature-desc'>Powered by advanced language models.</div>
            </div>
            
            <div class='feature-card'>
                <div class='feature-icon-wrapper icon-orange'>
                    <span>&#128274;</span>
                </div>
                <div class='feature-title'>Privacy Focused</div>
                <div class='feature-desc'>Your conversations stay secure.</div>
            </div>
            
            <div class='feature-card'>
                <div class='feature-icon-wrapper icon-teal'>
                    <span>&#9881;</span>
                </div>
                <div class='feature-title'>Customizable</div>
                <div class='feature-desc'>Choose from multiple personalities.</div>
            </div>
            
            <div class='feature-card'>
                <div class='feature-icon-wrapper icon-red'>
                    <span>&#128190;</span>
                </div>
                <div class='feature-title'>Export Data</div>
                <div class='feature-desc'>Download your conversations anytime.</div>
            </div>
        </div>
        
        <div style='margin-top: 48px; color: #64748b; font-size: 14px;'>
            Start a conversation by typing your message below.
        </div>
    </div>
    """, unsafe_allow_html=True)

# Main Interface
st.markdown(f"""
<div class='app-header'>
    <h1>{bot_name}</h1>
    <p>AI-Powered Assistant | {selected_model_name.split('(')[0].strip()} | {selected_personality.split(' ')[0]}</p>
</div>
""", unsafe_allow_html=True)

# Show welcome or chat
if not st.session_state.messages:
    show_welcome_screen()
else:
    st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
    
    for message in st.session_state.messages:
        role = message["role"]
        content = message["content"]
        
        if role == "user":
            st.markdown(f"""
            <div class='message-wrapper'>
                <div class='message-avatar avatar-user'>U</div>
                <div class='message-content'>
                    <div class='bubble-user'>{content}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class='message-wrapper'>
                <div class='message-avatar avatar-bot'>{bot_name[0] if bot_name else 'B'}</div>
                <div class='message-content'>
                    <div class='bubble-bot'>{content}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# Input area
st.markdown("<div class='input-container'>", unsafe_allow_html=True)

with st.form("chat_form", clear_on_submit=True):
    col1, col2 = st.columns([6, 1])
    
    with col1:
        user_input = st.text_area("", height=80, placeholder=f"Type your message to {bot_name}...", label_visibility="collapsed", key="main_input")
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        submitted = st.form_submit_button("Send", type="primary", use_container_width=True)

st.markdown("</div>", unsafe_allow_html=True)

# Handle submission
if submitted and user_input.strip():
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.session_state.message_count += 1
    st.rerun()

# Generate AI response
if st.session_state.messages:
    last_message = st.session_state.messages[-1]
    
    if last_message["role"] == "user":
        has_response = len(st.session_state.messages) >= 2 and st.session_state.messages[-2]["role"] == "assistant"
        
        if not has_response:
            with st.spinner("Thinking..."):
                try:
                    client = initialize_groq_client()
                    
                    api_messages = [{"role": "system", "content": get_system_prompt()}]
                    
                    for msg in st.session_state.messages[-10:]:
                        api_messages.append({"role": msg["role"], "content": msg["content"]})
                    
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
                    error_msg = f"Error: {str(e)}"
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})
                    st.error(error_msg)

# Footer
st.markdown("""
<div class='app-footer'>
    Privacy-focused | Local storage | Powered by Groq AI | Built by TechGeek8000
</div>
""", unsafe_allow_html=True)
