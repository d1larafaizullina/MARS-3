# Тестирование put запросов
from requests import put, get

print('редактирование работы с пустым json')
print(put('http://localhost:8080/api/v2/jobs/1').json())

print('редактирование работы с несуществующим id')
data_json = {"collaborators": "1, 3",
             "job": "deployment of residential modules 22 and 55 put"}
print(put('http://localhost:8080/api/v2/jobs/999', json=data_json).json())

print('редактирование работы с не правильным параметром')
data_json = {"bad_collaborators": "1, 3",
             "bad_job": "bad deployment of residential modules 22 and 55 bad"}
print(put('http://localhost:8080/api/v2/jobs/1', json=data_json).json())

print('корректное редактирование работы с существующим id')
data_json = {"collaborators": "1, 3",
             "job": "deployment of residential modules 22 and 55 put v2"}
print(put('http://localhost:8080/api/v2/jobs/1', json=data_json).json())

print('Получение всех работ')
print(get('http://localhost:8080/api/v2/jobs').json())
