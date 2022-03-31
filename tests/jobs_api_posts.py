from requests import get, post, delete

# Тестирование ответа сервера
# print('Получение всех работ')
# print(get('http://localhost:8080/api/jobs').json())
# print('Корректное получение одной работы')
# print(get('http://localhost:8080/api/jobs/1').json())
# print('Ошибочный запрос на получение одной работы — неверный id')
# print(get('http://localhost:8080/api/jobs/999').json())
# print('Ошибочный запрос на получение одной работы — строка')
# print(get('http://localhost:8080/api/jobs/s').json())

# Тестирование post запросов
print('Создание работы с пустым json')
print(post('http://localhost:8080/api/jobs').json())

print('Создание работы с существующим id')
data_json = {"id": 1, "collaborators": "1, 3",
             "job": "deployment of residential modules 33 and 44",
             "team_leader": 1, "work_size": 15, "is_finished": 0}
print(post('http://localhost:8080/api/jobs', json=data_json).json())

print('Создание работы с отсутствующим обязательным параметром team_leader')
data_json = {"collaborators": "1, 3",
             "job": "deployment of residential modules 33 and 44",
             "work_size": 15, "is_finished": 0}
print(post('http://localhost:8080/api/jobs', json=data_json).json())

print('Корректное создание работы')
data_json = {"collaborators": "1, 3",
             "job": "deployment of residential modules 33 and 44 api v1 posts",
             "team_leader": 1, "work_size": 15}
print(post('http://localhost:8080/api/jobs', json=data_json).json())

# delete_jobs
print('Удаление работы с несуществующим id')
print(delete('http://localhost:8080/api/jobs/999').json())
# новости с id = 999 нет в базе

print('Корректное удаление работы id==1 (закомментирована)')
# print(delete('http://localhost:8080/api/jobs/1').json())

print('Получение всех работ')
print(get('http://localhost:8080/api/jobs').json())
