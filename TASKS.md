# TASKS — AgriScanner

Rule for the AI: do ONE unchecked task at a time, test it, tick it, then update PROGRESS.md.

## Done (current scope — matches `app.py`)
- [x] 38-class leaf disease classification (MobileNetV2, loaded from `agriscanner-model.keras`)
- [x] Raw [0-255] inference with top-3 predictions and confidence bars
- [x] Severity label from confidence thresholds (SEVERE / MODERATE / MILD)
- [x] Healthy and low-confidence messaging
- [x] Open-Meteo weather strip (Vijayawada: temperature, humidity, rain)
- [x] Weather-based disease spread-risk assessment
- [x] Gemini AI treatment advice (model auto-detected per API key)
- [x] Image upload and camera capture
- [x] Streamlit demo, phone access over hotspot

## Next
- None. The scope is exactly the feature set implemented in `app.py`.
