import requests

API_KEY = "YOUR_RAPIDAPI_KEY"

def get_live_match():
    url = "https://cricbuzz-cricket.p.rapidapi.com/matches/v1/live"

    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": "cricbuzz-cricket.p.rapidapi.com"
    }

    try:
        res = requests.get(url, headers=headers)
        data = res.json()

        matches = []

        for t in data.get("typeMatches", []):
            for series in t.get("seriesMatches", []):
                wrapper = series.get("seriesAdWrapper")
                if wrapper:
                    matches.extend(wrapper.get("matches", []))

        # 🔥 IF NO LIVE MATCH → SEND DEMO DATA
        if not matches:
            return {
                "team1": "India",
                "team2": "Australia",
                "runs": 145,
                "wickets": 3,
                "overs": 15.2,
                "status": "Demo Mode (No Live Match)"
            }

        match = matches[0]

        info = match["matchInfo"]
        score = match["matchScore"]

        return {
            "team1": info["team1"]["teamName"],
            "team2": info["team2"]["teamName"],
            "runs": score["team1Score"]["inngs1"]["runs"],
            "wickets": score["team1Score"]["inngs1"]["wickets"],
            "overs": score["team1Score"]["inngs1"]["overs"],
            "status": "Live"
        }

    except Exception as e:
        return {"error": str(e)}