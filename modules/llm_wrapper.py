import os
from dotenv import load_dotenv
from groq import Groq
from langchain.chat_models import init_chat_model


# Load environment variables
load_dotenv()

# Get Groq API key
groq_api_key = os.getenv("GROQ_API_KEY")
llm = init_chat_model("llama3-8b-8192", model_provider="groq",groq_api_key=groq_api_key)
# Initialize Groq client
groq_client = Groq(api_key=groq_api_key) if groq_api_key else None

from pydantic import BaseModel, Field


# Pydantic
class model(BaseModel):
   

   
    eval: str = Field(description="generate a brief feedback on the given sentence commincation")
    score: int = Field(
        description="How score communication skills quality, from 1 to 10",le=10,ge=0
    )


def customLLMBot(user_input,prompt):
    """Handles AI responses with detailed feedback on verbal clarity, tone, pacing, and engagement."""
    
    # Enhanced system prompt for better AI feedback
    messages = [
        {
            "role": "system",
            "content": (
               prompt
            )
        },
        {"role": "user", "content": user_input}
    ]

    try:
        if groq_client:
            response = groq_client.chat.completions.create(
                messages=messages,
                model="llama3-8b-8192"
            )
            return response.choices[0].message.content
        else:
            return "Error: Groq API key not configured."
    except Exception as e:
        return f"API Error: {str(e)}"


def customLLMBotEval(user_input):
    structured_llm = llm.with_structured_output(model)

    output=structured_llm.invoke(f"Sentence : {user_input}")

    return output