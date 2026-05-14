import os
import io
import re
import logging
from flask import Flask, request, jsonify, Response, render_template
from flask_cors import CORS
from dotenv import load_dotenv

# --- FFmpeg Setup (Keep this from your original script for robustness) ---
# Make sure FFmpeg is installed and the path is correct for your system
ffmpeg_path = r"C:\ffmpeg\bin"
if os.path.exists(ffmpeg_path):
    os.environ["PATH"] += os.pathsep + ffmpeg_path

try:
    from pydub import AudioSegment
except ImportError:
    AudioSegment = None

from google.cloud import speech
from google.cloud import texttospeech

# Setup Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("google-voice-assistant")

# Load Environment Variables
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))


# ====================== CORE ENGINE ======================

class GoogleVoiceAssistant:
    def __init__(self):
        """Initializes Google Cloud clients."""
        if not os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
            logger.warning("GOOGLE_APPLICATION_CREDENTIALS not found in .env")
            
        self.stt_client = speech.SpeechClient()
        self.tts_client = texttospeech.TextToSpeechClient()

    def _to_wav(self, audio_bytes):
        """Converts incoming browser audio (WebM) to WAV using Pydub/FFmpeg."""
        if not AudioSegment:
            raise Exception("Pydub/FFmpeg not configured. Please install pydub and FFmpeg.")
        
        audio_segment = AudioSegment.from_file(io.BytesIO(audio_bytes))
        wav_io = io.BytesIO()
        audio_segment.export(wav_io, format="wav")
        return wav_io.getvalue()

    def speech_to_text(self, audio_bytes):
        """Processes audio and returns text transcription."""
        logger.info("Attempting Google STT...")
        try:
            # Convert WebM to WAV for better accuracy
            audio_wav = self._to_wav(audio_bytes)
            
            audio = speech.RecognitionAudio(content=audio_wav)
            config = speech.RecognitionConfig(
                encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
                language_code="en-US"
            )

            response = self.stt_client.recognize(config=config, audio=audio)
            
            if response.results:
                return response.results[0].alternatives[0].transcript
            return ""
            
        except Exception as e:
            logger.error(f"Google STT Provider failed: {e}")
            raise

    def text_to_speech(self, text):
        """Cleans text and generates MP3 audio."""
        logger.info("Attempting Google TTS...")
        
        # 1. Clean standard HTML tags (similar to your original logic)
        clean_text = re.sub(r'<[^>]+>', ' ', text)
        # 2. Collapse multiple spaces into one
        clean_text = re.sub(r'\s+', ' ', clean_text).strip()

        try:
            input_text = texttospeech.SynthesisInput(text=clean_text)
            voice = texttospeech.VoiceSelectionParams(
                language_code="en-US", 
                name="en-US-Journey-F"
            )
            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.MP3
            )

            response = self.tts_client.synthesize_speech(
                input=input_text, voice=voice, audio_config=audio_config
            )
            return response.audio_content
            
        except Exception as e:
            logger.error(f"Google TTS Provider failed: {e}")
            raise

    def get_assistant_response(self, text):
        """
        Placeholder for your backend logic. 
        You can replace this with Pandas logic to search a dataset, 
        or an API call to a Large Language Model.
        """
        user_input = text.lower()
        if "hello" in user_input or "hi" in user_input:
            return "Hello! I am your Google Voice Assistant. How can I help?"
        elif "resume" in user_input:
            return "This project highlights your skills in Python OOP, audio processing, and Google Cloud APIs."
        else:
            return f"I heard you say: '{text}'. This is a mock response from the engine."


# ====================== FLASK APP ======================

app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app)

# Instantiate the Engine
engine = GoogleVoiceAssistant()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/session')
def session(): 
    # Kept for compatibility with your frontend script
    return jsonify({"sessionId": "google-session-123"})

@app.route('/api/stt', methods=['POST'])
def stt_route():
    audio_file = request.files['audio'].read()
    try:
        text = engine.speech_to_text(audio_file)
        return jsonify({"text": text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/assistant', methods=['POST'])
def assistant_route():
    user_input = request.json.get("input", "")
    response_text = engine.get_assistant_response(user_input)
    return jsonify({"output": response_text})

@app.route('/api/tts', methods=['POST'])
def tts_route():
    raw_text = request.json.get("text", "")
    try:
        audio_data = engine.text_to_speech(raw_text)
        return Response(audio_data, mimetype="audio/mp3")
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)