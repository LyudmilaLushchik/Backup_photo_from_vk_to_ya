import vkontakte
import yandex
import configparser
import json


def copy_photo(photo_source, destination):
    '''
    Функция резервного копирования фотографий пользователя ВКонтакте
    в облачное хранилище Яндекс.Диск.
    '''
    user_id_status = False
    while not user_id_status:
        user_id_status = photo_source.get_user_id(input('Введите '
'короткое имя(screen_name) или id пользователя ВКонтакте: '))

    photo_source.get_albums()
    photo_source.select_album(input(f'Для резервного копирования фото из альбома '
'введите соответствующее по списку число(по умолчанию фотографии профиля): '))
    photos = photo_source.get_photos(input('Введите количество фотографий(по умолчанию 5): '))

    dir_ya_status = False
    while not dir_ya_status:
        dir_ya_status = destination.create_new_folder(input('Введите '
'название папки на Яндекс.Диске(по умолчанию photos_from_vk): '))
    return destination.upload_photo_to_disk(photos)

def log_report(files_uploaded):
        with open('results.json', 'w') as res_file:
            json.dump(files_uploaded, res_file)

if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read("settings.ini")
    token_vk = config["vkontakte"]["token"]
    token_ya = config["yandex"]["token"]
    default_vk = {}
    default_vk['photo_count'] = config['default_vk']['def_photo_count']
    default_vk['album'] = config['default_vk']['def_album']
    default_dir_ya = config['default_ya']['def_dir']
    vk_client = vkontakte.Vk(token_vk, **default_vk)
    ya_client = yandex.Ya(token_ya, default_dir_ya)
    log_report(copy_photo(vk_client, ya_client))