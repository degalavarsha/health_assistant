"""Chest X-ray multi-label classifier (research use only).

The model is loaded lazily on first use so the API starts fast and works
without the weights file. This is the legacy resnet18 model; it has no
external validation and will be replaced (see project plan).
"""
import logging
import os
import threading

from app.core.config import get_settings

log = logging.getLogger(__name__)

CXR_LABELS = [
    "Atelectasis", "Cardiomegaly", "Consolidation", "Edema", "Effusion",
    "Emphysema", "Fibrosis", "Hernia", "Infiltration", "Mass", "Nodule",
    "Pleural_Thickening", "Pneumonia", "Pneumothorax", "No Finding",
]

_lock = threading.Lock()
_state: dict = {}


class ModelUnavailable(RuntimeError):
    pass


def _load():
    import torch
    import torch.nn as nn
    from torchvision import models, transforms

    path = os.path.join(get_settings().models_dir, "chestxray_resnet18.pth")
    if not os.path.exists(path):
        raise ModelUnavailable("X-ray model weights not found")
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    net = models.resnet18(weights=None)
    net.fc = nn.Linear(net.fc.in_features, len(CXR_LABELS))
    net.load_state_dict(torch.load(path, map_location=device, weights_only=True))
    net.to(device).eval()
    tfm = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
    ])
    return {"net": net, "tfm": tfm, "device": device, "torch": torch}


def _get():
    with _lock:
        if "net" not in _state:
            _state.update(_load())
            log.info("X-ray model loaded")
    return _state


def predict(image_path: str) -> dict[str, float]:
    from PIL import Image

    s = _get()
    img = Image.open(image_path).convert("RGB")
    x = s["tfm"](img).unsqueeze(0).to(s["device"])
    with s["torch"].no_grad():
        probs = s["torch"].sigmoid(s["net"](x)).cpu().numpy()[0]
    return {label: float(p) for label, p in zip(CXR_LABELS, probs)}
