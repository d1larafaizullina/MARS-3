# Тестирование put запросов
from requests import put, get

# print('редактирование пользователя с пустым json')
# print(put('http://localhost:8080/api/v2/users/5').json())

# print('редактирование пользователя с несуществующим id')
# data_json = {"position": "position not_id"}
# print(put('http://localhost:8080/api/v2/users/999', json=data_json).json())

print('редактирование пользователя с не правильным параметром')
data_json = {"bad_position": "position bad",
             "bad_address": "bad address bad"}
print(put('http://localhost:8080/api/v2/users/1', json=data_json).json())

print('корректное редактирование пользователя с существующим id')
data_json = {"position": "v2 super pilot",
             "speciality": "v2 super repair engineer",
             'hashed_password': '123456'}
print(put('http://localhost:8080/api/v2/users/2', json=data_json).json())

print('Получение успешно отредактированного пользователя')
print(get('http://localhost:8080/api/v2/users/2').json())

print('Получение всех пользователей')
print(get('http://localhost:8080/api/v2/users').json())
