import time
import json
import requests
from progress.bar import Bar
from pprint import pprint
from typing import Callable, Iterator, Union, Optional


class Ya:
    URL = 'https://cloud-api.yandex.net/v1/disk/resources'
    folder = ''
    def __init__(self, token):
        '''
        Метод инициализации экземпляра класса по токену из полигона Яндекс.Диска.
        '''
        self.token = token
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)
        }

    def create_new_folder(self, dir_ya: str) -> bool:
        '''
        Метод создания папки на Яндекс.Диске.
        '''
        if dir_ya == '': dir_ya = 'photos_from_vk'

        folder_url = self.URL        
        params = {'path': dir_ya}
        response = requests.put(folder_url, headers=self.headers, params=params)

        dir_status = False
        if response.status_code == 201:
            print(f'Папка {dir_ya} на Яндекс.Диске создана.')
            dir_status = True
        if response.status_code == 409:
            print(f'Папка {dir_ya} на Яндекс.Диске уже существует.')
            dir_status = True

        if dir_status:
            self.folder = dir_ya
        return dir_status

    def upload_photo_to_disk(self, photos: list):
        '''
        Метод копирования файлов по ссылке в папку на Яндекс.Диске.
        Дополнительно метод сохраняет инфо по скопированным фото в json файл с результатами.
        '''
        result_list = []
        upload_url = self.URL + '/upload'
        bar = Bar('Прогресс копирования: ', max=len(photos))
        for photo in photos:
            params = {
                "path": f'{self.folder}/{photo["file_name"]}.jpg',
                "overwrite": "true",
                "url": f'{photo["url"]}'
            }
            requests.post(upload_url, headers=self.headers, params=params)
            result_list.append({"file_name": f'{photo["file_name"]}.jpg', "size": photo["size"]})
            bar.next()
            time.sleep(0.34)
        bar.finish()

        with open('results.json', 'w') as res_file:
            json.dump(result_list, res_file)
        return