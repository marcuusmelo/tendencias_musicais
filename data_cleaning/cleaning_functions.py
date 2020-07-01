"""
Collection of python functions to help cleaning data acquired in this project
"""

def clean_music_name(music_name):
    """
    DESCRIPTION: clean extra info from music name
    INPUT: music_name (str)
    OUTPUT: music_name (str)
    """
    breaking_substring_list = [
        ' (feat.',
        ' (with',
    ]

    for substring in breaking_substring_list:
        if substring in music_name:
            breaking_point = music_name.find(substring)
            music_name = music_name[:breaking_point]

    return music_name


def remove_special_chars(data_df, column_list):
    """
    DESCRIPTION: create a new column for strings with no special chars
    INPUT: data_df (DataFrame), column_list (list)
    OUTPUT: data_df (DataFrame)
    """
    # TODO: search for conversion lookup table
    for column in column_list:
        data_df[column] = data_df[column].str.encode('ascii', 'ignore').str.decode('ascii')

    return data_df


def make_cols_lowercase(data_df, column_list):
    """
    DESCRIPTION: create a new column for stings in lowercase
    INPUT: data_df (DataFrame), column_list (list)
    OUTPUT: data_df (DataFrame)
    """
    for column in column_list:
        data_df[column] = data_df[column].str.lower()

    return data_df


def add_metadata(data_df, metadata_dict):
    """
    DESCRIPTION: Add date and source metadata to dataframes
    INPUT: data_df (dataframe), metadata_dict (dict)
    OUTPUT: data_df (dataframe)
    """
    for key, value in metadata_dict.items():
        data_df[key] = value

    return data_df
