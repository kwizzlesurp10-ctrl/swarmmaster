# 🚀 SwarmMaster Quick Start Guide

## Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

## Configuration

Set your Hugging Face token:

**Windows (PowerShell):**
```powershell
$env:HF_TOKEN="your_token_here"
```

**Linux/Mac:**
```bash
export HF_TOKEN="your_token_here"
```

## Run the Application

```bash
python app.py
```

The app will launch at `http://127.0.0.1:7860`

## First Task

Try this example:
```
Create a complete business plan for an AI mentorship platform
```

## UI Features

1. **Task Input**: Enter your task in the text box (3+ characters)
2. **Advanced Settings**: Click to expand and configure:
   - **Model**: Select from available models
   - **Temperature**: Control creativity (0.0 = deterministic, 2.0 = very creative)
   - **Max Tokens**: Set response length (256-8192)
3. **Deploy Swarm**: Click to start the multi-agent process
4. **Clear**: Reset the chat and input
5. **Export Results**: Download the swarm output as a text file

## Troubleshooting

### "HF_TOKEN not set" Error
- Make sure you've set the `HF_TOKEN` environment variable
- Restart your terminal/IDE after setting the variable

### Import Errors
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Use a virtual environment for isolation

### Model Access Errors
- Verify your Hugging Face token has access to the selected model
- Some models may require special permissions or paid access

## Testing

Run the test suite:
```bash
pip install -r requirements-dev.txt
pytest
```

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Check [AGENTS.md](AGENTS.md) for development guidelines
- Customize models in `utils/config.py`
- Extend prompts in `utils/prompts.py`

