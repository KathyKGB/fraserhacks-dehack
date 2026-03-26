import re
from collections import defaultdict

IMPORTANT_TOPICS = {
    "Payments and Fees": [
        "payment", "fee", "fees", "charge", "charges", "billing", "subscription",
        "price", "pricing", "renewal", "renew automatically", "auto-renew"
    ],
    "Refunds and Cancellations": [
        "refund", "refunds", "cancel", "cancellation", "terminate", "termination"
    ],
    "Privacy and Data Use": [
        "privacy", "data", "personal information", "collect", "sharing", "third party",
        "cookies", "tracking"
    ],
    "User Responsibilities": [
        "user must", "you agree", "responsible", "prohibited", "not allowed",
        "misuse", "acceptable use", "account", "password", "security"
    ],
    "Liability and Disclaimers": [
        "liability", "liable", "disclaimer", "warranty", "as is", "damages",
        "indirect", "loss", "risk"
    ],
    "Disputes and Governing Law": [
        "governing law", "jurisdiction", "dispute", "arbitration", "court",
        "legal action"
    ],
    "Changes to Terms": [
        "change these terms", "modify", "updated terms", "notice", "changes to this agreement"
    ]
}

def clean_text(text):
    return re.sub(r"\s+", " ", text).strip()

def split_into_sentences(text):
    sentences = re.split(r'(?<=[.!?])\s+', text)
    return [s.strip() for s in sentences if s.strip()]

def sentence_score(sentence, keywords):
    sentence_lower = sentence.lower()
    score = 0
    for keyword in keywords:
        if keyword in sentence_lower:
            score += 1
    return score

def summarize_terms(text, max_sentences_per_topic=2):
    text = clean_text(text)
    sentences = split_into_sentences(text)
    topic_summaries = defaultdict(list)

    for topic, keywords in IMPORTANT_TOPICS.items():
        scored_sentences = []

        for sentence in sentences:
            score = sentence_score(sentence, keywords)
            if score > 0:
                scored_sentences.append((score, sentence))

        scored_sentences.sort(key=lambda x: x[0], reverse=True)

        chosen = []
        seen = set()

        for _, sentence in scored_sentences:
            normalized = sentence.lower()
            if normalized not in seen:
                chosen.append(sentence)
                seen.add(normalized)
            if len(chosen) >= max_sentences_per_topic:
                break

        if chosen:
            topic_summaries[topic] = chosen

    return dict(topic_summaries)

def print_summary(summary):
    if not summary:
        print("No major points could be identified.")
        return

    print("\nTERMS AND CONDITIONS SUMMARY\n")
    for topic, points in summary.items():
        print(topic + ":")
        for point in points:
            print(" - " + point)
        print()

print("Paste Terms and Conditions below.")
print("When you are done, type END on a new line.\n")

lines = []
while True:
    line = input()
    if line.strip() == "END":
        break
    lines.append(line)

terms_text = "\n".join(lines)

if not terms_text.strip():
    print("No text entered.")
else:
    summary = summarize_terms(terms_text)
    print_summary(summary)

