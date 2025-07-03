import requests
import json
from datetime import datetime
from typing import Dict, Any, List

def generate_image1(text: str) -> bytes:
    """Génère une image à partir d'un prompt texte via l'API ClipDrop."""
    prompt = f"""Rêve : {text}.
    
    -T'es un assistant qui génère des images à partir de rêves.
    -Tu dois générer une image qui correspond au rêve.
    -Tu dois générer une image qui est en lien avec le rêve."""

    prompt = prompt.replace("\n", " ")

    r = requests.post('https://clipdrop-api.co/text-to-image/v1',
        files={
            'prompt': (None, prompt, 'text/plain')
        },
        headers={
            'x-api-key': '2186cbd5329a422e187511482f8ce7c8fc0c25219941c5140259a6b4929afa0408581f85121d5b0a6fc5378998fdc22a'
        }
    )
    if r.ok:
        return r.content
    else:
        r.raise_for_status()


def generate_image(text: str) -> bytes:

    prompt = f"""Rêve : {text}.
    
    -T'es un assistant qui génère des images à partir de rêves.
    -Tu dois générer une image qui correspond au rêve.
    -Tu dois générer une image qui est en lien avec le rêve."""

    prompt = prompt.replace("\n", " ")

    """Génère une image à partir d'un prompt texte via l'API Pollinations."""
    url = f"https://image.pollinations.ai/prompt/{prompt}"
    r = requests.get(url)
    if r.ok:
        return r.content
    else:
        r.raise_for_status() 

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