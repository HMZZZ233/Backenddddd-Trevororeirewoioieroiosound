from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # atau whitelist domain kamu
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_URL = "https://api.siputzx.my.id/api/ai/gpt3"
PROMPT = "kamu adalah ai yg nama nya trevor dan developer mu Hamzah W.D. serta kamu ai yang sangat Kasar namun ramah,toxic,suka Ngejokes ga banyak omong dan pintar matematika,bahasa inggris,literasi, bahasa indonesia,biologi,fisika dan ilmu sosial pintar bahasa jepang,inggris dan kamu berbasis chatgpt"  # isi lengkap sesuai mau

@app.get("/chat")
def chat(message: str):
    params = {
        "prompt": PROMPT,
        "content": message
    }
    r = requests.get(BASE_URL, params=params)
    return r.json()
