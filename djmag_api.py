"""
Module to handle the HTML data acquisition from DJ Mag website
"""
from html_api import HtmlAPI

class DJMagAPI(HtmlAPI):
    """
    DESCRIPTION: Interface with DJ Mag via their website html
    ATTRIBUTES:
        - url (str)
    METHODS:
        - get_top_100_djs_json
    """
    def __init__(self):
        self.url = 'https://djmag.com/'

    def get_top_100_djs_json(self):
        """
        DESCRIPTION: Get a json with relevant info from top 100 djs from DJ Mag
        INPUT: None
        OUTPUT: dj_mag (dict/json)
        """
        dj_mag_html = self.fetch_html(uri='top100djs')
        dj_name_tag_group = dj_mag_html.findAll('div', {'class': 'top100dj-name'})

        dj_name_tag_list = [tag.findAll('a') for tag in dj_name_tag_group]
        dj_name_text_list = [tag[0].get_text() for tag in dj_name_tag_list]

        dj_mag = {'top100djs': []}
        for index, dj_name in enumerate(dj_name_text_list):
            song_info = {
                'artist': dj_name,
                'position': index + 1
            }
            dj_mag['top100djs'].append(song_info)

        return dj_mag


if __name__ == '__main__':
    dj_mag_api = DJMagAPI()
    top100djs = dj_mag_api.get_top_100_djs_json()
    print(top100djs)
