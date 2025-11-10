# ============================================
# AI-Powered Log Classifier using HuggingFace
# ============================================

from transformers import pipeline

# Load model once at startup
# (You can use smaller models like "valhalla/distilbart-mnli-12-1" if memory is limited)
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

# Define the categories you want the model to classify logs into
LOG_LABELS = ["error", "warning", "info", "performance", "security", "other"]

def classify_log(log_message: str) -> str:
    """
    Classify a log message into one of several categories
    using a pre-trained zero-shot NLP model.
    """
    if not log_message or log_message.strip() == "":
        return "other"

    # Run the HuggingFace zero-shot classification
    result = classifier(log_message, LOG_LABELS)

    # Extract the top predicted label
    predicted_label = result["labels"][0]
    confidence = result["scores"][0]

    # Optional: only return label if confidence > threshold
    if confidence < 0.5:
        predicted_label = "other"

    print(f"[LOG CLASSIFIER] Message: {log_message[:60]}... → {predicted_label} ({confidence:.2f})")
    return predicted_label
