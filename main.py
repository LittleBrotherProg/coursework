import requests
from progress.bar import ChargingBar


class VK:

   def __init__(self, access_token, user_id, version='5.131'):
       self.token = access_token
       self.id = user_id
       self.version = version
       self.params = {'access_token': self.token, 'v': self.version}

   def users_info(self):
       bar_user_info = ChargingBar('Получение данных о фото профиля', max = 100)
       url = 'https://api.vk.com/method/users.get'
       params = {'user_ids': self.id, 'fields': 'crop_photo'}
       response = requests.get(url, params={**self.params, **params})
       bar_user_info.next(100)
       bar_user_info.finish()
       return response.json()
   
   
   def profile_picture(self):
       bar_profile_picture = ChargingBar('Получение url и колличество лайков на фото', max = 100)
       user_info = vk.users_info()
       id_profile_picture = user_info['response'][0]['crop_photo']['photo']['id']
       bar_profile_picture.next(25)
       album_id = user_info['response'][0]['crop_photo']['photo']['album_id']
       bar_profile_picture.next(25)
       url = 'https://api.vk.com/method/photos.get'
       params= {'owner_id': self.id, 
                'album_id': album_id, 
                'photo_ids': id_profile_picture,
                'extended': '1'
                }
       info_photo = requests.get(url, params={**self.params, **params})
       url_photo = info_photo.json()['response']['items'][0]['sizes'][2]['url']
       bar_profile_picture.next(25)
       name_photo = info_photo.json()['response']['items'][0]['likes']['count']
       bar_profile_picture.next(25)
       bar_profile_picture.finish()
       return [url_photo, str(name_photo)]
    
class YA():
    def __init__(self, token, url_photo, name_photo):
        self.url_photo = url_photo
        self.headers = {
            'Content-Type': 'application/json', 
            'Authorization': token
        }
        self.params = {'path':'disk:/'}
        self.name_folder = 'Фото_профиля_ВК'
        self.name_photo = name_photo

    def create_folder(self):
        bar_create_folder = ChargingBar('Создание/Проверка папки для фото', max = 100)
        url = 'https://cloud-api.yandex.net/v1/disk/resources'
        info_folder = requests.get(url, headers={**self.headers}, params={**self.params})
        count_files = len(info_folder.json()['_embedded']['items'])
        bar_create_folder.next(25)
        for count in range(int(count_files)):
            bar_create_folder.next(25)
            type_files = info_folder.json()['_embedded']['items'][count]['type']
            count_name_folder = info_folder.json()['_embedded']['items'][count]['name']
            if type_files == 'dir':
                if self.name_folder != count_name_folder:
                    params = dict(path = self.params.get('path') + self.name_folder)  
                    requests.put(url, headers={**self.headers}, params={**params})
        bar_create_folder.finish()
        return
        
    def loading_profile_picture(self):
        bar_loading_profile_picture = ChargingBar('Загрузка файла на диск', max = 100)
        load_photo.create_folder()
        bar_loading_profile_picture.next(25)
        url_loading = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        bar_loading_profile_picture.next(25)
        params = dict(path = self.params.get('path') + self.name_folder + '/' + self.name_photo + '.jpg', url = self.url_photo)
        bar_loading_profile_picture.next(25)
        succsesful = requests.post(url_loading, params={**params}, headers={**self.headers})
        bar_loading_profile_picture.next(25)
        bar_loading_profile_picture.finish()
        info_file = [{'file_name':self.name_photo + '.jpg' }]
        return succsesful, info_file
       
access_token = 'vk1.a.QLcaZUwum5eLcpmS_5JYA8EtjcS4eYSAm1JwU2QkU052RCuZBYiUCNDW90TscffbWkLBJGisfkBmCBKlnKAkD3XTbOA7qjibCtRzNWtdHaChmLgeCZ34urTJ9vxvbr0YxJtvcl0jV9d_pByna4vAH4MhHLocFgqJOF-DftQwJHCc2g7-rmYbkm7lS_aRNFQkzS5HIfX2vNA0n7OUcHpzlg'
user_id = '422264572'
vk = VK(access_token, user_id)
info_photo = vk.profile_picture()
token_YA = 'y0_AgAAAAA8KgLcAADLWwAAAADa_KQ7iNJyZXM9TYq8pBI5cqN6ShBQyeU'
load_photo = YA(token_YA, info_photo[0], info_photo[1])
check  = load_photo.loading_profile_picture()
if str(check[0]) == '<Response [202]>':
    print(check[1])
    print('Succsesful')
else:
    print('Mistake', str(check[0]))

