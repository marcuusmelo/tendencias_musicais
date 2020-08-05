"""
Module to handle the Spotify data aqcisition
"""
import requests
import pandas as pd
from utilities.db_access import get_postgress_engine

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
        try:
            token = response.json()['access_token']
        except KeyError:
            token = ''

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
                'playlist_id_id': raw_playlist_json['id'],
                'main_artist_id_id': track_info['album']['artists'][0]['id'],
                'all_artists': '*'.join([info['name'] for info in track_info['artists']]),
                'all_artists_ids': '*'.join([info['id'] for info in track_info['artists']]),
                'release_date': track_info['album']['release_date'],
                'duration': track_info['duration_ms'],
                'song_name': track_info['name'],
                'popularity': track_info['popularity'],
                'position': index + 1,
            }

            playlist_info[playlist_name].append(track_info_pick)

        return playlist_info

    def get_artists_ids_from_db(self):
        """
        """
        engine = get_postgress_engine()
        query = """
            select distinct artist_id
            from tendencias_musicais_app_artists
        """
        artist_ids_df = pd.read_sql_query(query, engine)
        artist_ids_list = artist_ids_df['artist_id'].to_list()
        return artist_ids_list


    def pre_process_artists_json(self, artists_response_list):
        """
        """
        artists_info = {'artists': []}

        for artist_data in artists_response_list:
            genres = artist_data['genres']
            genres = genres + [''] * 3
            artists_info_pick = {
                'artist_id': artist_data['id'],
                'name': artist_data['name'],
                'music_genre_1': genres[0],
                'music_genre_2': genres[1],
                'music_genre_3': genres[2]
            }

            artists_info['artists'].append(artists_info_pick)

        return artists_info


    def get_several_artists_data(self, spotify_artist_list):
        """
        DESCRIPTION: Method to fetch multiple artist data from Spotify API
        INPUT: artist_id_list (list)
        OUTPUT: artists_json_response (json/dict)
        """
        def chunks(lst, n):
            """Yield successive n-sized chunks from lst."""
            for i in range(0, len(lst), n):
                yield lst[i:i + n]

        db_artist_list = self.get_artists_ids_from_db()
        new_artist_list = [id for id in spotify_artist_list if id not in db_artist_list]

        artists_response_list = []
        for ids_sublist in chunks(new_artist_list, 50):
            artists_parameter = ','.join(ids_sublist)
            artists_url = 'https://api.spotify.com/v1/artists/?ids={0}'.format(artists_parameter)
            headers = {'Authorization': 'Bearer {0}'.format(self.token)}
            artists_response = requests.get(artists_url, headers=headers)
            artists_json_response = artists_response.json()
            artists_response_list += artists_json_response['artists']

        artists_json_response = self.pre_process_artists_json(artists_response_list)

        return artists_json_response


if __name__ == '__main__':
    spotify_api = SpotifyAPI('', '')
    playlist_data = spotify_api.get_playlist_data('37i9dQZEVXbLRQDuF5jeBp')
    print(playlist_data)
