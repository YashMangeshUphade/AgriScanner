# GEMINI.md — AgriScanner

This project uses a shared context. Everything below is imported so Gemini CLI and Claude Code follow the same rules.

@./CLAUDE.md
@./PRD.md
@./ARCHITECTURE.md
@./TASKS.md

## Gemini-specific notes
- Give complete, copy-paste-ready code blocks, not partial snippets.
- Work on one task from TASKS.md at a time and update PROGRESS.md when finished.
- Never call `preprocess_input()` before model inference (the model already preprocesses; see the critical rules in CLAUDE.md).
