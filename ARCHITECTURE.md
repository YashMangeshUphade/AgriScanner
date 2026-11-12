# ARCHITECTURE — AgriScanner

Everything runs in a single Streamlit script, `app.py`.

## Overview
```
 Leaf image ──► predict() ──► MobileNetV2 (raw [0-255], 224x224)
                    │
                    ├─► Softmax ──► Top-3 + confidence bars
                    ├─► Confidence thresholds ──► Severity label
                    └─► Class label ──► display name

 Open-Meteo (Vijayawada) ──► weather + spread risk
 Disease + confidence + severity ──► Gemini (auto-detected model) ──► advice
                          Streamlit UI renders all of the above
```

## Functions / components in `app.py`
| Name | Responsibility |
|---|---|
| `load_model` | Loads `agriscanner-model.keras` (cached with `@st.cache_resource`); shows an error and stops if it fails |
| `predict(image)` | Resizes to 224x224, passes raw [0-255], applies softmax, returns top-3 indices + probabilities |
| `estimate_severity(confidence)` | Maps top-1 confidence to a label: >= 90 SEVERE, >= 75 MODERATE, else MILD |
| `get_weather_risk(disease_key)` | Open-Meteo call for Vijayawada (temperature, humidity, rain) + spread-risk label; returns "Weather data unavailable" on any error |
| `resolve_gemini_model()` | Ping-tests the preferred Gemini models and returns the first one the key can use; cached per session |
| `get_gemini_analysis(...)` | Builds the prompt, calls the resolved Gemini model, returns the text; returns a helpful "unavailable" message on error |
| UI section | Streamlit page: title, weather strip, upload/camera tabs, result card, top-3 bars, risk, advice, footer |

## Key decisions
- **MobileNetV2**: small, fast, runs comfortably on a laptop.
- **Built-in preprocessing**: the model expects raw [0-255]. Calling `preprocess_input()` again causes double preprocessing and prediction collapse. This is the most common bug source.
- **Streamlit over hotspot**: fastest way to demo on a laptop and phone without building a mobile app.
- **Single file**: all logic lives in `app.py` for a simple, self-contained demo.

## Data flow (single request)
1. Image in (PIL, converted to RGB, resized to 224x224, raw [0-255])
2. `model.predict` -> softmax -> top-3
3. Map top-1 confidence to a severity label
4. Fetch weather and compute a spread-risk label
5. If the leaf is not healthy, ask Gemini for treatment advice
6. Render everything in Streamlit

## Error handling
- Model load failure: show the error and `st.stop()`
- Weather/Open-Meteo failure: show "Weather data unavailable", never crash
- Gemini failure or quota exhaustion: show an "AI Analysis unavailable" message, never crash
