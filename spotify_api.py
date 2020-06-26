"""
Module to handle the Spotify data aqcisition
"""
import requests


class SpotifyAPI():
    """
    DESCRIPTION: Interface with Spotify via their API
    ATTRIBUTES:
        - client_id (str)
        - client_secret (str)
        - token (str)
    """

    def __init__(self):
        """
        Constructor method for SpotifyAPI
        """
        self.client_id = input('digite seu spotify client id: ')
        self.client_secret = input('digite seu spotify client secret: ')
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

    def get_playlist_data(self):
        """
        DESCRIPTION: Method to fetch playlist data from Spotify API
        INPUT: None
        OUTPUT: playlist_json_response (json/dict)
        """
        playlist_url = 'https://api.spotify.com/v1/playlists/37i9dQZEVXbLRQDuF5jeBp'
        headers = {'Authorization': 'Bearer {0}'.format(self.token)}
        playlist_response = requests.get(playlist_url, headers=headers)
        playlist_json_response = playlist_response.json()

        return playlist_json_response


if __name__ == '__main__':
    spotify_api = SpotifyAPI()
    playlist_data = spotify_api.get_playlist_data()
    print(playlist_data)
