import os
import sys
import pandas as pd

from utilities.db_access import get_db_connection, get_postgres_db_conn, get_postgress_engine


def load_to_postgres(table_name, csv_path):
    """
    """
    engine = get_postgress_engine()
    data_df = pd.read_csv(csv_path)

    data_df.to_sql(table_name, con=engine, if_exists='append', index=False)


def load_to_sqlite(table_name, csv_path):
    """
    """
    conn = get_db_connection()
    data_df = pd.read_csv(csv_path)

    data_df.to_sql(table_name, con=conn, if_exists='append', index=False)

    conn.commit()
    conn.close()


def load_files_in_storage(file_type='spotify', db_type='postgres'):
    """
    """
    storage_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        '..',
        'storage_music_trends'
    )
    storage_file_list = os.listdir(storage_path)
    selected_files = [x for x in storage_file_list if x.startswith(file_type)]

    table_lookup = {
        'spotify': 'tendencias_musicais_app_spotifydata',
        'billboard': '',
        'playlists': 'tendencias_musicais_app_playlists',
        'artists': 'tendencias_musicais_app_artists',
        'djmag': ''
    }
    table_name = table_lookup[file_type]

    for file_name in selected_files:
        print(file_name)
        file_path = os.path.join(storage_path, file_name)
        if db_type == 'sqlite':
            load_to_sqlite(table_name, file_path)
        elif db_type == 'postgres':
            load_to_postgres(table_name, file_path)
        else:
            print('please select a valid db type [sqlite, postgres]')


if __name__ == '__main__':
    file_type = sys.argv[1]
    load_files_in_storage(file_type)
