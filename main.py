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
    import requests
    import os

    url = "https://cricbuzz-cricket.p.rapidapi.com/matches/v1/live"

    headers = {
        "X-RapidAPI-Key": os.getenv("RAPID_API_KEY"),
        "X-RapidAPI-Host": "cricbuzz-cricket.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers)

    try:
        data = response.json()

        matches = []

        if "typeMatches" in data:
            for t in data["typeMatches"]:
                if "seriesMatches" in t:
                    for series in t["seriesMatches"]:
                        if "seriesAdWrapper" in series:
                            for match in series["seriesAdWrapper"]["matches"]:
                                matches.append(match)

        # 🔥 If live match exists
        if matches:
            match = matches[0]
            return {
                "team1": match["matchInfo"]["team1"]["teamName"],
                "team2": match["matchInfo"]["team2"]["teamName"],
                "status": match["matchInfo"]["status"]
            }

        # ⚠️ If NO match found
        return {
            "team1": "CSK",
            "team2": "MI",
            "status": "No live match — demo mode"
        }

    except Exception as e:
        return {
            "team1": "RCB",
            "team2": "KKR",
            "status": f"Fallback mode ({str(e)})"
        }


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