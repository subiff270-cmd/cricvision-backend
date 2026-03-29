from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from services.live_service import get_live_match
from services.predict_service import get_prediction

app = FastAPI()

# CORS (IMPORTANT)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# HOME
@app.get("/")
def home():
    return {"message": "CRICVISION AI Backend Running 🚀"}

# LIVE MATCH
@app.get("/live-match")
def live():
    return get_live_match()

# PREDICT
@app.get("/predict")
def predict(score: int, wickets: int, overs_left: int, player: str = ""):
    return get_prediction(score, wickets, overs_left, player)