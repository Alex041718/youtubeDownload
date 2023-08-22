from pytube import YouTube

# Lien de la vidéo YouTube que vous souhaitez télécharger
video_url = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'

# Créer un objet YouTube en utilisant le lien
youtube_video = YouTube(video_url)

# Choisir la meilleure résolution audio disponible
audio_stream = youtube_video.streams.filter(only_audio=True).first()

# Télécharger l'audio dans le dossier courant
audio_stream.download()

print("Téléchargement de l'audio terminé.")
