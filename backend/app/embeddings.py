from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image

_processor = None
_model = None


def visual_similarity(first_path: Path, second_path: Path) -> float:
    global _processor, _model
    if _processor is None or _model is None:
        from transformers import CLIPModel, CLIPProcessor

        _processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
        _model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
        _model.eval()

    import torch

    with Image.open(first_path).convert("RGB") as first, Image.open(second_path).convert("RGB") as second:
        inputs = _processor(images=[first, second], return_tensors="pt")
    with torch.no_grad():
        features = _model.get_image_features(**inputs)
    if not isinstance(features, torch.Tensor):
        features = features.pooler_output
    vectors = features / features.norm(dim=-1, keepdim=True)
    similarity = float((vectors[0] @ vectors[1]).item())
    return max(0.0, min(100.0, ((similarity + 1.0) / 2.0) * 100.0))
