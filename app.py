import streamlit as st
from io import BytesIO
import tempfile
from dotenv import load_dotenv
import os
from mistralai import Mistral
from utils.audio import transcribe_audio
from utils.image import generate_image
from utils.emotion import detect_emotion
from audiorecorder import audiorecorder
from utils.history import save_reve, load_historique
import base64
from datetime import datetime

load_dotenv()

st.set_page_config(page_title="Synthétiseur de rêves", layout="centered")
st.title("🌙 Synthétiseur de rêves")

st.write("Racontez votre rêve à voix haute ou uploadez un fichier audio. L'application va transcrire votre rêve, générer une image et détecter l'émotion associée.")

# Enregistrement audio
st.subheader("Ou enregistrez votre rêve directement :")
recorded_audio = audiorecorder("Démarrer l'enregistrement", "Arrêter l'enregistrement")

# Upload audio
uploaded_file = st.file_uploader("Uploader un fichier audio (.wav, .mp3)", type=["wav", "mp3"])

audio_bytes = None
if recorded_audio is not None and len(recorded_audio) > 0:
    # Convertir l'audio enregistré en bytes WAV
    audio_bytes = recorded_audio.export(format="wav").read()
    st.audio(audio_bytes, format='audio/wav')
elif uploaded_file is not None:
    audio_bytes = uploaded_file.read()
    st.audio(audio_bytes, format='audio/wav')

if audio_bytes:
    # Sauvegarde temporaire du fichier audio (upload ou enregistrement)
    with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp_file:
        tmp_file.write(audio_bytes)
        tmp_file_path = tmp_file.name
    # Transcription réelle
    with st.spinner("Transcription en cours..."):
        try:
            transcription = transcribe_audio(tmp_file_path)
        except Exception as e:
            st.error(f"Erreur lors de la transcription : {e}")
            transcription = None
    if transcription:
        st.subheader("Transcription du rêve :")
        st.write(transcription)
        # Détection d'émotion avec Mistral
        with st.spinner("Détection de l'émotion du rêve..."):
            try:
                emotion = detect_emotion(transcription)
                st.subheader("Émotion détectée :")
                st.write(emotion)
            except Exception as e:
                st.error(f"Erreur lors de la détection d'émotion : {e}")
        # Génération d'image avec ClipDrop
        with st.spinner("Génération de l'image du rêve..."):
            try:
                image_bytes = generate_image(transcription)
                st.image(BytesIO(image_bytes), caption="Image générée à partir du rêve", use_container_width=True)
                # Sauvegarde dans l'historique (image en base64)
                image_b64 = base64.b64encode(image_bytes).decode('utf-8')
                save_reve({
                    "date": datetime.now().isoformat(),
                    "transcription": transcription,
                    "emotion": emotion,
                    "image_b64": image_b64
                })
            except Exception as e:
                st.error(f"Erreur lors de la génération de l'image : {e}")

# Affichage de l'historique dans la sidebar
st.sidebar.title("Historique des rêves")
historique = load_historique()
for reve in reversed(historique):
    st.sidebar.markdown(f"**{reve['date']}**")
    st.sidebar.write(reve["transcription"])
    st.sidebar.write(f"Émotion : {reve['emotion']}")
    if "image_b64" in reve:
        st.sidebar.image(BytesIO(base64.b64decode(reve["image_b64"])), caption="Image du rêve", use_container_width=True)
    st.sidebar.markdown("---") 