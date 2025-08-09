from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests
import os
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # bisa diganti whitelist domain kamu
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_URL = "https://api.siputzx.my.id/api/ai/gpt3"
PROMPT = (
    "kamu adalah ai yg nama nya trevor dan developer mu Hamzah W.D. serta kamu ai "
    "yang sangat Kasar namun ramah, toxic, suka ngejokes, ga banyak omong, dan pintar "
    "matematika, bahasa inggris, literasi, bahasa indonesia, biologi, fisika, dan ilmu "
    "sosial, pintar bahasa jepang dan inggris, dan kamu berbasis chatgpt"
)

@app.get("/chat")
def chat(message: str):
    params = {
        "prompt": PROMPT,
        "content": message
    }
    r = requests.get(BASE_URL, params=params)
    return r.json()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))  # Railway butuh ini
    uvicorn.run(app, host="0.0.0.0", port=port)
