# I-Travel AI Travel Planner Agent - PowerPoint Content

## Slide 1: Introduction

### Title
I-Travel: AI Travel Planner Agent

### Slide Content
- An AI-powered travel planning system built with Streamlit
- Helps users plan trips through a conversational travel assistant
- Uses user preferences such as country, travel style, trip length, budget, timing, transport, and companions
- Supports itinerary generation, image and file sending, weather lookup, voice input, destination images, local memory, and Google Calendar export

### Speaker Notes
Good day everyone. Today, I will present our system called I-Travel, which stands for an AI Travel Planner Agent.

I-Travel is a system made to help users plan their trips in an easier and more organized way. It is built as a web application using Streamlit, and it works like a travel assistant that the user can talk to. The user can ask questions, request travel recommendations, and generate trip plans based on their preferences.

What makes I-Travel useful is that it does not only answer like a normal chatbot. It also considers the details selected by the user, such as the country they want to visit, their travel style, number of days, budget, travel date, transport preference, and who they are traveling with. Because of this, the system can give answers that are more connected to the user's actual travel needs.

The system also includes other helpful features. It can create itineraries, accept image and file attachments, check current weather, accept voice input, show destination images, remember the user's previous settings, and save the itinerary to Google Calendar. Overall, I-Travel is designed to make travel planning faster, simpler, and more convenient for users.

---

## Slide 2: Problem That the System Solves

### Title
The Travel Planning Problem

### Slide Content
- Travel planning is often time-consuming and scattered across different platforms
- Users need to check destinations, schedules, weather, budget, transport options, and calendars separately
- Users may also have travel screenshots, maps, booking details, or notes that are hard to combine with the main plan
- Generic chatbots may give answers that do not match the user's country, budget, travel style, or schedule
- Users may forget important planning details such as trip dates, transport needs, and weather conditions
- I-Travel solves this by combining personalized AI planning with practical travel tools in one system

### Speaker Notes
The problem that our system solves is the difficulty of planning a trip. Usually, when a person wants to travel, they need to do many things separately. They may search for destinations on one website, check the weather on another website, calculate the budget manually, look for transportation options, and then organize everything in a calendar.

This can take a lot of time, especially for users who do not yet have a clear plan. Sometimes, they know that they want to travel, but they are not sure where to go, what activities to do, how many days they should spend, or how much money they need. Because the information is scattered, the planning process can feel confusing and tiring.

Another problem is that general AI chatbots may give answers that are too broad. For example, they might suggest places that do not match the user's selected country, budget, travel style, or schedule. This means the user still needs to adjust the answer manually.

I-Travel helps solve this by putting the planning process in one system. The user can set their preferences, ask travel questions, upload travel images or files, generate an itinerary, check the weather, use voice input, and save the final plan to Google Calendar. In simple terms, I-Travel helps users move from "I want to travel" to "Here is my organized travel plan."

---

## Slide 3: How the System Processes a Request

### Title
Simple Request Process Flow

### Slide Content
- User Input
- Streamlit App
- Request Check
- Groq AI Model, Vision Model, or External API
- System Response
- Displayed to User

### Request Flow Diagram
```text
User Input
   |
   v
Streamlit App
   |
   v
Request Check
   |
   v
Groq AI Model / Vision Model / External API
   |
   v
System Response
   |
   v
Displayed to User
```

### Speaker Notes
This slide shows the simple process of how I-Travel handles a user's request.

First, the process starts with the user input. The user can type a message in the chat or use voice input. For example, the user can ask, "Plan a 3-day trip in the Philippines," or "Check the weather in Manila."

Second, the request goes to the Streamlit app. Streamlit is the main interface of the system. It receives the user's message and also keeps the user's selected travel preferences, such as country, budget, number of days, travel style, and travel date.

Third, the system performs a request check. This means the system checks what kind of request the user sent. It identifies if the user is asking for a travel recommendation, an itinerary, help with an uploaded image or file, a weather update, a voice transcription, or a Google Calendar action.

Fourth, the system sends the request to the correct service. If the user needs an AI-generated answer, the request goes to the Groq AI model. If the user uploads an image, the system can use a vision-capable Groq model to understand visible details. If the user uploads a document, the system extracts readable text and adds it to the request. If the user asks for weather, the system uses an external weather API. If the user wants to save an itinerary, the system uses the Google Calendar API.

Fifth, the system receives the result and prepares the response. The response can be a travel recommendation, a day-by-day itinerary, an explanation of an uploaded image or file, weather details, a voice transcript, or a calendar confirmation.

Lastly, the final response is displayed to the user in the chat interface. In simple terms, the flow is: the user sends a request, the app checks it, the system uses Groq or another API, and then the answer is shown back to the user.

---

## Slide 4: Demonstration of System Features

### Title
Feature Demonstration

### Slide Content
- Trip preference controls
- AI travel chat
- Image and file sending
- Itinerary generation with timing guardrail
- Destination confirmation and travel directions
- Quick weather check
- Voice input and transcription
- Destination image display
- Google Calendar export
- Local persistence and reset controls
- Light and dark theme mode

### Demo Procedure
1. Open the Streamlit application.
2. Show the left panel and explain the trip preference controls.
3. Set an example preference:
   - Country: Philippines
   - Style: Adventure or Cultural
   - Days: 3 to 5 days
   - Budget: PHP amount
   - Trip timing: example date such as 2026-06-10
   - Transport preference and companions
4. Ask the assistant a recommendation question:
   - "Recommend places for a 3-day adventure trip in the Philippines."
5. Show that the response follows the selected country, style, budget, and trip length.
6. Demonstrate image or file sending:
   - Attach a travel screenshot, map, PDF, DOCX file, TXT note, or Markdown note.
   - Ask: "Use this attachment to help me plan."
   - Show that the assistant uses details from the image or file.
7. Ask for a full itinerary:
   - "Make a 3-day itinerary for this trip."
8. Point out the morning, afternoon, and evening structure.
9. Demonstrate the timing guardrail by clearing the trip date and asking:
   - "Plan a trip for me."
   - Show that the system asks when the user wants to take the trip.
10. Confirm a recommended destination:
   - "I want to go there."
   - Show that the system provides travel logistics and directions first.
11. Use the weather feature:
   - Enter a city such as Manila, Cebu, or Tokyo.
   - Show temperature, weather condition, humidity, and wind speed.
12. Use voice input:
   - Record a short request.
   - Show the transcript preview or auto-send behavior.
13. After an itinerary appears, click Add to Google Calendar.
14. Show the generated calendar confirmation or explain that OAuth credentials are required.
15. Refresh the app and show that saved preferences and chat history are restored.
16. Show the theme toggle and reset controls.

### Demo Script
For the demonstration, I will first open the I-Travel application. On the left side of the screen, we can see the control panel. This is where the user can set their travel preferences. For example, the user can choose the country, travel style, number of days, budget, travel date, departure time, transport preference, and travel companions.

These settings are important because the assistant uses them when generating answers. For example, if I choose the Philippines as the country and set the travel style to adventure, the system should recommend places and activities that match those choices.

Next, I will type a sample question such as, "Recommend places for a 3-day adventure trip in the Philippines." After sending the message, the AI assistant will generate recommendations based on the selected preferences. Here, we can show that the answer is not random. It follows the country, style, number of days, and budget set by the user.

I will also show the new image and file sending feature. The user can attach a travel image, such as a map screenshot, or a file, such as a PDF, DOCX file, TXT note, or Markdown note. After attaching the file, the user can ask the assistant to use it for planning. For images, the system can understand visible details. For documents, the system extracts readable text and uses it as extra context for the response.

After that, I will ask the system to create a full itinerary. The system will provide a day-by-day travel plan, usually divided into morning, afternoon, and evening activities. This makes the plan easier to follow because the user can clearly see what to do each day.

I will also demonstrate the timing guardrail. If I remove the trip date and ask the system to plan a trip, it will ask when I want to take the trip first. This shows that the system tries to avoid creating an incomplete schedule.

Another feature is destination confirmation. If the assistant recommends a place and I type, "I want to go there," the system will give travel directions and logistics first instead of immediately creating another itinerary. This is useful because the user may need to know how to reach the destination before planning the full schedule.

Next, I will show the weather feature. I can enter a city name, such as Manila or Cebu, and the system will display the current temperature, weather condition, humidity, and wind speed.

The system also supports voice input. The user can record a request, and the system will transcribe it into text. This is helpful for users who prefer speaking instead of typing.

Finally, after generating an itinerary, I can click the Add to Google Calendar button. If the Google Calendar setup is available, the system can save the trip schedule as a calendar event. I can also refresh the page and show that the system remembers the user's preferences and chat history through local storage.

---

## Slide 5: Key Challenges and Limitations

### Title
Challenges and Current Limitations

### Slide Content
- **Accuracy & Verification**: AI suggestions need manual verification (prices, dates, opening hours)
- **External API Dependencies**: Relies on third-party services (Groq, OpenWeather, Google Calendar)
- **No Direct Booking**: Only plans itineraries; does not book flights, hotels, or transportation

### Speaker Notes
Even though I-Travel has many useful features, it still has some important limitations. For this presentation, I will focus on the top three.

The first limitation is Accuracy and Verification. The AI can give helpful suggestions, but details like prices, schedules, and opening hours can change. Users should check official sources before making final decisions.

The second limitation is External API Dependencies. Key features rely on third-party services—such as Groq for AI chat, OpenWeather for weather data, and Google Calendar for exporting. If these APIs are down or not configured, those features won't work.

The third limitation is No Direct Booking. The system is a planner, not a booking platform. It cannot book flights, hotels, or transport, so users must still use official websites for their final reservations.

Because of these limitations, I-Travel should be used as a planning assistant, helping to organize ideas, while users confirm the final details.

### Possible Improvements
- Add official source links for factual travel claims
- Integrate route, fare, hotel, and flight search APIs
- Add accessibility, dietary, sustainability, and safety preferences
- Add stronger validation for dates, transport schedules, and estimated costs

---

## Slide 6: Outro

### Title
Conclusion

### Slide Content
- I-Travel demonstrates a practical AI travel planning assistant
- It combines conversation, preferences, image/file sending, live weather, voice input, images, memory, and calendar export
- The system reduces the effort needed to create a personalized travel plan
- It works best as a planning assistant, while final travel decisions should still be verified

### Speaker Notes
To conclude, I-Travel is an AI-powered travel planning system that helps users create a more organized travel plan. It combines a conversational assistant with useful travel features, such as preference-based recommendations, itinerary generation, image and file sending, live weather checking, voice input, destination images, local memory, and Google Calendar export.

The main goal of the system is to make travel planning easier. Instead of using many separate tools, the user can interact with one system that helps them plan based on their own preferences. This can save time and make the planning process more convenient.

I-Travel is also different from a simple chatbot because it uses structured information from the user. It remembers the selected country, travel style, budget, number of days, schedule, and other details. Because of that, the answers can be more personalized and more useful.

However, the system still has limitations. Some travel details must still be verified from official sources, especially information related to safety, prices, schedules, bookings, and travel requirements. So, the best way to describe I-Travel is that it is a helpful travel planning assistant, but not a replacement for official travel information.

Overall, I-Travel shows how AI can be used to support a real-life task like travel planning. It helps users go from a simple travel idea to a clearer and more organized itinerary.

### Closing Line
Thank you for listening. This is I-Travel, an AI Travel Planner Agent designed to make travel planning easier, smarter, and more organized.
