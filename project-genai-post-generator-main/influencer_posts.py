import json

INFLUENCER_FILE = "influencer_posts.json"


def load_influencer_data(file_path=INFLUENCER_FILE):
    with open(file_path, encoding="utf-8") as f:
        return json.load(f)


def get_influencers(file_path=INFLUENCER_FILE):
    data = load_influencer_data(file_path)
    return [entry["influencer"] for entry in data]


def get_influencer_roles(file_path=INFLUENCER_FILE):
    data = load_influencer_data(file_path)
    return {entry["influencer"]: entry["role"] for entry in data}


def select_influencer_posts(influencer, topic, length, language, max_examples=3, file_path=INFLUENCER_FILE):
    data = load_influencer_data(file_path)
    entry = next((e for e in data if e["influencer"] == influencer), None)
    if entry is None:
        return {"role": None, "style_notes": "", "posts": []}

    def score(post):
        s = 0
        if post["topic"] == topic:
            s += 3
        if post["language"] == language:
            s += 2
        if post["length"] == length:
            s += 1
        return s

    ranked = sorted(entry["posts"], key=score, reverse=True)

    return {
        "role": entry["role"],
        "style_notes": entry["style_notes"],
        "posts": ranked[:max_examples],
    }


if __name__ == "__main__":
    print(get_influencers())
    selected = select_influencer_posts("Rohan Mehta", "Job Search", "Medium", "English")
    print(selected["style_notes"])
    print([p["text"][:60] for p in selected["posts"]])