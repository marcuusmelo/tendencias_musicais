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
        self.data_source_table = {
            'billboard': self.billboard_data,
            'dj_mag': self.dj_mag_data,
            'spotify': self.spotify_playlists_data
        }
        self.storage_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'storage_music_trends')


    def run_music_trends(self):
        """
        DESCRIPTION: runs all the methods needed to get the music trends
        INPUT: None
        OUTPUT: None
        """
        self.data_acquisition()
        self.data_cleaning()
        self.data_storage()


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
            'spotify': ['main_artist', 'all_artists', 'name']
        }

        for source_name, data_dict in self.data_source_table.items():
            lowercase_columns = lowercase_columns_table[source_name]

            for key, data_df in data_dict.items():

                # Add metadata
                metadata_dict = {
                    'timestamp': self.timestamp,
                    'source': source_name,
                    'source_detail': key
                }
                data_dict[key] = add_metadata(data_df, metadata_dict)

                # make lowercase
                data_dict[key] = make_cols_lowercase(data_df, lowercase_columns)

                # clean music name
                if source_name == 'spotify':
                    data_dict[key]['name'] = data_dict[key]['name'].apply(clean_music_name)


    def data_storage(self):
        """
        DESCRIPTION: Store each data dataframe as csv
        INPUT: None
        OUTPUT: None
        """
        self.data_source_table = {
            'billboard': self.billboard_data,
            'dj_mag': self.dj_mag_data,
            'spotify': self.spotify_playlists_data
        }

        if not os.path.exists(self.storage_path):
            os.makedirs(self.storage_path)

        file_path_base = '{0}/{1}_{2}_{3}.csv'

        for source_name, data_dict in self.data_source_table.items():
            for key, data_df in data_dict.items():
                file_path = file_path_base.format(
                    self.storage_path, source_name, key, self.timestamp_str_compact
                )
                data_df.to_csv(file_path, index=False)


if __name__ == '__main__':
    music_trends = MusicTrends()
    music_trends.run_music_trends()
