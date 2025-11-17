def setup_gemini_config():
    """
    Create a custom evaluation configuration using Gemini 2.0 Flash via OpenRouter
    """
    # Configure to use Gemini 2.0 Flash via OpenRouter
    evaluation_config = {
        "model_name": "google/gemini-2.0-flash-001",  # OpenRouter format for Gemini
        "provider": "openai_endpoint",  # Use OpenRouter as endpoint
        "openai_endpoint_url": "https://openrouter.ai/api/v1",
        "temperature": 0,  # Zero temp for consistent evaluation
    }

    print(f"Using Gemini 2.0 Flash for evaluation: {evaluation_config}")
    return evaluation_config
