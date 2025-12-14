# 🐝 SwarmMaster

An advanced multi-agent orchestration system built with Gradio and Hugging Face Inference API. SwarmMaster deploys specialized agent swarms to tackle complex creative and technical tasks.

## Features

- **Multi-Agent Orchestration**: Automatically deploys 5-10 specialized agents for each task
- **Streaming Responses**: Real-time output as agents work
- **Professional Outputs**: Designed for high-quality, production-ready deliverables
- **Easy Web Interface**: Beautiful Gradio-based UI with advanced settings
- **Model Selection**: Choose from multiple available models
- **Configurable Parameters**: Adjust temperature and max tokens for fine-tuned control
- **Export Functionality**: Download swarm results as formatted text files
- **Comprehensive Validation**: Input validation with clear error messages
- **Structured Logging**: Built-in logging without exposing sensitive information

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Hugging Face Token

Set your Hugging Face token as an environment variable:

**Windows (PowerShell):**
```powershell
$env:HF_TOKEN="your_token_here"
```

**Windows (CMD):**
```cmd
set HF_TOKEN=your_token_here
```

**Linux/Mac:**
```bash
export HF_TOKEN="your_token_here"
```

Or create a `.env` file (requires `python-dotenv`):
```
HF_TOKEN=your_token_here
```

### 3. Run the Application

```bash
python app.py
```

The app will launch at `http://127.0.0.1:7860` by default.

## Usage

1. Enter your task in the text box
2. Click "Deploy Swarm 🚀"
3. Watch as specialized agents work on your task
4. Review the final synthesized output

## Example Tasks

- "Redesign my dashboard to be visually stunning and engaging"
- "Create a complete business plan for an AI mentorship platform"
- "Build a production-ready multi-agent research system"

## Configuration

### Model Selection

By default, SwarmMaster uses `meta-llama/Meta-Llama-3.1-70B-Instruct`. You can:

1. **Select in UI**: Use the "Advanced Settings" accordion to choose from available models
2. **Environment Variable**: Set `SWARM_MODEL` to change the default:
   ```bash
   export SWARM_MODEL="meta-llama/Meta-Llama-3.1-8B-Instruct"
   ```

### Advanced Parameters

Configure via environment variables or the UI:

- `SWARM_TEMPERATURE`: Sampling temperature (default: 0.7, range: 0.0-2.0)
- `SWARM_MAX_TOKENS`: Maximum tokens to generate (default: 4096, max: 8192)

## Testing

Install development dependencies:

```bash
pip install -r requirements-dev.txt
```

Run the test suite:

```bash
pytest
```

The test suite includes:
- **Prompt building tests** (`tests/test_prompts.py`): Validates prompt construction and formatting
- **API client tests** (`tests/test_api.py`): Tests SwarmClient with mocked Hugging Face API calls
- **Integration tests** (`tests/test_app.py`): Tests `run_swarm` function with input validation and error handling
- **Validation tests** (`tests/test_validation.py`): Tests input validation for tasks, temperature, max_tokens, and models

All tests use mocking to avoid actual API calls during testing. The suite includes 36 tests covering all major functionality.

## Deployment

### Hugging Face Spaces

1. Create a new Space
2. Upload `app.py`, `requirements.txt`, and the `utils/` directory
3. Add `HF_TOKEN` as a Secret in Space settings
4. Deploy!

## License

MIT

