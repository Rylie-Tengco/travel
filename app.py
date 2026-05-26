import streamlit as st
import requests
import hashlib
import html
import re
import os
import tempfile
from urllib.parse import quote_plus
from groq import Groq

st.set_page_config(
    page_title="WanderMind · AI Travel Planner",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=DM+Sans:wght@400;500;700&display=swap');
:root {
    --bg-0: #08111a;
    --bg-1: #0d1723;
    --bg-2: #122235;
    --panel: rgba(13, 23, 35, 0.78);
    --panel-strong: rgba(18, 34, 53, 0.92);
    --line: rgba(125, 168, 194, 0.18);
    --line-strong: rgba(233, 168, 74, 0.26);
    --text: #f2e9db;
    --muted: #91a7b6;
    --soft-text: #c9d7df;
    --accent: #e9a84a;
    --accent-2: #66b4c9;
    --stat-value: #fff4df;
    --stat-label: #b7c7d2;
    --hero-bg: linear-gradient(135deg, rgba(19, 33, 50, 0.92), rgba(10, 18, 29, 0.86));
    --card-bg: rgba(13, 23, 35, 0.78);
    --card-bg-strong: rgba(18, 34, 53, 0.92);
    --card-border: var(--line);
    --panel-border: rgba(125, 168, 194, 0.18);
    --input-bg: rgba(10, 18, 29, 0.9);
    --input-border: rgba(125, 168, 194, 0.22);
    --input-focus: rgba(233, 168, 74, 0.55);
    --chat-input-bg: rgba(12, 21, 34, 0.92);
    --button-bg: linear-gradient(135deg, #f0b356, #e79f35);
    --button-bg-hover: linear-gradient(135deg, #f3bc67, #f0a93f);
    --button-text: #09111a;
    --weather-title: #e8a84a;
    --weather-temp: #fff4df;
    --weather-meta: #8aabb5;
    --weather-meta-2: #6a8898;
    --bubble-user-bg: linear-gradient(135deg, rgba(30, 58, 95, 0.95), rgba(22, 44, 72, 0.95));
    --bubble-assistant-bg: linear-gradient(135deg, rgba(21, 32, 48, 0.96), rgba(18, 34, 53, 0.96));
    --bubble-text: #dbeaf1;
    --bubble-label-user: #f0be6c;
    --bubble-label-assistant: #7fc1d4;
    --shadow: 0 24px 60px rgba(0, 0, 0, 0.35);
}
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
.stApp {
    background:
        radial-gradient(circle at top left, rgba(233, 168, 74, 0.14), transparent 24%),
        radial-gradient(circle at top right, rgba(102, 180, 201, 0.12), transparent 28%),
        linear-gradient(135deg, var(--bg-0) 0%, var(--bg-1) 45%, var(--bg-2) 100%);
    color: var(--text);
}
.stApp::before {
    content: "";
    position: fixed;
    inset: 0;
    pointer-events: none;
    background-image: linear-gradient(rgba(255,255,255,0.025) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.025) 1px, transparent 1px);
    background-size: 36px 36px;
    mask-image: linear-gradient(to bottom, rgba(0,0,0,0.35), transparent 85%);
    opacity: 0.35;
}
#MainMenu, footer, header { visibility: hidden; }
[data-testid="collapsedControl"] { display: none !important; }
section[data-testid="stSidebar"] { display: none !important; }
.app-shell {
    max-width: 1440px;
    margin: 0 auto;
    padding: 1.1rem 1rem 1.4rem;
}
.hero-card, .section-card, .message-card, .weather-card, .tip-box, .quick-stat {
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
    box-shadow: var(--shadow);
}
.hero-card {
    position: relative;
    overflow: hidden;
    background: var(--hero-bg);
    border: 1px solid var(--card-border);
    border-radius: 22px;
    padding: 1.15rem 1.2rem;
    margin-bottom: 0.95rem;
    animation: fadeUp 420ms ease both;
}
.hero-card::after {
    content: "";
    position: absolute;
    inset: -1px;
    background: linear-gradient(135deg, rgba(233,168,74,0.16), transparent 32%, rgba(102,180,201,0.10));
    pointer-events: none;
}
.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: 2.45rem;
    line-height: 1;
    font-weight: 700;
    letter-spacing: 0.01em;
    background: linear-gradient(90deg, #ffd89b, #e9a84a 55%, #fff0c9);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.25rem;
}
.hero-sub {
    color: var(--muted);
    font-size: 0.8rem;
    font-weight: 500;
    letter-spacing: 0.16em;
    text-transform: uppercase;
}
.hero-copy {
    color: var(--soft-text);
    font-size: 0.94rem;
    line-height: 1.65;
    max-width: 48ch;
    margin-top: 0.8rem;
}
.section-card {
    background: var(--card-bg);
    border: 1px solid var(--card-border);
    border-radius: 18px;
    padding: 0.95rem 0.95rem 1rem;
    margin-bottom: 0.8rem;
    animation: fadeUp 520ms ease both;
}
.section-label, .panel-label {
    font-size: 0.69rem;
    text-transform: uppercase;
    letter-spacing: 0.14em;
    color: var(--muted);
    margin-top: 1.05rem;
    margin-bottom: 0.7rem;
    font-weight: 700;
}
.quick-stat {
    background: var(--card-bg-strong);
    border: 1px solid var(--panel-border);
    border-radius: 16px;
    padding: 0.95rem 0.95rem;
    min-height: 84px;
    transition: transform 180ms ease, border-color 180ms ease, background 180ms ease;
}
.quick-stat:hover, .message-card:hover, .weather-card:hover, .tip-box:hover {
    transform: translateY(-1px);
    border-color: rgba(233, 168, 74, 0.24);
}
.quick-stat-label { color: var(--stat-label); font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.12em; }
.quick-stat-value { color: var(--stat-value); font-size: 0.96rem; font-weight: 700; margin-top: 0.3rem; }
.message-card {
    border-radius: 18px;
    padding: 0.92rem 1rem;
    margin: 0.7rem 0;
    border: 1px solid var(--card-border);
    transition: transform 180ms ease, border-color 180ms ease, box-shadow 180ms ease;
    animation: fadeUp 350ms ease both;
}
.chat-user {
    background: var(--bubble-user-bg);
    border-left: 3px solid #e9a84a;
    color: var(--text);
}
.chat-assistant {
    background: var(--bubble-assistant-bg);
    border-left: 3px solid #66b4c9;
    color: var(--bubble-text);
}
.chat-label {
    font-size: 0.68rem;
    text-transform: uppercase;
    letter-spacing: 0.13em;
    margin-bottom: 0.35rem;
    font-weight: 700;
}
.user-label { color: var(--bubble-label-user); }
.assistant-label { color: var(--bubble-label-assistant); }
.weather-card {
    background: var(--card-bg-strong);
    border: 1px solid rgba(233, 168, 74, 0.22);
    border-radius: 16px;
    padding: 0.9rem 1rem;
    margin-top: 0.5rem;
    transition: transform 180ms ease, border-color 180ms ease;
}
.tip-box {
    background: var(--card-bg-strong);
    border: 1px solid rgba(102, 180, 201, 0.18);
    border-radius: 16px;
    padding: 0.9rem 1rem;
    font-size: 0.83rem;
    color: var(--soft-text);
    margin-top: 0.7rem;
    line-height: 1.75;
}
.stTextInput > div > div > input,
.stSelectbox > div > div,
.stNumberInput > div > div > input,
.stTextArea textarea {
    background: var(--input-bg) !important;
    color: var(--text) !important;
    border: 1px solid var(--input-border) !important;
    border-radius: 12px !important;
    transition: border-color 180ms ease, box-shadow 180ms ease, transform 180ms ease !important;
}
.stSelectbox,
.stNumberInput,
.stTextInput,
.stCheckbox,
.stAudioInput,
.stToggle {
    margin-bottom: 0.9rem !important;
}
.stTextInput > div > div > input:focus,
.stSelectbox > div > div:focus-within,
.stNumberInput > div > div > input:focus,
.stTextArea textarea:focus {
    border-color: var(--input-focus) !important;
    box-shadow: 0 0 0 3px rgba(233, 168, 74, 0.12) !important;
}
.stButton > button {
    background: var(--button-bg) !important;
    color: var(--button-text) !important;
    border: none !important;
    border-radius: 12px !important;
    font-weight: 700 !important;
    transition: transform 180ms ease, filter 180ms ease, box-shadow 180ms ease !important;
    box-shadow: 0 10px 24px rgba(233, 168, 74, 0.18);
}
.stButton > button:hover {
    transform: translateY(-1px);
    filter: brightness(1.03);
}
.stChatInput {
    background: var(--chat-input-bg) !important;
    border: 1px solid var(--input-border) !important;
    border-radius: 16px !important;
    box-shadow: var(--shadow) !important;
}
.stDivider {
    margin: 1rem 0 !important;
}
.stChatInput textarea {
    background: transparent !important;
    color: var(--text) !important;
}
.stTextInput label, .stSelectbox label, .stNumberInput label, .stTextArea label,
.stCheckbox label, .stAudioInput label, .stToggle label, .stChatInput label {
    color: var(--text) !important;
}
.stTextInput input::placeholder,
.stNumberInput input::placeholder,
.stTextArea textarea::placeholder,
.stChatInput textarea::placeholder {
    color: var(--muted) !important;
    opacity: 1 !important;
}
.stSelectbox [data-baseweb="select"] > div,
.stSelectbox [data-baseweb="base-input"],
.stNumberInput [data-baseweb="input"] > div,
.stTextInput [data-baseweb="input"] > div,
.stTextArea [data-baseweb="textarea"] > div {
    background: var(--input-bg) !important;
    color: var(--text) !important;
}
.stImage img {
    border-radius: 14px;
}
@keyframes fadeUp {
    from { opacity: 0; transform: translateY(8px); }
    to { opacity: 1; transform: translateY(0); }
}
@media (max-width: 900px) {
    .app-shell { padding: 0.6rem 0.6rem 1rem; }
    .hero-title { font-size: 2rem; }
}
</style>
""", unsafe_allow_html=True)

for key, default in [("messages", []), ("api_key_set", False), ("weather_api_key_set", False), ("trip_date_text", ""), ("last_voice_audio_hash", ""), ("last_voice_transcript", ""), ("voice_preview_ready", False), ("voice_preview_text", ""), ("voice_preview_cleared", False), ("ignore_hash_once", ""), ("theme_mode", "dark")]:
    if key not in st.session_state:
        st.session_state[key] = default


def load_api_key(secret_keys, env_keys):
    for key_name in secret_keys:
        try:
            value = st.secrets.get(key_name, "")
        except Exception:
            value = ""
        if value:
            return str(value).strip()

    for key_name in env_keys:
        value = os.getenv(key_name, "").strip()
        if value:
            return value

    return ""

def get_theme_override_css(theme_mode):
    if theme_mode != "light":
        return ""

    return """
<style>
:root {
    --bg-0: #f6f8fb;
    --bg-1: #eef3f8;
    --bg-2: #e6edf5;
    --panel: rgba(255, 255, 255, 0.80);
    --panel-strong: rgba(255, 255, 255, 0.94);
    --line: rgba(52, 82, 108, 0.14);
    --line-strong: rgba(211, 140, 34, 0.24);
    --text: #122130;
    --muted: #5f7284;
    --soft-text: #31475b;
    --accent: #d38c22;
    --accent-2: #347b8f;
    --stat-value: #182838;
    --stat-label: #587085;
    --hero-bg: linear-gradient(135deg, rgba(255, 255, 255, 0.93), rgba(241, 246, 250, 0.92));
    --card-bg: rgba(255, 255, 255, 0.82);
    --card-bg-strong: rgba(255, 255, 255, 0.92);
    --card-border: rgba(52, 82, 108, 0.14);
    --panel-border: rgba(52, 82, 108, 0.14);
    --input-bg: rgba(255, 255, 255, 0.92);
    --input-border: rgba(52, 82, 108, 0.18);
    --input-focus: rgba(211, 140, 34, 0.55);
    --chat-input-bg: rgba(255, 255, 255, 0.92);
    --button-bg: linear-gradient(135deg, #e6ab42, #d38c22);
    --button-bg-hover: linear-gradient(135deg, #edbd64, #de992f);
    --button-text: #111b26;
    --weather-title: #bb7812;
    --weather-temp: #182838;
    --weather-meta: #547082;
    --weather-meta-2: #6a8898;
    --bubble-user-bg: linear-gradient(135deg, rgba(242, 248, 252, 0.98), rgba(233, 242, 249, 0.96));
    --bubble-assistant-bg: linear-gradient(135deg, rgba(251, 252, 253, 0.98), rgba(243, 247, 250, 0.96));
    --bubble-text: #203241;
    --bubble-label-user: #bb7812;
    --bubble-label-assistant: #347b8f;
    --shadow: 0 18px 38px rgba(34, 52, 72, 0.10);
}
.stApp {
    background:
        radial-gradient(circle at top left, rgba(211, 140, 34, 0.12), transparent 24%),
        radial-gradient(circle at top right, rgba(52, 123, 143, 0.10), transparent 28%),
        linear-gradient(135deg, var(--bg-0) 0%, var(--bg-1) 45%, var(--bg-2) 100%);
    color: var(--text);
}
.stApp::before {
    background-image: linear-gradient(rgba(18,33,48,0.04) 1px, transparent 1px), linear-gradient(90deg, rgba(18,33,48,0.04) 1px, transparent 1px);
    mask-image: linear-gradient(to bottom, rgba(0,0,0,0.16), transparent 85%);
    opacity: 0.45;
}
.hero-card::after {
    background: linear-gradient(135deg, rgba(211,140,34,0.14), transparent 32%, rgba(52,123,143,0.08));
}
.hero-title {
    background: linear-gradient(90deg, #b9750c, #d38c22 55%, #efb24d);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.hero-copy, .tip-box, .quick-stat-label, .section-label, .panel-label, .hero-sub {
    color: var(--muted) !important;
}
.quick-stat, .weather-card, .tip-box, .section-card, .message-card, .hero-card {
    background: var(--card-bg) !important;
    border-color: var(--card-border) !important;
}
.chat-user {
    background: var(--bubble-user-bg) !important;
    border-left-color: #d38c22 !important;
    color: var(--text) !important;
}
.chat-assistant {
    background: var(--bubble-assistant-bg) !important;
    border-left-color: #347b8f !important;
    color: var(--bubble-text) !important;
}
.quick-stat-label { color: var(--stat-label) !important; }
.quick-stat-value { color: var(--stat-value) !important; }
.user-label { color: var(--bubble-label-user) !important; }
.assistant-label { color: var(--bubble-label-assistant) !important; }
.stTextInput > div > div > input,
.stSelectbox > div > div,
.stNumberInput > div > div > input,
.stTextArea textarea,
.stChatInput,
.stChatInput textarea {
    background: var(--input-bg) !important;
    color: var(--text) !important;
    border-color: var(--input-border) !important;
}
.stTextInput > div > div > input:focus,
.stSelectbox > div > div:focus-within,
.stNumberInput > div > div > input:focus,
.stTextArea textarea:focus {
    border-color: var(--input-focus) !important;
    box-shadow: 0 0 0 3px rgba(211, 140, 34, 0.12) !important;
}
.stButton > button {
    background: var(--button-bg) !important;
    color: var(--button-text) !important;
    box-shadow: 0 10px 24px rgba(211, 140, 34, 0.16) !important;
}
.stChatInput {
    background: var(--chat-input-bg) !important;
}
.stTextInput label, .stSelectbox label, .stNumberInput label, .stTextArea label,
.stCheckbox label, .stAudioInput label, .stToggle label, .stChatInput label {
    color: var(--text) !important;
}
.stTextInput input::placeholder,
.stNumberInput input::placeholder,
.stTextArea textarea::placeholder,
.stChatInput textarea::placeholder {
    color: var(--muted) !important;
    opacity: 1 !important;
}
</style>
"""

@st.cache_data(show_spinner=False)
def get_weather(city, api_key):
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        r = requests.get(url, timeout=8)
        if r.status_code == 200:
            d = r.json()
            condition = d["weather"][0]["main"].lower()
            emoji_map = {"clear":"☀️","clouds":"☁️","rain":"🌧️","drizzle":"🌦️","thunderstorm":"⛈️","snow":"❄️","mist":"🌫️","fog":"🌫️","haze":"🌫️"}
            return {"city": d["name"], "temp": round(d["main"]["temp"]), "description": d["weather"][0]["description"], "humidity": d["main"]["humidity"], "wind": d["wind"]["speed"], "emoji": emoji_map.get(condition, "🌡️")}
    except Exception:
        pass
    return None

SYSTEM_PROMPT = """You are WanderMind, a friendly AI Travel Planner. Be conversational and natural.

IMPORTANT RULES:
- If the user says hello, hi, or just greets you — greet them back warmly and ask where they want to go. Keep it SHORT (2-3 lines max).
- Only create itineraries or long travel plans when the user EXPLICITLY asks for one (e.g. "plan a trip", "make an itinerary", "plan my travel").
- If the user asks for a trip plan or schedule and you do not know when they want to travel yet, ask: "When would you like to take the trip?" before creating the schedule.
- For simple questions, give short focused answers.
- Match the length of your response to what was asked. Short question = short answer.
- Use emojis naturally but don't overdo it.
- When you do create itineraries, organize by day with morning/afternoon/evening activities.
- When scheduling a trip, include the start date or travel window in the plan and make the schedule line up with it.
- Always tailor to the user's travel style, budget, and number of days set in their preferences.
- If the budget includes a numeric amount, treat it as a real spending limit. Use it to filter recommendations, estimate costs, and note whether the amount is a total trip budget or a per-day budget."""

def wants_trip_schedule(user_message):
    lowered = user_message.lower()
    return any(keyword in lowered for keyword in ["plan", "schedule", "itinerary", "trip", "travel", "vacation"])


def is_recommendation_response(user_text, assistant_text):
    user_lowered = user_text.lower()
    assistant_lowered = assistant_text.lower()
    user_keywords = [
        "recommend",
        "suggest",
        "itinerary",
        "plan",
        "trip",
        "vacation",
        "places",
        "visit",
    ]
    assistant_keywords = [
        "itinerary",
        "day 1",
        "day 2",
        "recommend",
        "must-visit",
        "places to visit",
        "travel plan",
        "morning",
        "afternoon",
        "evening",
    ]
    return any(keyword in user_lowered for keyword in user_keywords) or any(keyword in assistant_lowered for keyword in assistant_keywords)


def extract_destination(user_message, assistant_message):
    # Prefer destination hints from the latest user request.
    pattern = r"\b(?:in|to|visit|around)\s+([A-Za-z][A-Za-z\s\-]{1,40})"
    user_matches = re.findall(pattern, user_message, flags=re.IGNORECASE)
    for match in user_matches:
        cleaned = " ".join(match.strip().split())
        if len(cleaned) > 2:
            return cleaned

    # Fallback: use capitalized phrases from the AI response.
    place_like = re.findall(r"\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+){0,2})\b", assistant_message)
    for candidate in place_like:
        if candidate.lower() not in {"day", "morning", "afternoon", "evening", "budget", "luxury"}:
            return candidate

    return "travel destination"


def extract_place_candidates(text):
    stop_words = {
        "Day", "Morning", "Afternoon", "Evening", "Budget", "Luxury", "Travel", "Trip",
        "Plan", "Itinerary", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday",
        "Considering", "Both", "Which", "You", "Your", "I", "We", "They", "This", "That", "These", "Those"
    }
    candidates = re.findall(r"\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+){0,2})\b", text)
    cleaned = []
    for candidate in candidates:
        if candidate in stop_words:
            continue
        if len(candidate) < 3:
            continue
        if candidate not in cleaned:
            cleaned.append(candidate)
    return cleaned


@st.cache_data(show_spinner=False)
def fetch_place_image(place_name):
    def normalize_tokens(text):
        return [t for t in re.findall(r"[a-z]+", text.lower()) if len(t) > 2]

    def has_location_signal(description, extract):
        location_keywords = {
            "country", "city", "capital", "island", "state", "province", "town",
            "village", "region", "municipality", "district", "archipelago", "national park",
            "destination", "prefecture", "county", "territory", "resort"
        }
        blob = f"{description} {extract}".lower()
        return any(keyword in blob for keyword in location_keywords)

    def score_search_result(requested_place, title, snippet):
        requested = set(normalize_tokens(requested_place))
        title_tokens = set(normalize_tokens(title))
        snippet_tokens = set(normalize_tokens(snippet))
        overlap = len(requested.intersection(title_tokens.union(snippet_tokens)))
        score = overlap * 2
        if requested_place.lower() in title.lower():
            score += 3
        snippet_lower = snippet.lower()
        title_lower = title.lower()
        if "disambiguation" in title_lower or "disambiguation" in snippet_lower:
            score -= 4
        if any(k in snippet_lower for k in ["city", "country", "island", "region", "capital", "municipality"]):
            score += 2
        return score

    def search_wikipedia_title(query, requested_place):
        search_url = "https://en.wikipedia.org/w/api.php"
        params = {
            "action": "query",
            "list": "search",
            "srsearch": query,
            "format": "json",
            "utf8": 1,
            "srlimit": 5,
        }
        try:
            response = requests.get(search_url, params=params, timeout=6)
            if response.status_code != 200:
                return None
            data = response.json()
            results = data.get("query", {}).get("search", [])
            if not results:
                return None

            best_title = None
            best_score = -999
            for item in results:
                title = item.get("title", "")
                snippet = item.get("snippet", "")
                score = score_search_result(requested_place, title, snippet)
                if score > best_score:
                    best_score = score
                    best_title = title
            if best_score < 1:
                return None
            return best_title
        except Exception:
            return None

    @st.cache_data(show_spinner=False)
    def fetch_summary_image(title, requested_place):
        summary_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{quote_plus(title.replace(' ', '_'))}"
        try:
            response = requests.get(summary_url, timeout=6)
            if response.status_code != 200:
                return None
            data = response.json()

            description = data.get("description", "")
            extract = data.get("extract", "")
            if not has_location_signal(description, extract):
                return None

            requested_tokens = set(normalize_tokens(requested_place))
            compare_blob = f"{data.get('title', '')} {description} {extract}".lower()
            compare_tokens = set(normalize_tokens(compare_blob))
            if requested_tokens and len(requested_tokens.intersection(compare_tokens)) == 0:
                return None

            thumb = data.get("thumbnail", {})
            if thumb.get("source"):
                return thumb["source"]

            original = data.get("originalimage", {})
            if original.get("source"):
                return original["source"]
            return None
        except Exception:
            return None

    search_queries = [place_name]
    # Add a stronger query for common destination aliases.
    if " " in place_name:
        search_queries.append(f"{place_name} travel destination")

    seen = set()
    for query in search_queries:
        if query in seen:
            continue
        seen.add(query)
        title = search_wikipedia_title(query, place_name)
        if not title:
            continue
        image_url = fetch_summary_image(title, place_name)
        if image_url:
            return image_url
    return None


def build_response_images(user_message, assistant_message, limit=3):
    if not is_recommendation_response(user_message, assistant_message):
        return []

    destinations = []
    primary_destination = extract_destination(user_message, assistant_message)
    if primary_destination:
        destinations.append(primary_destination)

    for place in extract_place_candidates(assistant_message):
        if place not in destinations:
            destinations.append(place)

    destinations = destinations[:limit]
    images = []
    for place in destinations:
        image_url = fetch_place_image(place)
        if image_url:
            images.append({"url": image_url, "caption": place})

    return images


@st.cache_data(show_spinner=False)
def build_response_images_cached(user_message, assistant_message, limit=3):
    return tuple((item["url"], item["caption"]) for item in build_response_images(user_message, assistant_message, limit))


def chat_with_agent(user_message, trip_style, trip_days, budget, trip_date_text):
    client = Groq(api_key=st.session_state.groq_key)
    schedule_context = trip_date_text if trip_date_text else "Not provided yet"
    system = SYSTEM_PROMPT + f"\n\nUser's current trip preferences: Style={trip_style}, Days={trip_days}, Budget={budget}, Trip timing={schedule_context}"
    messages = [{"role": "system", "content": system}]
    for m in st.session_state.messages:
        messages.append({"role": m["role"], "content": m["content"]})
    messages.append({"role": "user", "content": user_message})
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        max_tokens=1200,
        temperature=0.7,
    )
    return response.choices[0].message.content


def audio_bytes_from_input(audio_input):
    if audio_input is None:
        return None
    if hasattr(audio_input, "getvalue"):
        return audio_input.getvalue()
    if hasattr(audio_input, "read"):
        return audio_input.read()
    try:
        return bytes(audio_input)
    except Exception:
        return None


def transcribe_voice_intent(audio_input):
    audio_bytes = audio_bytes_from_input(audio_input)
    if not audio_bytes:
        return None

    suffix = ".wav"
    audio_name = getattr(audio_input, "name", "") or ""
    if "." in audio_name:
        suffix = "." + audio_name.rsplit(".", 1)[-1].lower()
    # Create a named temp file on disk and pass its path to the Groq client.
    import os
    temp_path = None
    try:
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
        try:
            tmp.write(audio_bytes)
            tmp.flush()
            temp_path = tmp.name
        finally:
            tmp.close()

        with open(temp_path, "rb") as fp:
            result = Groq(api_key=st.session_state.groq_key).audio.transcriptions.create(
                model="whisper-large-v3",
                file=fp,
                response_format="text",
            )

        if isinstance(result, str):
            return result.strip()

        transcript = getattr(result, "text", "")
        return transcript.strip() if transcript else None
    finally:
        try:
            if temp_path and os.path.exists(temp_path):
                os.remove(temp_path)
        except Exception:
            pass

left, right = st.columns([1, 2.5], gap="large")

with left:
    st.markdown("""
    <div class="hero-card">
        <div class="hero-title">WanderMind</div>
        <div class="hero-sub">✈️ AI Travel Planner Agent</div>
        <div class="hero-copy">Shape a trip with a custom budget, live weather, and recommendation cards that adapt to your pace and style.</div>
    </div>
    """, unsafe_allow_html=True)

    groq_key = load_api_key(["groq_api_key", "GROQ_API_KEY"], ["GROQ_API_KEY"])
    weather_key = load_api_key(["openweather_api_key", "OPENWEATHER_API_KEY"], ["OPENWEATHER_API_KEY"])

    if groq_key:
        st.session_state.groq_key = groq_key
        st.session_state.api_key_set = True
    if weather_key:
        st.session_state.weather_key = weather_key
        st.session_state.weather_api_key_set = True

    theme_mode_enabled = st.toggle(
        "Light mode",
        value=st.session_state.get("theme_mode", "dark") == "light",
        help="Switch between light and dark mode.",
    )
    st.session_state.theme_mode = "light" if theme_mode_enabled else "dark"
    st.markdown(get_theme_override_css(st.session_state.theme_mode), unsafe_allow_html=True)

    st.divider()

    st.markdown('<div class="section-label">🗺️ Trip Preferences</div>', unsafe_allow_html=True)
    trip_style = st.selectbox("Travel Style", ["Adventure", "Relaxation", "Cultural", "Foodie", "Family", "Romantic"])
    trip_days = st.number_input("Number of Days", min_value=1, max_value=30, value=5)
    budget_scope = st.selectbox("Budget Scope", ["Total trip budget", "Budget per day"])
    budget_currency = st.selectbox("Currency", ["USD", "EUR", "GBP", "PHP", "JPY", "AUD", "CAD", "SGD"])
    budget_amount = st.number_input("Budget Amount", min_value=1.0, value=1500.0, step=50.0)
    budget = f"{budget_currency} {budget_amount:,.0f} ({budget_scope.lower()})"

    st.markdown('<div class="section-label">📅 Trip Timing</div>', unsafe_allow_html=True)
    trip_date_text = st.text_input(
        "When would you take the trip?",
        placeholder="e.g. 2026-06-10, next July, or around Christmas",
        value=st.session_state.trip_date_text,
        label_visibility="collapsed",
    )
    if trip_date_text != st.session_state.trip_date_text:
        st.session_state.trip_date_text = trip_date_text

    st.markdown('<div class="section-label">⚡ Quick Snapshot</div>', unsafe_allow_html=True)
    stat_cols = st.columns(3)
    with stat_cols[0]:
        st.markdown(f'<div class="quick-stat"><div class="quick-stat-label">Style</div><div class="quick-stat-value">{trip_style}</div></div>', unsafe_allow_html=True)
    with stat_cols[1]:
        st.markdown(f'<div class="quick-stat"><div class="quick-stat-label">Days</div><div class="quick-stat-value">{int(trip_days)}</div></div>', unsafe_allow_html=True)
    with stat_cols[2]:
        st.markdown(f'<div class="quick-stat"><div class="quick-stat-label">Budget</div><div class="quick-stat-value">{budget_currency} {budget_amount:,.0f}</div></div>', unsafe_allow_html=True)

    st.markdown('<div class="section-label">🎙️ Voice Intent</div>', unsafe_allow_html=True)
    auto_send = st.checkbox("Auto-send on record (push-to-talk)", value=False, help="When enabled, recordings are transcribed and sent immediately.")
    voice_audio = st.audio_input("Record your travel request", label_visibility="collapsed")
    if voice_audio is not None:
        voice_bytes = audio_bytes_from_input(voice_audio)
        voice_hash = hashlib.sha256(voice_bytes or b"").hexdigest() if voice_bytes else ""
        # If we flagged this exact audio to be ignored once (right after auto-send), skip processing it on the immediate rerun
        if st.session_state.get("ignore_hash_once") and st.session_state.get("ignore_hash_once") == voice_hash:
            # consume the ignore flag and skip this run (audio widget still contains the upload)
            st.session_state.ignore_hash_once = None
            skip_processing = True
        else:
            skip_processing = False

        if not skip_processing and voice_hash and voice_hash != st.session_state.last_voice_audio_hash:
            if not st.session_state.api_key_set:
                st.warning("Set the Groq API key in Streamlit secrets or the GROQ_API_KEY environment variable before using voice input.")
            else:
                with st.spinner("Transcribing your voice... 🎙️"):
                    transcript = transcribe_voice_intent(voice_audio)
                if transcript:
                    st.session_state.last_voice_audio_hash = voice_hash
                    st.session_state.last_voice_transcript = transcript
                    st.session_state.voice_preview_ready = True
                    st.session_state.voice_preview_text = transcript
                    if auto_send:
                        # Auto-send immediately (push-to-talk behavior)
                        st.session_state.voice_preview_ready = False
                        st.session_state.messages.append({"role": "user", "content": transcript})
                        if wants_trip_schedule(transcript) and not st.session_state.trip_date_text.strip():
                            st.session_state.messages.append({
                                "role": "assistant",
                                "content": "When would you like to take the trip? Once I have the timing, I can build and schedule the itinerary for you."
                            })
                        else:
                            with st.spinner("WanderMind is thinking... 🌍"):
                                try:
                                    reply = chat_with_agent(transcript, trip_style, trip_days, budget, st.session_state.trip_date_text)
                                    assistant_message = {"role": "assistant", "content": reply}
                                    images = build_response_images(transcript, reply)
                                    if images:
                                        assistant_message["images"] = images
                                    st.session_state.messages.append(assistant_message)
                                except Exception as e:
                                    st.error(f"Error: {str(e)}")
                        # keep dedupe hash so rerun doesn't reprocess the same audio
                        # set a one-time ignore so the immediate rerun doesn't process the same upload again
                        st.session_state.ignore_hash_once = voice_hash
                        st.rerun()
                    else:
                        # Show preview for user to edit/confirm before sending
                        pass
                else:
                    st.warning("I couldn't understand that recording. Try speaking a bit more clearly.")

    # If a previous discard requested clearing the preview, remove stored text before widget instantiation
    if st.session_state.get("voice_preview_cleared"):
        st.session_state.voice_preview_text = ""
        st.session_state.voice_preview_cleared = False

    # If a transcript preview is ready, show editable preview and action buttons
    if st.session_state.get("voice_preview_ready"):
        st.markdown("**Transcript preview — edit if needed, then Send or Discard**")
        st.text_area("Transcript preview", value=st.session_state.get("voice_preview_text", ""), height=120, key="voice_preview_text")
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            if st.button("Send Transcript", key="send_transcript"):
                transcript_text = st.session_state.voice_preview_text.strip()
                if transcript_text:
                    st.session_state.voice_preview_ready = False
                    st.session_state.messages.append({"role": "user", "content": transcript_text})
                    if wants_trip_schedule(transcript_text) and not st.session_state.trip_date_text.strip():
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": "When would you like to take the trip? Once I have the timing, I can build and schedule the itinerary for you."
                        })
                    else:
                        with st.spinner("WanderMind is thinking... 🌍"):
                            try:
                                reply = chat_with_agent(transcript_text, trip_style, trip_days, budget, st.session_state.trip_date_text)
                                assistant_message = {"role": "assistant", "content": reply}
                                images = build_response_images(transcript_text, reply)
                                if images:
                                    assistant_message["images"] = images
                                st.session_state.messages.append(assistant_message)
                            except Exception as e:
                                st.error(f"Error: {str(e)}")
                    # allow another recording after sending
                    st.session_state.last_voice_audio_hash = ""
                    st.rerun()
        with col2:
            if st.button("Discard", key="discard_transcript"):
                st.session_state.voice_preview_ready = False
                st.session_state.last_voice_transcript = ""
                st.session_state.voice_preview_cleared = True
                # clear dedupe so user can immediately record again
                st.session_state.last_voice_audio_hash = ""
                st.rerun()
        with col3:
            st.write(" ")
    st.divider()

    st.markdown('<div class="section-label">🌤️ Quick Weather Check</div>', unsafe_allow_html=True)
    weather_city = st.text_input("City", placeholder="e.g. Tokyo", label_visibility="collapsed")
    if st.button("Get Weather 🌤️", use_container_width=True):
        if not weather_city:
            st.warning("Enter a city name.")
        elif not st.session_state.weather_api_key_set:
            st.warning("Set the OpenWeatherMap key in Streamlit secrets or the OPENWEATHER_API_KEY environment variable first.")
        else:
            with st.spinner("Fetching..."):
                wd = get_weather(weather_city, st.session_state.weather_key)
                if wd:
                    st.markdown(f"""<div class="weather-card">
                        <div style="font-size:1.5rem">{wd['emoji']}</div>
                        <div style="font-weight:600;color:#e8a84a">{wd['city']}</div>
                        <div style="font-size:1.3rem;font-weight:700">{wd['temp']}°C</div>
                        <div style="color:#8aabb5;font-size:0.82rem">{wd['description'].capitalize()}</div>
                        <div style="color:#6a8898;font-size:0.75rem;margin-top:4px">💧 {wd['humidity']}% &nbsp;|&nbsp; 💨 {wd['wind']} m/s</div>
                    </div>""", unsafe_allow_html=True)
                else:
                    st.error("City not found.")

    st.divider()

    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.markdown("""<div class="tip-box">💡 <b>Try asking:</b><br>
    • "Plan 5 days in Tokyo"<br>
    • "What to pack for Bali?"<br>
    • "Luxury 3-day Rome trip"<br>
    • "Is Morocco safe to visit?"<br>
    • "Visa tips for Japan"
    </div>""", unsafe_allow_html=True)

with right:
    st.markdown("<div style='height:0.2rem'></div>", unsafe_allow_html=True)

    if not st.session_state.messages:
        st.markdown("""<div class="message-card chat-assistant">
            <div class="chat-label assistant-label">🌍 WanderMind</div>
            <b>Hello, fellow explorer! ✈️</b><br><br>
            I'm WanderMind, your personal AI travel planner. I can help you:<br>
            🗺️ &nbsp;Plan detailed day-by-day itineraries<br>
            🏨 &nbsp;Find hotels & restaurants for your budget<br>
            🌤️ &nbsp;Check weather at your destination<br>
            🎒 &nbsp;Get packing lists & travel tips<br>
            📋 &nbsp;Understand visa & safety requirements<br><br>
            <b>Where and when would you like to take the trip? 🌏</b>
        </div>""", unsafe_allow_html=True)

    for msg in st.session_state.messages:
        if msg["role"] == "user":
            safe_content = html.escape(msg["content"]).replace("\n", "<br>")
            st.markdown(f"""<div class="message-card chat-user"><div class="chat-label user-label">👤 You</div>{safe_content}</div>""", unsafe_allow_html=True)
        else:
            content = html.escape(msg["content"]).replace("\n", "<br>")
            st.markdown(f"""<div class="message-card chat-assistant"><div class="chat-label assistant-label">🌍 WanderMind</div>{content}</div>""", unsafe_allow_html=True)
            if msg.get("images"):
                image_cols = st.columns(min(len(msg["images"]), 3))
                for idx, image_data in enumerate(msg["images"]):
                    with image_cols[idx]:
                        if isinstance(image_data, str):
                            st.image(image_data, use_container_width=True)
                        else:
                            st.image(image_data["url"], caption=image_data.get("caption"), use_container_width=True)

    # ── KEY FIX: use st.chat_input — only fires when user presses Enter/Send ──
    user_input = st.chat_input("Ask me anything... e.g. Plan a 5-day trip to Tokyo")

    if user_input:
        if not st.session_state.api_key_set:
            st.error("⚠️ Set the Groq API key in Streamlit secrets or the GROQ_API_KEY environment variable first.")
        elif wants_trip_schedule(user_input) and not st.session_state.trip_date_text.strip():
            st.session_state.messages.append({"role": "user", "content": user_input})
            st.session_state.messages.append({
                "role": "assistant",
                "content": "When would you like to take the trip? Once I have the timing, I can build and schedule the itinerary for you."
            })
            st.rerun()
        else:
            st.session_state.messages.append({"role": "user", "content": user_input})
            with st.spinner("WanderMind is thinking... 🌍"):
                try:
                    reply = chat_with_agent(user_input, trip_style, trip_days, budget, st.session_state.trip_date_text)
                    assistant_message = {"role": "assistant", "content": reply}
                    images = [{"url": url, "caption": caption} for url, caption in build_response_images_cached(user_input, reply)]
                    if images:
                        assistant_message["images"] = images
                    st.session_state.messages.append(assistant_message)
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {str(e)}")
