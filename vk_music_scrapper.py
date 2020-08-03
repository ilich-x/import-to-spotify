import collections

import vk_api

from vk_api.audio import VkAudio
from datetime import date
from config import vk_login, vk_password


def auth_handler():
    # Код двухфакторной аутентификации
    key = input("Enter authentication code: ")
    remember_device = False

    return key, remember_device


def get_vk_music_list():
    print("VK Scrapping started")
    vk_session = vk_api.VkApi(vk_login, vk_password, auth_handler=auth_handler)

    try:
        vk_session.auth()
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return

    vkaudio = VkAudio(vk_session)
    # ? list
    all_vk_music = set()
    for track in vkaudio.get_iter():
        all_vk_music.add(f"{track['artist']}: {track['title']}")

    print("GOT ALL VK")

    return all_vk_music


if __name__ == "__main__":
    get_vk_music_list()
