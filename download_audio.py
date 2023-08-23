import argparse
from pytube import YouTube
import re
import sys

def download_audio(video_url):
    try:
        # Créer un objet YouTube en utilisant le lien
        youtube_video = YouTube(video_url)

        # Choisir la meilleure résolution audio disponible
        audio_stream = youtube_video.streams.filter(only_audio=True).first()

        title = re.sub(r'\s+', '-', youtube_video.title)
        # Télécharger l'audio dans le dossier courant
        audio_stream.download(output_path='downloads', filename=title+'.mp3')

        print(title)  # Imprimer le titre de la vidéo dans la sortie standard
    except Exception as e:
        print("Erreur lors du téléchargement :", str(e))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Télécharger l'audio à partir d'une vidéo YouTube.")
    parser.add_argument("video_url", type=str, help="Lien de la vidéo YouTube à télécharger")

    args = parser.parse_args()
    download_audio(args.video_url)
