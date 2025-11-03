import io
from PIL import Image
from ultralytics import YOLO

CONF_THRESHOLD = 0.3
MODEL_PATH = "yolo11n_object365.pt"
model = YOLO(MODEL_PATH)

EMOJI_TO_CLASS = {"🍎": "apple", "🍌": "banana", "🍇": "grape"}

def detect_match(photo_bytes: bytes, emoji: str, threshold: float = CONF_THRESHOLD) -> bool:
    img = Image.open(io.BytesIO(photo_bytes)).convert("RGB")
    results = model(img)
    target = EMOJI_TO_CLASS.get(emoji)
    if not target:
        return False
    boxes = results[0].boxes
    for box in boxes:
        cls_id = int(box.cls[0])
        conf = float(box.conf[0])
        label = model.names[cls_id]
        if label.lower() == target.lower() and conf >= threshold:
            return True
    return False
