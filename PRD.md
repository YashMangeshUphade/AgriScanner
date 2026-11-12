# PRD — AgriScanner

## Problem
Indian smallholder farmers often detect crop diseases late, and expert advice is not easily available in the field. Late or wrong treatment causes yield loss.

## Target users
- Primary: farmers in India (starting with the Andhra Pradesh region), low technical literacy, often limited connectivity
- Secondary: agricultural extension workers; judges/evaluators during the demo

## Product
An AI-powered plant disease detection app. The user photographs a leaf and instantly gets a diagnosis, a severity label, current local weather with a spread-risk note, and AI-generated treatment guidance.

## Features (all implemented in `app.py`)
- [x] Leaf image classification across 38 classes (MobileNetV2)
- [x] Top-3 predictions with confidence bars
- [x] Severity label from confidence thresholds (SEVERE / MODERATE / MILD)
- [x] Healthy and low-confidence messaging
- [x] Live Open-Meteo weather strip (Vijayawada: temperature, humidity, rain)
- [x] Weather-based disease spread-risk assessment
- [x] Gemini AI treatment advice (model auto-detected per API key)
- [x] Image upload or camera capture
- [x] Runs on a laptop, phone access over hotspot

## User flow
1. Open app (laptop, or phone via hotspot)
2. See the current local weather at the top
3. Upload or capture a leaf photo
4. App shows: disease name, confidence, severity, and top-3 predictions
5. App shows a weather-based spread-risk note
6. For a detected disease, app shows Gemini-generated treatment advice

## Out of scope
- Training on new datasets
- Native mobile app / app store release
- Crop yield prediction

## Success criteria
- Correct predictions in the live demo (no double-preprocessing collapse)
- Clear, defensible demo for judges

## Constraints
- 6-member student team, limited GPU access
- Demo runs on a Windows laptop; phone access over hotspot
- Gemini free tier has limited quota
