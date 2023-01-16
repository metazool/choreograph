from dotenv import load_dotenv
import logging
import os
import json
from typing import Optional
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

logging.basicConfig(level=logging.INFO)
load_dotenv()


def spotify_client():
    auth_manager = SpotifyClientCredentials()
    sp = spotipy.Spotify(auth_manager=auth_manager)
    return sp


def analysis(sp, track_id: str):
    return sp.audio_analysis(track_id)


def playlist_index(pl: dict):
    pl_name = pl["name"].replace(" ", "_")
    os.makedirs(pl_name, exist_ok=True)
    with open(os.path.join(pl_name, "index.json"), "w") as out:
        out.write(json.dumps(pl))


def playlist_tracks(sp, playlist_id: Optional[str] = ""):
    if not playlist_id:
        playlist_id = os.environ.get("SPOTIFY_PLAYLIST")
    try:
        pl = sp.playlist(playlist_id)
    except:
        # TODO check timeout exceptions, retry
        raise
    playlist_index(pl)

    pl_name = pl["name"].replace(" ", "_")
    os.makedirs(pl_name, exist_ok=True)
    tracks = pl["tracks"]["items"]
    for track in tracks:
        analysis = sp.audio_analysis(track["track"]["uri"])
        filename = track["track"]["name"].replace(" ", "_")
        with open(os.path.join(pl_name, filename), "w") as out:
            out.write(json.dumps(analysis))


def named_playlist(sp, name: str):
    """Get playlist with name `name` from my playlists"""
    playlists = sp.user_playlists(os.environ.get("SPOTIFY_USER"))
    uri = None
    while playlists:
        for i, playlist in enumerate(playlists["items"]):
            logging.info(playlist["name"])
            if playlist["name"] == name:
                uri = playlist["uri"]
    if not uri:
        return
    logging.info(f"Get tracks for {uri}")
    tracks = sp.playlist_tracks(uri)
    return tracks
