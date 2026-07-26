"""
🏢 Buddy AI Chatbot v3.1 - PROFESSIONAL EDITION
Clean, enterprise-grade AI assistant interface

Improvements in v3.1:
- Professional icon system (no emoji overload)
- Clean, minimal About section
- Removed non-functional features
- Corporate color scheme
- Refined typography
- Better spacing and layout

Author: TechGeek8000
Version: 3.1.0 (Professional Edition)
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

load_dotenv()

st.set_page_config(
    page_title="Buddy AI Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ──────────────────────────────────────────────
# PROFESSIONAL CSS THEME
# ──────────────────────────────────────────────

def get_professional_styles():
    """Return professional, minimal CSS"""
    
    return """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    
    /* Root Variables */
    :root {
        --primary: #2563eb;
        --primary-dark: #1d4ed8;
        --secondary: #64748b;
        --success: #059669;
        --warning: #d97706;
        --danger: #dc2626;
        --bg-primary: #ffffff;
        --bg-secondary: #f8fafc;
        --bg-tertiary: #f1f5f9;
        --text-primary: #0f172a;
        --text-secondary: #475569;
        --text-muted: #94a3b8;
        --border: #e2e8f0;
        --shadow-sm: 0 1px 2px rgba(0,0,0,0.05);
        --shadow-md: 0 4px 6px rgba(0,0,0,0.07);
        --shadow-lg: 0 10px 15px rgba(0,0,0,0.1);
        --radius-sm: 6px;
        --radius-md: 8px;
        --radius-lg: 12px;
        --radius-xl: 16px;
    }
    
    /* Main Container */
    .main {
        background-color: var(--bg-secondary);
        padding: 0;
    }
    
    /* Header */
    .app-header {
        background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
        padding: 24px 32px;
        margin: -24px -24px 24px -24px;
        box-shadow: var(--shadow-lg);
    }
    
    .app-header h1 {
        color: white;
        font-size: 28px;
        font-weight: 700;
        margin: 0;
        letter-spacing: -0.5px;
    }
    
    .app-header p {
        color: rgba(255,255,255,0.85);
        font-size: 14px;
        margin: 6px 0 0 0;
        font-weight: 400;
    }
    
    /* Welcome Screen */
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
        color: var(--text-primary);
        margin-bottom: 12px;
        letter-spacing: -0.5px;
    }
    
    .welcome-subtitle {
        font-size: 16px;
        color: var(--text-secondary);
        max-width: 500px;
        margin: 0 auto 48px;
        line-height: 1.6;
    }
    
    /* Feature Grid */
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
        border-radius: var(--radius-lg);
        border: 1px solid var(--border);
        transition: all 0.25s ease;
        text-align: left;
    }
    
    .feature-card:hover {
        transform: translateY(-4px);
        box-shadow: var(--shadow-lg);
        border-color: var(--primary);
    }
    
    .feature-icon-wrapper {
        width: 44px;
        height: 44px;
        border-radius: var(--radius-md);
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 16px;
        font-size: 20px;
    }
    
    .feature-icon-blue { background: #dbeafe; color: #2563eb; }
    .feature-icon-green { background: #d1fae5; color: #059669; }
    .feature-icon-purple { background: #ede9fe; color: #7c3aed; }
    .feature-icon-orange { background: #ffedd5; color: #ea580c; }
    .feature-icon-red { background: #fee2e2; color: #dc2626; }
    .feature-icon-teal { background: #ccfbf1; color: #0d9488; }
    
    .feature-title {
        font-size: 15px;
        font-weight: 600;
        color: var(--text-primary);
        margin-bottom: 6px;
    }
    
    .feature-desc {
        font-size: 13px;
        color: var(--text-secondary);
        line-height: 1.5;
    }
    
    /* Chat Messages */
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
    
    .message-bubble {
        padding: 14px 18px;
        border-radius: var(--radius-lg);
        font-size: 14px;
        line-height: 1.6;
        color: var(--text-primary);
    }
    
    .bubble-user {
        background: linear-gradient(135deg, #3b82f6, #2563eb);
        color: white;
        border-radius: 18px 18px 4px 18px;
        margin-left: auto;
        max-width: fit-content;
    }
    
    .bubble-bot {
        background: white;
        border: 1px solid var(--border);
        border-radius: 18px 18px 18px 4px;
        box-shadow: var(--shadow-sm);
    }
    
    .message-meta {
        font-size: 11px;
        color: var(--text-muted);
        margin-top: 6px;
        padding: 0 4px;
    }
    
    /* Input Area */
    .input-container {
        position: sticky;
        bottom: 0;
        background: white;
        border-top: 1px solid var(--border);
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
    
    .input-field {
        flex: 1;
    }
    
    .input-field textarea {
        border: 2px solid var(--border) !important;
        border-radius: var(--radius-lg) !important;
        padding: 14px 16px !important;
        font-size: 14px !important;
        transition: border-color 0.2s !important;
    }
    
    .input-field textarea:focus {
        border-color: var(--primary) !important;
        box-shadow: 0 0 0 3px rgba(37,99,235,0.1) !important;
    }
    
    .send-button {
        background: linear-gradient(135deg, #3b82f6, #2563eb) !important;
        color: white !important;
        border: none !important;
        padding: 14px 28px !important;
        border-radius: var(--radius-lg) !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        height: auto !important;
        transition: all 0.2s !important;
    }
    
    .send-button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 12px rgba(37,99,235,0.35) !important;
    }
    
    /* Sidebar Styling */
    .sidebar-section {
        margin-bottom: 24px;
    }
    
    .sidebar-title {
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        color: var(--text-muted);
        margin-bottom: 12px;
    }
    
    /* Stats Cards */
    .stats-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 10px;
    }
    
    .stat-item {
        background: var(--bg-tertiary);
        padding: 12px;
        border-radius: var(--radius-md);
        text-align: center;
    }
    
    .stat-value {
        font-size: 20px;
        font-weight: 700;
        color: var(--text-primary);
    }
    
    .stat-label {
        font-size: 11px;
        color: var(--text-secondary);
        margin-top: 2px;
    }
    
    /* About Section */
    .about-container {
        background: var(--bg-tertiary);
        border-radius: var(--radius-lg);
        padding: 20px;
        margin-top: 20px;
    }
    
    .about-title {
        font-size: 13px;
        font-weight: 600;
        color: var(--text-primary);
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    .about-content {
        font-size: 12px;
        color: var(--text-secondary);
        line-height: 1.7;
    }
    
    .about-content p {
        margin: 0 0 10px 0;
    }
    
    .about-content p:last-child {
        margin-bottom: 0;
    }
    
    .about-link {
        color: var(--primary);
        text-decoration: none;
    }
    
    .about-link:hover {
        text-decoration: underline;
    }
    
    /* Buttons */
    .action-button {
        width: 100%;
        padding: 10px 16px;
        border-radius: var(--radius-md);
        font-size: 13px;
        font-weight: 500;
        border: 1px solid var(--border);
        background: white;
        color: var(--text-primary);
        cursor: pointer;
        transition: all 0.2s;
        margin-bottom: 8px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    .action-button:hover {
        background: var(--bg-tertiary);
        border-color: var(--primary);
    }
    
    .action-button.primary {
        background: var(--primary);
        color: white;
        border-color: var(--primary);
    }
    
    .action-button.primary:hover {
        background: var(--primary-dark);
    }
    
    .action-button.danger {
        color: var(--danger);
        border-color: #fecaca;
    }
    
    .action-button.danger:hover {
        background: #fef2f2;
    }
    
    /* Export buttons */
    .export-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 8px;
    }
    
    /* Select boxes */
    .stSelectbox > div > div {
        background: white !important;
        border-radius: var(--radius-md) !important;
    }
    
    /* Text inputs */
    .stTextInput > div > div > input,
    .stTextinput > div > div > input {
        border-radius: var(--radius-md) !important;
    }
    
    /* Footer */
    .app-footer {
        text-align: center;
        padding: 24px;
        color: var(--text-muted);
        font-size: 12px;
        border-top: 1px solid var(--border);
        margin-top: 40px;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 6px;
    }
    
    ::-webkit-scrollbar-track {
        background: transparent;
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--border);
        border-radius: 3px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--text-muted);
    }
</style>
"""

# Apply styles
st.markdown(get_professional_styles(), unsafe_allow_html=True)

# ──────────────────────────────────────────────
# SIDEBAR - PROFESSIONAL DESIGN
# ──────────────────────────────────────────────

with st.sidebar:
    # Logo Section
    st.markdown("""
    <div style='padding: 24px 0 20px; text-align: center;'>
        <div style='width: 56px; height: 56px; background: linear-gradient(135deg, #3b82f6, #2563eb); 
             border-radius: 14px; display: inline-flex; align-items: center; 
             justify-content: center; margin-bottom: 14px; box-shadow: 0 4px 12px rgba(37,99,235,0.25);'>
            <span style='font-size: 28px;'>B</span>
        </div>
        <div style='font-size: 18px; font-weight: 700; color: #0f172a; margin-bottom: 4px;'>Buddy AI</div>
        <div style='font-size: 12px; color: #64748b;'>Professional Assistant v3.1</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    # Configuration Section
    st.markdown("<div class='sidebar-title'>Configuration</div>", unsafe_allow_html=True)
    
    api_key = os.getenv("GROQ_API_KEY", "")
    if not api_key:
        api_key = st.text_input("API Key", type="password", placeholder="Enter Groq API key", help="Get free key at console.groq.com")
        if api_key:
            os.environ["GROQ_API_KEY"] = api_key
    
    bot_name = st.text_input("Assistant Name", value=os.getenv("CHATBOT_NAME", "Buddy"))
    
    st.divider()
    
    # Personality Selection
    st.markdown("<div class='sidebar-title'>Personality Mode</div>", unsafe_allow_html=True)
    
    personalities = {
        "Friendly & Helpful": "You are a friendly and helpful AI assistant named {name}. You answer questions clearly and concisely.",
        "Professional Expert": "You are a professional AI expert named {name}. You provide detailed, well-structured responses with technical depth.",
        "Creative & Engaging": "You are a creative and engaging AI companion named {name}. You bring energy and creativity to conversations.",
        "Technical Specialist": "You are a technical specialist named {name}. You excel at programming, debugging, and technical explanations."
    }
    
    selected_personality = st.selectbox(
        "Response Style",
        options=list(personalities.keys()),
        label_visibility="collapsed"
    )
    
    # Model Selection
    models = {
        "Llama 3.3 70B (Recommended)": "llama-3.3-70b-versatile",
        "Llama 3.1 8B (Fast)": "llama-3.1-8b-instant",
        "Mixtral 8x7B": "mixtral-8x7b-32768"
    }
    
    selected_model_name = st.selectbox(
        "AI Model",
        options=list(models.keys()),
        label_visibility="collapsed"
    )
    model_id = models[selected_model_name]
    
    st.divider()
    
    # Session Statistics
    st.markdown("<div class='sidebar-title'>Session Statistics</div>", unsafe_allow_html=True)
    
    if 'message_count' not in st.session_state:
        st.session_state.message_count = 0
    if 'total_tokens' not in st.session_state:
        st.session_state.total_tokens = 0
    if 'start_time' not in st.session_state:
        st.session_state.start_time = time.time()
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class='stat-item'>
            <div class='stat-value'>{st.session_state.message_count}</div>
            <div class='stat-label'>Messages</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class='stat-item'>
            <div class='stat-value'>{st.session_state.total_tokens}</div>
            <div class='stat-label'>Tokens</div>
        </div>
        """, unsafe_allow_html=True)
    
    session_time = int(time.time() - st.session_state.start_time)
    minutes = session_time // 60
    seconds = session_time % 60
    
    st.markdown(f"""
    <div class='stat-item' style='margin-top: 10px;'>
        <div class='stat-value'>{minutes}m {seconds}s</div>
        <div class='stat-label'>Session Duration</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    # Export Options
    st.markdown("<div class='sidebar-title">Export Conversation</div>", unsafe_allow_html=True)
    
    export_col1, export_col2 = st.columns(2)
    with export_col1:
        if st.button("TXT", use_container_width=True, key="export_txt"):
            export_chat("txt")
    with export_col2:
        if st.button("JSON", use_container_width=True, key="export_json"):
            export_chat("json")
    
    st.divider()
    
    # Actions
    st.markdown("<div class='sidebar-title'>Actions</div>", unsafe_allow_html=True)
    
    if st.button("Clear History", use_container_width=True):
        if 'messages' in st.session_state:
            st.session_state.messages = []
        st.session_state.message_count = 0
        st.session_state.total_tokens = 0
        st.session_state.start_time = time.time()
        st.success("Chat history cleared")
        time.sleep(0.5)
        st.rerun()
    
    if st.button("Reset Session", use_container_width=True):
        st.session_state.clear()
        st.success("Session reset complete")
        time.sleep(0.5)
        st.rerun()
    
    st.divider()
    
    # Professional About Section
    st.markdown("""
    <div class='about-container'>
        <div class='about-title'>
            <span>About</span>
        </div>
        <div class='about-content'>
            <p><strong>Buddy AI v3.1</strong> is a professional AI assistant powered by <a href='https://groq.com' target='_blank' class='about-link'>Groq's</a> Llama 3 language model.</p>
            <p><strong>Features:</strong> Natural conversation, multiple response styles, conversation export, privacy-first design.</p>
            <p><strong>Technology:</strong> Python, Streamlit, Groq API</p>
            <p style='margin-top: 12px; padding-top: 12px; border-top: 1px solid #e2e8f0;'>
                Built by <strong>TechGeek8000</strong><br>
                <span style='color: #94a3b8;'>Version 3.1 Professional Edition</span>
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ──────────────────────────────────────────────
# HELPER FUNCTIONS
# ──────────────────────────────────────────────

def get_system_prompt():
    """Generate system prompt based on personality"""
    base_prompt = personalities.get(selected_personality, personalities["Friendly & Helpful"])
    return base_prompt.format(name=bot_name)


def initialize_groq_client():
    """Initialize Groq client"""
    key = os.getenv("GROQ_API_KEY", api_key)
    if not key:
        st.error("Please enter your Groq API key in the sidebar.")
        st.stop()
    return Groq(api_key=key)


def count_tokens(text):
    """Estimate token count"""
    return len(text.split()) * 1.3


def export_chat(format_type="txt"):
    """Export conversation to file"""
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
    """Display professional welcome screen"""
    st.markdown(f"""
    <div class='welcome-container'>
        <div class='welcome-title'>{bot_name}</div>
        <div class='welcome-subtitle'>
            Your intelligent AI assistant ready to help with questions, tasks, and conversations.
        </div>
        
        <div class='feature-grid'>
            <div class='feature-card'>
                <div class='feature-icon-wrapper feature-icon-blue'>
                    <span>&#x1F4AC;</span>
                </div>
                <div class='feature-title'>Natural Conversation</div>
                <div class='feature-desc'>Engage in fluid, human-like dialogue on any topic.</div>
            </div>
            
            <div class='feature-card'>
                <div class='feature-icon-wrapper feature-icon-green'>
                    <span>&#x26A1;</span>
                </div>
                <div class='feature-title'>Fast Responses</div>
                <div class='feature-desc'>Get answers in under one second with optimized performance.</div>
            </div>
            
            <div class='feature-card'>
                <div class='feature-icon-wrapper feature-icon-purple'>
                    <span>&#x1F9E0;</span>
                </div>
                <div class='feature-title'>Knowledge Base</div>
                <div class='feature-desc'>Powered by advanced language models with broad expertise.</div>
            </div>
            
            <div class='feature-card'>
                <div class='feature-icon-wrapper feature-icon-orange'>
                    <span>&#x1F512;</span>
                </div>
                <div class='feature-title'>Privacy Focused</div>
                <div class='feature-desc'>Your conversations stay secure and are never stored externally.</div>
            </div>
            
            <div class='feature-card'>
                <div class='feature-icon-wrapper feature-icon-teal'>
                    <span>&#x2699;</span>
                </div>
                <div class='feature-title'>Customizable</div>
                <div class='feature-desc'>Choose from multiple personalities to match your preference.</div>
            </div>
            
            <div class='feature-card'>
                <div class='feature-icon-wrapper feature-icon-red'>
                    <span>&#x1F4BE;</span>
                </div>
                <div class='feature-title'>Export Data</div>
                <div class='feature-desc'>Download and save your conversations anytime.</div>
            </div>
        </div>
        
        <div style='margin-top: 48px; color: #64748b; font-size: 14px;'>
            Start a conversation by typing your message below.
        </div>
    </div>
    """, unsafe_allow_html=True)

# ──────────────────────────────────────────────
# MAIN INTERFACE
# ──────────────────────────────────────────────

# Initialize messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Header
st.markdown(f"""
<div class='app-header'>
    <h1>{bot_name}</h1>
    <p>AI-Powered Assistant • {selected_model_name.split('(')[0].strip()} • {selected_personality.split(' ')[0]}</p>
</div>
""", unsafe_allow_html=True)

# Main content area
if not st.session_state.messages:
    # Show welcome screen
    show_welcome_screen()
else:
    # Show chat messages
    st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
    
    for message in st.session_state.messages:
        role = message["role"]
        content = message["content"]
        
        if role == "user":
            st.markdown(f"""
            <div class='message-wrapper'>
                <div class='message-avatar avatar-user'>U</div>
                <div class='message-content'>
                    <div class='message-bubble bubble-user'>{content}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class='message-wrapper'>
                <div class='message-avatar avatar-bot'>{bot_name[0] if bot_name else 'B'}</div>
                <div class='message-content'>
                    <div class='message-bubble bubble-bot'>{content}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# Input area
st.markdown("<div class='input-container'>", unsafe_allow_html=True)

with st.form("chat_form", clear_on_submit=True):
    col1, col2 = st.columns([6, 1])
    
    with col1:
        user_input = st.text_area(
            "",
            height=80,
            placeholder=f"Type your message to {bot_name}...",
            label_visibility="collapsed",
            key="professional_input"
        )
    
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
        has_response = (
            len(st.session_state.messages) >= 2 and 
            st.session_state.messages[-2]["role"] == "assistant"
        )
        
        if not has_response:
            with st.spinner("Thinking..."):
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
                    
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": ai_response
                    })
                    st.session_state.message_count += 1
                    
                    st.rerun()
                
                except Exception as e:
                    error_msg = f"Error: {str(e)}"
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": error_msg
                    })
                    st.error(error_msg)

# Footer
st.markdown(f"""
<div class='app-footer'>
    Privacy-focused • Local storage • Powered by Groq AI • Built by TechGeek8000
</div>
""", unsafe_allow_html=True)
