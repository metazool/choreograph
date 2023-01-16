from choreograph.spotify import spotify_client, playlist_tracks

if __name__ == '__main__':
    sp = spotify_client()
    playlist_tracks(sp)
