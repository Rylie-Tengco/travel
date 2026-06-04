import streamlit as st
import streamlit.components.v1 as components
import requests
import base64
import hashlib
import html
import json
import mimetypes
import re
import os
import tempfile
from datetime import date, datetime, timedelta
from io import BytesIO
from pathlib import Path
from urllib.parse import quote_plus
from groq import Groq

try:
    from google.auth.exceptions import RefreshError
    from google.auth.transport.requests import Request as GoogleAuthRequest
    from google.oauth2.credentials import Credentials as GoogleCredentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build as build_google_service
    from googleapiclient.errors import HttpError
except Exception:
    RefreshError = None
    GoogleAuthRequest = None
    GoogleCredentials = None
    InstalledAppFlow = None
    build_google_service = None
    HttpError = None

st.set_page_config(
    page_title="I-Travel · AI Travel Planner",
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
    --muted: #b4c5d1;
    --soft-text: #d3e0e8;
    --accent: #e9a84a;
    --accent-2: #66b4c9;
    --accent-soft: rgba(233, 168, 74, 0.14);
    --accent-strong: rgba(233, 168, 74, 0.32);
    --accent-2-soft: rgba(102, 180, 201, 0.16);
    --stat-value: #fff4df;
    --stat-label: #b7c7d2;
    --hero-title: linear-gradient(90deg, #ffd89b, #e9a84a 55%, #fff0c9);
    --hero-bg: linear-gradient(135deg, rgba(19, 33, 50, 0.92), rgba(10, 18, 29, 0.86));
    --hero-glow: linear-gradient(135deg, rgba(233,168,74,0.16), transparent 32%, rgba(102,180,201,0.10));
    --card-bg: rgba(13, 23, 35, 0.78);
    --card-bg-strong: rgba(18, 34, 53, 0.92);
    --card-border: var(--line);
    --panel-border: rgba(125, 168, 194, 0.18);
    --input-bg: rgba(10, 18, 29, 0.9);
    --input-border: rgba(125, 168, 194, 0.22);
    --input-focus: rgba(233, 168, 74, 0.55);
    --input-focus-ring: rgba(233, 168, 74, 0.12);
    --placeholder: #b4c5d1;
    --chat-bar-bg: rgba(11, 18, 29, 0.96);
    --chat-input-bg: rgba(12, 21, 34, 0.92);
    --chat-send-bg: rgba(255, 255, 255, 0.08);
    --chat-send-text: #f2e9db;
    --checkbox-bg: rgba(10, 18, 29, 0.92);
    --checkbox-check: #09111a;
    --audio-bg: rgba(12, 21, 34, 0.92);
    --audio-control-bg: rgba(255, 255, 255, 0.08);
    --audio-wave-bg: rgba(18, 34, 53, 0.88);
    --audio-wave-line: #e9a84a;
    --audio-text: #d3e0e8;
    --audio-muted: #b4c5d1;
    --audio-timer-bg: rgba(10, 18, 29, 0.72);
    --button-bg: linear-gradient(135deg, #f0b356, #e79f35);
    --button-bg-hover: linear-gradient(135deg, #f3bc67, #f0a93f);
    --button-text: #09111a;
    --weather-title: #e8a84a;
    --weather-temp: #fff4df;
    --weather-meta: #b0c3cf;
    --weather-meta-2: #a7bac7;
    --bubble-user-bg: linear-gradient(135deg, rgba(30, 58, 95, 0.95), rgba(22, 44, 72, 0.95));
    --bubble-assistant-bg: linear-gradient(135deg, rgba(21, 32, 48, 0.96), rgba(18, 34, 53, 0.96));
    --bubble-text: #dbeaf1;
    --bubble-label-user: #f0be6c;
    --bubble-label-assistant: #7fc1d4;
    --bubble-user-border: var(--accent);
    --bubble-assistant-border: var(--accent-2);
    --app-grid: rgba(255, 255, 255, 0.025);
    --app-grid-mask: rgba(0, 0, 0, 0.35);
    --app-accent-glow: rgba(233, 168, 74, 0.14);
    --app-accent-2-glow: rgba(102, 180, 201, 0.12);
    --shadow: 0 24px 60px rgba(0, 0, 0, 0.35);
    --button-shadow: rgba(233, 168, 74, 0.18);
}
[data-theme-mode="light"] {
    --bg-0: #f6f8fb;
    --bg-1: #eef3f8;
    --bg-2: #e6edf5;
    --panel: rgba(255, 255, 255, 0.80);
    --panel-strong: rgba(255, 255, 255, 0.94);
    --line: rgba(52, 82, 108, 0.14);
    --line-strong: rgba(211, 140, 34, 0.24);
    --text: #122130;
    --muted: #4e6375;
    --soft-text: #263c50;
    --accent: #a76507;
    --accent-2: #2b7184;
    --accent-soft: rgba(211, 140, 34, 0.12);
    --accent-strong: rgba(211, 140, 34, 0.26);
    --accent-2-soft: rgba(52, 123, 143, 0.12);
    --stat-value: #182838;
    --stat-label: #4e6375;
    --hero-title: linear-gradient(90deg, #875204, #a76507 55%, #bd7410);
    --hero-bg: linear-gradient(135deg, rgba(255, 255, 255, 0.93), rgba(241, 246, 250, 0.92));
    --hero-glow: linear-gradient(135deg, rgba(211,140,34,0.14), transparent 32%, rgba(52,123,143,0.08));
    --card-bg: rgba(255, 255, 255, 0.82);
    --card-bg-strong: rgba(255, 255, 255, 0.92);
    --card-border: rgba(52, 82, 108, 0.14);
    --panel-border: rgba(52, 82, 108, 0.14);
    --input-bg: rgba(255, 255, 255, 0.94);
    --input-border: rgba(52, 82, 108, 0.18);
    --input-focus: rgba(211, 140, 34, 0.55);
    --input-focus-ring: rgba(211, 140, 34, 0.13);
    --placeholder: #5b7082;
    --chat-bar-bg: rgba(255, 255, 255, 0.88);
    --chat-input-bg: rgba(255, 255, 255, 0.94);
    --chat-send-bg: #eef3f8;
    --chat-send-text: #31475b;
    --checkbox-bg: rgba(255, 255, 255, 0.96);
    --checkbox-check: #ffffff;
    --audio-bg: rgba(255, 255, 255, 0.92);
    --audio-control-bg: rgba(238, 243, 248, 0.98);
    --audio-wave-bg: rgba(255, 255, 255, 0.84);
    --audio-wave-line: #a76507;
    --audio-text: #263c50;
    --audio-muted: #4e6375;
    --audio-timer-bg: rgba(238, 243, 248, 0.98);
    --button-bg: linear-gradient(135deg, #d39224, #a76507);
    --button-bg-hover: linear-gradient(135deg, #df9f31, #b8710c);
    --button-text: #ffffff;
    --weather-title: #875204;
    --weather-temp: #182838;
    --weather-meta: #4b6476;
    --weather-meta-2: #526b7d;
    --bubble-user-bg: linear-gradient(135deg, rgba(242, 248, 252, 0.98), rgba(233, 242, 249, 0.96));
    --bubble-assistant-bg: linear-gradient(135deg, rgba(251, 252, 253, 0.98), rgba(243, 247, 250, 0.96));
    --bubble-text: #203241;
    --bubble-label-user: #875204;
    --bubble-label-assistant: #2b7184;
    --bubble-user-border: var(--accent);
    --bubble-assistant-border: var(--accent-2);
    --app-grid: rgba(18, 33, 48, 0.04);
    --app-grid-mask: rgba(0, 0, 0, 0.16);
    --app-accent-glow: rgba(211, 140, 34, 0.12);
    --app-accent-2-glow: rgba(52, 123, 143, 0.10);
    --shadow: 0 18px 38px rgba(34, 52, 72, 0.10);
    --button-shadow: rgba(211, 140, 34, 0.16);
}
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
.stApp {
    background:
        radial-gradient(circle at top left, var(--app-accent-glow), transparent 24%),
        radial-gradient(circle at top right, var(--app-accent-2-glow), transparent 28%),
        linear-gradient(135deg, var(--bg-0) 0%, var(--bg-1) 45%, var(--bg-2) 100%);
    color: var(--text);
}
.stApp::before {
    content: "";
    position: fixed;
    inset: 0;
    pointer-events: none;
    background-image: linear-gradient(var(--app-grid) 1px, transparent 1px), linear-gradient(90deg, var(--app-grid) 1px, transparent 1px);
    background-size: 36px 36px;
    mask-image: linear-gradient(to bottom, var(--app-grid-mask), transparent 85%);
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
    background: var(--hero-glow);
    pointer-events: none;
}
.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: 2.45rem;
    line-height: 1;
    font-weight: 700;
    letter-spacing: 0.01em;
    background: var(--hero-title);
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
    border-color: var(--accent-strong);
}
.quick-snapshot-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: 0.75rem;
    margin-top: 0.2rem;
}
.quick-stat-label { color: var(--stat-label); font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.12em; }
.quick-stat-value {
    color: var(--stat-value);
    font-size: 0.98rem;
    font-weight: 700;
    margin-top: 0.35rem;
    line-height: 1.25;
    word-break: break-word;
}
.message-card {
    border-radius: 18px;
    padding: 0.92rem 1rem;
    margin: 0;
    border: 1px solid var(--card-border);
    transition: transform 180ms ease, border-color 180ms ease, box-shadow 180ms ease;
    animation: fadeUp 350ms ease both;
}
.chat-user {
    background: var(--bubble-user-bg);
    border-left: 3px solid var(--bubble-user-border);
    color: var(--text);
}
.chat-assistant {
    background: var(--bubble-assistant-bg);
    border-left: 3px solid var(--bubble-assistant-border);
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
.calendar-confirmation {
    display: flex;
    flex-direction: column;
    gap: 0.7rem;
}
.calendar-confirmation-text {
    font-size: 0.95rem;
    line-height: 1.5;
}
.calendar-action {
    display: inline-flex;
    align-items: center;
    gap: 0.45rem;
    width: fit-content;
    max-width: 100%;
    padding: 0.55rem 0.72rem;
    border-radius: 10px;
    background: var(--accent-soft);
    border: 1px solid var(--accent-strong);
    color: var(--text) !important;
    font-size: 0.84rem;
    font-weight: 700;
    text-decoration: none !important;
    transition: transform 160ms ease, background 160ms ease, border-color 160ms ease;
}
.calendar-action:hover {
    transform: translateY(-1px);
    background: var(--accent-2-soft);
    border-color: var(--bubble-assistant-border);
}
.weather-card {
    background: var(--card-bg-strong);
    border: 1px solid var(--accent-strong);
    border-radius: 16px;
    padding: 0.9rem 1rem;
    margin-top: 0.5rem;
    transition: transform 180ms ease, border-color 180ms ease;
}
.weather-emoji { font-size: 1.5rem; }
.weather-city { color: var(--weather-title); font-weight: 700; }
.weather-temp { color: var(--weather-temp); font-size: 1.3rem; font-weight: 700; }
.weather-desc { color: var(--weather-meta); font-size: 0.82rem; }
.weather-meta { color: var(--weather-meta-2); font-size: 0.75rem; margin-top: 4px; }
.tip-box {
    background: var(--card-bg-strong);
    border: 1px solid var(--accent-2-soft);
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
.stTextArea textarea,
[data-testid="stTextInput"] input,
[data-testid="stNumberInput"] input,
[data-testid="stNumberInput"] button,
[data-testid="stTextArea"] textarea,
[data-baseweb="select"],
[data-baseweb="select"] > div,
[data-baseweb="base-input"],
[data-baseweb="input"],
[data-baseweb="input"] > div,
[data-baseweb="textarea"],
[data-baseweb="textarea"] > div {
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
.stTextArea textarea:focus,
[data-testid="stTextInput"] input:focus,
[data-testid="stNumberInput"] input:focus,
[data-testid="stTextArea"] textarea:focus,
[data-baseweb="select"]:focus-within,
[data-baseweb="input"]:focus-within,
[data-baseweb="textarea"]:focus-within {
    border-color: var(--input-focus) !important;
    box-shadow: 0 0 0 3px var(--input-focus-ring) !important;
}
[data-testid="stNumberInput"] [data-baseweb="input"],
[data-testid="stNumberInput"] [data-baseweb="input"] > div,
[data-testid="stNumberInput"] input,
[data-testid="stNumberInput"] button {
    outline: none !important;
    border-color: var(--input-border) !important;
}
[data-testid="stNumberInput"] [data-baseweb="input"],
[data-testid="stNumberInput"] [data-baseweb="input"] > div {
    overflow: hidden !important;
}
[data-testid="stNumberInput"] [data-baseweb="input"]:focus-within,
[data-testid="stNumberInput"] [data-baseweb="input"]:focus-within > div {
    border-color: var(--input-focus) !important;
    box-shadow: 0 0 0 3px var(--input-focus-ring) !important;
}
[data-testid="stNumberInput"] input:focus,
[data-testid="stNumberInput"] input:focus-visible,
[data-testid="stNumberInput"] button:focus,
[data-testid="stNumberInput"] button:focus-visible {
    outline: none !important;
    box-shadow: none !important;
}
.stButton > button,
[data-testid="stButton"] button {
    background: var(--button-bg) !important;
    color: var(--button-text) !important;
    border: none !important;
    border-radius: 12px !important;
    font-weight: 700 !important;
    transition: transform 180ms ease, filter 180ms ease, box-shadow 180ms ease !important;
    box-shadow: 0 10px 24px var(--button-shadow);
}
.stButton > button:hover,
[data-testid="stButton"] button:hover {
    transform: translateY(-1px);
    filter: brightness(1.03);
}
[data-testid="stCheckbox"],
[data-testid="stCheckbox"] label,
[data-testid="stCheckbox"] p,
[data-testid="stCheckbox"] span,
[data-testid="stCheckbox"] [data-testid="stMarkdownContainer"],
div[data-testid="stToggle"] label,
div[data-testid="stToggle"] p,
div[data-testid="stToggle"] span,
div[data-testid="stToggle"] [data-testid="stMarkdownContainer"] {
    color: var(--text) !important;
    background: transparent !important;
    box-shadow: none !important;
}
.st-key-voice_auto_send [data-testid="stCheckbox"] [data-baseweb="checkbox"] {
    display: inline-flex !important;
    align-items: center !important;
}
.st-key-voice_auto_send [data-testid="stCheckbox"] [data-baseweb="checkbox"] > div:first-child,
.st-key-voice_auto_send [data-testid="stCheckbox"] [data-baseweb="checkbox"] > span:first-child > div {
    position: relative !important;
}
.st-key-voice_auto_send [data-testid="stCheckbox"] [data-baseweb="checkbox"] > div:first-child,
.st-key-voice_auto_send [data-testid="stCheckbox"] [data-baseweb="checkbox"] > span:first-child > div {
    width: 1.05rem !important;
    height: 1.05rem !important;
    min-width: 1.05rem !important;
    background: var(--checkbox-bg) !important;
    border: 1.5px solid var(--input-border) !important;
    border-radius: 5px !important;
    color: var(--checkbox-check) !important;
    box-shadow: none !important;
    transition: background 160ms ease, border-color 160ms ease, box-shadow 160ms ease !important;
}
.st-key-voice_auto_send [data-testid="stCheckbox"] svg {
    background: transparent !important;
    color: var(--checkbox-check) !important;
    fill: none !important;
    opacity: 0 !important;
    stroke: currentColor !important;
    stroke-width: 3 !important;
}
.st-key-voice_auto_send [data-testid="stCheckbox"] [data-baseweb="checkbox"]:has(input:checked) > div:first-child,
.st-key-voice_auto_send [data-testid="stCheckbox"] [data-baseweb="checkbox"]:has(input:checked) > span:first-child > div,
.st-key-voice_auto_send [data-testid="stCheckbox"] [data-baseweb="checkbox"][aria-checked="true"] > div:first-child,
.st-key-voice_auto_send [data-testid="stCheckbox"] [data-baseweb="checkbox"][aria-checked="true"] > span:first-child > div,
.st-key-voice_auto_send [data-testid="stCheckbox"] [data-baseweb="checkbox"][data-wandermind-checked="true"] > div:first-child,
.st-key-voice_auto_send [data-testid="stCheckbox"] [data-baseweb="checkbox"][data-wandermind-checked="true"] > span:first-child > div,
.st-key-voice_auto_send [data-testid="stCheckbox"][data-wandermind-checked="true"] [data-baseweb="checkbox"] > div:first-child,
.st-key-voice_auto_send [data-testid="stCheckbox"][data-wandermind-checked="true"] [data-baseweb="checkbox"] > span:first-child > div {
    background: var(--accent) !important;
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px var(--input-focus-ring) !important;
}
.st-key-voice_auto_send [data-testid="stCheckbox"] [data-baseweb="checkbox"]:has(input:checked) > div:first-child::after,
.st-key-voice_auto_send [data-testid="stCheckbox"] [data-baseweb="checkbox"]:has(input:checked) > span:first-child > div::after,
.st-key-voice_auto_send [data-testid="stCheckbox"] [data-baseweb="checkbox"][aria-checked="true"] > div:first-child::after,
.st-key-voice_auto_send [data-testid="stCheckbox"] [data-baseweb="checkbox"][aria-checked="true"] > span:first-child > div::after,
.st-key-voice_auto_send [data-testid="stCheckbox"] [data-baseweb="checkbox"][data-wandermind-checked="true"] > div:first-child::after,
.st-key-voice_auto_send [data-testid="stCheckbox"] [data-baseweb="checkbox"][data-wandermind-checked="true"] > span:first-child > div::after,
.st-key-voice_auto_send [data-testid="stCheckbox"][data-wandermind-checked="true"] [data-baseweb="checkbox"] > div:first-child::after,
.st-key-voice_auto_send [data-testid="stCheckbox"][data-wandermind-checked="true"] [data-baseweb="checkbox"] > span:first-child > div::after {
    content: "";
    position: absolute;
    left: 50%;
    top: 50%;
    width: 0.34rem;
    height: 0.62rem;
    border: solid var(--checkbox-check);
    border-width: 0 0.14rem 0.14rem 0;
    transform: translate(-50%, -58%) rotate(45deg);
}
.st-key-voice_auto_send [data-testid="stCheckbox"] input {
    accent-color: var(--accent) !important;
}
[data-testid="stAudioInput"],
[data-testid="stAudioInput"] > div,
[data-testid="stAudioInput"] section,
[data-testid="stAudioInput"] [data-testid="stAudioInputRecorder"],
[data-testid="stAudioInput"] [data-testid="stAudioInputWaveform"],
[data-testid="stAudioInput"] [data-testid="stAudioInputTimer"] {
    background: var(--audio-bg) !important;
    color: var(--audio-text) !important;
    border-color: var(--input-border) !important;
}
[data-testid="stAudioInput"] section,
[data-testid="stAudioInput"] [data-testid="stAudioInputRecorder"],
[data-testid="stAudioInput"] [data-testid="stAudioInputWaveform"] {
    border: 1px solid var(--input-border) !important;
    border-radius: 14px !important;
    box-shadow: var(--shadow) !important;
}
[data-testid="stAudioInput"] button,
[data-testid="stAudioInput"] svg {
    background: var(--audio-control-bg) !important;
    color: var(--audio-muted) !important;
    fill: currentColor !important;
    border-radius: 12px !important;
}
[data-testid="stAudioInput"] canvas,
[data-testid="stAudioInput"] [role="progressbar"],
[data-testid="stAudioInput"] [aria-valuenow] {
    background: var(--audio-wave-bg) !important;
    color: var(--audio-wave-line) !important;
    accent-color: var(--accent) !important;
}
[data-testid="stAudioInput"] time,
[data-testid="stAudioInput"] code,
[data-testid="stAudioInput"] [data-testid="stAudioInputTimer"] {
    background: var(--audio-timer-bg) !important;
    color: var(--audio-text) !important;
    border: 1px solid var(--input-border) !important;
    border-radius: 10px !important;
    padding: 0.1rem 0.35rem !important;
}
.stChatInput,
[data-testid="stBottom"],
[data-testid="stBottom"] > div,
[data-testid="stBottom"] [data-testid="stVerticalBlock"],
[data-testid="stChatInput"],
[data-testid="stChatInput"] > div,
[data-testid="stChatInputContainer"],
[data-testid="stChatInputContainer"] > div {
    background: var(--chat-bar-bg) !important;
    color: var(--text) !important;
    border-color: var(--input-border) !important;
}
.stChatInput,
[data-testid="stChatInput"],
[data-testid="stChatInput"] > div,
[data-testid="stChatInputContainer"],
[data-testid="stChatInputContainer"] > div,
[data-testid="stChatInputContainer"] textarea {
    background: var(--chat-input-bg) !important;
    border: 1px solid var(--input-border) !important;
    border-radius: 16px !important;
    box-shadow: var(--shadow) !important;
}
[data-testid="stBottom"] {
    border: none !important;
    box-shadow: none !important;
}
[data-testid="stChatInputContainer"] button,
[data-testid="stChatInput"] button {
    background: var(--chat-send-bg) !important;
    color: var(--chat-send-text) !important;
    border: 1px solid var(--input-border) !important;
    border-radius: 12px !important;
}
[data-testid="stChatInputContainer"] button svg,
[data-testid="stChatInput"] button svg {
    color: var(--chat-send-text) !important;
    fill: currentColor !important;
}
[data-testid="stChatInputFileUploadButton"] button,
[data-testid="stChatInputSubmitButton"] {
    width: 2.35rem !important;
    height: 2.35rem !important;
    min-height: 2.35rem !important;
}
[data-testid="stChatInputFileUploadButton"] button:hover,
[data-testid="stChatInputSubmitButton"]:hover {
    border-color: var(--accent-strong) !important;
    background: var(--accent-soft) !important;
}
.stDivider {
    margin: 1rem 0 !important;
}
.stChatInput textarea,
[data-testid="stChatInput"] textarea,
[data-testid="stChatInputContainer"] textarea {
    background: transparent !important;
    color: var(--text) !important;
    padding: 0.72rem 0.2rem !important;
    line-height: 1.35 !important;
}
[data-testid="stChatInput"] [data-testid="stFileUploaderFile"],
[data-testid="stChatInput"] [data-testid="stUploadedFile"] {
    background: var(--accent-2-soft) !important;
    border: 1px solid var(--input-border) !important;
    border-radius: 12px !important;
    color: var(--text) !important;
}
[data-testid="stChatInput"] [data-testid="stFileUploaderFileName"],
[data-testid="stChatInput"] [data-testid="stUploadedFileName"] {
    color: var(--text) !important;
}
.stTextInput label, .stSelectbox label, .stNumberInput label, .stTextArea label,
.stCheckbox label, .stAudioInput label, .stToggle label, .stChatInput label,
.stTextInput label, .stSelectbox label, .stNumberInput label,
div[data-testid="stToggle"] label,
[data-testid="stTextInput"] label,
[data-testid="stSelectbox"] label,
[data-testid="stNumberInput"] label,
[data-testid="stCheckbox"] label,
[data-testid="stAudioInput"] label {
    color: var(--text) !important;
}
.stTextInput input::placeholder,
.stNumberInput input::placeholder,
.stTextArea textarea::placeholder,
.stChatInput textarea::placeholder,
[data-testid="stChatInputContainer"] textarea::placeholder {
    color: var(--placeholder) !important;
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
[data-baseweb="popover"],
[data-baseweb="menu"] {
    background: var(--panel-strong) !important;
    border: 1px solid var(--card-border) !important;
    border-radius: 14px !important;
    color: var(--text) !important;
    box-shadow: var(--shadow) !important;
}
[role="listbox"],
[role="option"] {
    background: var(--panel-strong) !important;
    color: var(--text) !important;
}
[role="option"]:hover,
[role="option"][aria-selected="true"] {
    background: var(--accent-soft) !important;
    color: var(--text) !important;
}
[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] li,
[data-testid="stMarkdownContainer"] span,
[data-testid="stMarkdownContainer"] strong {
    color: inherit;
}
.stImage img {
    border-radius: 14px;
}
.chat-spacer {
    height: 0.2rem;
}
html body .stApp section[data-testid="stMain"] div.stVerticalBlock.st-key-chat_shell {
    position: fixed !important;
    top: 1rem !important;
    right: 1rem !important;
    display: flex !important;
    flex-direction: column !important;
    overflow: hidden !important;
    max-height: calc(100vh - 2rem) !important;
    width: min(34vw, 520px) !important;
    height: calc(100vh - 2rem) !important;
    min-height: 0 !important;
    padding-bottom: 0.35rem !important;
    box-sizing: border-box !important;
    z-index: 5 !important;
}
html body .stApp section[data-testid="stMain"] div.stVerticalBlock.st-key-chat_shell > div {
    min-height: 0 !important;
}
html body .stApp section[data-testid="stMain"] div.stVerticalBlock.st-key-chat_shell .st-key-chat_feed {
    flex: 1 1 auto !important;
    display: flex !important;
    flex-direction: column !important;
    gap: 0.75rem !important;
    min-height: 0 !important;
    overflow-y: auto !important;
    height: auto !important;
    max-height: calc(100vh - 8rem) !important;
    padding: 0.35rem 0.35rem 0.6rem 0;
    margin-right: -0.1rem;
    overscroll-behavior: contain;
}
html body .stApp section[data-testid="stMain"] div.stVerticalBlock.st-key-chat_shell .st-key-chat_feed > div {
    min-height: 0 !important;
}
html body .stApp section[data-testid="stMain"] div.stVerticalBlock.st-key-chat_shell .st-key-chat_feed > [data-testid="stElementContainer"]:has(.message-card) {
    flex: 0 0 auto !important;
    height: fit-content !important;
    min-height: fit-content !important;
}
html body .stApp section[data-testid="stMain"] div.stVerticalBlock.st-key-chat_shell .st-key-chat_feed > [data-testid="stElementContainer"]:has(.message-card) [data-testid="stMarkdown"],
html body .stApp section[data-testid="stMain"] div.stVerticalBlock.st-key-chat_shell .st-key-chat_feed > [data-testid="stElementContainer"]:has(.message-card) [data-testid="stMarkdownContainer"] {
    height: auto !important;
    min-height: 0 !important;
    margin-bottom: 0 !important;
}
html body .stApp section[data-testid="stMain"] div.stVerticalBlock.st-key-chat_shell .st-key-chat_feed > [data-testid="stElementContainer"]:has([data-testid="stButton"]) {
    flex: 0 0 auto !important;
    height: auto !important;
    min-height: 3.15rem !important;
    overflow: visible !important;
}
html body .stApp section[data-testid="stMain"] div.stVerticalBlock.st-key-chat_shell .st-key-chat_feed [data-testid="stButton"] {
    margin: -0.2rem 0 0.35rem !important;
}
html body .stApp section[data-testid="stMain"] div.stVerticalBlock.st-key-chat_shell .st-key-chat_feed [data-testid="stButton"] button {
    width: fit-content !important;
    min-height: 2.55rem !important;
}
html body .stApp section[data-testid="stMain"] div.stVerticalBlock.st-key-chat_shell .st-key-chat_feed::-webkit-scrollbar {
    width: 10px;
}
html body .stApp section[data-testid="stMain"] div.stVerticalBlock.st-key-chat_shell .st-key-chat_feed::-webkit-scrollbar-thumb {
    background: var(--input-border);
    border-radius: 999px;
}
html body .stApp section[data-testid="stMain"] div.stVerticalBlock.st-key-chat_shell > [data-testid="stElementContainer"]:has(.stChatInput) {
    flex: 0 0 auto !important;
    overflow: visible !important;
    min-height: 76px !important;
}
@media (max-width: 1100px) {
    html body .stApp section[data-testid="stMain"] div.stVerticalBlock.st-key-chat_shell {
        position: static !important;
        width: auto !important;
        height: auto !important;
        right: auto !important;
        z-index: auto !important;
    }
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


PERSISTED_STATE_FILE = Path(__file__).with_name("travel_local_state.json")
GOOGLE_CALENDAR_SCOPES = ["https://www.googleapis.com/auth/calendar.events"]
GOOGLE_CALENDAR_TOKEN_FILE = Path(__file__).with_name("google_calendar_token.json")
PERSISTED_STATE_VERSION = 2
PERSISTED_STATE_DEFAULTS = {
    "state_version": PERSISTED_STATE_VERSION,
    "messages": [],
    "trip_country": "Philippines",
    "trip_style": "Adventure",
    "trip_days": 5,
    "budget_scope": "Total trip budget",
    "budget_currency": "PHP",
    "budget_amount": 1500.0,
    "trip_date_text": "",
    "departure_time_text": "",
    "transport_preference": "No preference yet",
    "travel_companions": "Not specified yet",
    "theme_mode": "dark",
}


def load_persisted_state():
    try:
        if not PERSISTED_STATE_FILE.exists():
            return {}
        data = json.loads(PERSISTED_STATE_FILE.read_text(encoding="utf-8"))
    except Exception:
        return {}

    return data if isinstance(data, dict) else {}


def save_persisted_state():
    persisted_messages = []
    for message in st.session_state.get("messages", []):
        persisted_message = dict(message)
        if persisted_message.get("attachments"):
            persisted_message["attachments"] = [
                {
                    key: value
                    for key, value in attachment.items()
                    if key not in {"data_url", "text"}
                }
                for attachment in persisted_message["attachments"]
            ]
        persisted_messages.append(persisted_message)

    payload = {
        "state_version": PERSISTED_STATE_VERSION,
        "messages": persisted_messages,
        "trip_country": st.session_state.get("trip_country", PERSISTED_STATE_DEFAULTS["trip_country"]),
        "trip_style": st.session_state.get("trip_style", PERSISTED_STATE_DEFAULTS["trip_style"]),
        "trip_days": int(st.session_state.get("trip_days", PERSISTED_STATE_DEFAULTS["trip_days"])),
        "budget_scope": st.session_state.get("budget_scope", PERSISTED_STATE_DEFAULTS["budget_scope"]),
        "budget_currency": st.session_state.get("budget_currency", PERSISTED_STATE_DEFAULTS["budget_currency"]),
        "budget_amount": float(st.session_state.get("budget_amount", PERSISTED_STATE_DEFAULTS["budget_amount"])),
        "trip_date_text": st.session_state.get("trip_date_text", PERSISTED_STATE_DEFAULTS["trip_date_text"]),
        "departure_time_text": st.session_state.get("departure_time_text", PERSISTED_STATE_DEFAULTS["departure_time_text"]),
        "transport_preference": st.session_state.get("transport_preference", PERSISTED_STATE_DEFAULTS["transport_preference"]),
        "travel_companions": st.session_state.get("travel_companions", PERSISTED_STATE_DEFAULTS["travel_companions"]),
        "theme_mode": st.session_state.get("theme_mode", PERSISTED_STATE_DEFAULTS["theme_mode"]),
    }

    try:
        PERSISTED_STATE_FILE.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    except Exception:
        pass


def save_and_rerun():
    save_persisted_state()
    st.rerun()


def reset_persisted_state():
    try:
        PERSISTED_STATE_FILE.unlink(missing_ok=True)
    except Exception:
        pass

    for key, default in PERSISTED_STATE_DEFAULTS.items():
        st.session_state[key] = default.copy() if isinstance(default, list) else default


def request_reset_persisted_state():
    st.session_state.reset_device_data_requested = True


class MissingTripStartDate(RuntimeError):
    pass


def google_calendar_credentials_path():
    configured_path = load_api_key(
        ["google_calendar_credentials_path", "GOOGLE_CALENDAR_CREDENTIALS_PATH"],
        ["GOOGLE_CALENDAR_CREDENTIALS_PATH"],
    )
    if configured_path:
        return Path(configured_path).expanduser()
    return Path(__file__).with_name("google_calendar_credentials.json")


COUNTRY_PLACEHOLDER = "Select a country"
COUNTRY_OPTIONS = [
    COUNTRY_PLACEHOLDER,
    "Argentina",
    "Australia",
    "Austria",
    "Bahrain",
    "Bangladesh",
    "Belgium",
    "Bhutan",
    "Brazil",
    "Bulgaria",
    "Cambodia",
    "Canada",
    "Chile",
    "China",
    "Colombia",
    "Costa Rica",
    "Croatia",
    "Czech Republic",
    "Denmark",
    "Dominican Republic",
    "Ecuador",
    "Egypt",
    "Estonia",
    "Finland",
    "France",
    "Georgia",
    "Germany",
    "Ghana",
    "Greece",
    "Guatemala",
    "Hungary",
    "Iceland",
    "India",
    "Indonesia",
    "Ireland",
    "Israel",
    "Italy",
    "Jamaica",
    "Japan",
    "Jordan",
    "Kazakhstan",
    "Kenya",
    "Laos",
    "Lebanon",
    "Lithuania",
    "Luxembourg",
    "Malaysia",
    "Maldives",
    "Malta",
    "Mexico",
    "Mongolia",
    "Morocco",
    "Nepal",
    "Netherlands",
    "New Zealand",
    "Nicaragua",
    "Norway",
    "Oman",
    "Panama",
    "Paraguay",
    "Peru",
    "Philippines",
    "Poland",
    "Portugal",
    "Qatar",
    "Romania",
    "Saudi Arabia",
    "Singapore",
    "Slovakia",
    "South Africa",
    "South Korea",
    "Spain",
    "Sweden",
    "Switzerland",
    "Taiwan",
    "Thailand",
    "Turkey",
    "United Arab Emirates",
    "United Kingdom",
    "United States",
    "Vietnam",
]

persisted_state = load_persisted_state()
persisted_state_version = int(persisted_state.get("state_version", 0)) if isinstance(persisted_state.get("state_version", 0), int) else 0
for key, default in [("messages", PERSISTED_STATE_DEFAULTS["messages"]), ("trip_country", PERSISTED_STATE_DEFAULTS["trip_country"]), ("trip_style", PERSISTED_STATE_DEFAULTS["trip_style"]), ("trip_days", PERSISTED_STATE_DEFAULTS["trip_days"]), ("budget_scope", PERSISTED_STATE_DEFAULTS["budget_scope"]), ("budget_currency", PERSISTED_STATE_DEFAULTS["budget_currency"]), ("budget_amount", PERSISTED_STATE_DEFAULTS["budget_amount"]), ("trip_date_text", PERSISTED_STATE_DEFAULTS["trip_date_text"]), ("departure_time_text", PERSISTED_STATE_DEFAULTS["departure_time_text"]), ("transport_preference", PERSISTED_STATE_DEFAULTS["transport_preference"]), ("travel_companions", PERSISTED_STATE_DEFAULTS["travel_companions"]), ("theme_mode", PERSISTED_STATE_DEFAULTS["theme_mode"]), ("api_key_set", False), ("weather_api_key_set", False), ("last_voice_audio_hash", ""), ("last_voice_transcript", ""), ("voice_preview_ready", False), ("voice_preview_text", ""), ("voice_preview_cleared", False), ("ignore_hash_once", ""), ("calendar_save_pending", False), ("chat_attachment_uploader_nonce", 0)]:
    if key not in st.session_state:
        st.session_state[key] = persisted_state.get(key, default)

if st.session_state.get("trip_country") not in COUNTRY_OPTIONS:
    st.session_state.trip_country = PERSISTED_STATE_DEFAULTS["trip_country"]
if st.session_state.get("trip_style") not in ["Adventure", "Relaxation", "Cultural", "Foodie", "Family", "Romantic"]:
    st.session_state.trip_style = PERSISTED_STATE_DEFAULTS["trip_style"]
try:
    st.session_state.trip_days = int(st.session_state.get("trip_days", PERSISTED_STATE_DEFAULTS["trip_days"]))
except Exception:
    st.session_state.trip_days = PERSISTED_STATE_DEFAULTS["trip_days"]
if st.session_state.get("budget_scope") not in ["Total trip budget", "Budget per day"]:
    st.session_state.budget_scope = PERSISTED_STATE_DEFAULTS["budget_scope"]
if st.session_state.get("budget_currency") not in ["USD", "EUR", "GBP", "PHP", "JPY", "AUD", "CAD", "SGD"]:
    st.session_state.budget_currency = PERSISTED_STATE_DEFAULTS["budget_currency"]
if st.session_state.get("transport_preference") not in ["No preference yet", "Budget-friendly", "Convenience-oriented", "Public transport", "Taxi / ride-hailing", "Private car", "Mixed options"]:
    st.session_state.transport_preference = PERSISTED_STATE_DEFAULTS["transport_preference"]
if st.session_state.get("travel_companions") not in ["Not specified yet", "Solo", "Couple", "Family", "Friends", "Group"]:
    st.session_state.travel_companions = PERSISTED_STATE_DEFAULTS["travel_companions"]
try:
    st.session_state.budget_amount = float(st.session_state.get("budget_amount", PERSISTED_STATE_DEFAULTS["budget_amount"]))
except Exception:
    st.session_state.budget_amount = PERSISTED_STATE_DEFAULTS["budget_amount"]
if not isinstance(st.session_state.get("messages"), list):
    st.session_state.messages = []
if persisted_state_version < PERSISTED_STATE_VERSION and st.session_state.get("budget_currency") == "USD":
    st.session_state.budget_currency = PERSISTED_STATE_DEFAULTS["budget_currency"]

if st.session_state.pop("reset_device_data_requested", False):
    reset_persisted_state()
    save_persisted_state()

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
    --muted: #4e6375;
    --soft-text: #263c50;
    --accent: #a76507;
    --accent-2: #2b7184;
    --accent-soft: rgba(211, 140, 34, 0.12);
    --accent-strong: rgba(211, 140, 34, 0.26);
    --accent-2-soft: rgba(52, 123, 143, 0.12);
    --stat-value: #182838;
    --stat-label: #4e6375;
    --hero-title: linear-gradient(90deg, #875204, #a76507 55%, #bd7410);
    --hero-bg: linear-gradient(135deg, rgba(255, 255, 255, 0.93), rgba(241, 246, 250, 0.92));
    --hero-glow: linear-gradient(135deg, rgba(211,140,34,0.14), transparent 32%, rgba(52,123,143,0.08));
    --card-bg: rgba(255, 255, 255, 0.82);
    --card-bg-strong: rgba(255, 255, 255, 0.92);
    --card-border: rgba(52, 82, 108, 0.14);
    --panel-border: rgba(52, 82, 108, 0.14);
    --input-bg: rgba(255, 255, 255, 0.94);
    --input-border: rgba(52, 82, 108, 0.18);
    --input-focus: rgba(211, 140, 34, 0.55);
    --input-focus-ring: rgba(211, 140, 34, 0.13);
    --placeholder: #5b7082;
    --chat-bar-bg: rgba(255, 255, 255, 0.88);
    --chat-input-bg: rgba(255, 255, 255, 0.94);
    --chat-send-bg: #eef3f8;
    --chat-send-text: #31475b;
    --checkbox-bg: rgba(255, 255, 255, 0.96);
    --checkbox-check: #ffffff;
    --audio-bg: rgba(255, 255, 255, 0.92);
    --audio-control-bg: rgba(238, 243, 248, 0.98);
    --audio-wave-bg: rgba(255, 255, 255, 0.84);
    --audio-wave-line: #a76507;
    --audio-text: #263c50;
    --audio-muted: #4e6375;
    --audio-timer-bg: rgba(238, 243, 248, 0.98);
    --button-bg: linear-gradient(135deg, #d39224, #a76507);
    --button-bg-hover: linear-gradient(135deg, #df9f31, #b8710c);
    --button-text: #ffffff;
    --weather-title: #875204;
    --weather-temp: #182838;
    --weather-meta: #4b6476;
    --weather-meta-2: #526b7d;
    --bubble-user-bg: linear-gradient(135deg, rgba(242, 248, 252, 0.98), rgba(233, 242, 249, 0.96));
    --bubble-assistant-bg: linear-gradient(135deg, rgba(251, 252, 253, 0.98), rgba(243, 247, 250, 0.96));
    --bubble-text: #203241;
    --bubble-label-user: #875204;
    --bubble-label-assistant: #2b7184;
    --bubble-user-border: var(--accent);
    --bubble-assistant-border: var(--accent-2);
    --app-grid: rgba(18, 33, 48, 0.04);
    --app-grid-mask: rgba(0, 0, 0, 0.16);
    --app-accent-glow: rgba(211, 140, 34, 0.12);
    --app-accent-2-glow: rgba(52, 123, 143, 0.10);
    --shadow: 0 18px 38px rgba(34, 52, 72, 0.10);
    --button-shadow: rgba(211, 140, 34, 0.16);
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

SYSTEM_PROMPT = """You are I-Travel, a friendly AI Travel Planner. Be conversational and natural.

IMPORTANT RULES:
- If the user says hello, hi, or just greets you — greet them back warmly and ask where they want to go. Keep it SHORT (2-3 lines max).
- Only create itineraries or long travel plans when the user EXPLICITLY asks for one (e.g. "plan a trip", "make an itinerary", "plan my travel").
- When the user confirms they want to go to a specific place you recommended, do not create a day-by-day itinerary yet. First give a specific numbered travel plan focused on how to get there from Imus, Cavite, Philippines, including airport, terminal, station, transport line, transfer, and landmark details when relevant, then ask for the specific details needed before making an itinerary.
- If the user asks for a trip plan or schedule and you do not know when they want to travel yet, ask: "When would you like to take the trip?" before creating the schedule.
- Always keep recommendations inside the selected country. Never suggest destinations outside the selected country.
- If the selected country conflicts with the user's request, adapt the plan to places within the chosen country instead of going global.
- For simple questions, give short focused answers.
- Match the length of your response to what was asked. Short question = short answer.
- Use emojis naturally but don't overdo it.
- When you do create itineraries, organize by day with morning/afternoon/evening activities.
- When a user confirms a specific recommended place, prioritize numbered directions and travel logistics first. Ask for missing specifics before making an itinerary.
- When scheduling a trip, include the start date or travel window in the plan and make the schedule line up with it.
- Always tailor to the user's travel style, budget, and number of days set in their preferences.
- If the budget includes a numeric amount, treat it as a real spending limit. Use it to filter recommendations, estimate costs, and note whether the amount is a total trip budget or a per-day budget."""

USER_HOME_BASE = "Imus, Cavite, Philippines"

def wants_trip_schedule(user_message):
    lowered = user_message.lower()
    return any(keyword in lowered for keyword in ["plan", "schedule", "itinerary", "trip", "travel", "vacation"])


def clean_destination_name(text):
    cleaned = re.sub(r"\s+", " ", text or "").strip(" .,!?:;\"'")
    cleaned = re.sub(r"\b(?:please|pls|for me|thanks|thank you)\b", "", cleaned, flags=re.IGNORECASE)
    return re.sub(r"\s+", " ", cleaned).strip(" .,!?:;\"'")


def looks_like_preference_answer(text):
    lowered = re.sub(r"[^a-z\s]", " ", (text or "").lower())
    lowered = re.sub(r"\s+", " ", lowered).strip()
    preference_terms = {
        "food", "cuisine", "japanese food", "local food", "hotel", "hostel",
        "guesthouse", "accommodation", "budget", "mid range", "high end",
        "cheap", "affordable", "solo", "family", "friends", "companions",
        "morning", "noon", "afternoon", "evening", "night",
    }
    preference_phrases = [
        "i want to try",
        "want to try",
        "i prefer",
        "i like",
        "open to",
        "around noon",
        "around morning",
        "around afternoon",
        "around evening",
    ]
    return any(term in lowered for term in preference_terms) or any(phrase in lowered for phrase in preference_phrases)


def extract_explicit_confirmed_destination(user_message):
    if looks_like_preference_answer(user_message):
        return ""

    patterns = [
        r"\b(?:i\s+want\s+to\s+go\s+to|i(?:'| a)?m\s+going\s+to|ill\s+go\s+to|i'll\s+go\s+to|let'?s\s+go\s+to|go\s+to|visit|choose|pick)\s+([A-Za-z][A-Za-z\s\-']{1,50})",
        r"\b(?:yes|okay|ok|sure),?\s+(?:i\s+(?:choose|pick|want\s+to\s+go\s+to)|let'?s\s+go\s+to|go\s+to|visit)\s+([A-Za-z][A-Za-z\s\-']{1,50})",
    ]
    for pattern in patterns:
        match = re.search(pattern, user_message, flags=re.IGNORECASE)
        if match:
            destination = clean_destination_name(match.group(1))
            if destination and destination.lower() not in {"there", "that place", "it", "that"}:
                return destination
    return ""


def is_affirmative_destination_confirmation(user_message):
    if looks_like_preference_answer(user_message):
        return False

    lowered = re.sub(r"[^a-z\s']", " ", user_message.lower())
    lowered = re.sub(r"\s+", " ", lowered).strip()
    direct_phrases = {
        "yes",
        "yeah",
        "yep",
        "sure",
        "ok",
        "okay",
        "yes please",
        "sure please",
        "go ahead",
        "let's go",
        "lets go",
        "i want to go there",
        "i'll go there",
        "ill go there",
        "i'm going there",
        "im going there",
        "that one",
        "that place",
    }
    if lowered in direct_phrases:
        return True
    return any(phrase in lowered for phrase in ["go there", "visit there", "choose that", "pick that"])


def find_latest_recommended_destination():
    for msg in reversed(st.session_state.get("messages", [])):
        if msg.get("role") != "assistant":
            continue
        images = msg.get("images") or []
        if len(images) == 1:
            image = images[0]
            caption = image.get("caption") if isinstance(image, dict) else ""
            if caption:
                return caption

        candidates = extract_place_candidates(msg.get("content", ""))
        if candidates:
            return candidates[0]
    return ""


def get_confirmed_destination(user_message):
    explicit_destination = extract_explicit_confirmed_destination(user_message)
    if explicit_destination:
        return explicit_destination
    if is_affirmative_destination_confirmation(user_message):
        return find_latest_recommended_destination()
    return ""


def wants_calendar_save(user_message):
    lowered = user_message.lower()
    calendar_terms = ["calendar", "google calendar", "gcal", "schedule it", "save it"]
    action_terms = ["mark", "put", "add", "save", "schedule", "book"]
    direct_phrases = [
        "mark that in the calendar",
        "mark it in the calendar",
        "put that in google calendar",
        "put it in google calendar",
        "add that to my calendar",
        "add it to my calendar",
        "save that to my calendar",
        "save it to my calendar",
    ]
    return any(phrase in lowered for phrase in direct_phrases) or (
        any(term in lowered for term in calendar_terms)
        and any(term in lowered for term in action_terms)
    )


def is_itinerary_text(text):
    lowered = text.lower()
    day_markers = re.findall(r"\bday\s+\d+\b", lowered)
    date_markers = re.findall(
        r"\b(?:jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|jun(?:e)?|jul(?:y)?|aug(?:ust)?|sep(?:tember)?|sept|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?)\s+\d{1,2}\b",
        lowered,
    )
    time_blocks = ["morning", "afternoon", "evening"]
    time_block_count = sum(1 for block in time_blocks if block in lowered)
    has_day_by_day_structure = len(set(day_markers)) >= 2 or (
        "day 1" in lowered and time_block_count >= 2
    )
    has_dated_schedule = len(set(date_markers)) >= 2 and time_block_count >= 2
    has_itinerary_label = "itinerary" in lowered or "day-by-day" in lowered
    return (has_day_by_day_structure or has_dated_schedule) and (
        has_itinerary_label or time_block_count >= 2
    )


def find_latest_itinerary_message():
    for msg in reversed(st.session_state.get("messages", [])):
        if msg.get("role") == "assistant" and is_itinerary_text(msg.get("content", "")):
            return msg.get("content", "")
    return ""


def parse_trip_start_date(*texts):
    month_lookup = {
        "jan": 1,
        "january": 1,
        "feb": 2,
        "february": 2,
        "mar": 3,
        "march": 3,
        "apr": 4,
        "april": 4,
        "may": 5,
        "jun": 6,
        "june": 6,
        "jul": 7,
        "july": 7,
        "aug": 8,
        "august": 8,
        "sep": 9,
        "sept": 9,
        "september": 9,
        "oct": 10,
        "october": 10,
        "nov": 11,
        "november": 11,
        "dec": 12,
        "december": 12,
    }

    for text in texts:
        if not text:
            continue
        text = str(text)
        match = re.search(r"\b(\d{4}-\d{2}-\d{2})\b", text)
        if match:
            try:
                return datetime.strptime(match.group(1), "%Y-%m-%d").date()
            except ValueError:
                pass

        month_day_match = re.search(
            r"\b(jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|jun(?:e)?|jul(?:y)?|aug(?:ust)?|sep(?:tember)?|sept|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?)\s+(\d{1,2})(?:,\s*(\d{4}))?\b",
            text,
            re.IGNORECASE,
        )
        if month_day_match:
            month_name, day_text, year_text = month_day_match.groups()
            year = int(year_text) if year_text else date.today().year
            try:
                parsed = date(year, month_lookup[month_name.lower()], int(day_text))
                if not year_text and parsed < date.today():
                    parsed = date(year + 1, parsed.month, parsed.day)
                return parsed
            except ValueError:
                pass
    return None


def missing_calendar_date_message():
    return "Sure - what date should I start it on? Send an exact date like 2026-06-10, and I will add it to Google Calendar."


def answer_pending_calendar_date(user_message, trip_country, trip_style, trip_days, budget):
    if not st.session_state.get("calendar_save_pending"):
        return None

    start_date = parse_trip_start_date(user_message)
    if not start_date:
        return "I still need the exact start date for the calendar event. Please send it like 2026-06-10."

    st.session_state.calendar_save_pending = False
    return save_latest_itinerary_to_calendar(
        trip_country,
        trip_style,
        trip_days,
        budget,
        start_date.isoformat(),
        remember_missing_date=True,
    )


def assistant_message(reply):
    if isinstance(reply, dict):
        return {"role": "assistant", **reply}
    return {"role": "assistant", "content": str(reply)}


def calendar_saved_message(link="", event_id="", calendar_id="primary"):
    message = {"content": "Trip added to Google Calendar."}
    if link:
        message["calendar_link"] = link
    if event_id:
        message["calendar_event_id"] = event_id
        message["calendar_id"] = calendar_id
    return message


def get_google_calendar_service(allow_interactive=True):
    if not all([GoogleAuthRequest, GoogleCredentials, InstalledAppFlow, build_google_service]):
        raise RuntimeError("Google Calendar libraries are not installed. Run `pip install -r requirements.txt` and restart the app.")

    credentials_path = google_calendar_credentials_path()
    if not credentials_path.exists():
        raise RuntimeError(f"Google Calendar credentials were not found at {credentials_path}.")

    def run_oauth_flow():
        flow = InstalledAppFlow.from_client_secrets_file(str(credentials_path), GOOGLE_CALENDAR_SCOPES)
        fresh_creds = flow.run_local_server(port=0)
        GOOGLE_CALENDAR_TOKEN_FILE.write_text(fresh_creds.to_json(), encoding="utf-8")
        return fresh_creds

    creds = None
    if GOOGLE_CALENDAR_TOKEN_FILE.exists():
        try:
            creds = GoogleCredentials.from_authorized_user_file(str(GOOGLE_CALENDAR_TOKEN_FILE), GOOGLE_CALENDAR_SCOPES)
        except Exception:
            GOOGLE_CALENDAR_TOKEN_FILE.unlink(missing_ok=True)
            creds = None

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(GoogleAuthRequest())
                GOOGLE_CALENDAR_TOKEN_FILE.write_text(creds.to_json(), encoding="utf-8")
            except Exception as exc:
                is_revoked_token = (RefreshError and isinstance(exc, RefreshError)) or "invalid_grant" in str(exc).lower()
                if is_revoked_token:
                    GOOGLE_CALENDAR_TOKEN_FILE.unlink(missing_ok=True)
                    creds = run_oauth_flow()
                else:
                    raise
        else:
            if not allow_interactive:
                raise RuntimeError("Google Calendar is not connected yet.")
            creds = run_oauth_flow()

    return build_google_service("calendar", "v3", credentials=creds)


def build_trip_calendar_event(itinerary_text, trip_country, trip_style, trip_days, budget, trip_date_text):
    start_date = parse_trip_start_date(trip_date_text, itinerary_text)
    if not start_date:
        raise MissingTripStartDate(missing_calendar_date_message())

    end_date = start_date + timedelta(days=int(trip_days))
    summary = f"{int(trip_days)}-day {trip_country} trip"
    description = "\n\n".join([
        "AI-generated travel itinerary from I-Travel.",
        f"Travel style: {trip_style}",
        f"Budget: {budget}",
        f"Trip length: {int(trip_days)} days",
        "Itinerary:",
        itinerary_text,
    ])
    return {
        "summary": summary,
        "location": trip_country,
        "description": description,
        "start": {"date": start_date.isoformat()},
        "end": {"date": end_date.isoformat()},
    }


def create_trip_calendar_event(itinerary_text, trip_country, trip_style, trip_days, budget, trip_date_text):
    service = get_google_calendar_service()
    calendar_id = "primary"
    event = build_trip_calendar_event(itinerary_text, trip_country, trip_style, trip_days, budget, trip_date_text)
    created = service.events().insert(calendarId=calendar_id, body=event).execute()
    return {
        "calendar_id": calendar_id,
        "event_id": created.get("id", ""),
        "link": created.get("htmlLink", ""),
    }


def is_calendar_event_missing(service, calendar_id, event_id):
    try:
        event = service.events().get(calendarId=calendar_id, eventId=event_id).execute()
    except Exception as exc:
        if HttpError and isinstance(exc, HttpError):
            status = getattr(getattr(exc, "resp", None), "status", None)
            return status in (404, 410)
        raise

    return event.get("status") == "cancelled"


def remove_deleted_calendar_confirmations():
    messages = st.session_state.get("messages", [])
    tracked_messages = [
        msg for msg in messages
        if msg.get("role") == "assistant" and msg.get("calendar_event_id")
    ]
    if not tracked_messages:
        return

    try:
        service = get_google_calendar_service(allow_interactive=False)
    except Exception:
        return

    changed = False
    active_messages = []
    for msg in messages:
        event_id = msg.get("calendar_event_id")
        if msg.get("role") == "assistant" and event_id:
            calendar_id = msg.get("calendar_id", "primary")
            try:
                if is_calendar_event_missing(service, calendar_id, event_id):
                    changed = True
                    continue
            except Exception:
                pass
        active_messages.append(msg)

    if changed:
        st.session_state.messages = active_messages
        save_persisted_state()


def save_latest_itinerary_to_calendar(trip_country, trip_style, trip_days, budget, trip_date_text, remember_missing_date=False):
    itinerary_text = find_latest_itinerary_message()
    if not itinerary_text:
        return "I could not find a recent itinerary to add yet. Ask me to create a trip plan first, then I can mark it in Google Calendar."

    try:
        created = create_trip_calendar_event(itinerary_text, trip_country, trip_style, trip_days, budget, trip_date_text)
    except MissingTripStartDate:
        if remember_missing_date:
            st.session_state.calendar_save_pending = True
        return missing_calendar_date_message()
    except Exception as exc:
        return f"I could not add it to Google Calendar yet: {exc}"

    return calendar_saved_message(created.get("link", ""), created.get("event_id", ""), created.get("calendar_id", "primary"))


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


MAX_ATTACHMENT_BYTES = 8 * 1024 * 1024
MAX_ATTACHMENT_TEXT_CHARS = 7000
MAX_CHAT_ATTACHMENTS = 5
IMAGE_ATTACHMENT_TYPES = {"image/jpeg", "image/png", "image/webp"}
DOCUMENT_ATTACHMENT_TYPES = {
    "application/pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "text/plain",
    "text/markdown",
}


def upload_bytes(uploaded_file):
    if uploaded_file is None:
        return b""
    if hasattr(uploaded_file, "getvalue"):
        return uploaded_file.getvalue()
    if hasattr(uploaded_file, "read"):
        return uploaded_file.read()
    try:
        return bytes(uploaded_file)
    except Exception:
        return b""


def detect_upload_mime(uploaded_file):
    uploaded_type = getattr(uploaded_file, "type", "") or ""
    if uploaded_type:
        return uploaded_type
    guessed_type, _ = mimetypes.guess_type(getattr(uploaded_file, "name", "") or "")
    return guessed_type or "application/octet-stream"


def extract_document_text(file_name, mime_type, file_bytes):
    try:
        if mime_type == "application/pdf" or file_name.lower().endswith(".pdf"):
            from pypdf import PdfReader

            reader = PdfReader(BytesIO(file_bytes))
            page_text = []
            for page_number, page in enumerate(reader.pages[:12], start=1):
                text = page.extract_text() or ""
                if text.strip():
                    page_text.append(f"Page {page_number}:\n{text.strip()}")
            return "\n\n".join(page_text).strip()

        if (
            mime_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            or file_name.lower().endswith(".docx")
        ):
            from docx import Document

            document = Document(BytesIO(file_bytes))
            paragraphs = [paragraph.text.strip() for paragraph in document.paragraphs if paragraph.text.strip()]
            return "\n".join(paragraphs).strip()

        if mime_type.startswith("text/") or file_name.lower().endswith((".txt", ".md")):
            return file_bytes.decode("utf-8", errors="replace").strip()
    except Exception as exc:
        return f"[Could not extract text from this document: {exc}]"

    return ""


def prepare_chat_attachments(uploaded_files):
    prepared = []
    warnings = []
    for uploaded_file in (uploaded_files or [])[:MAX_CHAT_ATTACHMENTS]:
        file_bytes = upload_bytes(uploaded_file)
        file_name = getattr(uploaded_file, "name", "attachment") or "attachment"
        mime_type = detect_upload_mime(uploaded_file)
        if not file_bytes:
            warnings.append(f"{file_name} was empty.")
            continue
        if len(file_bytes) > MAX_ATTACHMENT_BYTES:
            warnings.append(f"{file_name} is larger than 8 MB, so I skipped it.")
            continue

        attachment = {
            "name": file_name,
            "mime_type": mime_type,
            "size": len(file_bytes),
        }
        if mime_type in IMAGE_ATTACHMENT_TYPES:
            encoded = base64.b64encode(file_bytes).decode("ascii")
            attachment["kind"] = "image"
            attachment["data_url"] = f"data:{mime_type};base64,{encoded}"
        elif mime_type in DOCUMENT_ATTACHMENT_TYPES or file_name.lower().endswith((".pdf", ".docx", ".txt", ".md")):
            extracted_text = extract_document_text(file_name, mime_type, file_bytes)
            attachment["kind"] = "document"
            attachment["text"] = extracted_text[:MAX_ATTACHMENT_TEXT_CHARS]
            if len(extracted_text) > MAX_ATTACHMENT_TEXT_CHARS:
                attachment["truncated"] = True
            if not extracted_text:
                warnings.append(f"I could not find readable text in {file_name}.")
        else:
            warnings.append(f"{file_name} is not a supported image or document type.")
            continue

        prepared.append(attachment)

    if uploaded_files and len(uploaded_files) > MAX_CHAT_ATTACHMENTS:
        warnings.append(f"Only the first {MAX_CHAT_ATTACHMENTS} attachments were included.")

    return prepared, warnings


def build_attachment_context(attachments):
    if not attachments:
        return ""

    sections = []
    for idx, attachment in enumerate(attachments, start=1):
        name = attachment.get("name", f"Attachment {idx}")
        if attachment.get("kind") == "image":
            sections.append(
                f"Attachment {idx}: {name} is an image. Inspect it directly and use visible destination, route, booking, map, schedule, or document details when planning."
            )
        elif attachment.get("kind") == "document":
            extracted_text = attachment.get("text", "").strip()
            suffix = "\n[Text was truncated for length.]" if attachment.get("truncated") else ""
            sections.append(f"Attachment {idx}: {name}\nExtracted document text:\n{extracted_text}{suffix}")

    return "\n\n".join(sections)


def build_user_content_for_groq(user_message, attachments):
    attachment_context = build_attachment_context(attachments)
    text = user_message.strip()
    if attachment_context:
        text = f"{text}\n\nAttached travel context:\n{attachment_context}" if text else f"Please help me with these travel attachments.\n\nAttached travel context:\n{attachment_context}"

    image_attachments = [attachment for attachment in attachments or [] if attachment.get("kind") == "image"]
    if not image_attachments:
        return text

    content = [{"type": "text", "text": text}]
    for attachment in image_attachments:
        content.append({"type": "image_url", "image_url": {"url": attachment["data_url"]}})
    return content


def visible_user_message(user_message, attachments):
    text = user_message.strip()
    if text:
        return text
    if attachments:
        return "Please help me understand these travel attachments."
    return ""


def chat_with_agent(user_message, trip_country, trip_style, trip_days, budget, trip_date_text, current_date_text, confirmed_destination="", departure_time_text="", transport_preference="", travel_companions="", attachments=None):
    client = Groq(api_key=st.session_state.groq_key)
    attachments = attachments or []
    schedule_context = trip_date_text if trip_date_text else "Not provided yet"
    departure_context = departure_time_text if departure_time_text else "Not provided yet"
    transport_context = transport_preference if transport_preference and transport_preference != "No preference yet" else "Not provided yet"
    companions_context = travel_companions if travel_companions and travel_companions != "Not specified yet" else "Not provided yet"
    system = SYSTEM_PROMPT + f"\n\nCurrent date for planning: {current_date_text}\nUser's current trip preferences: Country={trip_country}, Style={trip_style}, Days={trip_days}, Budget={budget}, Trip timing={schedule_context}, Departure time={departure_context}, Transport preference={transport_context}, Travel companions={companions_context}"
    if confirmed_destination:
        system += f"""

Confirmed destination flow:
- The user has confirmed they want to go to {confirmed_destination}. Treat this as a request for a travel plan on how to get there, not as an itinerary request.
- Use {USER_HOME_BASE} as the user's starting point/current location.
- Do not create a day-by-day itinerary yet.
- Put the response in this order:
  1. Numbered Travel Plan: give detailed step-by-step directions from {USER_HOME_BASE} to {confirmed_destination}. Each step must be a specific action the user can follow, including transport mode, pickup/drop-off area, departure airport, likely airport terminal/check-in area when relevant, arrival airport, arrival terminal/transport area when relevant, train/bus line names, station or stop names, transfers, destination landmark/entrance, and estimated travel time when reasonable.
  2. Route options: include practical route choices labeled Option A, Option B, etc. when available, and explain which user each option fits best.
  3. Preparation notes: what to check before leaving, including schedules, fares, traffic, weather, operating hours, parking, and booking/reservation needs.
  4. Specifics needed before itinerary: ask only for missing details from the saved preferences, such as departure date/time, preferred transport mode, trip length, budget comfort, or whether they are traveling solo or with companions.
- For international trips from the Philippines, include the airport flow: Imus to NAIA, check the airline ticket for the exact NAIA terminal, board the Manila-to-destination-country flight, then after landing identify the airport rail/bus/taxi area and the next station/terminal to use.
- Keep the travel plan concrete and easy to follow. Avoid vague advice like "fly to Japan", "take public transportation", or "take a train" without naming likely airports, terminals/check-in areas, rail/bus lines, station names, and transfer points.
- If the exact terminal depends on the airline or arrival airport, say that clearly and tell the user what to verify on the ticket or airport signs.
- End by asking only for the specifics that are still marked "Not provided yet" or "Not specified yet" in the saved preferences.
- If exact transport schedules, fares, or traffic conditions are uncertain, say they should be checked before departure."""
    messages = [{"role": "system", "content": system}]
    for m in st.session_state.messages:
        messages.append({"role": m["role"], "content": m["content"]})
    messages.append({"role": "user", "content": build_user_content_for_groq(user_message, attachments)})
    model = "meta-llama/llama-4-scout-17b-16e-instruct" if any(attachment.get("kind") == "image" for attachment in attachments) else "llama-3.3-70b-versatile"
    response = client.chat.completions.create(
        model=model,
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


if not st.session_state.get("calendar_deletion_sync_checked"):
    remove_deleted_calendar_confirmations()
    st.session_state.calendar_deletion_sync_checked = True


left, right = st.columns([1, 2.5], gap="large")

with left:
    st.markdown("""
    <div class="hero-card">
        <div class="hero-title">I-Travel</div>
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

    if st.session_state.get("trip_country") in (None, "", COUNTRY_PLACEHOLDER) or st.session_state.get("trip_country") not in COUNTRY_OPTIONS:
        st.session_state.trip_country = "Philippines"

    theme_mode_enabled = st.toggle(
        "Light mode",
        value=st.session_state.get("theme_mode", "dark") == "light",
        help="Switch between light and dark mode.",
    )
    st.session_state.theme_mode = "light" if theme_mode_enabled else "dark"
    st.markdown(get_theme_override_css(st.session_state.theme_mode), unsafe_allow_html=True)

    current_date_text = date.today().isoformat()

    st.divider()

    st.markdown('<div class="section-label">🗺️ Trip Preferences</div>', unsafe_allow_html=True)
    st.caption("Your preferences and chat history are saved locally on this device and restored after refresh.")
    trip_country = st.selectbox("Country", COUNTRY_OPTIONS, key="trip_country", help="Choose one country so I-Travel keeps the trip focused there.")
    trip_style = st.selectbox("Travel Style", ["Adventure", "Relaxation", "Cultural", "Foodie", "Family", "Romantic"], key="trip_style")
    trip_days = st.number_input("Number of Days", min_value=1, max_value=30, value=5, key="trip_days")
    budget_scope = st.selectbox("Budget Scope", ["Total trip budget", "Budget per day"], key="budget_scope")
    budget_currency = st.selectbox("Currency", ["USD", "EUR", "GBP", "PHP", "JPY", "AUD", "CAD", "SGD"], key="budget_currency")
    budget_amount = st.number_input("Budget Amount", min_value=1.0, value=1500.0, step=50.0, key="budget_amount")
    budget = f"{budget_currency} {budget_amount:,.0f} ({budget_scope.lower()})"

    st.markdown('<div class="section-label">📅 Trip Timing</div>', unsafe_allow_html=True)
    st.caption(f"Planning from today's date: {current_date_text}")
    trip_date_text = st.text_input(
        "When would you take the trip?",
        placeholder="e.g. 2026-06-10, next July, or around Christmas",
        key="trip_date_text",
        label_visibility="collapsed",
    )
    departure_time_text = st.text_input(
        "Preferred departure or arrival time",
        placeholder="e.g. leave at 8 AM, arrive around noon",
        key="departure_time_text",
    )
    transport_preference = st.selectbox(
        "Transport Preference",
        ["No preference yet", "Budget-friendly", "Convenience-oriented", "Public transport", "Taxi / ride-hailing", "Private car", "Mixed options"],
        key="transport_preference",
    )
    travel_companions = st.selectbox(
        "Travel Companions",
        ["Not specified yet", "Solo", "Couple", "Family", "Friends", "Group"],
        key="travel_companions",
    )

    st.markdown('<div class="section-label">⚡ Quick Snapshot</div>', unsafe_allow_html=True)
    snapshot_departure = html.escape(departure_time_text or "Not set")
    snapshot_transport = html.escape(transport_preference)
    snapshot_companions = html.escape(travel_companions)
    st.markdown(f"""
    <div class="quick-snapshot-grid">
        <div class="quick-stat"><div class="quick-stat-label">Country</div><div class="quick-stat-value">{trip_country}</div></div>
        <div class="quick-stat"><div class="quick-stat-label">Style</div><div class="quick-stat-value">{trip_style}</div></div>
        <div class="quick-stat"><div class="quick-stat-label">Days</div><div class="quick-stat-value">{int(trip_days)}</div></div>
        <div class="quick-stat"><div class="quick-stat-label">Budget</div><div class="quick-stat-value">{budget_currency} {budget_amount:,.0f}</div></div>
        <div class="quick-stat"><div class="quick-stat-label">Time</div><div class="quick-stat-value">{snapshot_departure}</div></div>
        <div class="quick-stat"><div class="quick-stat-label">Transport</div><div class="quick-stat-value">{snapshot_transport}</div></div>
        <div class="quick-stat"><div class="quick-stat-label">Companions</div><div class="quick-stat-value">{snapshot_companions}</div></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-label">🎙️ Voice Intent</div>', unsafe_allow_html=True)
    with st.container(key="voice_auto_send"):
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
            if trip_country == COUNTRY_PLACEHOLDER:
                st.warning("Choose a country before using voice input.")
            elif not st.session_state.api_key_set:
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
                        confirmed_destination = get_confirmed_destination(transcript)
                        pending_calendar_reply = answer_pending_calendar_date(transcript, trip_country, trip_style, trip_days, budget)
                        if pending_calendar_reply:
                            st.session_state.messages.append(assistant_message(pending_calendar_reply))
                        elif wants_calendar_save(transcript):
                            calendar_reply = save_latest_itinerary_to_calendar(trip_country, trip_style, trip_days, budget, st.session_state.trip_date_text, remember_missing_date=True)
                            st.session_state.messages.append(assistant_message(calendar_reply))
                        elif wants_trip_schedule(transcript) and not confirmed_destination and not st.session_state.trip_date_text.strip():
                            st.session_state.messages.append({
                                "role": "assistant",
                                "content": "When would you like to take the trip? Once I have the timing, I can build and schedule the itinerary for you."
                            })
                        else:
                            with st.spinner("I-Travel is thinking... 🌍"):
                                try:
                                    reply = chat_with_agent(transcript, trip_country, trip_style, trip_days, budget, st.session_state.trip_date_text, current_date_text, confirmed_destination, st.session_state.departure_time_text, st.session_state.transport_preference, st.session_state.travel_companions)
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
                        save_and_rerun()
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
                    confirmed_destination = get_confirmed_destination(transcript_text)
                    pending_calendar_reply = answer_pending_calendar_date(transcript_text, trip_country, trip_style, trip_days, budget)
                    if pending_calendar_reply:
                        st.session_state.messages.append(assistant_message(pending_calendar_reply))
                    elif wants_calendar_save(transcript_text):
                        calendar_reply = save_latest_itinerary_to_calendar(trip_country, trip_style, trip_days, budget, st.session_state.trip_date_text, remember_missing_date=True)
                        st.session_state.messages.append(assistant_message(calendar_reply))
                    elif wants_trip_schedule(transcript_text) and not confirmed_destination and not st.session_state.trip_date_text.strip():
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": "When would you like to take the trip? Once I have the timing, I can build and schedule the itinerary for you."
                        })
                    else:
                        if trip_country == COUNTRY_PLACEHOLDER:
                            st.warning("Choose a country before sending a transcript.")
                        else:
                            with st.spinner("I-Travel is thinking... 🌍"):
                                try:
                                    reply = chat_with_agent(transcript_text, trip_country, trip_style, trip_days, budget, st.session_state.trip_date_text, current_date_text, confirmed_destination, st.session_state.departure_time_text, st.session_state.transport_preference, st.session_state.travel_companions)
                                    assistant_message = {"role": "assistant", "content": reply}
                                    images = build_response_images(transcript_text, reply)
                                    if images:
                                        assistant_message["images"] = images
                                    st.session_state.messages.append(assistant_message)
                                except Exception as e:
                                    st.error(f"Error: {str(e)}")
                    # allow another recording after sending
                    st.session_state.last_voice_audio_hash = ""
                    save_and_rerun()
        with col2:
            if st.button("Discard", key="discard_transcript"):
                st.session_state.voice_preview_ready = False
                st.session_state.last_voice_transcript = ""
                st.session_state.voice_preview_cleared = True
                # clear dedupe so user can immediately record again
                st.session_state.last_voice_audio_hash = ""
                save_and_rerun()
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
                    safe_city = html.escape(wd["city"])
                    safe_desc = html.escape(wd["description"].capitalize())
                    st.markdown(f"""<div class="weather-card">
                        <div class="weather-emoji">{wd['emoji']}</div>
                        <div class="weather-city">{safe_city}</div>
                        <div class="weather-temp">{wd['temp']}°C</div>
                        <div class="weather-desc">{safe_desc}</div>
                        <div class="weather-meta">💧 {wd['humidity']}% &nbsp;|&nbsp; 💨 {wd['wind']} m/s</div>
                    </div>""", unsafe_allow_html=True)
                else:
                    st.error("City not found.")

    st.divider()

    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.calendar_save_pending = False
        save_and_rerun()

    st.button("Reset Saved Device Data", use_container_width=True, on_click=request_reset_persisted_state)

    st.markdown("""<div class="tip-box">💡 <b>Try asking:</b><br>
    • "Plan 5 days in Tokyo"<br>
    • "What to pack for Bali?"<br>
    • "Luxury 3-day Rome trip"<br>
    • "Is Morocco safe to visit?"<br>
    • "Visa tips for Japan"
    </div>""", unsafe_allow_html=True)

with right:
    components.html(
        """
        <script>
        (function () {
            let lastFeedHeight = 0;
            let lastMessageCount = 0;

            function scrollChatToLatest(feed, force) {
                const parentDoc = window.parent && window.parent.document;
                const anchor = parentDoc && parentDoc.getElementById('chat-bottom-anchor');
                const shell = parentDoc && parentDoc.querySelector('div.stVerticalBlock.st-key-chat_shell');
                const messageCount = feed.querySelectorAll('.message-card').length;
                const heightChanged = feed.scrollHeight !== lastFeedHeight;
                const messageChanged = messageCount !== lastMessageCount;

                if (force || heightChanged || messageChanged) {
                    window.requestAnimationFrame(function () {
                        feed.scrollTop = feed.scrollHeight;
                        if (anchor && shell && window.getComputedStyle(shell).position !== 'fixed') {
                            anchor.scrollIntoView({ block: 'end', behavior: 'auto' });
                        }
                        lastFeedHeight = feed.scrollHeight;
                        lastMessageCount = messageCount;
                    });
                }
            }

            function applyChatLayout() {
                try {
                    const parentDoc = window.parent && window.parent.document;
                    if (!parentDoc) return;

                    const shell = parentDoc.querySelector('div.stVerticalBlock.st-key-chat_shell');
                    if (shell) {
                        shell.style.position = 'fixed';
                        shell.style.top = '1rem';
                        // place the fixed shell back over its original column instead of pinning to the viewport right
                        let container = shell.parentElement;
                        while (container && !container.classList.contains('stColumn')) {
                            container = container.parentElement;
                        }
                        if (container) {
                            const rect = container.getBoundingClientRect();
                            shell.style.setProperty('left', rect.left + 'px', 'important');
                            shell.style.setProperty('right', 'auto', 'important');
                            // match the column's width so there is no empty space
                            shell.style.setProperty('width', rect.width + 'px', 'important');
                            shell.style.boxSizing = 'border-box';

                        } else {
                            shell.style.right = '1rem';
                            shell.style.width = 'min(34vw, 520px)';
                        }
                        shell.style.height = 'calc(100vh - 2rem)';
                        shell.style.minHeight = '0';
                        shell.style.zIndex = '5';
                        shell.style.display = 'flex';
                        shell.style.flexDirection = 'column';
                    }

                    const feed = parentDoc.querySelector('div.stVerticalBlock.st-key-chat_shell .st-key-chat_feed');
                    if (feed) {
                        feed.style.flex = '1 1 auto';
                        feed.style.minHeight = '0';
                        feed.style.overflowY = 'auto';
                        scrollChatToLatest(feed, false);
                    }
                } catch (error) {
                    // Ignore layout hook failures and fall back to the CSS rules.
                }
            }

            applyChatLayout();
            const observer = new MutationObserver(applyChatLayout);
            const observedDoc = (window.parent && window.parent.document) || document;
            observer.observe(observedDoc.documentElement, { childList: true, subtree: true });
            setTimeout(function () {
                applyChatLayout();
                const parentDoc = window.parent && window.parent.document;
                const feed = parentDoc && parentDoc.querySelector('div.stVerticalBlock.st-key-chat_shell .st-key-chat_feed');
                if (feed) scrollChatToLatest(feed, true);
            }, 1000);
        })();
        </script>
        """,
        height=0,
    )

    with st.container(key="chat_shell"):
        st.markdown('<div class="chat-spacer"></div>', unsafe_allow_html=True)

        with st.container(key="chat_feed"):
            if not st.session_state.messages:
                st.markdown("""<div class="message-card chat-assistant">
                    <div class="chat-label assistant-label">🌍 I-Travel</div>
                    <b>Hello, fellow explorer! ✈️</b><br><br>
                    I'm I-Travel, your personal AI travel planner. I can help you:<br>
                    🗺️ &nbsp;Plan detailed day-by-day itineraries<br>
                    🏨 &nbsp;Find hotels & restaurants for your budget<br>
                    🌤️ &nbsp;Check weather at your destination<br>
                    🎒 &nbsp;Get packing lists & travel tips<br>
                    📋 &nbsp;Understand visa & safety requirements<br><br>
                    <b>Which country and when would you like to take the trip? 🌏</b>
                </div>""", unsafe_allow_html=True)

            for msg_idx, msg in enumerate(st.session_state.messages):
                if msg["role"] == "user":
                    safe_content = html.escape(msg["content"]).replace("\n", "<br>")
                    attachments_html = ""
                    if msg.get("attachments"):
                        img_htmls = []
                        doc_htmls = []
                        for attachment in msg["attachments"]:
                            name = html.escape(attachment.get("name", "attachment"))
                            if attachment.get("kind") == "image" and attachment.get("data_url"):
                                img_htmls.append(
                                    f'<img src="{attachment["data_url"]}" style="max-width: 100%; max-height: 200px; object-fit: cover; border-radius: 12px; border: 1px solid var(--line); margin-top: 8px; box-shadow: var(--shadow);" alt="{name}" title="{name}" />'
                                )
                            elif attachment.get("kind") == "document":
                                doc_htmls.append(
                                    f'<span style="display: inline-flex; align-items: center; gap: 6px; background: var(--line); border: 1px solid var(--line-strong); border-radius: 8px; padding: 5px 10px; font-size: 0.78rem; font-weight: 500; color: var(--text); margin-top: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">📎 {name}</span>'
                                )
                            elif attachment.get("kind") == "image" and not attachment.get("data_url"):
                                doc_htmls.append(
                                    f'<span style="display: inline-flex; align-items: center; gap: 6px; background: var(--line); border: 1px solid var(--line-strong); border-radius: 8px; padding: 5px 10px; font-size: 0.78rem; font-weight: 500; color: var(--text); margin-top: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">🖼️ {name}</span>'
                                )
                        
                        if img_htmls:
                            attachments_html += f'<div style="display: flex; flex-wrap: wrap; gap: 8px; margin-top: 2px;">{"".join(img_htmls)}</div>'
                        if doc_htmls:
                            attachments_html += f'<div style="display: flex; flex-wrap: wrap; gap: 6px; margin-top: 2px;">{"".join(doc_htmls)}</div>'

                    st.markdown(f"""<div class="message-card chat-user"><div class="chat-label user-label">👤 You</div><div>{safe_content}</div>{attachments_html}</div>""", unsafe_allow_html=True)
                else:
                    content = html.escape(msg["content"]).replace("\n", "<br>")
                    calendar_link = msg.get("calendar_link")
                    if calendar_link:
                        safe_link = html.escape(calendar_link, quote=True)
                        st.markdown(f"""<div class="message-card chat-assistant calendar-confirmation">
                            <div class="chat-label assistant-label">🌍 I-Travel</div>
                            <div class="calendar-confirmation-text">{content}</div>
                            <a class="calendar-action" href="{safe_link}" target="_blank" rel="noopener noreferrer">Open in Google Calendar</a>
                        </div>""", unsafe_allow_html=True)
                    else:
                        st.markdown(f"""<div class="message-card chat-assistant"><div class="chat-label assistant-label">🌍 I-Travel</div>{content}</div>""", unsafe_allow_html=True)
                    if msg.get("images"):
                        image_cols = st.columns(min(len(msg["images"]), 3))
                        for idx, image_data in enumerate(msg["images"]):
                            with image_cols[idx]:
                                if isinstance(image_data, str):
                                    st.image(image_data, use_container_width=True)
                                else:
                                    st.image(image_data["url"], caption=image_data.get("caption"), use_container_width=True)
                    if is_itinerary_text(msg.get("content", "")):
                        if st.button("Add to Google Calendar", key=f"calendar_add_{msg_idx}"):
                            with st.spinner("Adding this trip to Google Calendar..."):
                                try:
                                    created = create_trip_calendar_event(msg.get("content", ""), trip_country, trip_style, trip_days, budget, st.session_state.trip_date_text)
                                    calendar_reply = calendar_saved_message(created.get("link", ""), created.get("event_id", ""), created.get("calendar_id", "primary"))
                                except MissingTripStartDate:
                                    st.session_state.calendar_save_pending = True
                                    calendar_reply = missing_calendar_date_message()
                                except Exception as exc:
                                    calendar_reply = f"I could not add it to Google Calendar yet: {exc}"
                            st.session_state.messages.append(assistant_message(calendar_reply))
                            save_and_rerun()
            st.markdown('<div id="chat-bottom-anchor"></div>', unsafe_allow_html=True)

        chat_placeholder = "Ask me anything... e.g. Plan a 5-day trip to Tokyo" if not st.session_state.messages else ""
        chat_submission = st.chat_input(
            chat_placeholder,
            accept_file="multiple",
            file_type=["jpg", "jpeg", "png", "webp", "pdf", "docx", "txt", "md"],
            key=f"chat_input_{st.session_state.chat_attachment_uploader_nonce}",
        )

        if chat_submission:
            if isinstance(chat_submission, str):
                submitted_text = chat_submission
                uploaded_chat_files = []
            else:
                submitted_text = getattr(chat_submission, "text", "") or chat_submission.get("text", "")
                uploaded_chat_files = getattr(chat_submission, "files", []) or chat_submission.get("files", [])

            attachment_payload, attachment_warnings = prepare_chat_attachments(uploaded_chat_files)
            for warning in attachment_warnings:
                st.warning(warning)
            visible_content = visible_user_message(submitted_text, attachment_payload)
            if not visible_content:
                st.warning("Attach a supported image or document, or type a message first.")
            else:
                confirmed_destination = get_confirmed_destination(submitted_text)
                user_message_payload = {"role": "user", "content": visible_content}
                if attachment_payload:
                    user_message_payload["attachments"] = attachment_payload

                def clear_chat_attachments_after_send():
                    st.session_state.chat_attachment_uploader_nonce += 1

                if trip_country == COUNTRY_PLACEHOLDER:
                    st.warning("Choose a country first so I can keep the trip focused there.")
                elif st.session_state.get("calendar_save_pending"):
                    st.session_state.messages.append(user_message_payload)
                    pending_calendar_reply = answer_pending_calendar_date(submitted_text, trip_country, trip_style, trip_days, budget)
                    st.session_state.messages.append(assistant_message(pending_calendar_reply))
                    clear_chat_attachments_after_send()
                    save_and_rerun()
                elif submitted_text and wants_calendar_save(submitted_text):
                    st.session_state.messages.append(user_message_payload)
                    calendar_reply = save_latest_itinerary_to_calendar(trip_country, trip_style, trip_days, budget, st.session_state.trip_date_text, remember_missing_date=True)
                    st.session_state.messages.append(assistant_message(calendar_reply))
                    clear_chat_attachments_after_send()
                    save_and_rerun()
                elif not st.session_state.api_key_set:
                    st.error("⚠️ Set the Groq API key in Streamlit secrets or the GROQ_API_KEY environment variable first.")
                elif submitted_text and wants_trip_schedule(submitted_text) and not confirmed_destination and not st.session_state.trip_date_text.strip():
                    st.session_state.messages.append(user_message_payload)
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": "When would you like to take the trip? Once I have the timing, I can build and schedule the itinerary for you."
                    })
                    clear_chat_attachments_after_send()
                    save_and_rerun()
                else:
                    st.session_state.messages.append(user_message_payload)
                    with st.spinner("I-Travel is thinking... 🌍"):
                        try:
                            reply = chat_with_agent(submitted_text, trip_country, trip_style, trip_days, budget, st.session_state.trip_date_text, current_date_text, confirmed_destination, st.session_state.departure_time_text, st.session_state.transport_preference, st.session_state.travel_companions, attachments=attachment_payload)
                            assistant_message = {"role": "assistant", "content": reply}
                            images = [{"url": url, "caption": caption} for url, caption in build_response_images_cached(submitted_text, reply)]
                            if images:
                                assistant_message["images"] = images
                            st.session_state.messages.append(assistant_message)
                            clear_chat_attachments_after_send()
                            save_and_rerun()
                        except Exception as e:
                            st.error(f"Error: {str(e)}")

save_persisted_state()
