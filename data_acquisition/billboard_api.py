"""
Module to handle the HTML data acquisition from Billboard website
"""
from .html_api import HtmlAPI

class BillboardAPI(HtmlAPI):
    """
    DESCRIPTION: Interface with Billboard via their website html
    ATTRIBUTES:
        - url (str)
    METHODS:
        - get_billboard_hot_100_json
    """
    def __init__(self):
        self.url = 'https://www.billboard.com/'

    def get_billboard_hot_100_json(self):
        """
        DESCRIPTION: Get a json with relevant info from hot 100 songs from Billboard
        INPUT: None
        OUTPUT: billboard (dict/json)
        """
        billboard_html = self.fetch_html(uri='charts/hot-100')
        song_title_tag_list = billboard_html.findAll(
            'span',
            {'class': 'chart-element__information__song'}
        )
        artist_name_tag_list = billboard_html.findAll(
            'span',
            {'class': 'chart-element__information__artist'}
        )

        song_title_text_list = [tag.get_text() for tag in song_title_tag_list]
        artist_name_text_list = [tag.get_text() for tag in artist_name_tag_list]

        billboard = {'hot_100': []}
        for index, song in enumerate(song_title_text_list):
            song_info = {
                'title': song,
                'artist': artist_name_text_list[index],
                'position': index + 1
            }
            billboard['hot_100'].append(song_info)

        return billboard


if __name__ == '__main__':
    billboard_api = BillboardAPI()
    billboard_hot_100 = billboard_api.get_billboard_hot_100_json()
    print(billboard_hot_100)
