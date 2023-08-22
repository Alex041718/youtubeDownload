from flask import Flask, request, jsonify, send_file
from pytube import YouTube
from itsdangerous import URLSafeTimedSerializer
import re

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
s = URLSafeTimedSerializer(app.config['SECRET_KEY'])

# Route pour demander au server de telecharger l audio de la video
@app.route('/generate_download_link', methods=['GET'])
def generate_download_link():
    video_url = request.args.get('video_url')

    if not video_url:
        return jsonify({'error': 'Missing video_url parameter'}), 400

    try:
        youtube_video = YouTube(video_url)
        audio_stream = youtube_video.streams.filter(only_audio=True).first()

        title = re.sub(r'\s+', '-', youtube_video.title)
        # Telecharger l'audio dans le dossier downloads
        audio_stream.download(output_path='downloads', filename=title+'.mp3')


        # Generer un token securise avec une duree de validite
        token = s.dumps(title, salt='download-link')
        # Generer le lien de telechargement
        download_link = f'http://51.38.35.91:5001/download/{token}'
        return jsonify({'download_link': download_link})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    
    
# Route pour telecharger le fichier
@app.route('/download/<token>', methods=['GET'])
def secure_download(token):
    try:
        # Verifier le token et sa validite
        title = s.loads(token, salt='download-link', max_age=3600)  # Duree de validite de 1 heure

        # Generer le chemin complet vers le fichier
        file_path = f'downloads/{title}.mp3'

        # Fournir le fichier en telechargement
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)

"""Le client envoie une requête GET à votre API pour telecharger une video specifique. Votre API genère un lien de telechargement securise et temporise, et renvoie ce lien dans la reponse JSON.
Le client reçoit la reponse JSON de l'API contenant le lien de telechargement securise.
Le client clique sur le lien de telechargement dans la reponse JSON, ce qui declenche une nouvelle requête GET vers l'URL du lien securise.
Le serveur de l'API reçoit la requête pour le lien securise et verifie la validite du token.
Si le token est valide et que la duree de validite n'est pas depassee, le serveur de l'API renvoie le fichier à telecharger au client en utilisant la fonction send_file() de Flask.
Le client reçoit le fichier en reponse à sa requête et peut l'enregistrer localement sur son appareil."""