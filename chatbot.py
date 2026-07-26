"""
============================================
    YOUR PERSONAL AI CHATBOT
    Powered by Groq (FREE AI!)
============================================
"""

# SECTION 1: IMPORT LIBRARIES
import os
import sys
from dotenv import load_dotenv
from groq import Groq

# SECTION 2: LOAD CONFIGURATION
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
chatbot_name = os.getenv("CHATBOT_NAME", "Buddy")
system_prompt = os.getenv("CHATBOT_PERSONALITY", 
    "You are a friendly and helpful AI assistant.")

# SECTION 3: CHECK API KEY
if api_key == "PASTE_YOUR_GSK_KEY_HERE" or api_key is None:
    print("⚠️  ERROR: Please set your API key in .env file!")
    sys.exit(1)

# SECTION 4: INITIALIZE AI CLIENT
client = Groq(api_key=api_key)

print("=" * 50)
print(f"🤖 {chatbot_name} - Your Personal AI Chatbot")
print("=" * 50)
print("✅ Connected to Groq AI (FREE!)")
print("💬 Type your messages below")
print("🚪 Type 'quit', 'exit', or 'q' to stop")
print("🧹 Type 'clear' to reset conversation memory")
print("=" * 50)

# SECTION 5: CONVERSATION MEMORY
conversation_history = []
conversation_history.append({
    "role": "system",
    "content": system_prompt
})

# SECTION 6: MAIN CHAT FUNCTION
def chat_with_ai(user_message):
    try:
        conversation_history.append({
            "role": "user",
            "content": user_message
        })
        
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=conversation_history,
            temperature=0.7,
            max_tokens=1024,
        )
        
        ai_response = response.choices[0].message.content
        
        conversation_history.append({
            "role": "assistant",
            "content": ai_response
        })
        
        return ai_response
        
    except Exception as error:
        return f"❌ Error: {str(error)}"

# SECTION 7: MAIN LOOP
def main():
    while True:
        try:
            user_input = input(f"\n👤 You: ")
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print(f"\n👋 {chatbot_name}: Goodbye!")
                break
            
            if user_input.lower() == 'clear':
                conversation_history.clear()
                conversation_history.append({
                    "role": "system",
                    "content": system_prompt
                })
                print(f"\n🧹 Memory cleared!")
                continue
            
            if not user_input.strip():
                continue
            
            print(f"\n🤖 {chatbot_name}: ", end="")
            response = chat_with_ai(user_input)
            print(response)
            
        except KeyboardInterrupt:
            print(f"\n\n👋 Goodbye!")
            break

# SECTION 8: START!
if __name__ == "__main__":
    main()