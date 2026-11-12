# AGENTS.md — AgriScanner

Generic instructions for any AI coding agent. The full rules live in `CLAUDE.md`; read it first, then `TASKS.md`.

Top 3 rules:
1. Pass raw [0-255] images to the model. Never call `preprocess_input()` (double preprocessing breaks predictions).
2. Weather and Gemini calls are best-effort: wrap them so failures never crash the app.
3. No secrets in code. Ask before adding dependencies. One task at a time.
