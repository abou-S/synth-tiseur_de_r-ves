import os
from groq import Groq

def transcribe_audio(filename: str) -> str:
    """Transcrit un fichier audio en texte à l'aide de l'API Groq Whisper."""
    client = Groq()
    with open(filename, "rb") as file:
        transcription = client.audio.transcriptions.create(
            file=file,
            model="whisper-large-v3-turbo",
            prompt="Spécifie le contexte ou l'orthographe",  # Optionnel
            response_format="verbose_json",
            timestamp_granularities=["word", "segment"],
            language="fr",
            temperature=0.0
        )
        return transcription.text 