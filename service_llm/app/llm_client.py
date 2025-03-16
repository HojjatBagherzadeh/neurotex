import os
from openai import OpenAI
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from .config import config  # our simple config (reads from os.environ)

# Global variable to cache the local model pipeline
local_llm_pipeline = None

def load_local_llm(model_name: str):
    """
    Load the local LLM model using Hugging Face Transformers.
    This will download the model if it's not available locally.
    """
    global local_llm_pipeline
    if local_llm_pipeline is None:
        print(f"Loading local model: {model_name}")
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(model_name)
        local_llm_pipeline = pipeline("text-generation", model=model, tokenizer=tokenizer)
    return local_llm_pipeline


def analyze_function_openai(function_code: str) -> list[str]:
    """
    Analyze the function code using OpenAI's GPT-4o API. 
    Since I had an API-key for gpt-4o, I tested and used this model in my local tests.
    """
    api_key = os.environ.get("OPENAI_API_KEY", 'Your API KEY')
    client = OpenAI(api_key=api_key)
    try:
        response = client.chat.completions.create(
            model="gpt-4o",  # using GPT-4o model
            messages=[
                {"role": "system", "content": "You are a code review assistant."},
                {"role": "user", "content": f"Please review the following Python function:\n\n{function_code}\n\nProvide detailed improvement suggestions."}
            ],
            temperature=0.1,
        )
        # Use attribute access rather than subscripting
        content = response.choices[0].message.content
        # Split the response by newline to get individual suggestions (customize as needed)
        suggestions = [line.strip() for line in content.split("\n") if line.strip()]
        return suggestions
    except Exception as e:
        return [f"OpenAI API error: {e}"]

def analyze_function_deepseek(function_code: str) -> list[str]:
    """
    Analyze the function code using DeepSeek's API.
    I haven't use Deepseek LLM so far, so I copied the sample code from the internet on how to call
    deepseek API from here. (https://api-docs.deepseek.com/)
    """
    deepseek_api_url = os.environ.get("DEEPSEEK_API_URL", "https://api.deepseek.com")
    api_key = os.environ.get("Deepseek_API_KEY", 'Your API KEY')
    client = OpenAI(api_key=api_key, base_url=deepseek_api_url)

    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "You are a code review assistant."},
                {"role": "user", "content": f"Please review the following Python function:\n\n{function_code}\n\nProvide detailed improvement suggestions."}
            ],
            stream=False
        )
        # Use attribute access rather than subscripting
        content = response.choices[0].message.content
        # Split the response by newline to get individual suggestions (customize as needed)
        suggestions = [line.strip() for line in content.split("\n") if line.strip()]
        return suggestions
    except Exception as e:
        return [f"DeepSeek API exception: {e}"]

def analyze_function_local(function_code: str) -> list[str]:
    """
    Analyze the function code using a locally hosted LLM model .
    I used Qwen1.5-1.8B for this test.
    
    """
    # Get the model name from environment variables; default to 'gpt2' if not set.
    model_name = os.environ.get("LOCAL_MODEL_NAME", "Qwen/Qwen1.5-1.8B-Chat")
    try:
        llm_pipeline = load_local_llm(model_name)
        prompt = (
            f"Please review the following Python function:\n\n{function_code}\n\n"
            "Provide detailed improvement suggestions."
        )
        # Generate output with the local model
        output = llm_pipeline(prompt, max_length=200, do_sample=True)
        generated_text = output[0]["generated_text"]
        # Split the text into suggestions (customize the parsing as needed)
        suggestions = [line.strip() for line in generated_text.split("\n") if line.strip()]
        return suggestions
    except Exception as e:
        return [f"Local LLM exception: {e}"]

def analyze_function(function_code: str) -> list[str]:
    """
    Selects the appropriate analysis function based on the LLM_PROVIDER configuration.
    """
    provider = config.LLM_PROVIDER.lower()
    if provider == "openai":
        return analyze_function_openai(function_code)
    elif provider == "deepseek":
        return analyze_function_deepseek(function_code)
    elif provider == "local":
        return analyze_function_local(function_code)
    else:
        return ["No suggestions available."]
