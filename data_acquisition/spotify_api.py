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
    METHODS:
        - authentication
        - get_playlist_data
        - get_artist_data
    """

    def __init__(self, client_id, secret):
        """
        Constructor method for SpotifyAPI
        """
        self.client_id = client_id
        self.client_secret = secret
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
        token = response.json()['access_token']

        return token

    def get_several_playlists_data(self, playlists_table):
        """
        DESCRIPTION: Use the method get_playlist_data to get several playlists data
        INPUT: playlists_table (dict)
        OUTPUT: several_playlists_json_response
        """
        several_playlists_json_response = {}

        for playlist_name, playlist_id in playlists_table.items():
            playlist_info = {
                'playlist_id': playlist_id,
                'playlist_name': playlist_name
            }
            this_playlist_data = self.get_playlist_data(playlist_info)
            several_playlists_json_response.update(this_playlist_data)

        return several_playlists_json_response

    def get_playlist_data(self, playlist_info):
        """
        DESCRIPTION: Method to fetch playlist data from Spotify API
        INPUT: playlist_info (dict)
        OUTPUT: playlist_json_response (json/dict)
        """
        playlist_id = playlist_info['playlist_id']
        playlist_name = playlist_info['playlist_name']

        playlist_url = 'https://api.spotify.com/v1/playlists/{0}'.format(playlist_id)
        headers = {'Authorization': 'Bearer {0}'.format(self.token)}

        playlist_response = requests.get(playlist_url, headers=headers)
        playlist_raw_json_response = playlist_response.json()

        playlist_json_response = self.pre_process_playlist_json(
            playlist_raw_json_response,
            playlist_name
        )

        return playlist_json_response

    def pre_process_playlist_json(self, raw_playlist_json, playlist_name):
        """
        DESCRIPTION: Extract data from raw api reponse and put in json format
        INPUT: raw_playlist_json (json)
        OUTPUT: playlist_info (json)
        """
        playlist_info = {playlist_name: []}

        for index, track in enumerate(raw_playlist_json['tracks']['items']):
            track_info = track['track']

            track_info_pick = {
                'main_artist': track_info['album']['artists'][0]['name'],
                'main_artist_id': track_info['album']['artists'][0]['id'],
                'all_artists': '*'.join([info['name'] for info in track_info['artists']]),
                'all_artists_ids': '*'.join([info['id'] for info in track_info['artists']]),
                'release_date': track_info['album']['release_date'],
                'duration': track_info['duration_ms'],
                'name': track_info['name'],
                'popularity': track_info['popularity'],
                'position': index + 1
            }

            playlist_info[playlist_name].append(track_info_pick)

        return playlist_info

    def get_several_artists_data(self, artist_id_list):
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
    spotify_api = SpotifyAPI('', '')
    playlist_data = spotify_api.get_playlist_data('37i9dQZEVXbLRQDuF5jeBp')
    print(playlist_data)
