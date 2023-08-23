from pytube import YouTube
import re

# Lien de la vidéo YouTube que vous souhaitez télécharger
video_url = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'

# Créer un objet YouTube en utilisant le lien
youtube_video = YouTube(video_url)

# Choisir la meilleure résolution audio disponible
audio_stream = youtube_video.streams.filter(only_audio=True).first()



title = re.sub(r'\s+', '-', youtube_video.title)
# Télécharger l'audio dans le dossier courant
audio_stream.download(output_path='downloads', filename=title+'.mp3')

print("Téléchargement de l'audio terminé.")
