#classifying logs using simple keyword matching
def classify_log(log_message: str) -> str:
    """
    A simple log classifier based on keywords.
    In a real-world scenario, this could use an ML model.
    """
    if "error" in log_message.lower() or "failed" in log_message.lower():
        return "error"
    elif "warning" in log_message.lower():
        return "warning"
    elif "info" in log_message.lower() or "success" in log_message.lower():
        return "info"
    else:
        return "other"