# 🎙 Audio Transcription Service (FastAPI + Faster-Whisper)

## 📌 Overview

This project is a lightweight audio transcription service built using **FastAPI** and **faster-whisper**.  
It allows users to upload audio files and receive accurate transcriptions with timestamps.

The system includes:

- Audio upload validation  
- Format normalization using FFmpeg  
- Automatic segmentation for long audio  
- Timestamped transcription  
- Basic scalability considerations  

---

## 🛠 Tech Stack

- **Backend:** FastAPI  
- **Model:** faster-whisper (local inference)  
- **Audio Processing:** FFmpeg  
- **Templating:** Jinja2  
- **Python Version:** 3.9+  

---

## ⚙️ How It Works

1. User uploads an audio file.
2. File extension is validated against allowed formats:

    .wav, .mp3, .m4a, .aac

3. The file is normalized using FFmpeg:
  - Converted to mono
  - Resampled to 16 kHz
  - Saved as WAV
4. The processed file is passed to faster-whisper.
5. The model:
- Automatically segments long audio
- Generates transcription
- Preserves timestamps
6. The transcription result is returned to the user.

---

## 📂 Project Structure


    audio_transcription_app/
    │
    ├── app.py
    ├── requirements.txt
    ├── uploads/
    ├── templates/
    └── README.md


---

## 🚀 Setup Instructions

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/TalhaJavedAbbasi/audio-transcription-app.git
cd audio_transcription_app
```
### 2️⃣ Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```
### 4️⃣ Install FFmpeg

Make sure FFmpeg is installed and available in your system PATH.

Check installation:
```bash
ffmpeg -version
```
### 5️⃣ Run the Application
```bash
uvicorn app:app --reload
```
Open in browser:
```bash
http://127.0.0.1:8000
```
## 📡 API Endpoints
### POST /upload

Uploads an audio file for transcription.

### Request:

- Multipart form-data

- Field: file

### Response:

- Transcribed text with timestamps

## 🧠 Design Decisions
### ✅ Local Model (faster-whisper)

Using a local model ensures:

- No dependency on external APIs

- Lower long-term cost

- Full control over processing

### ✅ Audio Normalization

All files are converted to:

- Mono

- 16 kHz WAV

This ensures compatibility with Whisper models and avoids sampling/channel mismatches.

### ✅ Handling Long Audio

faster-whisper automatically segments long audio into manageable windows and preserves timestamps.
Batch size and compute type can be adjusted for performance optimization.

### ✅ Performance Optimization

- compute_type="int8" for reduced memory usage on CPU

- Adjustable batch_size for parallel chunk processing

## 📦 Scalability Considerations (Future Improvements)

For production-scale deployment:

  - Move transcription to background workers (Celery / RQ)

  - Store audio in object storage (e.g., S3)

  - Store transcripts in a database (PostgreSQL)

  - Add job status tracking

  - Implement authentication and rate limiting

  - Deploy behind load balancer with multiple workers

## ⚠️ Limitations

- Currently runs on a single instance

- File validation is extension-based

- No persistent database storage in the prototype

- Large files may increase processing time on CPU-only systems

## 🔮 Future Enhancements

- Streaming transcription

- Real-time progress tracking

- Subtitle file generation (SRT/VTT)

- Docker containerization

- Cloud deployment

- GPU acceleration support

## 👤 Author

Talha Abbasi

Software Engineer Assessment Submission