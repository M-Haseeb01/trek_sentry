# Trek Sentry

Overview

Trek Sentry is a real-time travel safety and disaster awareness platform that aggregates live global data—weather, floods, storms, traffic conditions, earthquakes, and air quality—and converts it into clear, actionable alerts. Using Google Gemini 3’s reasoning capabilities, the system simplifies complex technical data into easy-to-understand guidance, helping users decide whether it’s safe to travel.

Problem

During emergencies, travelers are often overwhelmed by fragmented, technical, and hard-to-interpret information spread across multiple sources. Incidents like the Murree 2022 snowstorm showed how lack of clear, centralized guidance can lead to confusion and dangerous outcomes.

Solution

Trek Sentry centralizes live global data and uses Gemini 3 to:

Analyze real-time conditions

Summarize the situation in plain language

Provide preparation tips and travel recommendations

Translate alerts into 100+ languages

Deliver optional audio alerts via text-to-speech

All insights are presented in one simple interface.

Gemini 3 Integration

Google Gemini 3 is central to Trek Sentry. It performs intelligent reasoning over live data streams to generate situation summaries, risk assessments, and recommendations. Gemini also powers multilingual translation, ensuring alerts are accessible globally. The AI-generated outputs are further passed to a TTS system for audio delivery.

Impact

Trek Sentry is designed for students, travelers, and millions of people moving globally. By delivering early, understandable, and actionable alerts, it helps users make safer decisions and reduces the risk of incidents caused by misinformation or delayed understanding.

Tech Stack

HTML, CSS, JavaScript, Python, Flask, Google Gemini 3, Open-Meteo APIs, USGS Earthquake API, aiohttp, Hugging Face, Piper TTS, Vercel

Local Setup 

Clone repository
Install dependencies
Add API keys
Run Flask server
