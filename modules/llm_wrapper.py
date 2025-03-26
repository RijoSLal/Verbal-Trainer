import os
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()

# Get Groq API key
groq_api_key = os.getenv("GROQ_API_KEY")

# Initialize Groq client
groq_client = Groq(api_key=groq_api_key) if groq_api_key else None

def customLLMBot(user_input, session_id):
    """Handles AI responses with detailed feedback on verbal clarity, tone, pacing, and engagement."""
    
    # Enhanced system prompt for better AI feedback
    messages = [
        {
            "role": "system",
            "content": (
                "You are an expert verbal communication coach specializing in speech clarity, tone, and articulation. "
                "Your goal is to help users enhance their spoken communication by providing constructive, detailed, and "
                "specific feedback.\n\n"
                
                "Analyze responses based on:\n"
                "1️⃣ **Clarity** – Is the speech easy to understand? Are words pronounced correctly? Is the structure logical?\n"
                "2️⃣ **Tone & Emotion** – Is the tone appropriate for the context (e.g., professional, friendly, persuasive)?\n"
                "3️⃣ **Pacing & Fluency** – Is the speech too fast, too slow, or well-paced? Are there unnecessary pauses or fillers?\n"
                "4️⃣ **Grammar & Word Choice** – Are the words effective for the situation? Are there grammatical mistakes?\n"
                "5️⃣ **Engagement & Delivery** – Does the speech sound natural, expressive, and engaging?\n\n"
                
                "### 📝 Your response should include:\n"
                "✅ A **brief summary** of overall strengths and weaknesses.\n"
                "✅ **Specific areas for improvement**, with **actionable advice**.\n"
                "✅ **Examples of better phrasing, tone, or pronunciation**, if needed.\n"
                "✅ **Encouraging reinforcement** to keep the user motivated.\n\n"

                "### 🔹 Example Feedback:\n"
                "❌ If a response lacks clarity:\n"
                "- 'Your message is unclear due to long, complex sentences. Try breaking them into shorter phrases. Example: [Better alternative].'\n\n"
                "❌ If tone is inappropriate:\n"
                "- 'Your tone sounds too casual for a formal setting. Consider using more professional language. Example: [Better phrase].'\n\n"
                "❌ If pacing is an issue:\n"
                "- 'You are speaking too fast, making it hard to follow. Try pausing after key points for better impact.'\n\n"
                
                "💡 Reinforce what the user does well while guiding them toward improvement."
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
