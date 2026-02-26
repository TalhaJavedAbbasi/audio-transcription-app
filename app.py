from fastapi import FastAPI, UploadFile, File, Request, Form
from fastapi.responses import HTMLResponse, Response
from fastapi.templating import Jinja2Templates
from faster_whisper import WhisperModel
import os
import subprocess
import json

app = FastAPI()
templates = Jinja2Templates(directory="templates")

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {".wav", ".mp3", ".m4a", ".aac"}

# Load model once
model = WhisperModel(
    "base",
    device="cpu",          # change to "cuda" if GPU available
    compute_type="int8",
)

MAX_UPLOAD_SIZE = 50 * 1024 * 1024  # 50 MB

def normalize_audio(input_path):
    output_path = input_path.rsplit(".", 1)[0] + "_16k.wav"
    command = [
        "ffmpeg",
        "-y",
        "-i", input_path,
        "-ac", "1",
        "-ar", "16000",
        output_path
    ]
    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return output_path

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/transcribe", response_class=HTMLResponse)
async def transcribe(request: Request, file: UploadFile = File(...)):

    file_extension = os.path.splitext(file.filename)[1].lower()
    if file_extension not in ALLOWED_EXTENSIONS:
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "error": "Unsupported file format."}
        )

    original_path = os.path.join(UPLOAD_FOLDER, file.filename)

    contents = await file.read()
    if len(contents) > MAX_UPLOAD_SIZE:
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "error": "File too large. Maximum allowed is 50 MB."}
        )

    # Save file
    with open(original_path, "wb") as buffer:
        buffer.write(contents)

    # Normalize to 16kHz mono WAV
    normalized_path = normalize_audio(original_path)

    # Transcribe
    segments, info = model.transcribe(normalized_path)

    formatted_segments = [
        {"start": round(s.start, 2), "end": round(s.end, 2), "text": s.text.strip()}
        for s in segments
    ]

    return templates.TemplateResponse(
        "index.html",
        {"request": request, "segments": formatted_segments, "language": info.language}
    )

@app.post("/download_json")
async def download_json(segments_json: str = Form(...)):
    segments = json.loads(segments_json)
    return Response(
        content=json.dumps(segments, indent=2),
        media_type="application/json",
        headers={"Content-Disposition": "attachment; filename=transcription.json"}
    )