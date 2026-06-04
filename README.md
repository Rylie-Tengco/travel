# I-Travel: AI Travel Planner Agent

I-Travel is a Streamlit-based AI travel planning assistant that helps users turn trip preferences, messages, images, and document files into practical travel advice, directions, day-by-day itineraries, weather checks, and Google Calendar events.

The app uses Groq for chat reasoning, image-aware requests, and voice transcription, OpenWeatherMap for current weather, local JSON persistence for saved preferences and chat history, and optional Google Calendar OAuth for saving generated itineraries.

## Project Overview

I-Travel is designed as an agentic travel planner rather than a generic chatbot. The user sets trip context in the control panel, then chats naturally with the assistant. The system uses that saved context on every response so recommendations stay aligned with the selected country, travel style, number of days, budget, timing, transport preference, and travel companions.

Key workflows include:

- Answering travel questions through a chat interface
- Accepting image and document attachments in chat
- Asking for trip timing before creating a schedule
- Creating day-by-day itineraries with morning, afternoon, and evening blocks
- Giving concrete travel logistics when the user confirms a destination
- Checking live weather for a city
- Transcribing recorded voice requests with Groq Whisper
- Saving recognized itineraries to Google Calendar
- Restoring preferences and chat history after refresh
- Showing destination images for recommendation-style responses

Built for ANLYTC4 / Analytics 4.

## System Architecture

```text
User
  |
  v
Streamlit Interface
  |-- Trip preferences
  |-- Trip timing and departure details
  |-- Voice input
  |-- Weather lookup
  |-- Chat input with file attachments
  |
  v
Session State + travel_local_state.json
  |-- Messages
  |-- Country, style, days, budget
  |-- Trip timing and transport preference
  |-- Travel companions
  |-- Theme mode
  |
  v
Agent Controller
  |-- Prompt assembly
  |-- Attachment preparation
  |-- Calendar intent detection
  |-- Missing-date clarification
  |-- Destination confirmation handling
  |-- Itinerary detection
  |-- Destination image lookup
  |
  v
External Services
  |-- Groq chat model
  |-- Groq vision-capable model for image requests
  |-- Groq Whisper transcription
  |-- OpenWeatherMap API
  |-- Google Calendar API
  |-- Wikimedia/Wikipedia image lookup
  |
  v
Rendered Output
  |-- Chat responses
  |-- User image and document attachment previews
  |-- Itineraries
  |-- Weather cards
  |-- Destination images
  |-- Calendar links
```

## Main Features

| Feature | Current implementation |
|---|---|
| Preference-aware planning | Sidebar controls set country, style, days, budget scope, currency, timing, departure time, transport preference, and companions |
| Country-scoped recommendations | The system prompt tells the agent to keep recommendations inside the selected country |
| Image and file sending | Chat input accepts images and documents so users can ask about maps, screenshots, booking details, travel notes, PDFs, DOCX files, TXT files, and Markdown files |
| Image understanding | Uploaded JPG, JPEG, PNG, and WebP files are sent to a Groq vision-capable model when included in a chat request |
| Document reading | Uploaded PDF, DOCX, TXT, and MD files are converted into text context for the AI response |
| Timing guardrail | If a user asks for a trip schedule without travel timing, the app asks when they want to take the trip before generating the itinerary |
| Destination confirmation flow | If the user confirms a recommended destination, the app asks the model for numbered travel directions from Imus, Cavite before making an itinerary |
| Conversation memory | Chat messages are stored in Streamlit session state and saved locally |
| Local persistence | `travel_local_state.json` stores preferences, theme, and chat history on the device |
| Voice input | `st.audio_input` records audio and Groq `whisper-large-v3` transcribes it |
| Push-to-talk mode | Optional auto-send submits a recording immediately after transcription |
| Weather lookup | OpenWeatherMap current weather endpoint returns temperature, condition, humidity, and wind speed |
| Calendar export | Google Calendar integration creates an all-day trip event from the latest itinerary |
| Calendar follow-up | If no exact start date is available, the app asks for one and resumes calendar saving |
| Destination images | Recommendation responses can include images found through Wikimedia/Wikipedia |
| Theme mode | Light and dark mode are available and persisted locally |

## Libraries Used

| Library | Purpose |
|---|---|
| `streamlit` | Web app interface, chat UI, forms, controls, audio input, and state |
| `groq` | LLM chat completions, vision-capable image requests, and Whisper transcription |
| `requests` | OpenWeatherMap and Wikimedia/Wikipedia HTTP requests |
| `google-api-python-client` | Google Calendar event creation |
| `google-auth-httplib2` | Google API authentication transport |
| `google-auth-oauthlib` | Google OAuth desktop flow |
| `pypdf` | Extracts readable text from uploaded PDF files |
| `python-docx` | Extracts readable text from uploaded DOCX files |

## Setup Instructions

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure API keys

Groq is required for chat and voice transcription. OpenWeatherMap is required only for the weather card. Google Calendar is optional.

Create `.streamlit/secrets.toml`:

```toml
groq_api_key = "your_groq_key"
openweather_api_key = "your_openweather_key"

# Optional if the OAuth file is not beside app.py:
google_calendar_credentials_path = "C:/path/to/google_calendar_credentials.json"
```

Or set environment variables in PowerShell:

```powershell
$env:GROQ_API_KEY = "your_groq_key"
$env:OPENWEATHER_API_KEY = "your_openweather_key"
$env:GOOGLE_CALENDAR_CREDENTIALS_PATH = "C:\path\to\google_calendar_credentials.json"
```

### 3. Optional Google Calendar setup

1. Enable the Google Calendar API in Google Cloud.
2. Create an OAuth desktop client.
3. Download the OAuth client file as `google_calendar_credentials.json`.
4. Place it beside `app.py`, or set `GOOGLE_CALENDAR_CREDENTIALS_PATH`.

The first calendar save opens the Google OAuth flow. The generated token is stored locally as `google_calendar_token.json`.

Private local files ignored by git:

- `.streamlit/secrets.toml`
- `travel_local_state.json`
- `google_calendar_credentials.json`
- `google_calendar_token.json`

### 4. Run the app

```bash
streamlit run app.py
```

## How To Use

1. Choose a country and trip preferences in the left panel.
2. Add timing such as `2026-06-10`, `next July`, or `around Christmas` if you want a schedule.
3. Chat with I-Travel in the right panel.
4. Attach an image or file if you want the assistant to use travel screenshots, maps, booking details, notes, PDFs, DOCX files, TXT files, or Markdown files.
5. Use voice input if you want to record a request instead of typing.
6. Use Quick Weather Check for current city weather.
7. After an itinerary appears, use Add to Google Calendar to create an all-day calendar event.

Attachment limits:

- Up to 5 files per chat message
- Maximum 8 MB per file
- Supported images: `.jpg`, `.jpeg`, `.png`, `.webp`
- Supported documents: `.pdf`, `.docx`, `.txt`, `.md`
- Document text is extracted and limited before being sent as AI context

## Example Prompts

- `Plan a 5-day cultural trip to Tokyo starting 2026-06-10.`
- `What should I pack for a beach trip to Palawan?`
- `Give me a budget-friendly food itinerary in Seoul.`
- `I want to go to Kyoto. How do I get there?`
- `Save this itinerary to my Google Calendar.`
- `Check the weather in Manila.`
- `Compare Cebu and Boracay for a family trip.`
- `I uploaded a map screenshot. Help me understand the route.`
- `Use this PDF travel guide to suggest a 2-day plan.`

## Project Structure

```text
travel/
├── app.py                         # Main Streamlit application
├── requirements.txt               # Python dependencies
├── README.md                      # Project setup and usage guide
├── PROJECT_REPORT.md              # Academic project report
├── .streamlit/secrets.toml         # Local secrets, ignored by git
├── travel_local_state.json         # Generated local app state, ignored by git
├── google_calendar_credentials.json# Optional OAuth client, ignored by git
└── google_calendar_token.json      # Generated OAuth token, ignored by git
```

## Test Cases

| # | Test | Expected behavior |
|---|---|---|
| 1 | Ask `Plan a 3-day trip` with no timing | App asks when the user wants to take the trip |
| 2 | Add timing, then ask for an itinerary | Agent creates a day-by-day plan with morning/afternoon/evening sections |
| 3 | Change country to Philippines and ask for Tokyo | Agent should keep recommendations within the selected country or ask to change country |
| 4 | Confirm a recommended place with `I want to go there` | Agent gives numbered travel logistics from Imus, Cavite before an itinerary |
| 5 | Use Quick Weather Check for Manila | Weather card shows live temperature, condition, humidity, and wind |
| 6 | Record a voice request | App transcribes the audio and shows a preview or auto-sends it |
| 7 | Attach a supported image and ask about it | App sends the image with the request and the assistant uses visible details in the answer |
| 8 | Attach a PDF, DOCX, TXT, or MD file | App extracts readable text and includes it as context for the assistant |
| 9 | Attach an unsupported file type or file larger than 8 MB | App shows a warning and skips the unsupported file |
| 10 | Click Add to Google Calendar without a date | App asks for an exact start date |
| 11 | Provide `2026-06-10` after the calendar prompt | App creates the calendar event if Google OAuth is configured |
| 12 | Refresh the page | Saved preferences and chat history are restored |
| 13 | Reset saved device data | Local persisted state is cleared and defaults are restored |

## Responsible AI Notes

I-Travel is a planning assistant, not an official travel authority. Users should verify visa rules, safety advisories, health requirements, prices, operating hours, transport schedules, and booking availability from official or provider sources before making final travel decisions.

The app stores preferences and chat history locally on the user's device. For privacy and file-size control, persisted chat history keeps attachment metadata but does not persist uploaded image data or extracted document text. API keys, Google OAuth credentials, and generated tokens should remain private and should not be committed to version control.

## License

Created for academic purposes under ANLYTC4.
