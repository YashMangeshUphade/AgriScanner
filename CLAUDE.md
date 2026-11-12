# CLAUDE.md — AgriScanner

Read this file first in every session. Detailed docs: @PRD.md, @ARCHITECTURE.md, @TASKS.md, @DESIGN.md, @PROGRESS.md

## Project
AgriScanner is a 6-member team project: an AI-powered plant disease detection system for Indian farmers. A leaf image goes in; the app returns the top-3 disease predictions with confidence, a severity label, live local weather, and Gemini-generated treatment advice.

## Tech stack
- Model: MobileNetV2 transfer learning, TensorFlow/Keras, loaded from `agriscanner-model.keras`
- Dataset: New Plant Diseases Dataset (38 classes)
- Demo app: Streamlit (runs on a Windows laptop, phone accessed over hotspot)
- External: Open-Meteo API (live weather, Vijayawada), Gemini API (treatment advice; model auto-detected per key)

## Critical rules (do not break)
1. **The model has preprocessing built in. Pass raw [0-255] images directly. NEVER call `preprocess_input()` before inference** — it causes double preprocessing and prediction collapse.
2. Do not commit API keys. Use `.env` / `st.secrets`. Never edit or print `.env`.
3. Do not retrain or overwrite the trained model file unless the task explicitly says so.
4. Ask before adding new dependencies.
5. Always give complete, copy-paste-ready files or code blocks, not partial snippets.

## Commands
- **Quick Launch**: Double-click `run_agriscanner.bat` to start the app instantly.
- Install: `pip install -r requirements.txt`
- Run demo: `streamlit run app.py`
- Run on phone: start Streamlit with `--server.address 0.0.0.0`, connect the phone via the laptop hotspot, open `http://<laptop-ip>:8501`

## Folder structure
```
agriscanner/
├── CLAUDE.md / GEMINI.md / AGENTS.md
├── PRD.md  ARCHITECTURE.md  TASKS.md  DESIGN.md  PROGRESS.md
├── app.py                   # the entire app (login + UI + inference + weather + Gemini)
├── agriscanner-model.keras  # trained model
├── requirements.txt         # pinned dependencies
├── run_agriscanner.bat      # Windows one-click launcher
├── .gitignore               # excludes secrets and caches
└── .streamlit/
    └── secrets.toml         # login credentials (users), git-ignored
```

## Conventions
- Python 3.x, PEP 8, type hints on new functions, short docstrings
- All app logic currently lives in `app.py`, in this order: constants -> helper functions -> UI
- `class_names` must match the training class order exactly; `display_names` is the human-readable label for the same index
- Show confidence as raw softmax probabilities (as a percentage)

## Workflow
- Read TASKS.md, work on ONE task at a time, tick it off when done
- After finishing, run the app and confirm it works before saying done
- Update PROGRESS.md at the end of every session
