import json
from datetime import datetime
from typing import Dict, Any, List

HISTO_FILE = "historique.json"

def save_reve(data: Dict[str, Any]):
    try:
        with open(HISTO_FILE, "r") as f:
            historique = json.load(f)
    except FileNotFoundError:
        historique = []
    historique.append(data)
    with open(HISTO_FILE, "w") as f:
        json.dump(historique, f, ensure_ascii=False, indent=2)

def load_historique() -> List[Dict[str, Any]]:
    try:
        with open(HISTO_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def clear_historique():
    with open(HISTO_FILE, "w") as f:
        json.dump([], f) 