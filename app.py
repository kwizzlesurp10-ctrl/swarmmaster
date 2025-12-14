import gradio as gr
import os
from typing import Generator, Tuple

from utils import (
    SwarmClient,
    build_swarm_prompt,
    SwarmConfig,
    SwarmLogger,
    ValidationError,
    APIError,
    ConfigurationError,
)
from utils.validation import validate_task, validate_temperature, validate_max_tokens


def run_swarm(
    task: str,
    model: str,
    temperature: float,
    max_tokens: int,
) -> Generator[str, None, None]:
    """
    Execute a swarm task and stream the response.
    
    Args:
        task: The user's task description.
        model: The model identifier to use.
        temperature: Sampling temperature (0.0-2.0).
        max_tokens: Maximum tokens to generate.
        
    Yields:
        Response chunks as strings.
    """
    # Validate inputs
    is_valid, error_msg = validate_task(task)
    if not is_valid:
        yield f"❌ {error_msg}"
        return
    
    is_valid, error_msg = validate_temperature(temperature)
    if not is_valid:
        yield f"❌ {error_msg}"
        return
    
    is_valid, error_msg = validate_max_tokens(max_tokens)
    if not is_valid:
        yield f"❌ {error_msg}"
        return
    
    # Validate token
    is_valid, error_msg = SwarmConfig.validate_token()
    if not is_valid:
        yield f"❌ Error: {error_msg}"
        SwarmLogger.log_error("ConfigurationError", error_msg, task)
        return
    
    # Initialize client with selected model
    try:
        swarm_client = SwarmClient(model=model, token=SwarmConfig.get_token())
    except Exception as e:
        error_msg = f"Failed to initialize client: {str(e)}"
        yield f"❌ {error_msg}"
        SwarmLogger.log_error("ConfigurationError", error_msg, task)
        return
    
    # Build prompt and log
    full_prompt = build_swarm_prompt(task)
    SwarmLogger.log_swarm_start(task, model)
    
    yield "🚀 Deploying Builder Swarm...\n\n"
    
    try:
        accumulated_length = 0
        for chunk in swarm_client.stream_swarm_response(
            full_prompt,
            max_tokens=max_tokens,
            temperature=temperature,
        ):
            accumulated_length = len(chunk)  # chunk is already accumulated, so this is the total length
            yield chunk
        
        SwarmLogger.log_swarm_complete(task, accumulated_length)
        
    except APIError as e:
        error_msg = f"API error: {str(e)}"
        yield f"❌ {error_msg}\n\nPlease check your HF_TOKEN and model access."
        SwarmLogger.log_error("APIError", error_msg, task)
    except Exception as e:
        error_msg = f"Unexpected error: {str(e)}"
        yield f"❌ {error_msg}\n\nPlease check your configuration and try again."
        SwarmLogger.log_error("UnexpectedError", error_msg, task)


def clear_chat() -> Tuple[list, str]:
    """Clear the chatbot and reset the task input."""
    return [], ""


def export_results(chatbot_history: list, task: str, model: str) -> str:
    """
    Export swarm results to a downloadable text file.
    
    Args:
        chatbot_history: The chatbot conversation history.
        task: The original task.
        model: The model used.
        
    Returns:
        Path to the exported file.
    """
    import tempfile
    from utils.export import format_export_content, export_to_file
    
    # Extract the last response from chatbot history
    response = ""
    if chatbot_history:
        # Chatbot history is typically [(user_msg, bot_msg), ...]
        # Get the last bot response
        for entry in chatbot_history:
            if isinstance(entry, tuple) and len(entry) == 2:
                response = entry[1] if entry[1] else response
            elif isinstance(entry, str):
                response = entry
    
    if not response:
        response = "No response generated."
    
    metadata = {
        "Temperature": "N/A",  # Could be passed as parameter if needed
        "Max Tokens": "N/A",
    }
    
    content = format_export_content(task, response, model, metadata)
    filename = export_to_file(content)
    
    # Create temporary file
    temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, prefix='swarmmaster_')
    temp_file.write(content)
    temp_file.close()
    
    return temp_file.name


with gr.Blocks(theme=gr.themes.Dark()) as demo:
    gr.Markdown(
        "# 🐝 SwarmMaster WebApp\n"
        "The ultimate multi-agent orchestrator — powered by you.\n\n"
        "Configure your swarm below, then enter a task to deploy specialized agents."
    )
    
    chatbot = gr.Chatbot(
        height=600,
        show_copy_button=True,
        label="Swarm Output",
        placeholder="Your swarm results will appear here...",
    )
    
    with gr.Row():
        with gr.Column(scale=3):
            txt = gr.Textbox(
                scale=4,
                placeholder="Enter your task (e.g., 'Design a viral AI tool')",
                label="Task",
                lines=3,
            )
        with gr.Column(scale=1):
            btn = gr.Button("Deploy Swarm 🚀", scale=1, variant="primary")
            clear_btn = gr.Button("Clear", scale=1, variant="secondary")
    
    with gr.Row():
        export_btn = gr.Button("📥 Export Results", scale=1, variant="secondary")
        export_file = gr.File(label="Download Export", visible=False)
    
    with gr.Accordion("⚙️ Advanced Settings", open=False):
        with gr.Row():
            model_dropdown = gr.Dropdown(
                choices=SwarmConfig.AVAILABLE_MODELS,
                value=SwarmConfig.get_model(),
                label="Model",
                info="Select the model to use for swarm execution",
            )
            temperature_slider = gr.Slider(
                minimum=0.0,
                maximum=2.0,
                value=SwarmConfig.get_temperature(),
                step=0.1,
                label="Temperature",
                info="Controls randomness (0.0 = deterministic, 2.0 = very creative)",
            )
            max_tokens_slider = gr.Slider(
                minimum=256,
                maximum=8192,
                value=SwarmConfig.get_max_tokens(),
                step=256,
                label="Max Tokens",
                info="Maximum number of tokens to generate",
            )
    
    gr.Examples(
        examples=[
            ["Redesign my dashboard to be visually stunning and engaging"],
            ["Create a complete business plan for an AI mentorship platform"],
            ["Build a production-ready multi-agent research system"],
        ],
        inputs=txt
    )
    
    # Event handlers
    btn.click(
        lambda: ([], []),
        None,
        chatbot,
    ).then(
        run_swarm,
        inputs=[txt, model_dropdown, temperature_slider, max_tokens_slider],
        outputs=chatbot,
        api_name="swarm",
    )
    
    clear_btn.click(
        clear_chat,
        outputs=[chatbot, txt],
    )
    
    export_btn.click(
        export_results,
        inputs=[chatbot, txt, model_dropdown],
        outputs=export_file,
    ).then(
        lambda: gr.update(visible=True),
        outputs=export_file,
    )

if __name__ == "__main__":
    demo.queue(max_size=20).launch()
