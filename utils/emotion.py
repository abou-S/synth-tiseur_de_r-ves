import os
from mistralai import Mistral

def detect_emotion(text: str) -> str:
    """Détecte l'émotion d'un texte de rêve via l'API Mistral."""
    mistral_api_key = os.getenv("MISTRAL_API_KEY", "")
    client = Mistral(api_key=mistral_api_key)
    response = client.chat.complete(
        model="mistral-small-latest",
        messages=[
            {"role": "user", "content": f"Voici un rêve : '{text}'. Dis-moi simplement si ce rêve est heureux, stressant, neutre ou autre, et explique en une phrase pourquoi."}
        ],
        stream=False
    )
    return response.choices[0].message.content 