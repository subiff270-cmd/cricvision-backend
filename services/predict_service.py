import random

def get_prediction(score, wickets, overs_left, player):
    base = int((score / 200) * 100)

    if wickets > 5:
        base -= 10

    if overs_left > 10:
        base += 5

    player_boost = {
        "Dhoni": 10,
        "Virat Kohli": 8,
        "AB de Villiers": 12,
        "Rohit Sharma": 9
    }

    boost = player_boost.get(player, 0)

    win = base + boost + random.randint(-5, 5)
    win = max(1, min(99, win))

    return {
        "win_probability": win,
        "predicted_score": score + overs_left * random.randint(6, 10),
        "risk": "Low" if win > 70 else "Medium" if win > 40 else "High",
        "momentum": "Positive" if win > 50 else "Negative",
        "player_impact": boost
    }