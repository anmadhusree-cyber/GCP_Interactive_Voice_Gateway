# GCP Interactive Voice Gateway

This is a voice-controlled chat application built with **Python** and **Flask**. It utilizes **Google Cloud Platform (GCP)** to convert speech into text and back into natural-sounding audio.

You can click the microphone icon, speak a message, and the assistant will reply with a fluid, natural voice.

---

## ✨ Features

* 🎙️ **Voice Chat:** Record your voice directly in the browser and hear the reply.
* ☁️ **Google AI:** Powered by Google Cloud Speech-to-Text and Text-to-Speech.
* 🧹 **Smart Text Cleaning:** Automatically removes code or symbols before speaking so the audio sounds natural.
* 💻 **Clean Interface:** A simple, modern chat design built with plain HTML, CSS, and JavaScript.

---

## 🛠️ Built With

* **Backend:** Python, Flask
* **Frontend:** HTML, CSS, JavaScript
* **APIs:** Google Cloud Platform (GCP)
* **Audio Tools:** Pydub, FFmpeg

---

## 🚀 How to Run the Project

**1. Get the code**

```bash
git clone https://github.com/yourusername/gcp-interactive-voice-gateway.git
cd gcp-interactive-voice-gateway

```

**2. Install dependencies**
Ensure you have **Python** installed, then run:

```bash
pip install -r requirements.txt

```

> **Note:** You must have **FFmpeg** installed on your system for audio conversion processing.

**3. Add your Google API Key**

* Obtain your service account key (JSON file) from the Google Cloud Console.
* Rename the file to `google_creds.json` and place it in the root project folder.
* Create a `.env` file in the root folder and add the following line:

```ini
GOOGLE_APPLICATION_CREDENTIALS=google_creds.json

```

**4. Start the app**

```bash
python app.py

```

Open your browser and navigate to `http://localhost:5000` to start chatting!