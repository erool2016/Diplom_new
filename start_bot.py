import main
import config_bot
import Data_Base
import vk_api


from vk_api.longpoll import VkLongPoll
vk = vk_api.VkApi(token=config_bot.token_vkinder_servis_key)
vk2 = vk_api.VkApi(token=config_bot.tok111)
longpoll = VkLongPoll(vk)




data_user_for_find = {} #словарь с данными для поиска id , sity, sex

def get_profile_user(user_id):
    '''получаем информацию о пользователе и заносим в словарь, возвращаем словарь'''

    req = vk2.method('users.get',
                         {
                             'user_id': user_id,
                             'fields': 'bdate,city,sex,photo_id,about'
                         }
                         )


    data_user_for_find['bdate']=req[0]['bdate']
    data_user_for_find['city'] = req[0]['city']['id']
    data_user_for_find['sex'] = req[0]['sex']

    return data_user_for_find

def change_sex(data_user_ff):
    if data_user_ff['sex'] == 1:
        data_user_for_find['sex'] = 2
        return data_user_for_find
    else:
        data_user_for_find['sex'] = 1
        return data_user_for_find

def start_find(user_id):
    '''начало поиска'''

    get_profile_user(user_id)
    change_sex(data_user_for_find)
    main.find_users(data_user_for_find,user_id)

def start():
    '''начало'''
    requests_longpoll, user_id = main.session_longpoll()
    print('-----', requests_longpoll,user_id)
    if requests_longpoll == 'hello':
        print('hello')
        start_find(user_id)
    elif requests_longpoll == 'more':
        start()
    else:
        print('пока')

        return


if __name__ == '__main__':
    Data_Base.drop_table()
    Data_Base.create_table()
    start()