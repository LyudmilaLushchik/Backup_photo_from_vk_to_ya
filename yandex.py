import sys
import time
import requests
from progress.bar import Bar
from pprint import pprint


class Ya:
    
    URL = 'https://cloud-api.yandex.net/v1/disk/resources'
    
    def __init__(self, token, dir):
        '''
        Метод инициализации экземпляра класса по токену из полигона Яндекс.Диска.
        '''
        self.token = token
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)
        }
        self.folder = dir

    def create_new_folder(self, dir_ya: str) -> bool:
        '''
        Метод создания папки на Яндекс.Диске.
        '''
        if dir_ya == '': dir_ya = self.folder

        folder_url = self.URL        
        params = {'path': dir_ya}
        response = requests.put(folder_url, headers=self.headers, params=params)

        dir_status = False
        if 'error' in response.json().keys():            
            print('ОШИБКА! Неверный токен Яндекс.Диска! Проверьте данные в файле settings.ini.')
            dir_status = False
            sys.exit()
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

        return result_list