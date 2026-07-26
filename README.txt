# 🤖 MY PERSONAL AI CHATBOT - SETUP GUIDE

## 📁 FILES IN THIS FOLDER:

1. **`.env`** - Configuration file (your API key goes here)
2. **`chatbot.py`** - The main chatbot program

---

## ⚡ QUICK START (3 Steps):

### Step 1: Edit .env File
1. Open `.env` file in Notepad
2. Find this line: `GROQ_API_KEY=your_api_key_here`
3. Replace `your_api_key_here` with your actual API key (starts with gsk_)
4. Save the file

### Step 2: Open Command Prompt
1. Press `Windows + R`
2. Type `cmd` and press Enter

### Step 3: Run the Chatbot
Type these commands:

```bash
cd D:\osamapersonaldata\my_Ai_Agents\my-chatbot
python chatbot.py
```

---

## 🎮 HOW TO USE:

- **Type your message** and press Enter
- **The AI will respond** automatically
- **Type `quit`** or `q` to exit
- **Type `clear`** to reset conversation memory

---

## ✨ CUSTOMIZATION (Optional):

Edit the `.env` file to change:

| Setting | What It Does | Example |
|---------|-------------|---------|
| `CHATBOT_NAME` | Name of your bot | `Buddy`, `Jarvis`, `Alexa` |
| `CHATBOT_PERSONALITY` | How it behaves | Make it funny, serious, etc. |

---

## ❓ TROUBLESHOOTING:

| Problem | Solution |
|---------|----------|
| "API Key not configured" | Check .env file has your real API key |
| "pip not recognized" | Use: `python -m pip install groq python-dotenv` |
| "ModuleNotFoundError" | Install libraries first (see above) |
| Connection errors | Check internet connection |
| Want to start fresh? | Type `clear` in the chat |

---

## 🎯 NEXT STEPS (After It's Working):

1. Try different personalities in .env
2. Change the AI model (edit chatbot.py, find "model=" line)
3. Add more features (I can help you!)

---

**Built with ❤️ using Python + Groq Free AI**
