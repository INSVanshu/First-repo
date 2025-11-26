def load_list(filename):
    """Load keywords/phrases from a text file."""
    items = []
    try:
        with open(filename, "r") as f:
            for line in f:
                if line.strip():
                    items.append(line.strip().lower())
    except FileNotFoundError:
        print(f"Warning: {filename} not found. Skipping.")
    return items

def sensational_score(text, sens_words):
    score = 0
    words = text.lower().split()
    for w in words:
        if w in sens_words:
            score += 1
    return score

def emotional_score(text, emo_words):
    score = 0
    for w in text.lower().split():
        if w in emo_words:
            score += 1
    return score

def adjective_score(text, adjectives):
    score = 0
    for w in text.lower().split():
        if w in adjectives:
            score += 1
    return score

def caps_score(text):
    score = 0
    for w in text.split():
        if len(w) > 4 and w.isupper():
            score += 1
    return score

def punctuation_score(text):
    score = 0
    score += text.count("!!!")
    score += text.count("??")
    score += text.count("!")
    return score

def number_absence_score(text):
    for c in text:
        if c.isdigit():
            return 0
    return 2  

def sentence_length_score(text):
    score = 0
    sentences = text.split(".")
    for s in sentences:
        if len(s.split()) > 30:
            score += 1
    return score

def url_score(text, bad_domains):
    text = text.lower()
    score = 0
    for d in bad_domains:
        if d in text:
            score += 3
    return score

def anonymity_score(text, anon_phrases):
    text = text.lower()
    score = 0
    for p in anon_phrases:
        if p in text:
            score += 2
    return score

def title_mismatch_score(title, content, sens_words):
    title_hits = sum(1 for w in title.lower().split() if w in sens_words)
    content_hits = sum(1 for w in content.lower().split() if w in sens_words)

    if title_hits >= 2 and content_hits == 0:
        return 2
    return 0

def repetition_score(text):
    freq = {}
    words = text.lower().split()
    for w in words:
        freq[w] = freq.get(w, 0) + 1

    score = 0
    for w, c in freq.items():
        if c > 10:
            score += 1
    return score

def detect_fake_news(title, content, lists):
    total = 0

    total += sensational_score(content, lists["sensational"])
    total += emotional_score(content, lists["emotional"])
    total += adjective_score(content, lists["adjectives"])
    total += caps_score(content)
    total += punctuation_score(content)
    total += number_absence_score(content)
    total += sentence_length_score(content)
    total += url_score(content, lists["bad_domains"])
    total += anonymity_score(content, lists["anonymous"])
    total += title_mismatch_score(title, content, lists["sensational"])
    total += repetition_score(content)

    return total

def classify(score):
    if score >= 15:
        return "LIKELY FAKE NEWS"
    elif score >= 7:
        return "SUSPICIOUS / POSSIBLY FAKE"
    else:
        return "LIKELY REAL NEWS"

if __name__ == "__main__":

    lists = {
        "sensational": load_list("sensational_words.txt"),
        "emotional": load_list("emotional_words.txt"),
        "adjectives": load_list("adjectives.txt"),
        "bad_domains": load_list("bad_domains.txt"),
        "anonymous": load_list("anonymous_phrases.txt")
    }

    print("\n--------------- FAKE NEWS DETECTOR ---------------\n")
    title = input("Enter article TITLE: ")
    print("--------------------------------------------------")
    content = input("Enter article CONTENT: ")

    score = detect_fake_news(title, content, lists)
    result = classify(score)

    print("\n--------------------------------------------------")
    print(f"Final Score: {score}")
    print(f"Classification: {result}")
    print("--------------------------------------------------\n")
