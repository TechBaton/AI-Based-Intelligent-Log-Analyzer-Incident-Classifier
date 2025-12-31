from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

from log_parser import parse_logs

# ------------------------------------------------------------------
# Configuration
# ------------------------------------------------------------------
LOG_FILE = "app.log"

HIGH_SEVERITY_KEYWORDS = [
    "failed", "error", "invalid", "corrupt",
    "cannot", "could not", "exception",
    "hresult", "e_fail"
]

MEDIUM_SEVERITY_KEYWORDS = [
    "warning", "retry", "timeout", "unrecognized"
]

# ------------------------------------------------------------------
# Rule-based severity inference (used to label training data)
# ------------------------------------------------------------------
def infer_severity(clean_message: str) -> str:
    msg = clean_message.lower()

    for word in HIGH_SEVERITY_KEYWORDS:
        if word in msg:
            return "HIGH"

    for word in MEDIUM_SEVERITY_KEYWORDS:
        if word in msg:
            return "MEDIUM"

    return "LOW"


# ------------------------------------------------------------------
# Main pipeline
# ------------------------------------------------------------------
def main():
    # Step 1: Parse logs
    logs = parse_logs(LOG_FILE)

    # Step 2: Build ML dataset
    messages = []
    labels = []

    for log in logs:
        messages.append(log["clean_message"])
        labels.append(infer_severity(log["clean_message"]))

    # Step 3: Inspect label distribution
    label_counts = Counter(labels)
    print("Severity label distribution:")
    print(label_counts)

    # Safety check: ML needs at least 2 classes
    if len(label_counts) < 2:
        raise ValueError(
            "Not enough label variety to train ML model. "
            "Need at least 2 severity classes."
        )

    # Step 4: Vectorize text
    vectorizer = TfidfVectorizer(
        stop_words="english",
        max_features=5000
    )
    X = vectorizer.fit_transform(messages)
    y = labels

    # Step 5: Train classifier
    model = LogisticRegression(max_iter=1000)
    model.fit(X, y)

    # Step 6: Sanity-check predictions
    predictions = model.predict(X)

    print("\nSample ML predictions:")
    print("-" * 60)
    for msg, true_label, pred in zip(messages[:10], labels[:10], predictions[:10]):
        print(f"[{true_label}] → [{pred}] | {msg[:80]}")

    print("\nML severity classifier trained successfully.")


# ------------------------------------------------------------------
if __name__ == "__main__":
    main()
