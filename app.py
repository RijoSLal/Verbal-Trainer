from flask import Flask, render_template, request, jsonify
import os
from modules.llm_wrapper import customLLMBot
from modules.training_modules import run_training_module
from database.db_setup import init_db, save_user_response, get_user_progress
from modules.speech_processing import transcribe_audio  # Import transcription function

app = Flask(__name__)
init_db()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if request.method == 'POST':
        try:
            user_input = request.form['user_input']
            session_id = request.remote_addr
            scenario = request.form.get('scenario', 'casual')

            scenario_prompts = {
                "casual": "Respond like a friendly conversation partner.",
                "interview": "Act as a job interviewer and ask professional questions.",
                "debate": "Challenge the user's response with counterarguments.",
                "storytelling": "Encourage storytelling by helping structure an engaging narrative."
            }
            prompt = scenario_prompts.get(scenario, "Respond normally.")

            response = customLLMBot(f"{prompt} {user_input}", session_id=session_id)

            return jsonify({'response': response})
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    return render_template('chat.html')

@app.route('/train', methods=['POST'])
def train():
    try:
        module_type = request.form.get('module_type')
        user_input = request.form.get('user_input')
        session_id = request.remote_addr

        if not module_type or not user_input:
            return jsonify({'error': 'Missing module type or user input'}), 400

        feedback_data = run_training_module(module_type, user_input, session_id)
        feedback_text = feedback_data.get("feedback", "No feedback provided.")
        score = feedback_data.get("score", 0)

        save_user_response(session_id, module_type, user_input, feedback_text, score)

        return jsonify({'feedback': feedback_text, 'score': score})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/assessment', methods=['GET', 'POST'])
def assessment():
    if request.method == 'POST':
        try:
            user_text = request.form.get('user_text', '').strip()
            session_id = request.remote_addr

            if not user_text:
                return jsonify({'error': 'No input received for assessment'}), 400

            feedback = customLLMBot(f"Evaluate this presentation: {user_text}", session_id=session_id)

            return jsonify({'feedback': feedback})
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    return render_template('assessment.html')

@app.route('/assessment_audio', methods=['POST'])
def assessment_audio():
    try:
        audio_file = request.files.get('audio')

        if not audio_file:
            return jsonify({'error': 'No audio file received'}), 400

        transcript = transcribe_audio(audio_file)
        session_id = request.remote_addr

        if not transcript.strip():
            return jsonify({'error': "Could not transcribe audio. Please try again."})

        feedback = customLLMBot(f"Evaluate this spoken presentation: {transcript}", session_id=session_id)

        return jsonify({'feedback': feedback, 'transcript': transcript})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/upload_voice', methods=['POST'])
def upload_voice():
    """ Handles voice recording upload and saves it in static/uploads """
    try:
        audio_file = request.files.get('audio')

        if not audio_file:
            return jsonify({'error': 'No audio file uploaded'}), 400

        upload_folder = "static/uploads"
        os.makedirs(upload_folder, exist_ok=True)

        file_path = os.path.join(upload_folder, "user_audio.wav")
        audio_file.save(file_path)

        return jsonify({'message': 'Audio uploaded successfully!', 'path': file_path})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/progress')
def progress():
    try:
        session_id = request.remote_addr  # Get user session ID
        progress_data = get_user_progress(session_id)  # Retrieve progress data
        
        # 🔍 Debugging: Log Retrieved Data
        print(f"Progress Data for {session_id}: {progress_data}")

        if not progress_data or len(progress_data) == 0:
            return jsonify({"message": "No progress data found"}), 404  # Return a 404 status if no progress exists

        return jsonify([
            {
                "module_type": row[0],
                "user_input": row[1] or "N/A",
                "ai_feedback": row[2] or "No feedback",
                "score": row[3] if row[3] is not None else 0,
                "timestamp": row[4] if row[4] else "Unknown Time"
            }
            for row in progress_data
        ])
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Return error if something goes wrong



if __name__ == '__main__':
    app.run(debug=True)