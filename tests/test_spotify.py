from choreograph.spotify import spotify_client, playlist


def test_connect():
    sp = spotify_client()


def test_playlist():
    sp = spotify_client()
    tracks = playlist(sp, "ETM Final")
    print(tracks)
