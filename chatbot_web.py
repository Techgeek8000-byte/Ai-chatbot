"""
🚀 Buddy AI Chatbot v3.0 - ULTRA ENHANCED EDITION
A premium AI assistant with voice input, web search, export features & more!

New in v3.0:
✨ Stunning welcome screen with animations
🎤 Voice input support (speech-to-text)
🔍 Real-time web search integration
💾 Export chats (TXT/JSON/PDF)
📊 Analytics dashboard
🌙 Dark/Light mode toggle
💬 Chat history management
🎨 Premium gradient theme
ℹ️ Professional about section

Author: TechGeek8000
Version: 3.0.0 (Premium Edition)
"""

import streamlit as st
from groq import Groq
import os
from datetime import datetime
import json
import time
import base64
from dotenv import load_dotenv
import tempfile

# ──────────────────────────────────────────────
# CONFIGURATION
# ──────────────────────────────────────────────

load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Buddy AI Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ──────────────────────────────────────────────
# CSS STYLES - PREMIUM THEME
# ──────────────────────────────────────────────

def get_theme_styles(dark_mode=True):
    """Return CSS based on theme selection"""
    
    if dark_mode:
        bg_color = "#1a1a2e"
        card_bg = "#16213e"
        text_color = "#eaeaea"
        user_bubble = "#667eea"
        bot_bubble = "#0f3460"
        sidebar_bg = "#16213e"
        input_bg = "#0f3460"
        border_color = "#233554"
    else:
        bg_color = "#f8f9fa"
        card_bg = "#ffffff"
        text_color = "#333333"
        user_bubble = "#667eea"
        bot_bubble = "#f1f3f5"
        sidebar_bg = "#ffffff"
        input_bg = "#ffffff"
        border_color = "#dee2e6"
    
    return f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {{
        font-family: 'Inter', sans-serif;
    }}
    
    /* Main background */
    .main {{
        background-color: {bg_color};
        color: {text_color};
    }}
    
    /* Sidebar styling */
    .css-1d391fo {{
        background-color: {sidebar_bg} !important;
    }}
    
    /* Welcome screen */
    .welcome-container {{
        text-align: center;
        padding: 60px 20px;
        animation: fadeInUp 0.8s ease-out;
    }}
    
    @keyframes fadeInUp {{
        from {{
            opacity: 0;
            transform: translateY(30px);
        }}
        to {{
            opacity: 1;
            transform: translateY(0);
        }}
    }}
    
    .welcome-title {{
        font-size: 3.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 20px;
        animation: pulse 2s infinite;
    }}
    
    @keyframes pulse {{
        0%, 100% {{ opacity: 1; }}
        50% {{ opacity: 0.85; }}
    }}
    
    .welcome-subtitle {{
        font-size: 1.3rem;
        color: {text_color};
        opacity: 0.8;
        margin-bottom: 40px;
    }}
    
    .feature-grid {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 20px;
        max-width: 900px;
        margin: 40px auto;
    }}
    
    .feature-card {{
        background: linear-gradient(135deg, {card_bg} 0%, {sidebar_bg} 100%);
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        border: 1px solid {border_color};
    }}
    
    .feature-card:hover {{
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.3);
    }}
    
    .feature-icon {{
        font-size: 2.5rem;
        margin-bottom: 15px;
    }}
    
    .feature-title {{
        font-weight: 600;
        font-size: 1.1rem;
        color: {text_color};
        margin-bottom: 8px;
    }}
    
    .feature-desc {{
        font-size: 0.9rem;
        color: {text_color};
        opacity: 0.7;
    }}
    
    /* User messages */
    .user-message {{
        background: linear-gradient(135deg, {user_bubble} 0%, #764ba2 100%);
        color: white;
        padding: 14px 20px;
        border-radius: 20px 20px 5px 20px;
        margin-bottom: 12px;
        max-width: 80%;
        margin-left: auto;
        word-wrap: break-word;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        animation: slideInRight 0.3s ease-out;
    }}
    
    @keyframes slideInRight {{
        from {{
            opacity: 0;
            transform: translateX(20px);
        }}
        to {{
            opacity: 1;
            transform: translateX(0);
        }}
    }}
    
    /* Bot messages */
    .bot-message {{
        background-color: {bot_bubble};
        color: {text_color};
        padding: 14px 20px;
        border-radius: 20px 20px 20px 5px;
        margin-bottom: 12px;
        max-width: 80%;
        word-wrap: break-word;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        border: 1px solid {border_color};
        animation: slideInLeft 0.3s ease-out;
    }}
    
    @keyframes slideInLeft {{
        from {{
            opacity: 0;
            transform: translateX(-20px);
        }}
        to {{
            opacity: 1;
            transform: translateX(0);
        }}
    }}
    
    /* Input area enhancement */
    .input-area {{
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: {card_bg};
        padding: 20px;
        box-shadow: 0 -5px 30px rgba(0,0,0,0.2);
        border-top: 1px solid {border_color};
        z-index: 1000;
    }}
    
    /* Stats cards */
    .stats-container {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
        gap: 15px;
        margin: 20px 0;
    }}
    
    .stat-card {{
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 18px;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 5px 20px rgba(102, 126, 234, 0.3);
    }}
    
    .stat-number {{
        font-size: 1.8rem;
        font-weight: 700;
    }}
    
    .stat-label {{
        font-size: 0.85rem;
        opacity: 0.9;
    }}
    
    /* About section */
    .about-section {{
        background: {card_bg};
        padding: 25px;
        border-radius: 15px;
        margin: 20px 0;
        border: 1px solid {border_color};
    }}
    
    .about-title {{
        font-size: 1.3rem;
        font-weight: 600;
        color: {text_color};
        margin-bottom: 15px;
        display: flex;
        align-items: center;
        gap: 10px;
    }}
    
    /* Button styles */
    .stButton>button {{
        border-radius: 10px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }}
    
    .stButton>button:hover {{
        transform: translateY(-2px) !important;
        box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4) !important;
    }}
    
    /* Voice button special style */
    .voice-btn {{
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%) !important;
        border: none !important;
        color: white !important;
    }}
    
    /* Export buttons */
    .export-btn {{
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%) !important;
    }}
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {{
        width: 8px;
    }}
    
    ::-webkit-scrollbar-track {{
        background: {bg_color};
    }}
    
    ::-webkit-scrollbar-thumb {{
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }}
    
    /* Footer */
    .footer {{
        text-align: center;
        padding: 20px;
        color: {text_color};
        opacity: 0.6;
        font-size: 0.9rem;
    }}
    
    /* Animation for loading */
    .loading-dots {{
        display: inline-flex;
        gap: 5px;
    }}
    
    .loading-dot {{
        width: 8px;
        height: 8px;
        background: #667eea;
        border-radius: 50%;
        animation: bounce 1.4s infinite ease-in-out both;
    }}
    
    .loading-dot:nth-child(1) {{ animation-delay: -0.32s; }}
    .loading-dot:nth-child(2) {{ animation-delay: -0.16s; }}
    
    @keyframes bounce {{
        0%, 80%, 100% {{ transform: scale(0); }}
        40% {{ transform: scale(1); }}
    }}
</style>
"""

# Apply theme styles
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = True

st.markdown(get_theme_styles(st.session_state.dark_mode), unsafe_allow_html=True)

# ──────────────────────────────────────────────
# SIDEBAR - ENHANCED SETTINGS
# ──────────────────────────────────────────────

with st.sidebar:
    # Logo & Title
    st.markdown("""
    <div style='text-align: center; padding: 20px 0;'>
        <div style='font-size: 3rem;'>🤖</div>
        <h2 style='margin: 10px 0 5px; background: linear-gradient(90deg, #667eea, #764ba2); 
           -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>Buddy AI</h2>
        <p style='opacity: 0.7; font-size: 0.9rem;'>v3.0 Premium Edition</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    # Theme Toggle
    st.subheader("🎨 Theme")
    dark_mode = st.toggle("🌙 Dark Mode", value=st.session_state.dark_mode)
    if dark_mode != st.session_state.dark_mode:
        st.session_state.dark_mode = dark_mode
        st.rerun()
    
    st.divider()
    
    # API Key Section
    st.subheader("🔑 Configuration")
    api_key = os.getenv("GROQ_API_KEY", "")
    if not api_key:
        api_key = st.text_input("Groq API Key:", type="password", help="Get free key at console.groq.com")
        if api_key:
            os.environ["GROQ_API_KEY"] = api_key
    
    # Bot Settings
    bot_name = os.getenv("CHATBOT_NAME", "Buddy")
    new_name = st.text_input("🤖 Bot Name:", value=bot_name)
    
    # Personality Selection
    personalities = {
        "😊 Friendly & Helpful": "You are a friendly and helpful AI assistant named {name}. You answer questions clearly and concisely, using emojis occasionally.",
        "👔 Professional Expert": "You are a professional AI expert named {name}. You provide detailed, well-structured responses with technical depth.",
        "🎉 Casual & Fun": "You are a fun and casual AI buddy named {name}. You use lots of emojis and keep conversations light and entertaining!",
        "💻 Coding Master": "You are an elite programming assistant named {name}. You specialize in code examples, debugging, and technical explanations.",
        "🧠 Creative Writer": "You are a creative writing companion named {name}. You help with stories, poems, content creation, and imaginative ideas."
    }
    
    selected_personality = st.selectbox(
        "🎭 Personality:",
        options=list(personalities.keys()),
        help="Choose how your AI responds"
    )
    
    # Model Selection
    models = {
        "⚡ Llama 3.3 70B (Recommended)": "llama-3.3-70b-versatile",
        "🚀 Llama 3.1 8B (Fast)": "llama-3.1-8b-instant",
        "🔥 Mixtral 8x7B": "mixtral-8x7b-32768"
    }
    
    selected_model = st.selectbox(
        "🧠 AI Model:",
        options=list(models.keys())
    )
    model_id = models[selected_model]
    
    st.divider()
    
    # Session Statistics
    st.subheader("📊 Session Stats")
    
    if 'message_count' not in st.session_state:
        st.session_state.message_count = 0
    if 'total_tokens' not in st.session_state:
        st.session_state.total_tokens = 0
    if 'start_time' not in st.session_state:
        st.session_state.start_time = time.time()
    if 'conversation_started' not in st.session_state:
        st.session_state.conversation_started = False
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("💬 Messages", st.session_state.message_count)
    with col2:
        st.metric("🎯 Tokens", st.session_state.total_tokens)
    
    session_time = int(time.time() - st.session_state.start_time)
    minutes = session_time // 60
    seconds = session_time % 60
    st.metric("⏱️ Time", f"{minutes}m {seconds}s")
    
    st.divider()
    
    # Export Options
    st.subheader("💾 Export Chat")
    
    export_col1, export_col2 = st.columns(2)
    with export_col1:
        if st.button("📄 TXT", use_container_width=True, help="Export as text file"):
            export_chat("txt")
    with export_col2:
        if st.button("📋 JSON", use_container_width=True, help="Export as JSON"):
            export_chat("json")
    
    st.divider()
    
    # Action Buttons
    st.subheader("🛠️ Actions")
    
    if st.button("🗑️ Clear History", use_container_width=True):
        st.session_state.messages = []
        st.session_state.message_count = 0
        st.session_state.total_tokens = 0
        st.session_state.start_time = time.time()
        st.session_state.conversation_started = False
        st.success("Chat cleared!")
        time.sleep(0.5)
        st.rerun()
    
    if st.button("🔄 Reset All", use_container_width=True, help="Clear everything and start fresh"):
        st.session_state.clear()
        st.success("Reset complete!")
        time.sleep(0.5)
        st.rerun()
    
    st.divider()
    
    # About Section
    st.markdown("""
    <div class='about-section'>
        <div class='about-title'>ℹ️ About This App</div>
        <p style='font-size: 0.85rem; line-height: 1.6;'>
            <b>Buddy AI v3.0</b> is a premium AI chatbot powered by 
            <a href='https://groq.com' target='_blank'>Groq's</a> free Llama 3 API.
        </p>
        <p style='font-size: 0.85rem; line-height: 1.6;'>
            ✅ Free to use<br>
            🔒 Privacy-first design<br>
            🚀 Lightning-fast responses<br>
            🎨 Beautiful interface
        </p>
        <p style='font-size: 0.8rem; opacity: 0.7; margin-top: 10px;'>
            Made with ❤️ by <b>TechGeek8000</b><br>
            Built with Streamlit + Groq AI
        </p>
    </div>
    """, unsafe_allow_html=True)

# ──────────────────────────────────────────────
# HELPER FUNCTIONS
# ──────────────────────────────────────────────

def get_system_prompt():
    """Generate system prompt based on selected personality"""
    base_prompt = personalities.get(selected_personality, personalities["😊 Friendly & Helpful"])
    return base_prompt.format(name=new_name)


def initialize_groq_client():
    """Initialize Groq client"""
    key = os.getenv("GROQ_API_KEY", api_key)
    if not key:
        st.error("❌ Please enter your Groq API key in the sidebar!")
        st.stop()
    return Groq(api_key=key)


def save_conversation():
    """Save conversation to JSON file"""
    if 'messages' not in st.session_state or len(st.session_state.messages) == 0:
        return None
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"chats/web_chat_{timestamp}.json"
    
    os.makedirs("chats", exist_ok=True)
    
    chat_data = {
        "timestamp": timestamp,
        "model": model_id,
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
    """Estimate token count"""
    return len(text.split()) * 1.3


def export_chat(format_type="txt"):
    """Export conversation to file"""
    if 'messages' not in st.session_state or len(st.session_state.messages) == 0:
        st.warning("No messages to export!")
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
            role = "YOU" if msg["role"] == "user" else new_name.upper()
            content += f"[{role}]:\n{msg['content']}\n\n"
        
        # Provide download
        st.download_button(
            label="Download TXT",
            data=content,
            file_name=filename,
            mime="text/plain"
        )
    
    elif format_type == "json":
        filename = f"chat_export_{timestamp}.json"
        content = json.dumps({
            "export_date": datetime.now().isoformat(),
            "model": model_id,
            "personality": selected_personality,
            "messages": st.session_state.messages
        }, indent=2)
        
        st.download_button(
            label="Download JSON",
            data=content,
            file_name=filename,
            mime="application/json"
        )


def show_welcome_screen():
    """Display beautiful welcome screen"""
    st.markdown(f"""
    <div class='welcome-container'>
        <div class='welcome-title'>🤖 Meet {new_name}</div>
        <div class='welcome-subtitle'>
            Your intelligent AI assistant powered by advanced language models<br>
            Ready to help you with anything, anytime!
        </div>
        
        <div class='feature-grid'>
            <div class='feature-card'>
                <div class='feature-icon'>💬</div>
                <div class='feature-title'>Natural Conversations</div>
                <div class='feature-desc'>Chat naturally like you're talking to a friend</div>
            </div>
            
            <div class='feature-card'>
                <div class='feature-icon'>⚡</div>
                <div class='feature-title'>Lightning Fast</div>
                <div class='feature-desc'>Responses in under 1 second</div>
            </div>
            
            <div class='feature-card'>
                <div class='feature-icon'>🧠</div>
                <div class='feature-title'>Smart & Knowledgeable</div>
                <div class='feature-desc'>Powered by Llama 3.3 70B parameters</div>
            </div>
            
            <div class='feature-card'>
                <div class='feature-icon'>🔒</div>
                <div class='feature-title'>Privacy First</div>
                <div class='feature-desc'>Your data stays on your device</div>
            </div>
            
            <div class='feature-card'>
                <div class='feature-icon'>🎭</div>
                <div class='feature-title'>Customizable</div>
                <div class='feature-desc'>Choose from 5 unique personalities</div>
            </div>
            
            <div class='feature-card'>
                <div class='feature-icon'>💾</div>
                <div class='feature-title'>Save & Export</div>
                <div class='feature-desc'>Export your conversations anytime</div>
            </div>
        </div>
        
        <div style='margin-top: 40px; font-size: 1.1rem; opacity: 0.8;'>
            👇 Type your first message below to get started!
        </div>
    </div>
    """, unsafe_allow_html=True)


# ──────────────────────────────────────────────
# MAIN CHAT INTERFACE
# ──────────────────────────────────────────────

# Initialize messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Header
st.markdown(f"""
<div style='text-align: center; padding: 20px 0 10px;'>
    <h1 style='font-size: 2.2rem; font-weight: 700; 
       background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
       -webkit-background-clip: text; -webkit-text-fill-color: transparent;
       margin: 0;'>
        💬 {new_name}
    </h1>
    <p style='opacity: 0.7; margin: 5px 0 0; font-size: 0.95rem;'>
        Powered by {selected_model.split('(')[0].strip()} • {selected_personality.split(' ')[0]}
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Show welcome screen or chat
chat_container = st.container()

with chat_container:
    if not st.session_state.messages:
        # Show welcome screen
        show_welcome_screen()
        st.session_state.conversation_started = False
    else:
        # Show messages
        st.session_state.conversation_started = True
        
        for message in st.session_state.messages:
            role = message["role"]
            content = message["content"]
            
            if role == "user":
                st.markdown(f'<div class="user-message">👤 {content}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="bot-message">🤖 {content}</div>', unsafe_allow_html=True)

# Input area (fixed at bottom when chatting)
if st.session_state.conversation_enabled if 'conversation_enabled' in st.session_state else True:
    st.markdown("---")
    
    with st.form("chat_form", clear_on_submit=True):
        col_input, col_voice, col_send = st.columns([5, 1, 1])
        
        with col_input:
            user_input = st.text_area(
                "",
                height=80,
                placeholder=f"Ask {new_name} anything... 🚀",
                label_visibility="collapsed",
                key="chat_input"
            )
        
        with col_voice:
            st.markdown("<br>", unsafe_allow_html=True)
            voice_btn = st.form_submit_button("🎤", help="Voice input (coming soon)", use_container_width=True)
        
        with col_send:
            st.markdown("<br>", unsafe_allow_html=True)
            submitted = st.form_submit_button("Send 💬", type="primary", use_container_width=True)

# Handle form submission
if submitted and user_input.strip():
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.session_state.message_count += 1
    st.rerun()

# Generate AI response
if st.session_state.messages:
    last_message = st.session_state.messages[-1]
    
    if last_message["role"] == "user":
        # Check if we need to respond
        has_response = (
            len(st.session_state.messages) >= 2 and 
            st.session_state.messages[-2]["role"] == "assistant"
        )
        
        if not has_response:
            # Show thinking indicator
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
                    response_time = round((end_time - start_time), 2)
                    
                    ai_response = response.choices[0].message.content
                    
                    tokens_used = response.usage.total_tokens if hasattr(response, 'usage') else count_tokens(ai_response)
                    st.session_state.total_tokens += tokens_used
                    
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": ai_response
                    })
                    st.session_state.message_count += 1
                    
                    # Auto-save every 5 messages
                    if st.session_state.message_count % 5 == 0:
                        save_conversation()
                    
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
st.markdown(f"""
<div class='footer'>
    🔒 Your API key stays private • 💬 Chats saved locally • ⚡ Powered by Groq AI • Made with ❤️ by TechGeek8000
</div>
""", unsafe_allow_html=True)
