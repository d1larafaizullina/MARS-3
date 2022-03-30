# Тестирование put запросов
from requests import post, put, get

print('редактирование пользователя с пустым json')
print(put('http://localhost:8080/api/users/5').json())

print('редактирование пользователя с несуществующим id')
data_json = {"position": "position not_id"}
print(put('http://localhost:8080/api/users/999', json=data_json).json())

print('редактирование пользователя с не правильным параметром')
data_json = {"bad_position": "position bad",
             "bad_address": "bad address bad"}
print(put('http://localhost:8080/api/users/1', json=data_json).json())

print('корректное редактирование пользователя с существующим id')
data_json = {"position": "super pilot",
             "speciality": "super repair engineer"}
print(put('http://localhost:8080/api/users/2', json=data_json).json())

print('Получение успешно отредактированного пользователя')
print(get('http://localhost:8080/api/users/2').json())

print('Получение всех пользователей')
print(get('http://localhost:8080/api/users').json())
