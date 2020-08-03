import json
import requests
import pprint

from vk_music_scrapper import get_vk_music_list
from config import spotify_user_id, spotify_token


class SpotyImport(object):
    def create_playlist(self):
        request_body = json.dumps(
            {"name": "VK", "description": "Твоя музяка из вк", "public": True,}
        )

        response = requests.post(
            f"https://api.spotify.com/v1/users/{spotify_user_id}/playlists",
            data=request_body,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {spotify_token}",
            },
        )

        if response.status_code != 201:
            pprint.pprint("playlist")
            pprint.pprint(response)

        response_json = response.json()

        return response_json["id"]

    def get_spotify_uri(self, track):
        query = f"https://api.spotify.com/v1/search?query={track}&type=track&&market=RU&offset=0&limit=5"
        response = requests.get(
            query,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {spotify_token}",
            },
        )
        if response.status_code != 200:
            pprint.pprint("get_uri")
            pprint.pprint(response.json())

        response_json = response.json()
        songs = response_json["tracks"]["items"]

        if len(songs) == 0:
            return None
        uri = songs[0]["uri"]

        return uri

    def import_songs(self, songs_list):
        print("Spotify playlist created")
        playlist_id = self.create_playlist()

        # songs_uris = []
        for track in songs_list:
            uri = self.get_spotify_uri(track)
            if uri is not None:
                # pprint.pprint(uri)
                # songs_uris.append(uri)

                # request_data = json.dumps(songs_uris)

                query = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks?uris={uri}"

                response = requests.post(
                    query,
                    # data=request_data,
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {spotify_token}",
                    },
                )

                # check for valid response status
                if response.status_code != 201:
                    pprint.pprint("add")
                    pprint.pprint(response.json())

        print("Enjoy your music")


if __name__ == "__main__":
    list_of_songs = get_vk_music_list()
    spoty = SpotyImport()
    spoty.import_songs(list_of_songs)
