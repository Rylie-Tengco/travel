# ✈️ WanderMind — AI Travel Planner Agent

> An intelligent AI-powered travel planning agent built with Python, Groq, Streamlit, and the OpenWeatherMap API.

---

## 📌 Project Overview

WanderMind is an agentic AI system that helps users plan personalized travel itineraries through a conversational chat interface. It demonstrates key agentic behaviors including multi-step reasoning, tool usage (weather API), short-term memory (conversation context), and goal-oriented task completion.

**Built for:** ANLYTC4 Final Project  
**Course:** Analytics 4  

---

## 🧠 System Architecture

```
User Input (Streamlit Chat)
        ↓
Preference Context (travel style, days, budget)
        ↓
Groq LLM (Reasoning Engine)
        ↓
    ┌───────────────────────┐
    │  Tool: OpenWeatherMap │  ← External API
    └───────────────────────┘
        ↓
Itinerary / Recommendations (Response)
        ↓
Chat UI with Memory (Streamlit Session State)
```

### Agentic Features
| Feature | Implementation |
|---|---|
| **Multi-step reasoning** | Groq plans day-by-day itineraries with morning/afternoon/evening breakdown |
| **Tool usage** | OpenWeatherMap API for live weather at destination |
| **Short-term memory** | Full conversation history passed on every API call |
| **Goal-oriented behavior** | Agent asks follow-up questions to refine recommendations |
| **Personalization** | Adapts to travel style, budget, and trip length preferences |

---

## 🛠️ Libraries Used

| Library | Purpose |
|---|---|
| `groq` | LLM reasoning engine |
| `streamlit` | Chat web interface |
| `requests` | OpenWeatherMap API calls |

---

## ⚙️ Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/ai-travel-planner.git
cd ai-travel-planner
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Get your API keys
- **Groq API key:** https://console.groq.com/keys
- **OpenWeatherMap key (free):** https://openweathermap.org/api → Sign up → API Keys
- Set them once as Streamlit secrets or environment variables so users do not need to re-enter them after refresh.

Example ` .streamlit/secrets.toml `:
```toml
groq_api_key = "your_groq_key"
openweather_api_key = "your_openweather_key"
```

Example PowerShell environment variables:
```powershell
$env:GROQ_API_KEY = "your_groq_key"
$env:OPENWEATHER_API_KEY = "your_openweather_key"
```

### 4. Run the app
```bash
streamlit run app.py
```

### 5. Use the app
1. Set your Groq and OpenWeatherMap keys once in secrets or environment variables
2. Set your travel style, number of days, and budget
3. Start chatting!

---

## 💬 Example Prompts

- *"Plan me a 5-day trip to Tokyo on a mid-range budget"*
- *"What should I pack for a beach trip to Palawan?"*
- *"Give me a cultural itinerary for Rome, 7 days, luxury budget"*
- *"What are the visa requirements for Filipinos going to Japan?"*
- *"Best street food spots in Bangkok?"*

---

## 📁 Project Structure

```
ai-travel-planner/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
└── README.md           # This file
```

---

## 🧪 Test Cases

| # | Input | Expected Output |
|---|---|---|
| 1 | "Plan a 3-day trip to Paris" | Day-by-day itinerary with activities |
| 2 | "Budget trip to Bali for 7 days" | Budget-friendly recommendations |
| 3 | "What to pack for Iceland in winter?" | Packing list with winter gear |
| 4 | "Best food in Tokyo" | Restaurant and food recommendations |
| 5 | "Visa requirements for the Philippines to Japan" | Visa information |
| 6 | "Family-friendly activities in Singapore" | Kid-friendly recommendations |
| 7 | "Luxury honeymoon in Maldives 5 days" | Luxury resort and experience suggestions |
| 8 | Check weather for "Manila" | Live weather data from API |
| 9 | "Is it safe to travel to Morocco?" | Safety tips and advice |
| 10 | "Compare Cebu vs Boracay for a beach trip" | Comparison with pros and cons |

---

## 🤖 Responsible AI Reflection

WanderMind is designed with the following ethical considerations:
- **Transparency:** Users are informed they are interacting with an AI agent
- **Accuracy:** Users are encouraged to verify visa and safety information from official sources
- **Bias awareness:** The agent may have biases toward popular tourist destinations
- **Data privacy:** No user data is stored beyond the current session

---

## 📄 License

This project was created for academic purposes under ANLYTC4.
