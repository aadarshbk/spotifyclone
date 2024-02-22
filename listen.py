from bottle import Bottle, request, response, run, HTTPResponse
import json

app = Bottle()

# Define the music variable globally
music = [
    {"id": 1, "title": "Song 1", "artist": "Artist 1", "duration": "3:45"},
    {"id": 2, "title": "Song 2", "artist": "Artist 2", "duration": "4:12"},
    {"id": 3, "title": "Song 3", "artist": "Artist 3", "duration": "2:58"}
]

currently_playing = None

@app.route("/songs", method="GET")
def get_songs():
    return json.dumps(music)

@app.route("/play/<song_id:int>", method="POST")
def play_song(song_id):
    global currently_playing
    song = next((song for song in music if song["id"] == song_id), None)
    if song is None:
        return HTTPResponse(body=json.dumps({"error": "Song not found"}), status=404)
    currently_playing = song
    return json.dumps({"message": f"Now playing: {song['title']} by {song['artist']}"})

@app.route("/stop", method="POST")
def stop_song():
    global currently_playing
    if currently_playing is None:
        return HTTPResponse(body=json.dumps({"error": "No song currently playing"}), status=400)
    message = f"Stopped: {currently_playing['title']} by {currently_playing['artist']}"
    currently_playing = None
    return json.dumps({"message": message})

if __name__ == "__main__":
    run(app, host="localhost", port=8080, debug=True)
