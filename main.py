import vk
import ya
from typing import Callable, Iterator, Union, Optional


def copy_photo(photo_source, destination):
    '''
    Функция резервного копирования фотографий пользователя ВКонтакте
    в облачное хранилище Яндекс.Диск.
    '''
    user_id_status = False
    while not user_id_status:
        user_id_status = photo_source.get_user_id(input('Введите \
короткое имя(screen_name) или id пользователя ВКонтакте: '))
    photo_source.get_albums()
    photo_source.select_album(input(f'Для резервного копирования фото из альбома \
введите соответствующее по списку число(по умолчанию фотографии профиля): '))
    photos = photo_source.get_photos(input('Введите количество фотографий(по умолчанию 5): '))

    dir_ya_status = False
    while not dir_ya_status:
        dir_ya_status = destination.create_new_folder(input('Введите \
название папки на Яндекс.Диске(по умолчанию photos_from_vk): '))
    destination.upload_photo_to_disk(photos)

if __name__ == '__main__':
    TOKEN_VK = '_'
    TOKEN_YA = '_'
    vk_client = vk.Vk(TOKEN_VK)
    ya_client = ya.Ya(TOKEN_YA)
    copy_photo(vk_client, ya_client)