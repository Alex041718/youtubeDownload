const express = require('express');
const { exec } = require('child_process');
const fs = require('fs');

const hostname = 'localhost';
const app = express();
const port = 5001;

// Route pour générer le lien de téléchargement
app.get('/generate_download_link', (req, res) => {
  const videoUrl = req.query.video_url;

  if (!videoUrl) {
    return res.status(400).json({ error: 'Missing video_url parameter' });
  }

  const pythonScript = 'python3 download_audio.py'; // Assurez-vous que le chemin est correct
  const command = `${pythonScript} ${videoUrl}`;

  exec(command, (error, stdout, stderr) => {
    if (error) {
      return res.status(500).json({ error: error.message });
    }
    
    const downloadLink = `http://${hostname}:${port}/download/${stdout.trim()}`;
    return res.json({ download_link: downloadLink });
  });
});

// Route pour télécharger le fichier en utilisant le token
app.get('/download/:token', (req, res) => {
  const token = req.params.token;

  if (!token) {
    return res.status(400).json({ error: 'Missing token parameter' });
  }

  const fileName = token + '.mp3';
  const filePath = `downloads/${fileName}`;

  // Vérifier si le fichier existe
  if (fs.existsSync(filePath)) {
    res.download(filePath, fileName); // Télécharger le fichier
  } else {
    res.status(404).json({ error: 'File not found' });
  }
});

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
