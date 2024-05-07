from flask import Flask, render_template, jsonify
from research.spotify_script import get_token, request_valid_song  # Ensure your script is named spotify_script.py

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get-song', methods=['POST'])
def get_song():
    access_token = get_token()
    song_details = request_valid_song(access_token)
    return jsonify(song_details)

if __name__ == '__main__':
    app.run()