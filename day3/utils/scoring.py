def score_responses(responses):
    scores = {}

    for i, res in enumerate(responses):
        score = 0

        # Length score
        score += min(len(res) // 40, 10)

        # Reasoning keywords
        keywords = ["because", "therefore", "hence", "thus"]
        for word in keywords:
            if word in res.lower():
                score += 2

        scores[f"Player {i+1}"] = score

    return scores