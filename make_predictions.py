import torch
import torch.nn.functional as F
from sentence_transformers import SentenceTransformer
from model_training.model import MLPClassifier
import json

# Load model + label map once at module level
with open("model_training/models/label_map.json", "r") as f:
    label_map = json.load(f)

model = MLPClassifier(input_dim=384, hidden1=128, hidden2=64, output_dim=len(label_map))
checkpoint = torch.load("model_training/models/mlp_mode_classifier.pt", map_location=torch.device("cpu"))
model.load_state_dict(checkpoint['model_state_dict'])
model.eval()

embedder = SentenceTransformer("all-MiniLM-L6-v2")

class Prediction:
    def __init__(self, question):
        self.question = question

    def embed(self):
        embedding = embedder.encode([self.question])
        return torch.tensor(embedding, dtype=torch.float32)

    def predict(self):
        tensor = self.embed()
        with torch.no_grad():
            logits = model(tensor)
            probs = F.softmax(logits, dim=1)
            pred_label_id = torch.argmax(probs, dim=1).item()
        return pred_label_id

    def decode(self, pred_label_id):
        return label_map[str(pred_label_id)]