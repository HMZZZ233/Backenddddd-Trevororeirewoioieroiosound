from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
import requests
app = FastAPI()
@app.get("/proxy-audio")
def proxy_audio(url: str):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(url, headers=headers, stream=True)
    return StreamingResponse(response.raw, media_type="audio/wav")