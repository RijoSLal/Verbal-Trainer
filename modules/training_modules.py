from modules.llm_wrapper import customLLMBot

def run_training_module(module_type, user_input, session_id):
    """Generates AI-driven feedback based on the selected training module."""
    prompts = {
        "impromptu": (
            "Analyze the following impromptu speech for clarity, structure, and engagement. "
            "Provide feedback with suggestions for improvement: "
        ),
        "storytelling": (
            "Evaluate this storytelling attempt. Focus on narrative flow, vocabulary, and emotional impact. "
            "Provide constructive criticism: "
        ),
        "conflict_resolution": (
            "Assess this conflict resolution response. Evaluate empathy, assertiveness, and professionalism. "
            "Give feedback with specific improvements: "
        )
    }

    if module_type not in prompts:
        return "Invalid module type"

    # Send the input to the AI for feedback
    feedback = customLLMBot(prompts[module_type] + user_input, session_id)

    # Generate a score based on AI response (out of 10)
    score = generate_score(feedback)
    
    return {
        "feedback": feedback,
        "score": score
    }

def generate_score(feedback):
    """Assigns a score based on AI feedback (basic heuristic approach)."""
    if "excellent" in feedback.lower() or "outstanding" in feedback.lower():
        return 9.5
    elif "great" in feedback.lower() or "strong" in feedback.lower():
        return 8.0
    elif "good" in feedback.lower() or "decent" in feedback.lower():
        return 7.0
    elif "needs improvement" in feedback.lower() or "could be better" in feedback.lower():
        return 5.5
    else:
        return 6.0  # Default average score
