import unittest

from spotify_api import SpotifyAPI


class TestSpotifyAPI(unittest.TestCase):

    def test_authentication_bad_credentials(self):
        spotify_api = SpotifyAPI('', '')
        received_token = spotify_api.authentication()
        expected_token = ''

        self.assertEqual(received_token, expected_token)


if __name__ == '__main__':
    unittest.main()
