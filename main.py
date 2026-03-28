from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests
import random

app = FastAPI()

# CORS (VERY IMPORTANT)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔑 PUT YOUR RAPID API KEY HERE
API_KEY = "YOUR_RAPIDAPI_KEY"


# ---------------- HOME ----------------
@app.get("/")
def home():
    return {"message": "CRICVISION AI Backend Running 🚀"}


# ---------------- LIVE MATCH ----------------
@app.get("/live-match")
def live_match():
    url = "https://cricbuzz-cricket.p.rapidapi.com/matches/v1/live"

    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": "cricbuzz-cricket.p.rapidapi.com"
    }

    try:
        res = requests.get(url, headers=headers)
        data = res.json()

        match = data["typeMatches"][0]["seriesMatches"][0]["seriesAdWrapper"]["matches"][0]

        info = match["matchInfo"]
        score = match.get("matchScore", {})

        return {
            "team1": info["team1"]["teamName"],
            "team2": info["team2"]["teamName"],
            "status": info["status"],
            "score": score
        }

    except Exception as e:
        return {"message": "No live match found", "error": str(e)}


# ---------------- AI PREDICTION ----------------
@app.get("/predict")
def predict(score: int, wickets: int, overs_left: int, player: str = ""):

    import random

    base_prob = int((score / 200) * 100)

    # dynamic fluctuation 🔥
    fluctuation = random.randint(-5, 5)

    # wickets effect
    if wickets > 5:
        base_prob -= 10

    # overs effect
    if overs_left > 10:
        base_prob += 5

    # player impact
    player_impact = 0

    if player == "Dhoni":
        player_impact = 10
    elif player == "Virat Kohli":
        player_impact = 8
    elif player == "AB de Villiers":
        player_impact = 12
    elif player == "Rohit Sharma":
        player_impact = 9

    win_probability = base_prob + player_impact + fluctuation
    win_probability = max(1, min(99, win_probability))

    predicted_score = score + (overs_left * random.randint(6, 10))

    risk = "Low" if win_probability > 70 else "Medium" if win_probability > 40 else "High"
    momentum = "Positive" if win_probability > 50 else "Negative"

    return {
        "win_probability": win_probability,
        "predicted_score": predicted_score,
        "risk": risk,
        "momentum": momentum,
        "player_impact": player_impact
    }