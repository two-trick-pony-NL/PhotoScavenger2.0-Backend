import time
import io
from PIL import Image
from .emoji import EMOJI_TO_CLASS
from .analytics import track_event

CONF_THRESHOLD = 0.2
MODEL_PATH = "yolo11n_object365.pt"

# Global placeholder
model = None

def get_model():
    """Lazy-load YOLO only on first use."""
    global model
    if model is None:
        from ultralytics import YOLO  # moved inside to avoid import-time side effects
        model = YOLO(MODEL_PATH)
        print("✅ Loaded YOLO model.")
    return model

# Precompute normalized label set lazily
LABELS = None
def get_labels():
    global LABELS
    if LABELS is None:
        LABELS = {name.lower() for name in get_model().names.values()}
    return LABELS

def normalize_label(label: str) -> str:
    label = label.strip().lower()
    labels = get_labels()
    if label.endswith("s") and label[:-1] in labels:
        return label[:-1]
    return label

def detect_match(photo_bytes: bytes, emoji: str, player_id, threshold: float = CONF_THRESHOLD) -> bool:
    img = Image.open(io.BytesIO(photo_bytes)).convert("RGB")
    model_instance = get_model()
    start_time = time.time()
    results = model_instance(img)
    inference_time = time.time() - start_time
    print(f"🕒 Inference time: {inference_time:.2f} seconds")
    
    target = normalize_label(EMOJI_TO_CLASS.get(emoji, ""))
    if not target:
        return False

    for box in results[0].boxes:
        cls_id = int(box.cls[0])
        conf = float(box.conf[0])
        label = normalize_label(model_instance.names[cls_id])
        print(f"Detected: {label} ({conf:.2f}) vs Target: {target}")
        CORRECT = label == target and conf >= threshold
        
        track_event(player_id, "Object Detected", {
            "detected_label": label,
            "target_label": target,
            "confidence": conf, 
            "is_match": CORRECT,
            "inference_time_ms": round(inference_time*1000, 1)
        })
        
        if CORRECT:
            print(f"✅ Match found: {label} ({conf:.2f})")
            return True
    return False
