from flask import Flask, request, jsonify, send_file
from pytube import YouTube
from itsdangerous import URLSafeTimedSerializer
import re

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
s = URLSafeTimedSerializer(app.config['SECRET_KEY'])

# Route pour demander au server de télécharger l'audio de la vidéo
@app.route('/generate_download_link', methods=['GET'])
def generate_download_link():
    video_url = request.args.get('video_url')

    if not video_url:
        return jsonify({'error': 'Missing video_url parameter'}), 400

    try:
        youtube_video = YouTube(video_url)
        audio_stream = youtube_video.streams.filter(only_audio=True).first()

        title = re.sub(r'\s+', '-', youtube_video.title)
        # Télécharger l'audio dans le dossier downloads
        audio_stream.download(output_path='downloads', filename=title+'.mp3')


        # Générer un token sécurisé avec une durée de validité
        token = s.dumps(title, salt='download-link')
        # Générer le lien de téléchargement
        download_link = f'http://localhost:5001/download/{token}'
        return jsonify({'download_link': download_link})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    
    
# Route pour télécharger le fichier
@app.route('/download/<token>', methods=['GET'])
def secure_download(token):
    try:
        # Vérifier le token et sa validité
        title = s.loads(token, salt='download-link', max_age=3600)  # Durée de validité de 1 heure

        # Générer le chemin complet vers le fichier
        file_path = f'downloads/{title}.mp3'

        # Fournir le fichier en téléchargement
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)

"""Le client envoie une requête GET à votre API pour télécharger une vidéo spécifique. Votre API génère un lien de téléchargement sécurisé et temporisé, et renvoie ce lien dans la réponse JSON.
Le client reçoit la réponse JSON de l'API contenant le lien de téléchargement sécurisé.
Le client clique sur le lien de téléchargement dans la réponse JSON, ce qui déclenche une nouvelle requête GET vers l'URL du lien sécurisé.
Le serveur de l'API reçoit la requête pour le lien sécurisé et vérifie la validité du token.
Si le token est valide et que la durée de validité n'est pas dépassée, le serveur de l'API renvoie le fichier à télécharger au client en utilisant la fonction send_file() de Flask.
Le client reçoit le fichier en réponse à sa requête et peut l'enregistrer localement sur son appareil."""