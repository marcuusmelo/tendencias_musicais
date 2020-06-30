"""
Module to handle the Spotify data aqcisition
"""
import requests
from credentials import SPOTIFY_CLIENT_ID, SPOTIFY_SECRET

class SpotifyAPI():
    """
    DESCRIPTION: Interface with Spotify via their API
    ATTRIBUTES:
        - client_id (str)
        - client_secret (str)
        - token (str)
    METHODS:
        - authentication
        - get_playlist_data
        - get_artist_data
    """

    def __init__(self):
        """
        Constructor method for SpotifyAPI
        """
        self.client_id = SPOTIFY_CLIENT_ID
        self.client_secret = SPOTIFY_SECRET
        self.token = self.authentication()

    def authentication(self):
        """
        DESCRIPTION: Method to handle the authentication with Spotify API
        INPUT: None
        OUTPUT: token (str)
        """
        grant_type = 'client_credentials'
        body_params = {'grant_type': grant_type}
        auth_url = 'https://accounts.spotify.com/api/token'
        response = requests.post(
            auth_url,
            data=body_params,
            auth=(self.client_id, self.client_secret)
        )
        print(response.json())
        token = response.json()['access_token']

        return token

    def get_playlist_data(self, playlist_id):
        """
        DESCRIPTION: Method to fetch playlist data from Spotify API
        INPUT: playlist_id (str)
        OUTPUT: playlist_json_response (json/dict)
        """
        playlist_url = 'https://api.spotify.com/v1/playlists/{0}'.format(playlist_id)
        headers = {'Authorization': 'Bearer {0}'.format(self.token)}
        playlist_response = requests.get(playlist_url, headers=headers)
        playlist_json_response = playlist_response.json()

        return playlist_json_response

    def get_artist_data(self, artist_id_list):
        """
        DESCRIPTION: Method to fetch multiple artist data from Spotify API
        INPUT: artist_id_list (list)
        OUTPUT: artists_json_response (json/dict)
        """
        artists_parameter = ','.join(artist_id_list)
        artists_url = 'https://api.spotify.com/v1/artists/{0}'.format(artists_parameter)
        headers = {'Authorization': 'Bearer {0}'.format(self.token)}
        artists_response = requests.get(artists_url, headers=headers)
        artists_json_response = artists_response.json()

        return artists_json_response


if __name__ == '__main__':
    spotify_api = SpotifyAPI()
    playlist_data = spotify_api.get_playlist_data('37i9dQZEVXbLRQDuF5jeBp')
    print(playlist_data)
