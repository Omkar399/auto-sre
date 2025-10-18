#!/usr/bin/env python3
"""
Galileo Observability Demo
Simple example showing how to log LLM interactions with Galileo
"""

from datetime import datetime
from google import genai
from google.genai import types
from galileo import galileo_context
from galileo.config import GalileoPythonConfig
from dotenv import load_dotenv
import os

def main():
    # Load environment variables from the .env file
    load_dotenv(override=True)
    
    # Check required API keys
    if not os.getenv("GALILEO_API_KEY"):
        print("❌ GALILEO_API_KEY not found in .env file!")
        return
    
    if not os.getenv("GEMINI_API_KEY"):
        print("❌ GEMINI_API_KEY not found in .env file!")
        return
    
    print("=" * 70)
    print("🔭 Galileo Observability Demo")
    print("=" * 70)
    print()
    
    # Set the project and Log stream, these are created if they don't exist.
    # You can also set these using the GALILEO_PROJECT and GALILEO_LOG_STREAM
    # environment variables.
    project_name = os.getenv("GALILEO_PROJECT", "MyFirstEvaluation")
    log_stream_name = os.getenv("GALILEO_LOG_STREAM", "MyFirstLogStream")
    
    print(f"📊 Initializing Galileo...")
    print(f"   Project: {project_name}")
    print(f"   Log Stream: {log_stream_name}")
    
    galileo_context.init(
        project=project_name,
        log_stream=log_stream_name
    )
    
    # Get the Galileo logger instance
    logger = galileo_context.get_logger_instance()
    
    # Start a Galileo session
    logger.start_session()
    print("✅ Galileo session started")
    print()
    
    # Initialize the Gemini client
    print("🧠 Initializing Gemini client...")
    client = genai.Client()
    print("✅ Gemini client ready")
    print()
    
    # Define a system prompt with guidance
    system_prompt = """
You are a helpful assistant that wants to provide a user as much
information as possible. Avoid saying I don't know.
"""
    
    # Define a user prompt with a question
    user_prompt = "Describe Galileo"
    
    MODEL_NAME = "gemini-2.0-flash-exp"
    
    print(f"💭 Sending prompt to {MODEL_NAME}...")
    print(f"   User: {user_prompt}")
    print()
    
    # Start a trace
    logger.start_trace(name="Conversation step", input=user_prompt)
    
    # Capture the current time in nanoseconds for logging
    start_time_ns = datetime.now().timestamp() * 1_000_000_000
    
    # Send a request to the LLM
    response = client.models.generate_content(
        model=MODEL_NAME,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt
        ),
        contents=user_prompt
    )
    
    # Log an LLM span using the response from Gemini
    logger.add_llm_span(
        input=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        output=response.text,
        model=MODEL_NAME,
        num_input_tokens=response.usage_metadata.prompt_token_count,
        num_output_tokens=response.usage_metadata.candidates_token_count,
        total_tokens=response.usage_metadata.total_token_count,
        duration_ns=(datetime.now().timestamp() * 1_000_000_000) - start_time_ns,
    )
    
    # Conclude and flush the logger
    logger.conclude(output=response.text)
    logger.flush()
    
    print("=" * 70)
    print("✨ Response from Gemini:")
    print("=" * 70)
    print()
    print(response.text)
    print()
    
    # Show Galileo information after the response
    config = GalileoPythonConfig.get()
    project_url = f"{config.console_url}project/{logger.project_id}"
    log_stream_url = f"{project_url}/log-streams/{logger.log_stream_id}"
    
    print("=" * 70)
    print("🚀 GALILEO LOG INFORMATION:")
    print("=" * 70)
    print(f"🔗 Project   : {project_url}")
    print(f"📝 Log Stream: {log_stream_url}")
    print()
    print("✅ Interaction logged successfully to Galileo!")
    print("   View your logs at the URLs above.")
    print()

if __name__ == "__main__":
    main()

