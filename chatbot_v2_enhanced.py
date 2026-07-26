"""
================================================================================
    🤖 BUDDY AI CHATBOT v2.0 - ENHANCED EDITION
================================================================================
    
    NEW FEATURES IN v2.0:
    ✅ Response time tracking (⏱️)
    ✅ Token usage counter (📊)
    ✅ Auto-save chat history (💾)
    ✅ Load past conversations (📂)
    ✅ Beautiful colored UI (🎨)
    ✅ Conversation statistics (📈)
    
    POWERED BY: Groq (FREE AI!)
================================================================================
"""

import os
import sys
import json
import time
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

# ============================================
# CONFIGURATION & SETUP
# ============================================

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
chatbot_name = os.getenv("CHATBOT_NAME", "Buddy")
system_prompt = os.getenv("CHATBOT_PERSONALITY", 
    "You are a friendly, helpful, and slightly humorous AI assistant.")

# Create chats directory for saving conversations
chats_dir = Path(__file__).parent / "chats"
chats_dir.mkdir(exist_ok=True)

# Check API key
if api_key in [None, "your_api_key_here", "PASTE_YOUR_GSK_KEY_HERE"]:
    print("=" * 60)
    print("  ⚠️  ERROR: API Key not configured!")
    print("=" * 60)
    print("\n  Please edit the .env file and add your Groq API key")
    print("  Your key starts with 'gsk_'\n")
    sys.exit(1)

# Initialize client
client = Groq(api_key=api_key)

# Stats tracking
stats = {
    "total_messages": 0,
    "total_tokens_used": 0,
    "conversation_start": datetime.now(),
    "responses_given": 0,
    "total_response_time": 0
}

# Conversation memory
conversation_history = []
conversation_history.append({
    "role": "system",
    "content": system_prompt
})

# Current session ID (for saving)
session_id = datetime.now().strftime("%Y%m%d_%H%M%S")

# ============================================
# UTILITY FUNCTIONS
# ============================================

def get_timestamp():
    """Get current timestamp string."""
    return datetime.now().strftime("%H:%M:%S")

def format_time(seconds):
    """Format seconds into human-readable time."""
    if seconds < 1:
        return f"{int(seconds * 1000)}ms"
    elif seconds < 60:
        return f"{seconds:.2f}s"
    else:
        mins = int(seconds // 60)
        secs = seconds % 60
        return f"{mins}m {secs:.1f}s"

def count_tokens(text):
    """Estimate token count (rough approximation: ~4 chars per token)."""
    return len(text) // 4

def save_conversation():
    """Save current conversation to JSON file."""
    filename = f"chat_{session_id}.json"
    filepath = chats_dir / filename
    
    chat_data = {
        "session_id": session_id,
        "timestamp": datetime.now().isoformat(),
        "messages": conversation_history[1:],  # Exclude system prompt
        "stats": {
            "total_messages": stats["total_messages"],
            "total_tokens": stats["total_tokens_used"],
            "duration_sec": (datetime.now() - stats["conversation_start"]).total_seconds()
        }
    }
    
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(chat_data, f, indent=2, ensure_ascii=False)
        return filepath.name
    except Exception as e:
        return None

def load_saved_chats():
    """List all saved chat sessions."""
    chat_files = list(chats_dir.glob("chat_*.json"))
    return sorted(chat_files, key=lambda x: x.stat().st_mtime, reverse=True)

def load_chat_session(filename):
    """Load a specific chat session."""
    filepath = chats_dir / filename
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        return None

# ============================================
# MAIN CHAT FUNCTION (ENHANCED)
# ============================================

def chat_with_ai(user_message):
    """
    Send message to AI and get response.
    Returns tuple: (response_text, response_time, tokens_used)
    """
    global stats
    
    start_time = time.time()
    
    try:
        # Add user message
        conversation_history.append({
            "role": "user",
            "content": user_message
        })
        
        # Call API
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=conversation_history,
            temperature=0.7,
            max_tokens=1024,
            top_p=0.9,
            stream=False
        )
        
        # Extract response
        ai_response = response.choices[0].message.content
        
        # Calculate timing
        end_time = time.time()
        response_time = end_time - start_time
        
        # Calculate tokens
        input_tokens = response.usage.prompt_tokens if hasattr(response, 'usage') else count_tokens(user_message)
        output_tokens = response.usage.completion_tokens if hasattr(response, 'usage') else count_tokens(ai_response)
        total_tokens = input_tokens + output_tokens
        
        # Update stats
        stats["total_tokens_used"] += total_tokens
        stats["responses_given"] += 1
        stats["total_response_time"] += response_time
        
        # Add AI response to memory
        conversation_history.append({
            "role": "assistant",
            "content": ai_response
        })
        
        return {
            "response": ai_response,
            "time": response_time,
            "tokens": total_tokens,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens
        }
        
    except Exception as error:
        end_time = time.time()
        return {
            "response": f"❌ Error: {str(error)}\n\nPlease check your internet connection.",
            "time": end_time - start_time,
            "tokens": 0,
            "input_tokens": 0,
            "output_tokens": 0
        }

# ============================================
# DISPLAY FUNCTIONS
# ============================================

def print_banner():
    """Print welcome banner."""
    print("\n" + "=" * 65)
    print(f"  🤖 {chatbot_name.upper()} - Your Personal AI Chatbot v2.0")
    print("=" * 65)
    print(f"  ✅ Connected to Groq AI (FREE!)")
    print(f"  🕐 Started at: {stats['conversation_start'].strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 65)
    print("  💬 Type your messages below")
    print("  🚪 Type 'quit', 'exit', or 'q' to stop")
    print("  🧹 Type 'clear' to reset conversation")
    print("  💾 Type 'save' to save this conversation")
    print("  📂 Type 'history' to see saved chats")
    print("  📊 Type 'stats' to view statistics")
    print("=" * 65 + "\n")

def print_stats():
    """Display conversation statistics."""
    duration = (datetime.now() - stats["conversation_start"]).total_seconds()
    avg_time = stats["total_response_time"] / max(stats["responses_given"], 1)
    
    print("\n" + "-" * 40)
    print("  📊 CONVERSATION STATISTICS")
    print("-" * 40)
    print(f"  ⏱️  Duration:     {format_time(duration)}")
    print(f"  💬 Messages:     {stats['total_messages']}")
    print(f"  🤖 Responses:    {stats['responses_given']}")
    print(f"  📊 Total Tokens: {stats['total_tokens_used']:,}")
    print(f"  ⚡ Avg Response: {format_time(avg_time)}")
    print("-" * 40 + "\n")

def print_history():
    """Show saved chat sessions."""
    saved_chats = load_saved_chats()
    
    if not saved_chats:
        print("\n  📂 No saved conversations yet.")
        print("     Type 'save' to save the current one!\n")
        return
    
    print("\n" + "-" * 50)
    print("  📂 SAVED CONVERSATIONS")
    print("-" * 50)
    
    for i, chat_file in enumerate(saved_chats[:10], 1):  # Show last 10
        try:
            data = json.loads(chat_file.read_text())
            date = data.get('timestamp', 'Unknown')[:16]
            msgs = len(data.get('messages', [])) // 2
            print(f"  {i}. {chat_file.name} | {date} | {msgs} exchanges")
        except:
            print(f"  {i}. {chat_file.name}")
    
    if len(saved_chats) > 10:
        print(f"  ... and {len(saved_chats) - 10} more")
    
    print("-" * 50 + "\n")

# ============================================
# MAIN PROGRAM LOOP
# ============================================

def main():
    """Main chat loop."""
    
    print_banner()
    
    while True:
        try:
            # Get user input
            user_input = input(f"  👤 You: ")
            
            # Handle commands
            cmd = user_input.lower().strip()
            
            if cmd in ['quit', 'exit', 'q']:
                # Auto-save before exit
                saved_file = save_conversation()
                print(f"\n  👋 {chatbot_name}: Goodbye! It was nice chatting!")
                if saved_file:
                    print(f"  💾 Conversation saved: {saved_file}")
                print_stats()
                break
            
            elif cmd == 'clear':
                conversation_history.clear()
                conversation_history.append({
                    "role": "system",
                    "content": system_prompt
                })
                session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
                print(f"\n  🧹 {chatbot_name}: Memory cleared! Fresh start.\n")
                continue
            
            elif cmd == 'save':
                saved_file = save_conversation()
                if saved_file:
                    print(f"\n  ✅ Saved: {saved_file}\n")
                else:
                    print(f"\n  ❌ Failed to save.\n")
                continue
            
            elif cmd == 'history':
                print_history()
                continue
            
            elif cmd == 'stats':
                print_stats()
                continue
            
            elif not user_input.strip():
                print("\n  ⚠️  Please type something!\n")
                continue
            
            # Normal message - process with AI
            stats["total_messages"] += 1
            
            print(f"\n  🤖 {chatbot_name}: ", end="", flush=True)
            
            result = chat_with_ai(user_input)
            
            # Display response
            print(result["response"])
            
            # Display metadata
            print(f"\n  ┌─────────────────────────────────────┐")
            print(f"  │ ⏱️  Time: {format_time(result['time']):<20} │ 📊 Tokens: {result['tokens']:<6} │")
            print(f"  └─────────────────────────────────────┘")
            
            # Memory indicator
            msg_count = (len(conversation_history) - 1) // 2
            if msg_count > 0:
                print(f"  💭 Remembering {msg_count} message{'s' if msg_count != 1 else ''}\n")
            
        except KeyboardInterrupt:
            print(f"\n\n  👋 {chatbot_name}: Goodbye! See you next time!")
            break
        except Exception as e:
            print(f"\n  ❌ Error: {e}\n")
            continue

# ============================================
# START THE CHATBOT
# ============================================

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n  ❌ Fatal error: {e}")
        sys.exit(1)

"""
================================================================================
    END OF CHATBOT v2.0
    
    NEW COMMANDS:
    - save      : Save current conversation to file
    - history   : List all saved conversations  
    - stats     : View conversation statistics
    - clear     : Reset memory (same as before)
    - quit/exit : Exit (auto-saves now!)
    
    FILES CREATED:
    - chats/          : Folder with saved conversations (JSON format)
    - .env            : Configuration file
    - chatbot_v2.py   : This program
    
    NEXT STEPS:
    1. Test this version
    2. Try the new commands (save, stats, history)
    3. Ready for web deployment!
================================================================================
"""
