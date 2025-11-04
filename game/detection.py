import io
from PIL import Image
from ultralytics import YOLO
from .emoji import EMOJI_TO_CLASS

CONF_THRESHOLD = 0.3
MODEL_PATH = "yolo11n_object365.pt"
model = YOLO(MODEL_PATH)


# Precompute normalized label set for smarter plural handling
LABELS = {name.lower() for name in model.names.values()}

def normalize_label(label: str) -> str:
    label = label.strip().lower()
    # If both plural and singular exist in the model's labels, normalize to singular
    if label.endswith("s") and label[:-1] in LABELS:
        return label[:-1]
    return label

def detect_match(photo_bytes: bytes, emoji: str, threshold: float = CONF_THRESHOLD) -> bool:
    img = Image.open(io.BytesIO(photo_bytes)).convert("RGB")
    results = model(img)
    target = normalize_label(EMOJI_TO_CLASS.get(emoji, ""))
    if not target:
        return False

    for box in results[0].boxes:
        cls_id = int(box.cls[0])
        conf = float(box.conf[0])
        label = normalize_label(model.names[cls_id])
        print(f"Detected: {label} ({conf:.2f}) vs Target: {target}")
        if label == target and conf >= threshold:
            print(f"✅ Match found: {label} ({conf:.2f})")
            return True
    return False
