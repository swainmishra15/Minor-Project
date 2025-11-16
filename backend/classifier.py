import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch.nn.functional as F

# ----------------------------
# CONFIG
# ----------------------------
MODEL_NAME = "facebook/bart-large-mnli"
LOG_LABELS = ["error", "warning", "info", "performance", "security", "other"]

# Auto-detect GPU
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

print(f"🔥 Loading model: {MODEL_NAME} on {DEVICE} ...")

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)
model.to(DEVICE)
model.eval()

print("✅ NLP Model Ready!")


def classify_log(log_message: str, threshold: float = 0.45):
    """
    Improved zero-shot log classifier using PyTorch.
    Much faster and more configurable than pipeline().
    """

    if not log_message or log_message.strip() == "":
        return "other"

    # Encode labels for NLI
    hypothesis_templates = [f"This text is about {label}." for label in LOG_LABELS]

    # Tokenize pair: (log_message, each hypothesis)
    encodings = tokenizer(
        [log_message] * len(hypothesis_templates),
        hypothesis_templates,
        truncation=True,
        padding=True,
        return_tensors="pt"
    )

    encodings = {k: v.to(DEVICE) for k, v in encodings.items()}

    with torch.no_grad():
        outputs = model(**encodings)
        logits = outputs.logits

    # Convert logits → probabilities
    probs = F.softmax(logits[:, [0, 2]], dim=1)[:, 1]  
    # class index 1 = "entailment" for BART NLI

    # Pick top label
    best_idx = torch.argmax(probs).item()
    best_label = LOG_LABELS[best_idx]
    best_conf = probs[best_idx].item()

    # Threshold handling
    if best_conf < threshold:
        return "other"

    print(f"[LOG CLASSIFIER] {log_message[:50]} → {best_label} ({best_conf:.2f})")
    return best_label
