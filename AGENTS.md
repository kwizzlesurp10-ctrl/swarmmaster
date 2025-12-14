Repository Guidelines

## Project Structure & Module Organization
- `app.py`: Gradio UI, Hugging Face client setup, and the streaming `run_swarm` orchestrator.
- `requirements.txt`: Runtime dependencies for the web app and Hugging Face SDK.
- `README.md`: Setup, deployment, and usage notes; keep it aligned with any new options you add.
- Add new modules near `app.py`; factor shared helpers (e.g., prompt builders, API utilities) into a small `utils/` module to keep the UI layer lean.

## Build, Test, and Development Commands
- `pip install -r requirements.txt` — install required packages (use a virtualenv if desired).
- `python app.py` — launch the Gradio app locally at http://127.0.0.1:7860.
- `pytest` — run the test suite once added; ensure it passes before opening a PR.

## Coding Style & Naming Conventions
- Follow PEP 8 with 4-space indentation; add type hints for public functions.
- Use `snake_case` for functions/variables, `PascalCase` for classes, and `UPPER_SNAKE_CASE` for constants such as `MODEL` or prompt strings.
- Keep Gradio callbacks minimal and side-effect free; isolate API calls and prompt assembly in helpers to simplify testing.
- Keep multiline prompts in triple-quoted strings; avoid embedding secrets or runtime-specific values in code.

## Testing Guidelines
- Framework: `pytest` (add to `requirements-dev.txt` when introduced).
- Name tests `test_*.py`; place beside the code they cover or under `tests/`.
- Mock Hugging Face calls when exercising `run_swarm`; assert streaming chunks accumulate correctly and errors surface to the UI.
- Cover input validation paths (empty task, missing `HF_TOKEN`) and any prompt/parameter construction logic.

## Commit & Pull Request Guidelines
- Commit messages: prefer Conventional Commits (`feat:`, `fix:`, `docs:`, `chore:`); keep subjects under 72 characters.
- Pull requests: include a summary, manual test notes (commands run), and screenshots/GIFs for UI changes. Link related issues.
- Keep changes focused; call out any refactors or prompt changes that affect model behavior.

## Security & Configuration Tips
- Do not commit `HF_TOKEN` or other secrets. Use environment variables or a local `.env` excluded by `.gitignore`; set secrets in deployment targets (e.g., Hugging Face Spaces).
- Validate model access before shipping; document model changes or new parameters in `README.md`.
- Avoid logging sensitive tokens or request bodies; prefer structured debug logs without secrets when needed.

## Architecture Overview
- `run_swarm` builds a task-specific prompt and streams responses from `InferenceClient`; chunks are accumulated and rendered in the Gradio `Chatbot`.
- UI is a single `Blocks` layout with a textbox, button, examples, and chatbot; extend it by following the existing row/column structure to keep layout consistent.
