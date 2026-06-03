# I-Travel AI Travel Planner Agent: Project Report

## Introduction

I-Travel is an AI-powered travel planning system implemented as a Streamlit web application. It helps users plan trips through a conversational interface supported by structured travel preferences, live weather lookup, voice transcription, local memory, destination-image enrichment, and optional Google Calendar export.

The project demonstrates an agentic AI workflow because the system does more than answer isolated prompts. It maintains user context, applies guardrails before producing schedules, uses external services when needed, and supports a practical planning flow from early recommendations to itinerary scheduling. The current implementation is contained mainly in `app.py` and uses Groq for language-model reasoning and voice transcription, OpenWeatherMap for current weather, and the Google Calendar API for event creation.

## Problem Statement

Travel planning usually requires a user to gather information from several places: destination guides, weather websites, budget notes, transport options, calendar tools, and personal constraints. This can make the planning process slow and fragmented, especially when the user is still deciding where to go or when they need an organized schedule.

I-Travel addresses this problem by acting as a focused AI travel planner. The user sets travel context such as country, travel style, number of days, budget, trip timing, departure time, preferred transport, and companions. The assistant then uses those values as active planning constraints in every response. Instead of giving generic travel advice, it adapts answers to the user's selected preferences and keeps recommendations inside the chosen country.

The system also supports real travel-planning actions. It can check live weather, transcribe spoken requests, remember prior chat context after a page refresh, provide detailed directions when a user confirms a destination, and save generated itineraries to Google Calendar. These features make the application closer to a task-oriented travel assistant than a basic chatbot.

## Agent Design

I-Travel is designed around a clear role: a friendly AI travel planner that gives short answers for simple questions and more detailed day-by-day plans only when the user explicitly asks for a trip schedule or itinerary. The system prompt gives the model behavioral rules and the current trip context before each Groq chat completion call.

The main agent behaviors are:

1. **Preference-aware reasoning.** The app collects country, travel style, trip length, budget scope, currency, budget amount, travel timing, departure time, transport preference, and travel companions. These values are inserted into the model prompt.

2. **Country constraint.** The agent is instructed to keep recommendations inside the selected country. If the selected country conflicts with the user's request, the model should adapt the answer back to the chosen country instead of freely recommending global destinations.

3. **Timing clarification.** If the user asks for a schedule, itinerary, trip, or vacation plan but has not provided trip timing, the app asks when the user wants to take the trip before calling the LLM for a full schedule.

4. **Destination confirmation flow.** If the user confirms that they want to visit a specific destination, the app treats that as a logistics request first. It asks the model for numbered travel directions from Imus, Cavite, Philippines to the confirmed destination, including likely transport modes, airports, terminals, stations, transfers, landmarks, and preparation notes.

5. **Conversation memory.** User and assistant messages are stored in Streamlit session state and persisted in `travel_local_state.json`, so the conversation and preferences can be restored after refresh.

6. **Tool usage.** The app uses OpenWeatherMap for live weather, Groq Whisper for audio transcription, Wikimedia/Wikipedia APIs for destination images, and Google Calendar for itinerary export.

7. **Calendar intent handling.** When the user asks to save an itinerary to a calendar, the app finds the latest itinerary-like assistant message. If an exact start date is missing, it asks for one and resumes the calendar save after the user provides a valid date.

The central chat model is `llama-3.3-70b-versatile`, and voice transcription uses `whisper-large-v3`.

## System Architecture

I-Travel follows a layered architecture:

```text
User
  |
  v
Streamlit Interface
  |-- Trip preferences
  |-- Timing and transport controls
  |-- Voice input
  |-- Weather check
  |-- Chat input
  |
  v
Session State and Local Persistence
  |-- messages
  |-- country, style, days, budget
  |-- trip date and departure time
  |-- transport preference and companions
  |-- theme mode
  |
  v
Agent Controller Logic
  |-- prompt assembly
  |-- destination confirmation detection
  |-- missing timing guardrail
  |-- calendar intent detection
  |-- itinerary detection
  |-- response image lookup
  |
  v
External Services
  |-- Groq chat completions
  |-- Groq Whisper transcription
  |-- OpenWeatherMap current weather
  |-- Google Calendar API
  |-- Wikimedia/Wikipedia image APIs
  |
  v
Rendered Output
  |-- chat responses
  |-- weather cards
  |-- destination images
  |-- itinerary calendar controls
  |-- Google Calendar links
```

The interface is split into two main columns. The left panel contains the hero section, API-key loading status, light/dark mode toggle, trip preferences, timing fields, voice input, weather lookup, reset controls, and example prompts. The right panel contains the fixed chat interface with user and assistant messages, generated destination images, and Google Calendar controls when an itinerary is detected.

Streamlit reruns the script after interactions. State is preserved through `st.session_state`, and selected values are written to `travel_local_state.json` at the end of each run.

## Implementation

The application is implemented in `app.py`. It imports Streamlit, Groq, Requests, Google Calendar client libraries, and standard Python utilities for dates, JSON, hashing, temporary files, paths, HTML escaping, and regular expressions.

### Configuration and State

The function `load_api_key` reads credentials from Streamlit secrets first and then from environment variables. Supported configuration names include:

- `groq_api_key` or `GROQ_API_KEY`
- `openweather_api_key` or `OPENWEATHER_API_KEY`
- `google_calendar_credentials_path` or `GOOGLE_CALENDAR_CREDENTIALS_PATH`

The local persistence file is `travel_local_state.json`. The persisted state includes:

- Chat messages
- Selected country
- Travel style
- Number of days
- Budget scope, currency, and amount
- Trip timing
- Departure time
- Transport preference
- Travel companions
- Theme mode

The default country is Philippines, the default travel style is Adventure, the default trip length is five days, and the default currency is PHP.

### Prompting and Chat

The system prompt defines I-Travel's behavior. It tells the model to respond conversationally, avoid long plans unless requested, keep suggestions inside the selected country, ask for timing before scheduling, and respect budget limits. The `chat_with_agent` function builds the final system message by adding the current date and current user preferences, then appends conversation history and the latest user message before calling Groq.

If a confirmed destination is detected, `chat_with_agent` adds a special instruction block. This block changes the expected response from an itinerary to a concrete numbered travel plan from Imus, Cavite. This helps the system produce useful logistics before moving into day-by-day scheduling.

### Weather Lookup

The `get_weather` function calls OpenWeatherMap's current weather endpoint with metric units. When the city is found, it returns the city name, temperature, weather description, humidity, wind speed, and an emoji based on the weather condition. The left panel renders these values in a weather card.

### Voice Input

Voice input uses Streamlit's `st.audio_input`. The app hashes the recorded audio to avoid processing the same recording repeatedly across reruns. The `transcribe_voice_intent` function writes the audio bytes to a temporary file and sends it to Groq's `whisper-large-v3` transcription model.

The user can preview and edit the transcript before sending it. If auto-send is enabled, the transcript is submitted immediately after transcription, creating a push-to-talk style workflow.

### Google Calendar Export

The calendar integration uses OAuth credentials and the Google Calendar API. If the Google libraries and OAuth file are available, the app can create all-day events in the user's primary calendar.

The app detects itinerary-like assistant responses with `is_itinerary_text`, which looks for day markers, date markers, and morning/afternoon/evening structure. When such a message appears, the interface shows an Add to Google Calendar button.

The function `build_trip_calendar_event` builds the event summary, location, description, start date, and end date. The description includes the trip preferences and the itinerary text. If the trip start date is missing, a `MissingTripStartDate` exception triggers a follow-up message asking the user for an exact date such as `2026-06-10`.

### Destination Images

For recommendation-style responses, the app attempts to identify destination or place names and fetch related images through Wikimedia/Wikipedia. Found images are shown below the assistant response with captions. This improves the visual usefulness of recommendations while keeping the primary planning logic text-based.

### Interface and Styling

The app uses custom CSS for a polished dark/light interface. It includes a fixed chat panel, styled message cards, weather cards, quick snapshot cards, animated transitions, and a local theme toggle. JavaScript is used to keep the chat panel fixed and automatically scroll to the latest message.

## Testing and Evaluation

Testing should cover both functional behavior and response quality. Because the app depends on LLM output and external APIs, evaluation should combine manual testing with integration checks.

Important functional tests include:

1. **Preference handling.** Changing country, style, days, budget, date, departure time, transport preference, and companions should influence the next answer.

2. **Missing timing guardrail.** If the user asks for an itinerary without trip timing, the app should ask when the trip will happen before generating a schedule.

3. **Country constraint.** If the selected country is Philippines and the user asks for Japan, the assistant should keep the response within the selected country or clarify the mismatch.

4. **Destination confirmation.** If the assistant recommends a place and the user says "I want to go there," the next response should provide logistics from Imus, Cavite rather than immediately creating a day-by-day itinerary.

5. **Weather lookup.** A valid city and valid OpenWeatherMap key should return weather details. Missing keys or invalid cities should show helpful messages.

6. **Voice transcription.** Recorded audio should produce a transcript. Preview mode should allow editing, sending, or discarding. Auto-send mode should submit the transcript directly.

7. **Calendar save.** When an itinerary exists, the Add to Google Calendar button should create an all-day event if Google OAuth is configured and a start date is available.

8. **Calendar date follow-up.** If the user asks to save an itinerary but no exact date is available, the app should ask for a date and then complete the save after receiving one.

9. **Persistence.** Refreshing the app should restore saved preferences and chat history from `travel_local_state.json`.

10. **Reset controls.** Clear Chat should remove messages, and Reset Saved Device Data should restore persisted values to defaults.

Qualitative evaluation should focus on whether responses are useful, realistic, and aligned with the selected preferences. A good response should reflect the selected travel style, respect the budget, fit the trip length, and avoid overclaiming on topics that may change.

## Responsible AI Reflection

I-Travel can reduce the effort required to plan a trip, but it should not be treated as an official source for high-impact travel decisions. Travel advice can affect money, safety, legal compliance, and scheduling, so the assistant should be transparent about uncertainty.

A key risk is hallucination. The Groq language model may produce plausible but incorrect or outdated information about visas, safety, transportation, prices, attraction hours, hotel availability, or local rules. The app partially reduces this risk by narrowing the model's role, passing structured user preferences, asking for missing timing before schedules, and using live weather for current weather conditions. However, users should still verify important details with official government, airline, transit, tourism, and booking sources before making final decisions.

Bias is another concern. AI-generated travel recommendations may favor popular destinations and mainstream activities while overlooking local communities, accessibility needs, sustainability concerns, or less commercial options. The system's preference controls help personalize the response, but future versions could add accessibility, sustainability, dietary, safety, and pace preferences.

Privacy also matters. The app saves chat history and trip preferences locally in `travel_local_state.json`. This improves continuity but means travel information remains on the user's device. API keys, Google OAuth credentials, and tokens are private files and are ignored by git through `.gitignore`.

Overall, I-Travel demonstrates responsible AI practices through scoped prompting, user-controlled preferences, local persistence, reset controls, and explicit reliance on external APIs where appropriate. It should be presented as a planning assistant rather than an authoritative travel source.

## Handling AI Hallucinations

Hallucinations are especially important in a travel planner because the user may rely on the assistant for schedules, transportation details, entry rules, estimated costs, operating hours, and safety expectations. I-Travel manages this risk in several ways:

- The system prompt defines a narrow travel-planner role.
- Structured preferences reduce vague or unrelated answers.
- The app asks for missing timing before creating schedules.
- Weather is fetched from OpenWeatherMap rather than guessed by the model.
- Calendar creation uses the latest detected itinerary text and explicit date parsing instead of relying only on free-form model output.
- The confirmed-destination flow asks for practical logistics while reminding users to check schedules, fares, traffic, weather, operating hours, parking, and reservations.

Future improvements could include official-source browsing for visa and safety questions, source links for factual travel claims, stronger validation for transport schedules and costs, and automated tests for the guardrail logic.

## Conclusion

I-Travel successfully demonstrates an agentic AI travel planning system. It combines a Streamlit chat interface with Groq reasoning, preference memory, live weather lookup, voice transcription, destination-image enrichment, Google Calendar export, and local persistence.

The project shows how an AI assistant can be designed around a specific workflow instead of acting as a general chatbot. By combining structured user preferences with targeted controller logic and external services, I-Travel supports a realistic planning process from initial questions to a saved trip schedule.

Future work could add document uploads, official-source verification, route and fare APIs, hotel or flight search, collaborative planning, accessibility filters, and automated regression tests. Even in its current form, I-Travel provides a complete proof of concept for a practical AI travel planner agent.
