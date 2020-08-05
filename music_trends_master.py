"""
Master script for the different processes of the music trend analysis software
"""
import os
from datetime import datetime
import pandas as pd

from credentials import SPOTIFY_CLIENT_ID, SPOTIFY_SECRET
from music_trends_constants import TOP_50_PLAYLIST_ID_TABLE
from data_acquisition.billboard_api import BillboardAPI
from data_acquisition.djmag_api import DJMagAPI
from data_acquisition.spotify_api import SpotifyAPI
from data_cleaning.cleaning_functions import clean_music_name, make_cols_lowercase, add_metadata
from utilities.load_to_sql import load_files_in_storage


class MusicTrends():
    """
    DESCRIPTION: Main process of music trends software
    ATTRIBUTES:
        - timestamp: datetime
        - timestamp_str_compact: str
        - dj_mag_data: dict of dataframes
        - billboard_data: dict of dataframes
        - spotify_playlists_data: dict of dataframes
    """
    def __init__(self):
        self.timestamp = datetime.now()
        self.timestamp_str_compact = self.timestamp.strftime('%Y%m%d%H%M%S')
        self.dj_mag_data = {}
        self.billboard_data = {}
        self.spotify_playlists_data = {}
        self.artists_data = {}
        self.data_source_table = {
            'billboard': self.billboard_data,
            'dj_mag': self.dj_mag_data,
            'spotify': self.spotify_playlists_data,
            'artists': self.artists_data
        }
        self.storage_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'storage_music_trends'
        )
        self.sql_upload_list = ['artists', 'playlists', 'spotify']


    def run_music_trends(self):
        """
        DESCRIPTION: runs all the methods needed to get the music trends
        INPUT: None
        OUTPUT: None
        """
        self.data_acquisition()
        self.data_cleaning()
        self.data_local_storage()
        self.data_s3_upload()
        self.data_sql_upload()
        self.local_storage_cleanup()


    def get_artist_list(self):
        """
        DESCRIPTION: Get a list of unique artists in the new spotify data
        INPUT: None
        OUTPUT: artist_list (list)
        """
        spotify_playlist_df_list = self.spotify_playlists_data.values()
        spotify_playlist_df = pd.concat(spotify_playlist_df_list, ignore_index=True)
        artist_list = list(spotify_playlist_df['main_artist_id_id'].unique())
        return artist_list


    def data_acquisition(self):
        """
        DESCRIPTION: Fetch music data from dj mag, billboard and spotify.
                     This method updates the following attributes:
                     - self.dj_mag_data
                     - self.billboard_data
                     - self.spotify_playlists_data
        INPUT: None
        OUTPUT: None
        """
        billboard_api = BillboardAPI()
        djmag_api = DJMagAPI()
        spotify_api = SpotifyAPI(SPOTIFY_CLIENT_ID, SPOTIFY_SECRET)

        dj_mag_data_json = djmag_api.get_top_100_djs_json()
        for key, value in dj_mag_data_json.items():
            self.dj_mag_data[key] = pd.DataFrame(value)

        billboard_data_json = billboard_api.get_billboard_hot_100_json()
        for key, value in billboard_data_json.items():
            self.billboard_data[key] = pd.DataFrame(value)

        spotify_playlists_data_json = spotify_api.get_several_playlists_data(TOP_50_PLAYLIST_ID_TABLE)
        for key, value in spotify_playlists_data_json.items():
            self.spotify_playlists_data[key] = pd.DataFrame(value)

        artists_list = self.get_artist_list()
        spotify_artists_data_json = spotify_api.get_several_artists_data(artists_list)
        for key, value in spotify_artists_data_json.items():
            self.artists_data[key] = pd.DataFrame(value)


    def data_cleaning(self):
        """
        DESCRIPTION: Clean data acquired
                     This method updates the following attributes:
                     - self.dj_mag_data
                     - self.billboard_data
                     - self.spotify_playlists_data
        INPUT: None
        OUTPUT: None
        """
        # Note that I am not using the remove_special_chars for now for simplicity
        lowercase_columns_table = {
            'billboard': ['title', 'artist'],
            'dj_mag': ['artist'],
            'spotify': ['all_artists', 'song_name'],
            'artists': ['name', 'music_genre_1', 'music_genre_2', 'music_genre_3']
        }

        for source_name, data_dict in self.data_source_table.items():
            lowercase_columns = lowercase_columns_table[source_name]

            for key, data_df in data_dict.items():
                if data_dict[key].empty:
                    continue

                # make lowercase
                data_dict[key] = make_cols_lowercase(data_df, lowercase_columns)

                if source_name != 'artists':
                    # Add metadata
                    metadata_dict = {
                        'source_date': self.timestamp,
                    }
                    data_dict[key] = add_metadata(data_df, metadata_dict)

                    # clean music name
                    if source_name == 'spotify':
                        data_dict[key]['song_name'] = data_dict[key]['song_name'].apply(clean_music_name)

    def data_local_storage(self):
        """
        DESCRIPTION: Store each data dataframe as csv
        INPUT: None
        OUTPUT: None
        """
        if not os.path.exists(self.storage_path):
            os.makedirs(self.storage_path)

        file_path_base = '{0}/{1}_{2}_{3}.csv'

        for source_name, data_dict in self.data_source_table.items():
            for key, data_df in data_dict.items():
                file_path = file_path_base.format(
                    self.storage_path, source_name, key, self.timestamp_str_compact
                )
                if not data_df.empty:
                    data_df.to_csv(file_path, index=False)

    def data_s3_upload(self):
        pass

    def data_sql_upload(self):
        for source_data_type in self.sql_upload_list:
            load_files_in_storage(source_data_type)

    def local_storage_cleanup(self):
        pass


if __name__ == '__main__':
    music_trends = MusicTrends()
    music_trends.run_music_trends()
